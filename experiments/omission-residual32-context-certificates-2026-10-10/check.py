#!/usr/bin/env python3
"""Compile fresh Lean objects and audit all five conditional exclusions.

Run from the repository root through its pinned `lake env python3`.
Build products and full logs are confined to ignored `.cache/`.
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parent.parent
CACHE = ROOT / ".cache/residual32-context-certificates-2026-10-10"
PREFIX = "Residual32ContextsProof"
EXPECTED = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight(manifest):
    """Read-only identity validation; this never invokes Lean or writes files."""
    checked = {}

    def verify(label, actual, expected):
        if actual != expected:
            raise ValueError(f"Provenance mismatch for {label}: expected {expected}, got {actual}")
        checked[label] = actual

    source = ROOT / manifest["source_reference"]
    archive = source.read_bytes()
    verify("source archive", hashlib.sha256(archive).hexdigest(),
           manifest["source_archive_sha256"])
    verify("uncompressed source", hashlib.sha256(gzip.decompress(archive)).hexdigest(),
           manifest["source_uncompressed_sha256"])
    for label, reference, digest_key in [
        ("diagnostic", manifest["diagnostic_reference"], "diagnostic_sha256"),
        ("pending contexts", manifest["pending_contexts_reference"], "pending_contexts_sha256"),
        ("generator", str((BUNDLE / "generate.py").relative_to(ROOT)), "generator_sha256"),
        ("exporter", "scripts/omission_lean_export.py", "exporter_sha256"),
    ]:
        verify(label, sha(ROOT / reference), manifest[digest_key])
    for name, expected in manifest["files"].items():
        verify("generated source " + name, sha(BUNDLE / name), expected)
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true",
                        help="validate all recorded source identities without compiling or writing")
    args = parser.parse_args()
    manifest = json.loads((BUNDLE / "manifest.json").read_text())
    identities = preflight(manifest)
    if args.preflight_only:
        print(json.dumps({"preflight_passed": True, "validated_identities": identities}, indent=2))
        return
    lean = shutil.which("lean")
    if lean is None:
        raise RuntimeError("Run through the pinned Lake environment")
    version = subprocess.check_output([lean, "--version"], text=True).strip()
    assert "version 4.24.0," in version
    env = dict(os.environ)
    env["LEAN_PATH"] = str(CACHE) + os.pathsep + env.get("LEAN_PATH", "")
    env["LEAN_NUM_THREADS"] = "1"
    (CACHE / PREFIX).mkdir(parents=True, exist_ok=True)
    modules = ["Catalog"] + [c["module"].split(".")[-1] for c in manifest["contexts"]] + ["Audit"]
    checked, audit = [], ""
    for name in modules:
        source = BUNDLE / PREFIX / (name + ".lean")
        output = CACHE / PREFIX / (name + ".olean")
        log = CACHE / (name + ".log")
        started = time.monotonic()
        with log.open("w") as stream:
            result = subprocess.run([lean, "-j1", "--root=" + str(BUNDLE),
                                     "-o", str(output), str(source)], cwd=ROOT,
                                    env=env, stdout=stream, stderr=subprocess.STDOUT)
        elapsed = round(time.monotonic() - started, 3)
        text = log.read_text()
        print(f"{name}: exit {result.returncode}, {elapsed}s", flush=True)
        if result.returncode != 0 or "warning:" in text:
            raise RuntimeError(text)
        checked.append({"module": PREFIX + "." + name, "seconds": elapsed,
                        "source_sha256": sha(source), "log_sha256": sha(log),
                        "olean_sha256": sha(output)})
        if name == "Audit":
            audit = text
    matches = dict(re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit))
    for context in manifest["contexts"]:
        name = context["theorem"]
        assert name in matches, f"Missing theorem audit: {name}"
        actual = {a.strip() for a in matches[name].split(",") if a.strip()}
        assert actual <= EXPECTED, (name, actual)
    assert len(matches) == 5
    (BUNDLE / "axioms.txt").write_text(audit)
    report = {"scope": manifest["scope"], "lean": version,
              "manifest_sha256": sha(BUNDLE / "manifest.json"),
              "checker_sha256": sha(Path(__file__)), "all_modules_passed": True,
              "validated_identities": identities,
              "conditional_exclusions": 5, "modules": checked,
              "axioms_sha256": sha(BUNDLE / "axioms.txt"),
              "axioms": {n: [a.strip() for a in v.split(",") if a.strip()]
                         for n, v in matches.items()},
              "geometric_transfer_checked": False, "complete_32_hole_exclusion": False,
              "frozen_tree_modified": False}
    (BUNDLE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
