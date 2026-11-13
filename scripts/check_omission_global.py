#!/usr/bin/env python3
"""Audit and assemble the complete real-point octagon proof in an isolated directory.

This checker does not run any unfinished arithmetic jobs. Full mode refuses
partial, stale, or mutated prerequisite records. Conditional mode checks the
generic population and hole-budget bridges, and cannot report a global result.
Run under ``lake env python3`` after checking the separate certificate families.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from check_axioms import audit_output


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def require_hash(path, expected):
    if not Path(path).is_file() or digest(path) != expected:
        raise ValueError(f"Missing or changed proof input: {path}")


def verify_import_layout(directory):
    """Unlisted objects must not shadow another family's imported module."""
    directory = Path(directory).resolve()
    manifest = read_json(directory / "export.json")
    allowed = {str(Path(name).with_suffix(".olean")) for name in manifest["files"]}
    found = {str(path.relative_to(directory)) for path in directory.rglob("*.olean")}
    if found - allowed:
        raise ValueError(f"Unlisted objects could shadow checked imports: {sorted(found - allowed)}")


def verify_complete_family(directory, repo, lean_version):
    """Read-only validation of a full existing source/object/audit binding."""
    directory, repo = Path(directory).resolve(), Path(repo).resolve()
    manifest_path = directory / "export.json"
    record_path = directory / "kernel-check.json"
    manifest, report = read_json(manifest_path), read_json(record_path)
    if report.get("complete") is not True:
        raise ValueError(f"Incomplete prerequisite family: {directory}")
    verify_import_layout(directory)
    binding = report["binding"]
    require_hash(manifest_path, binding["manifest"])
    if binding["lean"] != lean_version:
        raise ValueError(f"Toolchain mismatch: {directory}")
    fingerprint = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    if fingerprint != report["fingerprint"]:
        raise ValueError(f"Invalid binding fingerprint: {directory}")
    snapshot = {str(manifest_path): digest(manifest_path), str(record_path): digest(record_path)}
    for name, sha in binding["inputs"].items():
        path = Path(name)
        path = path if path.is_absolute() else repo / path
        require_hash(path, sha)
        snapshot[str(path)] = sha
    expected_modules = set()
    for name, sha in manifest["files"].items():
        source = directory / name
        if source.suffix != ".lean" or not source.resolve().is_relative_to(directory):
            raise ValueError(f"Invalid source path: {name}")
        module = source.stem
        if module in expected_modules:
            raise ValueError(f"Duplicate module name: {module}")
        expected_modules.add(module)
        require_hash(source, sha)
        record = report["modules"].get(module, {})
        if record.get("exit") != 0 or record.get("audited") is not True:
            raise ValueError(f"Unchecked prerequisite module: {source}")
        if record.get("source_sha256") != sha:
            raise ValueError(f"Source and check record disagree: {source}")
        obj = source.with_suffix(".olean")
        require_hash(obj, record["olean_sha256"])
        axioms = record.get("axioms")
        if isinstance(axioms, dict):
            if not axioms and re.search(r"^#print axioms ", source.read_text(), re.MULTILINE):
                raise ValueError(f"Empty axiom record: {source}")
            for theorem, recorded in axioms.items():
                if audit_output(record["stdout"], theorem) != sorted(recorded):
                    raise ValueError(f"Axiom record disagrees with output: {source}")
        elif isinstance(axioms, list):
            names = re.findall(r"^'([^']+)' (?:depends on axioms:|does not depend)",
                               record["stdout"], re.MULTILINE)
            if len(names) != 1 or audit_output(record["stdout"], names[0]) != sorted(axioms):
                raise ValueError(f"Invalid arithmetic axiom record: {source}")
        else:
            raise ValueError(f"Missing axiom record: {source}")
        snapshot[str(source)] = sha
        snapshot[str(obj)] = record["olean_sha256"]
    if set(report["modules"]) != expected_modules:
        raise ValueError(f"Source and checked module lists disagree: {directory}")
    return manifest, snapshot


def verify_snapshot(snapshot):
    for path, sha in snapshot.items():
        require_hash(path, sha)


def verify_dependency(directory, dependency):
    """Require the directory selected for import to be the one actually checked."""
    inputs = read_json(Path(directory) / "kernel-check.json")["binding"]["inputs"]
    path = Path(dependency).resolve()
    if str(path) not in inputs:
        raise ValueError(f"Prerequisite record does not bind the selected dependency: {path}")
    require_hash(path, inputs[str(path)])


