#!/usr/bin/env python3
"""Export/check the 2,685 balanced geometric rows without an arithmetic root."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from check_axioms import audit_output
from check_omission_geometry import verify_sources
from check_omission_global import digest, require_hash, verify_snapshot


def export(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    manifest = verify_sources(source)
    if manifest.get("arithmetic_prefix") != "BalancedProof":
        raise ValueError("This export requires the linked BalancedProof catalog")
    if output.exists():
        raise FileExistsError(output)
    output.mkdir(parents=True)
    for item in manifest["modules"]:
        name = item["module"] + ".lean"
        (output / name).write_bytes((source / name).read_bytes())
    aggregate = (source / "BalancedGeometry.lean").read_text()
    aggregate = aggregate.replace("import BalancedProof.Root\n", "").replace("import BalancedOccupancy\n", "")
    aggregate = aggregate.split("theorem real_configuration_bound", 1)[0]
    aggregate += "#print axioms all_geometric_rows\nend OmissionBalanced\n"
    (output / "BalancedRows.lean").write_text(aggregate)
    result = {"kind": "balanced_rows_only", "scope": "All 2685 actual balanced geometric rows; no population bound",
              "arithmetic_prefix": "BalancedProof", "rows": 2685,
              "parent_manifest_sha256": digest(source / "export.json"),
              "modules": manifest["modules"], "files": {
                  p.name: digest(p) for p in sorted(output.glob("*.lean"))}}
    (output / "export.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def run(directory, arithmetic, memory=2500, resume=False):
    repo = Path(__file__).resolve().parents[1]
    directory, arithmetic = Path(directory).resolve(), Path(arithmetic).resolve()
    manifest = json.loads((directory / "export.json").read_text())
    if manifest.get("kind") != "balanced_rows_only" or manifest.get("rows") != 2685:
        raise ValueError("Wrong balanced row family")
    if memory < 1:
        raise ValueError("Memory must be positive")
    start = 0
    for m in manifest["modules"]:
        if (not re.fullmatch(r"Geometry[0-9]{5}", m["module"]) or m["start"] != start or
                not start < m["end"] <= 2685):
            raise ValueError("Invalid or discontinuous balanced row blocks")
        start = m["end"]
    if start != 2685:
        raise ValueError("Incomplete balanced row coverage")
    modules = [(m["module"], [f"OmissionBalanced.{m['module']}.row_bound"]) for m in manifest["modules"]]
    modules.append(("BalancedRows", ["OmissionBalanced.all_geometric_rows"]))
    if set(manifest["files"]) != {m + ".lean" for m, _ in modules}:
        raise ValueError("Geometry module list disagrees with manifest")
    for name, sha in manifest["files"].items():
        require_hash(directory / name, sha)
    arith = json.loads((arithmetic / "export.json").read_text())
    if arith.get("module_prefix") != "BalancedProof" or arith.get("namespace") != "OmissionBalanced":
        raise ValueError("Wrong balanced catalog")
    catalog_source = arithmetic / "BalancedProof/Catalog.lean"
    catalog_obj = arithmetic / "BalancedProof/Catalog.olean"
    catalog = json.loads((arithmetic / "kernel-check.json").read_text())["modules"]["Catalog"]
    require_hash(catalog_source, arith["files"]["BalancedProof/Catalog.lean"])
    if catalog["source_sha256"] != arith["files"]["BalancedProof/Catalog.lean"]:
        raise ValueError("Catalog source and check record disagree")
    require_hash(catalog_obj, catalog["olean_sha256"])
    if catalog.get("audited") is not True or catalog.get("exit") != 0:
        raise ValueError("The catalog has not passed")
    audit_output(catalog["stdout"], "OmissionBalanced.code_correct")
    inputs = [repo / "lean-toolchain", repo / "lake-manifest.json", catalog_source, catalog_obj,
              arithmetic / "export.json"]
    inputs += sorted((repo / ".lake/build/lib/lean/ErdosSzekeres").rglob("*.olean"))
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(directory), str(arithmetic), env.get("LEAN_PATH", "")])
    version = subprocess.check_output(["lean", "--version"], env=env, text=True).strip()
    binding = {"manifest": digest(directory / "export.json"), "lean": version,
               "inputs": {str(p): digest(p) for p in inputs}}
    fingerprint = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    path = directory / "kernel-check.json"
    previous = json.loads(path.read_text()) if resume and path.exists() else {}
    records = previous.get("modules", {}) if previous.get("fingerprint") == fingerprint else {}
    report = {"scope": manifest["scope"], "binding": binding, "fingerprint": fingerprint,
              "modules": records, "complete": False}
    def save():
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(report, indent=2) + "\n")
        temporary.replace(path)
    save()
    for name, expected in modules:
        source, obj = directory / (name + ".lean"), directory / (name + ".olean")
        prior = records.get(name, {})
        if resume and prior.get("audited") is True and prior.get("exit") == 0 and obj.exists() and (
                prior.get("olean_sha256") == digest(obj)):
            print(f"{name}: verified resume record", flush=True)
            continue
        started = time.monotonic()
        process = subprocess.run(["lean", "-j", "1", "-s", "32768", "-M", str(memory),
                                  str(source), "-o", str(obj)], cwd=repo, env=env,
                                 text=True, capture_output=True)
        record = {"source_sha256": digest(source), "exit": process.returncode,
                  "seconds": round(time.monotonic() - started, 3), "stdout": process.stdout,
                  "stderr": process.stderr, "audited": False}
        records[name] = record
        if process.returncode == 0:
            try:
                record["axioms"] = {n: audit_output(process.stdout, n) for n in expected}
                record["olean_sha256"] = digest(obj)
                record["audited"] = True
            except ValueError as error:
                record["audit_error"] = str(error)
        save()
        print(f"{name}: exit={process.returncode}, audited={record['audited']}, {record['seconds']} seconds", flush=True)
        if not record["audited"]:
            raise RuntimeError(f"Balanced row check failed; see {path}\n" +
                               (process.stdout + process.stderr)[-3000:])
    verify_snapshot(binding["inputs"])
    report["complete"] = True
    save()
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    exporter = commands.add_parser("export")
    exporter.add_argument("source", type=Path)
    exporter.add_argument("output", type=Path)
    checker = commands.add_parser("check")
    checker.add_argument("directory", type=Path)
    checker.add_argument("--arithmetic", type=Path, required=True)
    checker.add_argument("--memory", type=int, default=2500)
    checker.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.command == "export":
        result = export(args.source, args.output)
        print(json.dumps({"rows": result["rows"], "modules": len(result["files"])}))
    else:
        result = run(args.directory, args.arithmetic, args.memory, args.resume)
        print(json.dumps({"complete": result["complete"], "modules": len(result["modules"])}))
