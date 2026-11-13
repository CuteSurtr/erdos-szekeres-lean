#!/usr/bin/env python3
"""Export omission rows directly to OPB and check RoundingSat proof logs.

The input variables are holes: x(i+1) is true iff state i is omitted. No CNF
translation or floating-point rounding is used. A checked UNSAT proof concerns
this finite row system only; its geometric necessity is a separate obligation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from omission_row_probe import read_rows


def encode(n, rows, budget):
    if type(n) is not int or n < 1 or type(budget) is not int or not 0 <= budget <= n:
        raise ValueError("Invalid number of states or hole budget")
    # Reuse the input validator even when called directly, outside the CLI.
    read_rows({"states": [None] * n, "constraints": [
        {"support": support, "rhs": demand} for support, demand in rows]})
    lines = [f"* #variable= {n} #constraint= {len(rows) + 1} #equal= 0 intsize= {n.bit_length() + 1}"]
    for support, demand in rows:
        lines.append(" ".join(f"+1 x{i+1}" for i in support) + f" >= {demand} ;")
    lines.append(" ".join(f"-1 x{i+1}" for i in range(n)) + f" >= {-budget} ;")
    return "\n".join(lines) + "\n"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def execute(command, log, seconds):
    with log.open("w") as stream:
        try:
            return subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                  timeout=seconds).returncode
        except subprocess.TimeoutExpired:
            return None


def run(source, folder, budget, seconds, checker_seconds, solver, checker):
    if seconds < 1 or checker_seconds < 1:
        raise ValueError("Invalid time limit")
    source, solver, checker = (path.resolve() for path in (source, solver, checker))
    data = json.loads(source.read_text())
    n, rows = read_rows(data)
    if budget is None:
        budget = data["hole_budget"] + 1
    opb = encode(n, rows, budget)
    folder.mkdir(parents=True, exist_ok=False)
    folder = folder.resolve()
    instance, proof, log, check_log, report = (folder / name for name in
        ("instance.opb", "proof.pbp", "solver.log", "checker.log", "result.json"))
    instance.write_text(opb)
    command = [str(solver), str(instance), f"--time-limit={seconds}",
               f"--proof-log={proof}", "--print-sol=1"]
    record = {
        "scope": "Exact Boolean omission rows; geometric transfer is not certified here",
        "source": str(source), "source_sha256": sha256(source),
        "script_sha256": sha256(Path(__file__)), "states": n, "rows": len(rows),
        "hole_budget_tested": budget, "seconds_limit": seconds,
        "checker_seconds_limit": checker_seconds, "solver_command": command,
        "solver_sha256": sha256(solver), "checker_sha256": sha256(checker),
        "status": "running", "veripb_verified": False,
        "artifacts": {"instance": {"path": str(instance), "sha256": sha256(instance)}}}
    report.write_text(json.dumps(record, indent=2) + "\n")
    started = time.monotonic()
    code = execute(command, log, seconds + 30)
    output = log.read_text()
    verdicts = [line for line in output.splitlines() if line.startswith("s ")]
    record.update(solver_exit_code=code, seconds=time.monotonic() - started,
                  status="unsat" if code == 0 and verdicts == ["s UNSATISFIABLE"] else
                  "sat" if code == 0 and verdicts == ["s SATISFIABLE"] else "unknown")
    # Check SAT conclusions as well: VeriPB verifies the full assignment.
    if record["status"] in ("unsat", "sat") and proof.exists():
        check_command = [str(checker), str(instance), str(proof)]
        record["checker_command"] = check_command
        check_code = execute(check_command, check_log, checker_seconds)
        expected = "s VERIFIED " + ("UNSATISFIABLE" if record["status"] == "unsat" else "SATISFIABLE")
        record.update(checker_exit_code=check_code,
                      veripb_verified=check_code == 0 and expected in check_log.read_text().splitlines())
    for label, path in (("proof", proof), ("solver_log", log), ("checker_log", check_log)):
        if path.exists():
            record["artifacts"][label] = {"path": str(path), "sha256": sha256(path),
                                           "bytes": path.stat().st_size}
    report.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: record[key] for key in
        ("status", "veripb_verified", "states", "hole_budget_tested", "seconds")}), flush=True)
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--holes", type=int)
    parser.add_argument("--seconds", type=int, default=600)
    parser.add_argument("--checker-seconds", type=int, default=600)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output_dir, args.holes, args.seconds, args.checker_seconds,
        args.solver, args.checker)