def populate_overlay(repo, output):
    """Lean resolves a top-level package in one directory, so mirror its objects.

    Existing local library objects are read-only symlinks; only the new module
    is compiled in this overlay. Nothing in the shared build tree is changed.
    """
    allowed = {"ResidualReduction", "ResidualBudgets", "ConditionalAudit", "BalancedPopulation",
               "Residual124Bridge", "Final317", "Final318", "BalancedBudgets",
               "ResidualCoverBridge", "BalancedCoverBridge", "FinalCover317",
               "BalancedCover60Bridge", "ResidualCover31Bridge", "FinalCover316", "FinalCover315"}
    for obj in output.glob("*.olean"):
        if obj.stem not in allowed:
            raise ValueError(f"Unexpected object could shadow a prerequisite: {obj}")
    for directory in output.iterdir():
        if directory.is_dir() and directory.name != "ErdosSzekeres":
            raise ValueError(f"Unexpected package could shadow a prerequisite: {directory}")
    library = repo / ".lake/build/lib/lean/ErdosSzekeres"
    for source in library.rglob("*.olean"):
        target = output / "ErdosSzekeres" / source.relative_to(library)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.name == "PopulationBounds.olean":
            if target.is_symlink():
                target.unlink()
            continue
        if target.is_symlink():
            if target.resolve() != source.resolve():
                raise ValueError(f"Unexpected overlay link: {target}")
        elif target.exists():
            raise ValueError(f"Unexpected overlay object: {target}")
        else:
            target.symlink_to(source.resolve())


