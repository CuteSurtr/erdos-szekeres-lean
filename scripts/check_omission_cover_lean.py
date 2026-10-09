#!/usr/bin/env python3
"""Hash-bind Lean checks of arithmetic cover-cut transfer modules.

Run under ``lake env python3``. The generic rounding lemma and the original
catalog must already be compiled. The normal CLI compiles the listed module;
``record_build`` also records an already observed successful invocation, provided
its frozen source still matches the manifest. Generated sources/objects stay in
an ignored directory. Neither an LP result nor Python margin replay substitutes
for the Lean build and final theorem axiom report.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from check_omission_lean import audit_output


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources(directory):
    manifest = json.loads((directory / "export.json").read_text())
    for key in ("module", "namespace", "catalog_namespace"):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", manifest[key]):
            raise ValueError(f"Invalid {key}")
    if not re.fullmatch(r"(?:[A-Za-z][A-Za-z0-9_]*\.)?Catalog", manifest["catalog_module"]):
        raise ValueError("Invalid original catalog module")
    name = manifest["module"] + ".lean"
    if set(manifest["files"]) != {name}:
        raise ValueError("Unexpected cover transfer source list")
    if digest(directory / name) != manifest["files"][name]:
        raise ValueError("Cover transfer source hash mismatch")
    for key in ("source", "certificate"):
        if digest(Path(manifest[key])) != manifest[key + "_sha256"]:
            raise ValueError(f"Changed {key} data")
    return manifest


def binding(directory, arithmetic, manifest, version):
    repo = Path(__file__).resolve().parents[1]
    catalog = arithmetic / manifest["catalog_module"].replace(".", "/")
    paths = [repo / "lean-toolchain", repo / "lake-manifest.json",
             arithmetic / "export.json", catalog.with_suffix(".lean"),
             catalog.with_suffix(".olean"),
             repo / "ErdosSzekeres/Omission/CoverCuts.lean",
             repo / ".lake/build/lib/lean/ErdosSzekeres/Omission/CoverCuts.olean",
             repo / ".lake/build/lib/lean/ErdosSzekeres/OmissionCertificates.olean",
             repo / ".lake/build/lib/lean/ErdosSzekeres/OmissionPacking.olean"]
    return {"manifest": digest(directory / "export.json"), "lean": version,
            "inputs": {str(path.resolve()): digest(path) for path in paths}}


def record_build(directory, arithmetic, exit_code, stdout, stderr="", seconds=None,
                 version=None):
    """Record an invocation whose exit code and output were observed by caller."""
    directory, arithmetic = directory.resolve(), arithmetic.resolve()
    manifest = verify_sources(directory)
    if version is None:
        version = subprocess.check_output(["lean", "--version"], text=True).strip()
    bound = binding(directory, arithmetic, manifest, version)
    fingerprint = hashlib.sha256(json.dumps(bound, sort_keys=True).encode()).hexdigest()
    module = manifest["module"]
    report = {"scope": manifest["scope"], "binding": bound,
              "fingerprint": fingerprint, "modules": {}, "complete": False}
    record = {"exit": exit_code, "source_sha256": manifest["files"][module + ".lean"],
              "stdout": stdout, "stderr": stderr, "audited": False}
    if seconds is not None:
        record["seconds"] = seconds
    if exit_code == 0:
        theorem = manifest["namespace"] + ".all_rows"
        record["axioms"] = {theorem: audit_output(stdout, theorem)}
        record["olean_sha256"] = digest(directory / (module + ".olean"))
        record["audited"] = True
        report["complete"] = True
    report["modules"][module] = record
    temporary = directory / "kernel-check.json.tmp"
    temporary.write_text(json.dumps(report, indent=2) + "\n")
    temporary.replace(directory / "kernel-check.json")
    return report


def run(directory, arithmetic, memory=6000):
    directory, arithmetic = directory.resolve(), arithmetic.resolve()
    manifest = verify_sources(directory)
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(directory), str(arithmetic),
                                        env.get("LEAN_PATH", "")])
    module = manifest["module"]
    version = subprocess.check_output(["lean", "--version"], env=env, text=True).strip()
    started = time.monotonic()
    result = subprocess.run(["lean", "-j", "1", "-s", "32768", "-M", str(memory),
                             "--root=" + str(directory),
                             str(directory / (module + ".lean")), "-o",
                             str(directory / (module + ".olean"))],
                            env=env, text=True, capture_output=True)
    report = record_build(directory, arithmetic, result.returncode, result.stdout,
                          result.stderr, time.monotonic() - started, version)
    if not report["complete"]:
        raise RuntimeError("Cover-cut Lean check failed; see kernel-check.json")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--arithmetic", type=Path, required=True)
    parser.add_argument("--memory", type=int, default=6000)
    args = parser.parse_args()
    if args.memory < 1:
        parser.error("Memory limit must be positive")
    report = run(args.directory, args.arithmetic, args.memory)
    print(json.dumps({"complete": report["complete"], "modules": len(report["modules"])}))
