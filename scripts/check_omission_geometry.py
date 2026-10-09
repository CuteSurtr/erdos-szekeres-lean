#!/usr/bin/env python3
"""Check all balanced geometric rows and the 192-point corollary.

Run under ``lake env python3`` after building the main library and the separate
balanced arithmetic certificate. Generated sources and objects stay ignored.
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
    prefix = manifest.get("arithmetic_prefix", "")
    if prefix and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", prefix):
        raise ValueError("Invalid arithmetic module prefix")
    expected = {"BalancedGeometry.lean"}
    if prefix:
        expected.add("BalancedOccupancy.lean")
    start = 0
    for block in manifest["modules"]:
        name = block["module"]
        if (not re.fullmatch(r"Geometry[0-9]{5}", name) or
                block["start"] != start or not start < block["end"] <= 2685):
            raise ValueError("Invalid or discontinuous row blocks")
        expected.add(name + ".lean")
        start = block["end"]
    if start != 2685 or set(manifest["files"]) != expected:
        raise ValueError("Incomplete geometry source manifest")
    for name, sha in manifest["files"].items():
        if digest(directory / name) != sha:
            raise ValueError(f"Source hash mismatch: {name}")
    return manifest


def run(directory, arithmetic, resume=False, memory=6000):
    repo = Path(__file__).resolve().parents[1]
    directory, arithmetic = directory.resolve(), arithmetic.resolve()
    manifest = verify_sources(directory)
    prefix = manifest.get("arithmetic_prefix", "")
    arithmetic_manifest = json.loads((arithmetic / "export.json").read_text())
    if arithmetic_manifest.get("module_prefix", "") != prefix:
        raise ValueError("Geometry and arithmetic module prefixes differ")
    arithmetic_sources = arithmetic / prefix if prefix else arithmetic
    occupancy = (directory / "BalancedOccupancy.lean" if prefix else
                 repo / "experiments/omission-balanced-lean-2026-10-09/Occupancy.lean")
    # Bind resumptions to both source and compiled local prerequisites. Mathlib
    # and toolchain revisions are pinned by the two tracked configuration files.
    inputs = [repo / "lean-toolchain", repo / "lake-manifest.json", occupancy,
              arithmetic / "export.json", arithmetic_sources / "Catalog.olean",
              arithmetic_sources / "Root.olean"]
    inputs += sorted((repo / ".lake/build/lib/lean/ErdosSzekeres").rglob("*.olean"))
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(directory), str(arithmetic), env.get("LEAN_PATH", "")])
    version = subprocess.check_output(["lean", "--version"], text=True, env=env).strip()
    binding = {"manifest": digest(directory / "export.json"), "lean": version,
               "inputs": {str(p): digest(p) for p in inputs}}
    fingerprint = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    path = directory / "kernel-check.json"
    old = json.loads(path.read_text()) if resume and path.exists() else {}
    records = old.get("modules", {}) if old.get("fingerprint") == fingerprint else {}
    report = {"scope": manifest["scope"], "binding": binding, "fingerprint": fingerprint,
              "modules": records, "complete": False}
    modules = [(occupancy, ["OmissionBalanced.occupied_card_le"])]
    modules += [(directory / (m["module"] + ".lean"),
                 [f"OmissionBalanced.{m['module']}.row_bound"]) for m in manifest["modules"]]
    modules += [(directory / "BalancedGeometry.lean",
                 ["OmissionBalanced.all_geometric_rows", "OmissionBalanced.real_configuration_bound"])]
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
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--memory", type=int, default=6000)
    args = parser.parse_args()
    if args.memory < 1:
        parser.error("Memory limit must be positive")
    result = run(args.directory, args.arithmetic, args.resume, args.memory)
    print(json.dumps({"complete": result["complete"], "modules": len(result["modules"])}))