def run(output, residual_arithmetic, residual_cycles, residual_blocks,
        balanced_arithmetic=None, balanced_geometry=None, conditional_only=False,
        memory=3000, bound=317, residual124_arithmetic=None,
        residual_cover_arithmetic=None, residual_cover_cuts=None,
        balanced_cover_arithmetic=None, balanced_cover_cuts=None,
        balanced_cover_budget=59, residual_cover_budget=30):
    if memory < 1:
        raise ValueError("Memory must be positive")
    if bound not in (315, 316, 317, 318):
        raise ValueError("The supported forcing thresholds are 315 through 318")
    cover_paths = [residual_cover_arithmetic, residual_cover_cuts,
                   balanced_cover_arithmetic, balanced_cover_cuts]
    cover = any(p is not None for p in cover_paths)
    if cover and (not all(p is not None for p in cover_paths) or conditional_only):
        raise ValueError("The cover route requires both arithmetic/cut pairs and a full assembly")
    if cover and ((balanced_cover_budget, residual_cover_budget) not in [(59, 30), (60, 30), (60, 31)]
                  or bound != 406 - balanced_cover_budget - residual_cover_budget):
        raise ValueError("Cover budgets and requested global threshold disagree")
    if not cover and bound not in (317, 318):
        raise ValueError("The original route supports only thresholds 317 and 318")
    balanced_cover_namespace = "OmissionBalancedCover" + ("60" if balanced_cover_budget == 60 else "")
    residual_cover_namespace = "OmissionResidualCover" + ("31" if residual_cover_budget == 31 else "")
    balanced_cover_prefix = "BalancedCover60Proof" if balanced_cover_budget == 60 else "BalancedCoverProof"
    residual_cover_prefix = "ResidualCover31Proof" if residual_cover_budget == 31 else "ResidualCoverProof"
    repo = Path(__file__).resolve().parents[1]
    output = Path(output).resolve()
    paths = [Path(p).resolve() for p in
             (residual_arithmetic, residual_cycles, residual_blocks)]
    if not conditional_only:
        if balanced_arithmetic is None or balanced_geometry is None:
            raise ValueError("Full assembly requires both balanced directories")
        paths += [Path(balanced_arithmetic).resolve(), Path(balanced_geometry).resolve()]
        if cover:
            paths += [Path(p).resolve() for p in cover_paths]
        elif bound == 318:
            if residual124_arithmetic is None:
                raise ValueError("Threshold 318 requires the original 29-hole arithmetic family")
            paths.append(Path(residual124_arithmetic).resolve())
    if output in paths or any(output.is_relative_to(p) or p.is_relative_to(output) for p in paths):
        raise ValueError("The output directory must be separate from every prerequisite")
    version = subprocess.check_output(["lean", "--version"], text=True).strip()
    for directory in paths:
        verify_import_layout(directory)
    snapshot = {}
    for directory in paths[1:3]:
        _, binding = verify_complete_family(directory, repo, version)
        snapshot.update(binding)
        verify_dependency(directory, paths[0] / "Catalog.olean")
    for obj in paths[1].glob("*.olean"):
        verify_dependency(paths[2], obj)
    if cover:
        manifests = {}
        for index in range(4, 9):
            manifest, binding = verify_complete_family(paths[index], repo, version)
            manifests[index] = manifest
            snapshot.update(binding)
        if manifests[4].get("kind") != "balanced_rows_only" or manifests[4].get("rows") != 2685:
            raise ValueError("The cover route needs the complete balanced rows-only geometry")
        for index, expected in [(5, (residual_cover_namespace, 154, 1589, residual_cover_budget,
                                    residual_cover_prefix)),
                                (7, (balanced_cover_namespace, 252, 2905, balanced_cover_budget,
                                    balanced_cover_prefix))]:
            m = manifests[index]
            actual = tuple(m.get(k) for k in ["namespace", "states", "rows", "budget", "module_prefix"])
            if actual != expected:
                raise ValueError("Wrong compressed arithmetic target")
        verify_dependency(paths[4], paths[3] / "BalancedProof/Catalog.olean")
        verify_dependency(paths[6], paths[0] / "Catalog.olean")
        verify_dependency(paths[8], paths[3] / "BalancedProof/Catalog.olean")
        for index, expected in [(6, (154, 1187, 402)), (8, (252, 2685, 220))]:
            m = manifests[index]
            if tuple(m.get(k) for k in ["states", "original_rows", "derived_rows"]) != expected:
                raise ValueError("Wrong rounded-cover cut family")
    elif not conditional_only:
        manifests = []
        for directory in [paths[0] if bound == 317 else paths[5], paths[3], paths[4]]:
            manifest, binding = verify_complete_family(directory, repo, version)
            manifests.append(manifest)
            snapshot.update(binding)
        residual, balanced, geometry = manifests
        expected_residual = (("OmissionResidual", 154, 1187, 30, "") if bound == 317 else
                             ("OmissionResidual124", 154, 1187, 29, "Residual124"))
        if (residual.get("namespace"), residual.get("states"), residual.get("rows"),
                residual.get("budget"), residual.get("module_prefix", "")) != expected_residual:
            raise ValueError("Unexpected residual arithmetic target")
        if (balanced.get("namespace"), balanced.get("states"), balanced.get("rows"),
                balanced.get("budget"), balanced.get("module_prefix")) != (
                    "OmissionBalanced", 252, 2685, 59, "BalancedProof"):
            raise ValueError("Unexpected balanced arithmetic target")
        if geometry.get("arithmetic_prefix") != "BalancedProof":
            raise ValueError("Balanced geometry imports the wrong arithmetic family")
        verify_dependency(paths[4], paths[3] / "BalancedProof/Catalog.olean")
        verify_dependency(paths[4], paths[3] / "BalancedProof/Root.olean")
    output.mkdir(parents=True, exist_ok=True)
    populate_overlay(repo, output)
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(output), *(str(p) for p in paths),
                                       env.get("LEAN_PATH", "")])
    artifact = repo / "experiments/omission-global-assembly-2026-10-10"
    prefix = "ErdosSzekeres.Omission.Partition."
    population = [prefix + n for n in ["asymmetric_of_bounds", "forces_of_population_bounds",
        "avoiding_card_le_of_population_bounds", "forces_318_of_population_bounds",
        "forces_317_of_population_bounds"]]
    budget = ["OmissionResidual." + n for n in ["excludes_hole_budget_mono",
        "residual_bound_of_hole_budget", "forces_of_hole_budget",
        "forces_318_of_twenty_nine_holes", "forces_317_of_thirty_holes"]]
    balanced_population = 251 - balanced_cover_budget if cover else 192
    residual_population = 153 - residual_cover_budget if cover else (123 if bound == 317 else 124)
    final = ["ErdosSzekeres.Omission." + n for n in [f"balanced_population_{balanced_population}",
        f"residual_population_{residual_population}",
        f"forces_convex_octagon_{bound}", f"convex_octagon_of_card_ge_{bound}"]]
    modules = [(repo / "ErdosSzekeres/Omission/PopulationBounds.lean",
                output / "ErdosSzekeres/Omission/PopulationBounds.olean", []),
               (repo / "experiments/omission-residual-geometry-2026-10-09/ResidualReduction.lean",
                output / "ResidualReduction.olean", ["OmissionResidual." + n for n in
                    ["feasible_holes", "residual_bound_of_arithmetic", "forces_317_of_arithmetic"]]),
               (artifact / "ResidualBudgets.lean", output / "ResidualBudgets.olean", budget),
               (artifact / "ConditionalAudit.lean", output / "ConditionalAudit.olean", population + budget)]
    if cover:
        residual_bridge = "ResidualCover31Bridge" if residual_cover_budget == 31 else "ResidualCoverBridge"
        balanced_bridge = "BalancedCover60Bridge" if balanced_cover_budget == 60 else "BalancedCoverBridge"
        modules += [
            (artifact / "BalancedBudgets.lean", output / "BalancedBudgets.olean",
             ["OmissionBalanced.feasible_holes", "OmissionBalanced.balanced_bound_of_hole_budget"]),
            (artifact / (residual_bridge + ".lean"), output / (residual_bridge + ".olean"),
             [residual_cover_namespace + "." + n for n in ["base_catalog_matches", "cut_catalog_matches",
                                                     "all_cover_rows", "exclusion_transfer"]]),
            (artifact / (balanced_bridge + ".lean"), output / (balanced_bridge + ".olean"),
             [balanced_cover_namespace + "." + n for n in ["base_catalog_matches", "cut_catalog_matches",
                                                     "all_cover_rows", "exclusion_transfer"]]),
            (artifact / f"FinalCover{bound}.lean", output / f"FinalCover{bound}.olean", final)]
    elif not conditional_only:
        modules.append((artifact / "BalancedPopulation.lean", output / "BalancedPopulation.olean",
                        ["ErdosSzekeres.Omission.balanced_population_192"]))
        if bound == 318:
            modules.append((artifact / "Residual124Bridge.lean", output / "Residual124Bridge.olean",
                            ["OmissionResidual124.catalog_matches", "OmissionResidual124.exclusion_transfer"]))
        modules.append((artifact / f"Final{bound}.lean", output / f"Final{bound}.olean", final))
    for source, _, _ in modules:
        snapshot[str(source)] = digest(source)
    snapshot[str(Path(__file__).resolve())] = digest(__file__)
    report = {"scope": "Conditional geometric bridges only" if conditional_only else
              f"Closed ordinary real-point theorem ForcesConvexNGon {bound} 8",
              "arithmetic_route": "rounded_cover" if cover else "original",
              "hole_budgets": {"balanced": balanced_cover_budget, "residual": residual_cover_budget}
                  if cover else None,
              "lean": version, "inputs": snapshot, "modules": {},
              "conditional_bridges_checked": False, "complete": False}
    report_path = output / "global-check.json"
    def save():
        temporary = report_path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(report, indent=2) + "\n")
        temporary.replace(report_path)
    save()
    for source, obj, expected in modules:
        started = time.monotonic()
        process = subprocess.run(["lean", "-j", "1", "-s", "32768", "-M", str(memory),
                                  str(source), "-o", str(obj)], cwd=repo, env=env,
                                 text=True, capture_output=True)
        record = {"source_sha256": digest(source), "exit": process.returncode,
                  "seconds": round(time.monotonic() - started, 3), "stdout": process.stdout,
                  "stderr": process.stderr, "audited": False}
        report["modules"][source.stem] = record
        if process.returncode == 0:
            try:
                record["axioms"] = {n: audit_output(process.stdout, n) for n in expected}
                record["olean_sha256"] = digest(obj)
                record["audited"] = True
            except ValueError as error:
                record["audit_error"] = str(error)
        save()
        print(f"{source.stem}: exit={process.returncode}, audited={record['audited']}, "
              f"{record['seconds']} seconds", flush=True)
        if not record["audited"]:
            raise RuntimeError(f"Assembly failed; see {report_path}\n" +
                               (process.stdout + process.stderr)[-3000:])
    verify_snapshot(snapshot)
    report["conditional_bridges_checked"] = True
    report["complete"] = not conditional_only
    save()
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--residual-arithmetic", type=Path, required=True)
    parser.add_argument("--residual-cycles", type=Path, required=True)
    parser.add_argument("--residual-blocks", type=Path, required=True)
    parser.add_argument("--balanced-arithmetic", type=Path)
    parser.add_argument("--balanced-geometry", type=Path)
    parser.add_argument("--bound", type=int, choices=[315, 316, 317, 318], default=317)
    parser.add_argument("--residual124-arithmetic", type=Path)
    parser.add_argument("--residual-cover-arithmetic", type=Path)
    parser.add_argument("--residual-cover-cuts", type=Path)
    parser.add_argument("--balanced-cover-arithmetic", type=Path)
    parser.add_argument("--balanced-cover-cuts", type=Path)
    parser.add_argument("--balanced-cover-budget", type=int, choices=[59, 60], default=59)
    parser.add_argument("--residual-cover-budget", type=int, choices=[30, 31], default=30)
    parser.add_argument("--conditional-only", action="store_true")
    parser.add_argument("--memory", type=int, default=3000)
    args = parser.parse_args()
    result = run(args.output, args.residual_arithmetic, args.residual_cycles,
                 args.residual_blocks, args.balanced_arithmetic, args.balanced_geometry,
                 args.conditional_only, args.memory, args.bound, args.residual124_arithmetic,
                 args.residual_cover_arithmetic, args.residual_cover_cuts,
                 args.balanced_cover_arithmetic, args.balanced_cover_cuts,
                 args.balanced_cover_budget, args.residual_cover_budget)
    print(json.dumps({k: result[k] for k in ["conditional_bridges_checked", "complete"]}))
