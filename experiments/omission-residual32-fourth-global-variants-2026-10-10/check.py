#!/usr/bin/env python3
"""Check source identities and freshly compile128 rows in16-row chunks."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DEFAULT_CACHE = ROOT / ".cache/residual32-fourth-global-variants-2026-10-10"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight(manifest):
    checked = {}
    for name, expected in manifest["external_inputs"].items():
        actual = sha(ROOT / name)
        if actual != expected:
            raise ValueError("Changed external source: " + name)
        checked[name] = actual
    for name, expected in {**manifest["inputs"], **manifest["files"], "generate.py": manifest["generator_sha256"]}.items():
        actual = sha(HERE / name)
        if actual != expected:
            raise ValueError("Changed bundle input: " + name)
        checked[str((HERE / name).relative_to(ROOT))] = actual
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_CACHE)
    args = parser.parse_args()
    manifest = json.loads((HERE / "manifest.json").read_text())
    checked = preflight(manifest)
    if args.preflight_only:
        print(json.dumps({"passed": True, "identities": len(checked)}))
        return
    cache = args.output.resolve()
    (cache / "FourthGlobalProof").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["LEAN_PATH"] = str(cache) + os.pathsep + env.get("LEAN_PATH", "")
    env["LEAN_NUM_THREADS"] = "1"
    version = subprocess.check_output(["lean", "--version"], text=True).strip()
    if "version 4.24.0," not in version:
        raise ValueError("Use pinned Lean4.24.0")
    report = {"scope": manifest["scope"], "complete": False, "lean": version,
              "manifest_sha256": sha(HERE / "manifest.json"), "checker_sha256": sha(Path(__file__)),
              "validated_identities": checked, "modules": {}, "rows": 128, "part_size": 16}
    audits = []
    for module in manifest["modules"]:
        src = HERE / "FourthGlobalProof" / (module + ".lean")
        obj = cache / "FourthGlobalProof" / (module + ".olean")
        log = cache / (module + ".log")
        start = time.monotonic()
        p = subprocess.run(["lean", "-j1", "-s", "32768", "-M", "14000", "--root=" + str(HERE),
                            "-o", str(obj), str(src)], cwd=ROOT, env=env, text=True, capture_output=True)
        text = p.stdout + p.stderr
        log.write_text(text)
        record = {"exit": p.returncode, "seconds": round(time.monotonic()-start, 3),
                  "source_sha256": sha(src), "log_sha256": sha(log)}
        report["modules"][module] = record
        print(module, p.returncode, record["seconds"], flush=True)
        if p.returncode or "warning:" in text:
            (HERE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")
            raise RuntimeError(text)
        expected = [] if module == "Data" else ([manifest["namespace"] + "." + module + ".checked"] if module.startswith("Part") else [manifest["namespace"] + ".checked", manifest["namespace"] + ".all_rows"])
        matches = dict(re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text))
        record["axioms"] = {}
        for name in expected:
            if name not in matches:
                raise ValueError("Missing theorem audit: " + name)
            actual = {a.strip() for a in matches[name].split(",") if a.strip()}
            if not actual <= STANDARD:
                raise ValueError("Unexpected axioms: " + str(actual))
            record["axioms"][name] = sorted(actual)
        record["olean_sha256"] = sha(obj)
        audits.append(text)
        (HERE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")
    (HERE / "axioms.txt").write_text("".join(audits))
    report["axioms_sha256"] = sha(HERE / "axioms.txt")
    report["complete"] = True
    (HERE / "kernel-check.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
