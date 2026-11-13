#!/usr/bin/env python3
"""Fresh kernel check of the CONDITIONAL 2,650-row bridge to ES(8) <= 313.

Run from the repository root through the pinned Lake environment:

    LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
      experiments/omission-residual32-bridge2650-2026-10-11/check.py

All residual32 experiment modules this bridge depends on (frozen 2,469-row
catalog and its geometric transfer, the 129 added rows with their Fourth/Sixth
families, the 48 relaxed Sixth rows, the four attained-rank cores, the zero-state
lemma), the balanced 190 bridge and this bundle are compiled from tracked
sources, one Lean process at a time (`-j1`, `LEAN_NUM_THREADS=1`), into a fresh
ignored overlay under `.cache/`. The older, large prerequisite objects (original
residual catalog, residual cycle/block geometry, residual and balanced cut
transfers, balanced rows-only geometry and the 61-hole balanced arithmetic
certificate) are not recompiled: each object and its source are linked into the
overlay only after their SHA-256 match the committed complete 314-point gate
record `omission-global-assembly-2026-10-10/global-cover-314-check.json`.

The result is conditional. `Excludes2650Zero 32` is an explicit hypothesis of
the final theorems and is not proved here.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parents[1]
EXPERIMENTS = ROOT / "experiments"
CACHE_PARENT = ROOT / ".cache"
RECORD_314 = EXPERIMENTS / "omission-global-assembly-2026-10-10/global-cover-314-check.json"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}
FORBIDDEN = re.compile(r"\b(?:sorry|admit|sorryAx|native_decide)\b|^\s*(?:private\s+)?axiom\s", re.M)
AUDIT = re.compile(r"'([^']+)' depends on axioms: \[([^\]]*)\]")
NO_AXIOMS = re.compile(r"'([^']+)' does not depend on any axioms")

# Older prerequisite object directories, reused only after hash pinning.
REUSED_DIRS = [
    ".cache/omission-lean-full/residual",
    ".cache/omission-residual-geometry",
    ".cache/omission-residual-blocks",
    ".cache/omission-cover-transfer-residual-v2",
    ".cache/omission-balanced-linked",
    ".cache/omission-balanced-rows-only",
    ".cache/omission-balanced-cover61-fused-linked",
    ".cache/omission-cover-transfer-balanced-v2",
]

# Freshly compiled modules, in dependency order: (bundle, module).
FRESH = [
    ("omission-residual32-context-certificates-2026-10-10", "Residual32ContextsProof.Catalog"),
    ("omission-residual32-transfer-2026-10-10", "OriginalBinding"),
    ("omission-residual32-transfer-2026-10-10", "OldcutsBinding"),
    ("omission-residual32-transfer-2026-10-10", "GeometricBinding"),
    ("omission-residual32-transfer-2026-10-10", "NewCuts"),
    ("omission-residual32-transfer-2026-10-10", "Transfer"),
    ("omission-residual32-case4-2026-10-10", "Witness"),
    ("omission-residual32-witness-coupled-2026-10-10", "LeanCore"),
    ("omission-residual32-witness-coupled-2026-10-10", "Geometry"),
    ("omission-residual32-fourth-global-variants-2026-10-10", "FourthGlobalProof.Data"),
    *(("omission-residual32-fourth-global-variants-2026-10-10", f"FourthGlobalProof.Part0{k}")
      for k in range(8)),
    ("omission-residual32-fourth-global-variants-2026-10-10", "FourthGlobalProof.Root"),
    ("omission-residual32-added-rows-2026-10-10", "AddedRows"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedCore"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedTemplate"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedTemplateCheck"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedTemplateGeometry"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedProof.Data"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedProof.Part00"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedProof.Part01"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedProof.Part02"),
    ("omission-residual32-sixth-relaxed-2026-10-10", "SixthRelaxedProof.Root"),
    ("omission-residual-rank-attainment-2026-10-10", "RankAttainment"),
    ("omission-residual-rank-attainment-2026-10-10", "CoupledDomain"),
    *(("omission-residual32-rank-certificates-2026-10-10", f"Rank{kind}{name}")
      for name in ("One", "Two", "Three", "Four") for kind in ("Core", "Geometry")),
    ("omission-residual32-context-certificates-2026-10-10", "ZeroState"),
    ("omission-global-assembly-2026-10-10", "BalancedBudgets"),
    ("omission-global-assembly-2026-10-10", "BalancedCover61FusedBridge"),
    ("omission-residual32-bridge2650-2026-10-11", "Residual32Bridge2650.Catalog"),
    ("omission-residual32-bridge2650-2026-10-11", "Residual32Bridge2650.Matches"),
    ("omission-residual32-bridge2650-2026-10-11", "Residual32Bridge2650.Rows"),
    ("omission-residual32-bridge2650-2026-10-11", "Residual32Bridge2650.Final"),
]

NS = "OmissionResidual32Bridge2650."
# Theorems of this bundle whose axiom audit must be present and standard.
REQUIRED = {
    "Residual32Bridge2650.Catalog": ["code_correct"],
    "Residual32Bridge2650.Matches": ["rowCode_injective", "support2650_eq_of_rowCode",
                                     "support2650_eq_of_codes",
                                     "prefix_matches", "added_matches", "relaxed_matches",
                                     "rank_one_matches", "rank_two_matches",
                                     "rank_three_matches", "rank_four_matches",
                                     "suffix_demand"],
    "Residual32Bridge2650.Rows": ["row_of_missing", "all_rows_2650",
                                  "holes_sum_add_population",
                                  "residual_bound_of_excludes2650",
                                  "residual_bound_121_of_excludes",
                                  "excludes2650Zero_of_node"],
    "Residual32Bridge2650.Final": ["balanced_population_190", "all_rows_2650",
                                   "residual_bound_121_of_excludes",
                                   "forces_convex_octagon_313_of_excludes",
                                   "convex_octagon_of_card_ge_313_of_excludes",
                                   "forces_convex_octagon_313_of_node"],
}
FINAL_SIGNATURES = {
    "Excludes2650Zero": "OmissionResidual32Bridge2650.Excludes2650Zero : ℕ → Prop",
    "residual": ("OmissionResidual32Bridge2650.residual_bound_121_of_excludes : "
                 "OmissionResidual32Bridge2650.Excludes2650Zero 32 → "
                 "ErdosSzekeres.Omission.Partition.ResidualBound 121"),
    "forces": ("OmissionResidual32Bridge2650.forces_convex_octagon_313_of_excludes : "
               "OmissionResidual32Bridge2650.Excludes2650Zero 32 → "
               "ErdosSzekeres.ForcesConvexNGon 313 8"),
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path):
    path = Path(path)
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def load_generator():
    spec = importlib.util.spec_from_file_location("bridge2650_generate", BUNDLE / "generate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def module_path(module):
    return Path(*module.split(".")).with_suffix(".lean")


def imports_of(source):
    names = []
    for line in Path(source).read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            names += stripped.split()[1:]
        elif stripped and not stripped.startswith("--") and names:
            break
    return names


def pinned_314():
    record = json.loads(RECORD_314.read_text())
    if not record.get("complete"):
        raise ValueError("The 314-point gate record is not complete")
    pins = {}
    for key, value in record["inputs"].items():
        for prefix in ("/workspace/erdos-szekeres-lean/", str(ROOT) + "/"):
            if key.startswith(prefix):
                key = key[len(prefix):]
        pins[key] = value
    return pins


def library_dirs():
    return [Path(p) for p in os.environ.get("LEAN_PATH", "").split(os.pathsep) if p]


def find_library(module, dirs):
    target = module_path(module).with_suffix(".olean")
    return [d / target for d in dirs if (d / target).is_file()]


def preflight():
    """Read-only identity and import-closure validation; never invokes Lean."""
    manifest = json.loads((BUNDLE / "manifest.json").read_text())
    generator = load_generator()
    checked = {}

    def verify(label, actual, expected):
        if actual != expected:
            raise ValueError(f"Identity mismatch for {label}: expected {expected}, got {actual}")
        checked[label] = actual

    archive, _, n, rows = generator.load_source()
    verify("source archive", hashlib.sha256(archive).hexdigest(), manifest["source_archive_sha256"])
    verify("uncompressed source", generator.SOURCE_SHA, manifest["source_uncompressed_sha256"])
    verify("generator", sha(BUNDLE / "generate.py"), manifest["generator_sha256"])
    verify("exporter", sha(ROOT / manifest["exporter"]), manifest["exporter_sha256"])
    verify("row reader", sha(ROOT / "scripts/omission_row_probe.py"), manifest["row_reader_sha256"])
    regenerated = generator.catalog_text(n, rows)
    catalog = BUNDLE / "Residual32Bridge2650/Catalog.lean"
    if catalog.read_text() != regenerated:
        raise ValueError("Catalog.lean differs from the exporter output for the pinned source")
    for name, expected in manifest["files"].items():
        verify("bundle source " + name, sha(BUNDLE / name), expected)
    lean_files = {str(p.relative_to(BUNDLE)) for p in BUNDLE.rglob("*.lean")}
    if lean_files != set(manifest["files"]):
        raise ValueError(f"Unexpected Lean files in bundle: {sorted(lean_files ^ set(manifest['files']))}")
    return manifest, checked


def closure(lib_dirs):
    """Classify every import as library, fresh (earlier in plan) or pinned reuse."""
    pins = pinned_314()
    fresh_order = {module: k for k, (_, module) in enumerate(FRESH)}
    fresh_sources = {}
    for bundle, module in FRESH:
        source = EXPERIMENTS / bundle / module_path(module)
        if not source.is_file():
            raise FileNotFoundError(source)
        if FORBIDDEN.search(source.read_text()):
            raise ValueError(f"Forbidden proof token in {source}")
        if find_library(module, lib_dirs):
            raise ValueError(f"Fresh module would be shadowed by a library object: {module}")
        fresh_sources[module] = source
    reused, pending = {}, []

    def classify(module, importer, importer_index):
        if module in fresh_order:
            if importer_index is not None and fresh_order[module] >= importer_index:
                raise ValueError(f"{importer} imports {module} before it is compiled")
            return
        if module in reused or find_library(module, lib_dirs):
            return
        hits = [Path(ROOT / d) for d in REUSED_DIRS
                if (ROOT / d / module_path(module).with_suffix(".olean")).is_file()]
        if len(hits) != 1:
            raise ValueError(f"Import {module} of {importer} found in {len(hits)} reuse directories")
        olean = hits[0] / module_path(module).with_suffix(".olean")
        source = hits[0] / module_path(module)
        for path in (olean, source):
            key = rel(path)
            if key not in pins:
                raise ValueError(f"Reused prerequisite is not pinned by the 314 record: {key}")
            if sha(path) != pins[key]:
                raise ValueError(f"Reused prerequisite differs from the 314 record: {key}")
        reused[module] = {"olean": rel(olean), "olean_sha256": pins[rel(olean)],
                          "source": rel(source), "source_sha256": pins[rel(source)]}
        pending.append(module)

    for k, (_, module) in enumerate(FRESH):
        for name in imports_of(fresh_sources[module]):
            classify(name, module, k)
    while pending:
        module = pending.pop()
        for name in imports_of(ROOT / reused[module]["source"]):
            if name in fresh_order:
                raise ValueError(f"Reused {module} imports freshly compiled {name}")
            classify(name, module, None)
    return fresh_sources, dict(sorted(reused.items()))


def parse_audits(text):
    audits = {name: sorted(a.strip() for a in body.split(",") if a.strip())
              for name, body in AUDIT.findall(text)}
    for name in NO_AXIOMS.findall(text):
        audits[name] = []
    return audits


def run_lean(lean, bundle_dir, source, target, env, memory):
    command = [lean, "-j1", "-s", "32768", "-M", str(memory), "--root=" + str(bundle_dir),
               "-o", str(target), str(source)]
    timer = Path("/usr/bin/time")
    wrapped = ([str(timer), "-l"] if platform.system() == "Darwin" and timer.exists() else []) + command
    started = time.monotonic()
    proc = subprocess.run(wrapped, cwd=ROOT, env=env, text=True, capture_output=True)
    seconds = round(time.monotonic() - started, 3)
    rss = re.search(r"(\d+)\s+maximum resident set size", proc.stderr)
    return proc, seconds, int(rss.group(1)) if rss else None


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", type=Path, help="fresh overlay directory under .cache/")
    parser.add_argument("--preflight-only", action="store_true",
                        help="validate identities and the import closure without compiling")
    parser.add_argument("--memory", type=int, default=8000, help="Lean -M heap limit in MB")
    parser.add_argument("--resume", action="store_true",
                        help="development only: keep the longest prefix of modules from an earlier "
                             "run in --output whose sources and objects are unchanged; every later "
                             "module is recompiled and the record is marked not single-invocation")
    args = parser.parse_args()
    started_all = time.monotonic()
    manifest, identities = preflight()
    lean = shutil.which("lean")
    if lean is None:
        raise RuntimeError("Run through the pinned `lake env`")
    lib_dirs = library_dirs()
    fresh_sources, reused = closure(lib_dirs)
    if args.preflight_only:
        print(json.dumps({"preflight_passed": True, "fresh_modules": len(FRESH),
                          "reused_objects": len(reused), "validated_identities": identities},
                         indent=2))
        return
    version = subprocess.check_output([lean, "--version"], text=True).strip()
    if "version 4.24.0," not in version:
        raise ValueError("Use the pinned Lean 4.24.0 toolchain")
    lake = shutil.which("lake")
    up_to_date = subprocess.run([lake, "build", "--no-build", "ErdosSzekeres"], cwd=ROOT,
                                text=True, capture_output=True)
    if up_to_date.returncode != 0 or "All targets up-to-date" not in up_to_date.stdout:
        raise RuntimeError("The maintained library build is not up to date")
    CACHE_PARENT.mkdir(exist_ok=True)
    output = (args.output.resolve() if args.output else
              Path(tempfile.mkdtemp(prefix="residual32-bridge2650-", dir=CACHE_PARENT)))
    if not output.is_relative_to(CACHE_PARENT.resolve()):
        raise ValueError("The overlay must live under the ignored .cache/ directory")
    output.mkdir(parents=True, exist_ok=True)
    progress_path = output / "progress.json"
    previous, created_empty, invocation = {}, True, 1
    if any(output.rglob("*.olean")):
        if not args.resume:
            raise ValueError("Use a fresh output directory without Lean objects")
        earlier = json.loads(progress_path.read_text()) if progress_path.exists() else {}
        previous = earlier.get("modules", {})
        created_empty = earlier.get("overlay_created_empty")
        invocation = earlier.get("invocation", 1) + 1
    # Link pinned reused objects into the overlay.
    for module, item in reused.items():
        target = output / module_path(module).with_suffix(".olean")
        target.parent.mkdir(parents=True, exist_ok=True)
        source = (ROOT / item["olean"]).resolve()
        if target.is_symlink() and target.resolve() == source:
            continue
        if target.exists() or target.is_symlink():
            raise ValueError(f"Unexpected object in overlay: {target}")
        target.symlink_to(source)
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(output)] + [str(d) for d in lib_dirs])
    env["LEAN_NUM_THREADS"] = "1"
    report = {
        "scope": ("CONDITIONAL bridge: ES(8) <= 313 follows from Excludes2650Zero 32. "
                  "The arithmetic exclusion is NOT proved here and ES(8) <= 313 is NOT proved."),
        "lean": version, "platform": platform.platform(),
        "fresh_build": False, "complete": False, "overlay_created_empty": created_empty,
        "invocation": invocation,
        "checker_sha256": sha(Path(__file__)), "manifest_sha256": sha(BUNDLE / "manifest.json"),
        "validated_identities": identities,
        "reuse_pin_record": rel(RECORD_314), "reuse_pin_record_sha256": sha(RECORD_314),
        "reused_objects": reused, "modules": {},
    }
    audit_text, keep = [], True
    for k, (bundle, module) in enumerate(FRESH):
        source = fresh_sources[module]
        target = output / module_path(module).with_suffix(".olean")
        target.parent.mkdir(parents=True, exist_ok=True)
        log = output / (module + ".log")
        old = previous.get(module)
        keep = keep and bool(old) and old.get("source_sha256") == sha(source) \
            and target.is_file() and old.get("olean_sha256") == sha(target)
        if keep:
            entry = dict(old, invocation=old.get("invocation", 1))
            text = log.read_text()
        else:
            proc, seconds, rss = run_lean(lean, EXPERIMENTS / bundle, source, target, env, args.memory)
            text = proc.stdout + proc.stderr
            log.write_text(text)
            entry = {"bundle": "experiments/" + bundle, "source": rel(source),
                     "source_sha256": sha(source), "exit": proc.returncode,
                     "seconds": seconds, "max_rss_bytes": rss, "invocation": invocation}
            if proc.returncode != 0 or "warning:" in proc.stdout or "error:" in proc.stdout:
                report["modules"][module] = entry
                progress_path.write_text(json.dumps(report, indent=2) + "\n")
                print(text[-6000:], file=sys.stderr)
                raise RuntimeError(f"Lean failed or warned in {module}; log: {log}")
            entry["olean_sha256"] = sha(target)
        audits = parse_audits(text)
        for name, axioms in audits.items():
            if not set(axioms) <= STANDARD:
                raise ValueError(f"Nonstandard axioms in {name}: {axioms}")
        for name in REQUIRED.get(module, []):
            if NS + name not in audits:
                raise ValueError(f"Missing axiom audit for {NS + name} in {module}")
        entry["axioms"] = audits
        report["modules"][module] = entry
        if module in REQUIRED:
            audit_text.append(f"===== {module} =====\n{text}")
        progress_path.write_text(json.dumps(report, indent=2) + "\n")
        print(f"[{k + 1}/{len(FRESH)}] {module}: {entry['seconds']}s, "
              f"max RSS {entry.get('max_rss_bytes')}", flush=True)
    final_log = (output / "Residual32Bridge2650.Final.log").read_text()
    flat = re.sub(r"\s+", " ", final_log)
    for label, signature in FINAL_SIGNATURES.items():
        if signature not in flat:
            raise ValueError(f"Final statement differs from the expected {label} signature")
    library = ROOT / ".lake/build/lib/lean/ErdosSzekeres"
    report["library_objects"] = {rel(p): sha(p) for p in sorted(library.rglob("*.olean"))}
    report["final_theorems"] = {
        NS + "forces_convex_octagon_313_of_excludes": FINAL_SIGNATURES["forces"],
        NS + "residual_bound_121_of_excludes": FINAL_SIGNATURES["residual"],
        NS + "Excludes2650Zero": FINAL_SIGNATURES["Excludes2650Zero"],
    }
    report["final_axioms"] = {name: report["modules"]["Residual32Bridge2650.Final"]["axioms"][NS + name]
                              for name in REQUIRED["Residual32Bridge2650.Final"]}
    report["compile_seconds"] = round(sum(m["seconds"] for m in report["modules"].values()), 3)
    report["wall_seconds"] = round(time.monotonic() - started_all, 3)
    report["max_rss_bytes"] = max((m.get("max_rss_bytes") or 0) for m in report["modules"].values())
    report["overlay"] = rel(output)
    report["fresh_build"] = bool(created_empty) and all(
        m["invocation"] == invocation for m in report["modules"].values())
    report["complete"] = True
    (BUNDLE / "axioms.txt").write_text("\n".join(audit_text))
    report["axioms_sha256"] = sha(BUNDLE / "axioms.txt")
    (BUNDLE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")
    progress_path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Conditional bridge checked in {report['wall_seconds']}s; "
          f"record: {rel(BUNDLE / 'kernel-check.json')}", flush=True)


if __name__ == "__main__":
    main()
