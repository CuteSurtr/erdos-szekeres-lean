#!/usr/bin/env python3
"""Check exported omission modules with hash-bound resume records.

Run under ``lake env python3``. Sources must match export.json; only successful
Lean invocations with the expected standard-axiom report are resumable. A
selected block run never counts as a complete tree check. Generated files and
build products belong in an ignored directory, not the source tree. Independent
parts may run in parallel; the catalog is checked first and the root last.
Only the coordinating process writes the shared progress record.
"""
import argparse
from concurrent.futures import CancelledError, ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from omission_lean_export import sha256


ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def audit_output(output, expected):
    match = re.search(r"'" + re.escape(expected) +
                      r"' depends on axioms: \[([^]]*)\]", output)
    if match is None:
        raise ValueError(f"Missing axiom report: {expected}")
    axioms = {a.strip() for a in match[1].split(",") if a.strip()}
    if not axioms <= ALLOWED:
        raise ValueError(f"Unexpected axioms: {sorted(axioms - ALLOWED)}")
    return sorted(axioms)


def verify_sources(directory):
    manifest = json.loads((directory / "export.json").read_text())
    prefix = manifest.get("module_prefix", "")
    if prefix and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", prefix):
        raise ValueError("Invalid module prefix")
    relative = lambda name: f"{prefix}/{name}" if prefix else name
    for name, digest in manifest["files"].items():
        pattern = (re.escape(prefix) + "/" if prefix else "") + r"(?:Catalog|Root|Part[0-9]+)\.lean"
        if not re.fullmatch(pattern, name):
            raise ValueError(f"Invalid source name: {name}")
        if sha256(directory / name) != digest:
            raise ValueError(f"Source hash mismatch: {name}")
    expected = {relative("Catalog.lean"), relative("Root.lean")} | {
        relative(p["module"] + ".lean") for p in manifest["parts"]}
    if set(manifest["files"]) != expected:
        raise ValueError("Module list and file manifest disagree")
    return manifest


def run(directory, modules=None, resume=False, memory=6000, workers=1):
    if type(workers) is not int or workers < 1:
        raise ValueError("Worker count must be positive")
    if type(memory) is not int or memory < 1:
        raise ValueError("Memory limit must be positive")
    directory = directory.resolve()
    repo = Path(__file__).resolve().parents[1]
    manifest = verify_sources(directory)
    prefix = manifest.get("module_prefix", "")
    sources = directory / prefix if prefix else directory
    relative = lambda name: f"{prefix}/{name}" if prefix else name
    namespace = manifest["namespace"]
    theorem = {"Catalog": f"{namespace}.code_correct", **{
        p["module"]: f"{namespace}.node{p['root']}" for p in manifest["parts"]}}
    theorem["Root"] = (f"{namespace}.excludes_budget"
                       if manifest["root"] == manifest["full_tree_root"]
                       else f"{namespace}.node{manifest['root']}")
    if modules and (set(modules) - theorem.keys()):
        raise ValueError("Unknown module selection")
    # A root needs every part; a selected part needs only the catalog.
    selected = list(theorem) if not modules or "Root" in modules else list(dict.fromkeys([
        "Catalog", *(m for m in modules if m != "Catalog")]))
    env = dict(os.environ)
    env["LEAN_PATH"] = str(directory) + os.pathsep + env.get("LEAN_PATH", "")
    version = subprocess.check_output(["lean", "--version"], text=True, env=env).strip()
    inputs = [repo / "lean-toolchain", repo / "lake-manifest.json",
              repo / ".lake/build/lib/lean/ErdosSzekeres/OmissionCertificates.olean",
              repo / ".lake/build/lib/lean/ErdosSzekeres/OmissionPacking.olean"]
    binding = {"manifest": sha256(directory / "export.json"), "lean": version,
               "inputs": {str(p.relative_to(repo)): sha256(p) for p in inputs}}
    fingerprint = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    record_path = directory / "kernel-check.json"
    previous = json.loads(record_path.read_text()) if resume and record_path.exists() else {}
    records = previous.get("modules", {}) if previous.get("fingerprint") == fingerprint else {}
    report = {"scope": manifest["scope"], "binding": binding, "fingerprint": fingerprint,
              "modules": records, "complete": False}
    def save():
        temporary = record_path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(report, indent=2) + "\n")
        temporary.replace(record_path)

    def resumable(name):
        obj = sources / f"{name}.olean"
        old = records.get(name, {})
        if (resume and old.get("exit") == 0 and old.get("audited") is True
                and obj.exists() and old.get("olean_sha256") == sha256(obj)):
            print(f"{name}: verified resume record", flush=True)
            return True
        return False

    def compile_module(name):
        obj = sources / f"{name}.olean"
        command = ["lean", "-j", "1", "-s", "32768", "-M", str(memory),
                   "--root=" + str(directory),
                   str(sources / f"{name}.lean"), "-o", str(obj)]
        started = time.monotonic()
        result = subprocess.run(command, text=True, capture_output=True, env=env, cwd=repo)
        record = {"exit": result.returncode, "seconds": round(time.monotonic() - started, 3),
                  "source_sha256": manifest["files"][relative(f"{name}.lean")],
                  "stdout": result.stdout, "stderr": result.stderr, "audited": False}
        if result.returncode == 0:
            try:
                record["axioms"] = audit_output(result.stdout, theorem[name])
                record["olean_sha256"] = sha256(obj)
                record["audited"] = True
            except (ValueError, OSError) as error:
                record["audit_error"] = str(error)
        return record

    def record_result(name, record):
        records[name] = record
        save()
        print(f"{name}: exit={record['exit']}, audited={record['audited']}, "
              f"{record['seconds']} seconds", flush=True)
        return record["audited"]

    def failure(name):
        record = records[name]
        return RuntimeError(f"Kernel check failed; see {record_path}\n" +
                            (record["stdout"] + record["stderr"])[-2000:])

    # Keep dependencies sequential. Each part imports only the catalog.
    if not resumable("Catalog"):
        if not record_result("Catalog", compile_module("Catalog")):
            raise failure("Catalog")
    pending = [m for m in selected if m not in ("Catalog", "Root") and not resumable(m)]
    failed = None
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(compile_module, name): name for name in pending}
        try:
            for future in as_completed(futures):
                name = futures[future]
                try:
                    record = future.result()
                except CancelledError:
                    continue
                if not record_result(name, record) and failed is None:
                    failed = name
                    # Preserve results already running; cancel queued work.
                    for other in futures:
                        other.cancel()
        except BaseException:
            # An interrupt or process-launch error must not drain a long queue.
            for future in futures:
                future.cancel()
            raise
    if failed is not None:
        raise failure(failed)
    if "Root" in selected and not resumable("Root"):
        if not record_result("Root", compile_module("Root")):
            raise failure("Root")
    report["complete"] = (selected == list(theorem) and all(
        records[m].get("audited") is True for m in theorem))
    save()
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--module", action="append", help="Check selected blocks only")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--memory", type=int, default=6000, help="Lean memory limit in MiB")
    parser.add_argument("--workers", type=int, default=1,
                        help="Parallel part checks; --memory applies to each worker")
    args = parser.parse_args()
    if args.memory < 1:
        parser.error("Memory limit must be positive")
    if args.workers < 1:
        parser.error("Worker count must be positive")
    result = run(args.directory, args.module, args.resume, args.memory, args.workers)
    print(json.dumps({"complete": result["complete"], "recorded_modules": len(result["modules"])}))
