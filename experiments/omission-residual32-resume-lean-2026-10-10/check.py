#!/usr/bin/env python3
"""Fresh kernel compilation with frozen-input and prerequisite-object checks.

Run from the repository root with its pinned `lake env python3`.
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parent.parent
CACHE = ROOT / ".cache/residual32-resume-lean-2026-10-10"
OLD = ROOT / "experiments/omission-residual32-context-certificates-2026-10-10"
TRANSFER = ROOT / "experiments/omission-residual32-transfer-2026-10-10"
PATHS = [CACHE, ROOT / ".cache/residual32-context-certificates-2026-10-10",
         ROOT / ".cache/residual32-transfer-2026-10-10",
         ROOT / ".cache/omission-lean-full/residual", ROOT / ".cache/omission-residual-geometry",
         ROOT / ".cache/omission-residual-blocks", ROOT / ".cache/omission-cover-transfer-residual-v2"]
STANDARD = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight(manifest):
    identities = {}

    def require(path, expected):
        actual = sha(path)
        if actual != expected:
            raise ValueError(f"Changed prerequisite: {path}; expected {expected}, got {actual}")
        identities[str(path.relative_to(ROOT))] = actual

    require(BUNDLE / "generate.py", manifest["generator_sha256"])
    for name, expected in manifest["external_inputs"].items():
        require(ROOT / name, expected)
    for name, expected in manifest["files"].items():
        require(BUNDLE / name, expected)
    for proof in manifest["proofs"]:
        require(ROOT / proof["archive"], proof["archive_sha256"])
    source = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
    actual = hashlib.sha256(gzip.decompress(source.read_bytes())).hexdigest()
    if actual != manifest["source_uncompressed_sha256"]:
        raise ValueError("Changed uncompressed source identity")
    old = json.loads((OLD / "kernel-check.json").read_text())
    if not old["all_modules_passed"]:
        raise ValueError("The catalog prerequisite has no successful check record")
    require(OLD / "manifest.json", old["manifest_sha256"])
    catalog = next(x for x in old["modules"] if x["module"] == "Residual32ContextsProof.Catalog")
    require(PATHS[1] / "Residual32ContextsProof/Catalog.olean", catalog["olean_sha256"])
    transfer = json.loads((TRANSFER / "kernel-check.json").read_text())
    if not transfer["complete"]:
        raise ValueError("The geometric transfer prerequisite is incomplete")
    for name, record in transfer["modules"].items():
        require(TRANSFER / (name + ".lean"), record["source_sha256"])
        require(PATHS[2] / (name + ".olean"), record["olean_sha256"])
    for name, expected in transfer["imports"].items():
        require(ROOT / name, expected)
    for name, expected in transfer["external_sources"].items():
        require(ROOT / name, expected)
    return identities


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((BUNDLE / "manifest.json").read_text())
    identities = preflight(manifest)
    if args.preflight_only:
        print(json.dumps({"passed": True, "validated_identities": len(identities)}))
        return
    version = subprocess.check_output(["lean", "--version"], text=True).strip()
    if "version 4.24.0," not in version:
        raise ValueError("Use the repository's pinned Lean4.24.0")
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join(map(str, PATHS)) + os.pathsep + env.get("LEAN_PATH", "")
    env["LEAN_NUM_THREADS"] = "1"
    (CACHE / "Residual32ResumeProof").mkdir(parents=True, exist_ok=True)
    units = [(p["module"], [p["theorem"]]) for p in manifest["proofs"]]
    units += [("Residual32ResumeProof.Geometry", [p["geometric_theorem"] for p in manifest["proofs"]])]
    report = {"scope": manifest["scope"], "lean": version, "complete": False,
              "manifest_sha256": sha(BUNDLE / "manifest.json"), "checker_sha256": sha(Path(__file__)),
              "validated_identities": identities, "modules": {},
              "conditional_exclusions": 6, "geometric_context_exclusions": 6,
              "complete_32_hole_exclusion": False, "frozen_tree_modified": False}
    audit = []
    for name, theorems in units:
        relative = Path(*name.split("."))
        src, out = BUNDLE / relative.with_suffix(".lean"), CACHE / relative.with_suffix(".olean")
        started = time.monotonic()
        p = subprocess.run(["lean", "-j1", "-s", "32768", "-M", "14000",
                            "--root=" + str(BUNDLE), "-o", str(out), str(src)],
                           cwd=ROOT, env=env, text=True, capture_output=True)
        text = p.stdout + p.stderr
        log = CACHE / (name + ".log")
        log.write_text(text)
        record = {"exit": p.returncode, "seconds": round(time.monotonic() - started, 3),
                  "source_sha256": sha(src), "log_sha256": sha(log)}
        print(name, record["exit"], record["seconds"], flush=True)
        report["modules"][name] = record
        if p.returncode or "warning:" in text:
            (BUNDLE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")
            raise RuntimeError(text)
        matches = dict(re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text))
        record["axioms"] = {}
        for theorem in theorems:
            if theorem not in matches:
                raise ValueError("Missing axiom audit: " + theorem)
            actual = {x.strip() for x in matches[theorem].split(",") if x.strip()}
            if not actual <= STANDARD:
                raise ValueError("Unexpected axioms: " + str((theorem, actual)))
            record["axioms"][theorem] = sorted(actual)
        record["olean_sha256"] = sha(out)
        audit.append(text)
        (BUNDLE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")
    (BUNDLE / "axioms.txt").write_text("".join(audit))
    report["axioms_sha256"] = sha(BUNDLE / "axioms.txt")
    report["complete"] = True
    (BUNDLE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
