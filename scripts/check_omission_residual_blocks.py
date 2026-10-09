#!/usr/bin/env python3
"""Check all 23 block rows and their composition with the cycle rows.

Run under ``lake env python3`` after building the main library and the separate
residual arithmetic catalog. Generated sources and objects stay ignored.
Every geometry module is hash checked and its theorem's axioms audited.
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
from omission_geometry_export import digest


def verify_sources(directory):
    manifest = json.loads((directory / "export.json").read_text())
    expected_rows = [973, *range(1165, 1187)]
    if manifest["block_rows"] != 23 or manifest["total_rows"] != 1187:
        raise ValueError("Incorrect block scope")
    if [m["row"] for m in manifest["modules"]] != expected_rows:
        raise ValueError("Missing or misordered block rows")
    expected = {"ResidualAllGeometry.lean"}
    for block in manifest["modules"]:
        if block["module"] != f"ResidualBlock{block['row']:05d}":
            raise ValueError("Invalid block module name")
        expected.add(block["module"] + ".lean")
    if set(manifest["files"]) != expected:
        raise ValueError("Incomplete block manifest")
    for name, sha in manifest["files"].items():
        if digest(directory / name) != sha:
            raise ValueError(f"Source hash mismatch: {name}")
    return manifest


def run(directory, arithmetic, cycles, resume=False, memory=6000):
    repo = Path(__file__).resolve().parents[1]
    directory, arithmetic, cycles = directory.resolve(), arithmetic.resolve(), cycles.resolve()
    manifest = verify_sources(directory)
    catalog_module = manifest.get("catalog_module", "Catalog")
    if re.fullmatch(r"(?:[A-Za-z][A-Za-z0-9_]*\.)?Catalog", catalog_module) is None:
        raise ValueError("Invalid arithmetic catalog module")
    catalog = arithmetic / catalog_module.replace(".", "/")
    # Bind resumptions to both source and compiled local prerequisites. Mathlib
    # and toolchain revisions are pinned by the two tracked configuration files.
    inputs = [repo / "lean-toolchain", repo / "lake-manifest.json",
              arithmetic / "export.json", catalog.with_suffix(".lean"), catalog.with_suffix(".olean")]
    inputs += sorted((repo / ".lake/build/lib/lean/ErdosSzekeres").rglob("*.olean"))
    inputs += [cycles / "export.json"] + sorted(cycles.glob("*.olean"))
    if not (cycles / "ResidualGeometry.olean").exists():
        raise ValueError("Complete cycle proof is required first")
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(directory), str(arithmetic), str(cycles), env.get("LEAN_PATH", "")])
    version = subprocess.check_output(["lean", "--version"], text=True, env=env).strip()
    binding = {"manifest": digest(directory / "export.json"), "lean": version,
               "inputs": {str(p): digest(p) for p in inputs}}
    fingerprint = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    path = directory / "kernel-check.json"
    old = json.loads(path.read_text()) if resume and path.exists() else {}
    records = old.get("modules", {}) if old.get("fingerprint") == fingerprint else {}
    report = {"scope": manifest["scope"], "binding": binding, "fingerprint": fingerprint,
              "modules": records, "complete": False}
    modules = [(directory / (m["module"] + ".lean"),
                 [f"OmissionResidual.{m['module']}.row_bound"]) for m in manifest["modules"]]
    modules += [(directory / "ResidualAllGeometry.lean",
                 ["OmissionResidual.all_geometric_rows"])]
    for source, theorems in modules:
        name = source.stem
        obj = directory / (name + ".olean")
        prior = records.get(name, {})
        if (resume and prior.get("audited") is True and prior.get("exit") == 0
                and obj.exists() and prior.get("olean_sha256") == digest(obj)):
            print(f"{name}: verified resume record", flush=True)
            continue
        started = time.monotonic()
        result = subprocess.run(["lean", "-j", "1", "-s", "32768", "-M", str(memory),
                                 str(source), "-o", str(obj)], cwd=repo, env=env,
                                text=True, capture_output=True)
        record = {"exit": result.returncode, "seconds": round(time.monotonic() - started, 3),
                  "source_sha256": digest(source), "stdout": result.stdout, "stderr": result.stderr,
                  "audited": False}
        if result.returncode == 0:
            try:
                record["axioms"] = {t: audit_output(result.stdout, t) for t in theorems}
                record["olean_sha256"] = digest(obj)
                record["audited"] = True
            except (ValueError, OSError) as error:
                record["audit_error"] = str(error)
        records[name] = record
        path.write_text(json.dumps(report, indent=2) + "\n")
        print(f"{name}: exit={record['exit']}, audited={record['audited']}, {record['seconds']} seconds", flush=True)
        if not record["audited"]:
            raise RuntimeError(f"Check failed; see {path}\n" + (result.stdout + result.stderr)[-3000:])
    report["complete"] = True
    path.write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--arithmetic", type=Path, required=True)
    parser.add_argument("--cycles", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--memory", type=int, default=6000)
    args = parser.parse_args()
    if args.memory < 1:
        parser.error("Memory limit must be positive")
    result = run(args.directory, args.arithmetic, args.cycles, args.resume, args.memory)
    print(json.dumps({"complete": result["complete"], "modules": len(result["modules"])}))
