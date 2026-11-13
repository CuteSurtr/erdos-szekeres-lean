#!/usr/bin/env python3
"""Assemble an explicitly versioned cover route, preserving the first 317 gate.

Profiles pin exact arithmetic and cut-transfer manifests. A complete record
requires all prerequisite objects, source bindings, semantic catalog bridges,
the final real-point theorem, and standard-axiom audits to pass. This script
does not search, generate arithmetic certificates, or weaken incomplete gates.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import time

import check_omission_global as original_gate
from check_axioms import audit_output
from check_omission_global import (
    digest, read_json, require_hash, verify_complete_family, verify_dependency,
    verify_import_layout, verify_snapshot,
)


def read_profile(path):
    profile = read_json(path)
    if profile.get("version") != 1:
        raise ValueError("Unsupported assembly profile version")
    for side, states, original_rows in [("balanced", 252, 2685), ("residual", 154, 1187)]:
        item = profile[side]
        if (item["states"], item["original_rows"]) != (states, original_rows):
            raise ValueError("Wrong original geometric row system")
        if item["rows"] != original_rows + item["derived_rows"] or item["derived_rows"] < 1:
            raise ValueError("Invalid extended row cardinalities")
        if not 0 <= item["budget"] < states:
            raise ValueError("Invalid hole budget")
        for key in ["namespace", "module_prefix", "cut_module", "cut_namespace", "bridge"]:
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", item[key]):
                raise ValueError("Invalid Lean module or namespace in profile")
        for key in ["arithmetic_manifest_sha256", "cut_manifest_sha256", "augmented_source_sha256"]:
            if not re.fullmatch(r"[a-f0-9]{64}", item[key]):
                raise ValueError("Profile must pin exact manifest identities")
    expected_bound = 406 - profile["balanced"]["budget"] - profile["residual"]["budget"]
    if profile["bound"] != expected_bound:
        raise ValueError("Cover budgets and forcing threshold disagree")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", profile["final_module"]):
        raise ValueError("Invalid final assembly module")
    return profile


def verify_cover_profile(item, arithmetic, cuts, arithmetic_manifest, cut_manifest):
    require_hash(arithmetic / "export.json", item["arithmetic_manifest_sha256"])
    require_hash(cuts / "export.json", item["cut_manifest_sha256"])
    keys = ["namespace", "states", "rows", "budget", "module_prefix"]
    if any(arithmetic_manifest.get(key) != item[key] for key in keys):
        raise ValueError("Profile and arithmetic target disagree")
    for key in ["states", "original_rows", "derived_rows"]:
        if cut_manifest.get(key) != item[key]:
            raise ValueError("Profile and cut-transfer dimensions disagree")
    if (cut_manifest.get("module"), cut_manifest.get("namespace")) != (
            item["cut_module"], item["cut_namespace"]):
        raise ValueError("Profile and cut-transfer identity disagree")
    if arithmetic_manifest.get("source_sha256") != item["augmented_source_sha256"]:
        raise ValueError("Profile and arithmetic use different extended row systems")
    # V1 transfer manifests predate augmented-source metadata. Their exact
    # support/demand identification is established by the checked Lean bridge.
    if ("augmented_source_sha256" in cut_manifest and
            cut_manifest["augmented_source_sha256"] != item["augmented_source_sha256"]):
        raise ValueError("Arithmetic and cut transfer use different extended row systems")


def populate_profile_overlay(repo, output, module_names):
    allowed = set(module_names)
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


def run(profile_path, output, residual_arithmetic, residual_cycles, residual_blocks,
        balanced_arithmetic, balanced_geometry, residual_cover_arithmetic,
        residual_cover_cuts, balanced_cover_arithmetic, balanced_cover_cuts, memory=3000):
    if memory < 1:
        raise ValueError("Memory must be positive")
    profile_path, output = Path(profile_path).resolve(), Path(output).resolve()
    profile = read_profile(profile_path)
    repo = Path(__file__).resolve().parents[1]
    artifact = repo / "experiments/omission-global-assembly-2026-10-10"
    paths = [Path(p).resolve() for p in [residual_arithmetic, residual_cycles, residual_blocks,
        balanced_arithmetic, balanced_geometry, residual_cover_arithmetic, residual_cover_cuts,
        balanced_cover_arithmetic, balanced_cover_cuts]]
    if any(output == p or output.is_relative_to(p) or p.is_relative_to(output) for p in paths):
        raise ValueError("The output must be separate from every prerequisite")
    version = subprocess.check_output(["lean", "--version"], text=True).strip()
    for directory in paths:
        verify_import_layout(directory)
    snapshot, manifests = {}, {}
    for index in [1, 2, 4, 5, 6, 7, 8]:
        manifests[index], binding = verify_complete_family(paths[index], repo, version)
        snapshot.update(binding)
    if (manifests[4].get("kind"), manifests[4].get("rows")) != ("balanced_rows_only", 2685):
        raise ValueError("The complete balanced rows-only geometry is required")
    for index in [1, 2, 6]:
        verify_dependency(paths[index], paths[0] / "Catalog.olean")
    for obj in paths[1].glob("*.olean"):
        verify_dependency(paths[2], obj)
    for index in [4, 8]:
        verify_dependency(paths[index], paths[3] / "BalancedProof/Catalog.olean")
    for side, arithmetic_index, cut_index in [("residual", 5, 6), ("balanced", 7, 8)]:
        verify_cover_profile(profile[side], paths[arithmetic_index], paths[cut_index],
                             manifests[arithmetic_index], manifests[cut_index])
    prefix = "ErdosSzekeres.Omission.Partition."
    population = [prefix + n for n in ["asymmetric_of_bounds", "forces_of_population_bounds",
        "avoiding_card_le_of_population_bounds", "forces_318_of_population_bounds",
        "forces_317_of_population_bounds"]]
    budget = ["OmissionResidual." + n for n in ["excludes_hole_budget_mono",
        "residual_bound_of_hole_budget", "forces_of_hole_budget",
        "forces_318_of_twenty_nine_holes", "forces_317_of_thirty_holes"]]
    balanced_population = 251 - profile["balanced"]["budget"]
    residual_population = 153 - profile["residual"]["budget"]
    bound = profile["bound"]
    final = ["ErdosSzekeres.Omission." + n for n in [f"balanced_population_{balanced_population}",
        f"residual_population_{residual_population}", f"forces_convex_octagon_{bound}",
        f"convex_octagon_of_card_ge_{bound}"]]
    modules = [(repo / "ErdosSzekeres/Omission/PopulationBounds.lean",
                output / "ErdosSzekeres/Omission/PopulationBounds.olean", []),
               (repo / "experiments/omission-residual-geometry-2026-10-09/ResidualReduction.lean",
                output / "ResidualReduction.olean", ["OmissionResidual." + n for n in
                    ["feasible_holes", "residual_bound_of_arithmetic", "forces_317_of_arithmetic"]]),
               (artifact / "ResidualBudgets.lean", output / "ResidualBudgets.olean", budget),
               (artifact / "ConditionalAudit.lean", output / "ConditionalAudit.olean", population + budget),
               (artifact / "BalancedBudgets.lean", output / "BalancedBudgets.olean",
                ["OmissionBalanced.feasible_holes", "OmissionBalanced.balanced_bound_of_hole_budget"])]
    for side in ["residual", "balanced"]:
        item = profile[side]
        modules.append((artifact / (item["bridge"] + ".lean"), output / (item["bridge"] + ".olean"),
            [item["namespace"] + "." + n for n in ["base_catalog_matches", "cut_catalog_matches",
                                                   "all_cover_rows", "exclusion_transfer"]]))
    modules.append((artifact / (profile["final_module"] + ".lean"),
                    output / (profile["final_module"] + ".olean"), final))
    output.mkdir(parents=True, exist_ok=True)
    populate_profile_overlay(repo, output, [source.stem for source, _, _ in modules])
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(output), *(str(p) for p in paths), env.get("LEAN_PATH", "")])
    for source, _, _ in modules:
        snapshot[str(source)] = digest(source)
    for path in [profile_path, Path(__file__).resolve(), Path(original_gate.__file__).resolve(),
                 repo / "scripts/check_axioms.py"]:
        snapshot[str(path)] = digest(path)
    report = {"scope": f"Closed ordinary real-point theorem ForcesConvexNGon {bound} 8",
              "profile": profile, "profile_sha256": digest(profile_path), "lean": version,
              "inputs": snapshot, "modules": {}, "complete": False}
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
    report["complete"] = True
    save()
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["profile", "output", "residual-arithmetic", "residual-cycles", "residual-blocks",
                 "balanced-arithmetic", "balanced-geometry", "residual-cover-arithmetic",
                 "residual-cover-cuts", "balanced-cover-arithmetic", "balanced-cover-cuts"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--memory", type=int, default=3000)
    args = vars(parser.parse_args())
    args["profile_path"] = args.pop("profile")
    result = run(**args)
    print(json.dumps({"complete": result["complete"], "bound": result["profile"]["bound"]}))
