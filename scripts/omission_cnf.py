#!/usr/bin/env python3
"""Search omission rows with CaDiCaL after a Z3 cardinality-to-CNF translation.

SAT assignments are checked against both the CNF and the original integer rows.
UNSAT certificates are independently checked by drat-trim. Neither Z3's CNF
translation nor the geometric meaning of the rows is certified in this script.
Thus an UNSAT result is not an end-to-end Lean or planar theorem.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from omission_row_probe import read_rows, valid_holes
from realize_model import check_cnf, read_model


def encode(n, rows, budget, prefix_sets=None):
    import z3
    if type(budget) is not int or not 0 <= budget <= n:
        raise ValueError("Invalid hole budget")
    holes = [z3.Bool(f"h_{i}") for i in range(n)]
    goal = z3.Goal()
    for support, demand in rows:
        goal.add(z3.PbGe([(holes[i], 1) for i in support], demand) if support
                 else z3.BoolVal(demand == 0))
    goal.add(z3.PbLe([(h, 1) for h in holes], budget) if holes else z3.BoolVal(True))
    if prefix_sets is not None:
        if not prefix_sets or any(len(set(s)) != len(s) or
                                  not all(type(i) is int and 0 <= i < n for i in s)
                                  for s in prefix_sets):
            raise ValueError("Invalid prefix alternatives")
        goal.add(z3.Or([z3.And([z3.Not(holes[i]) for i in s]) for s in prefix_sets]))
    tactic = z3.Then("simplify", z3.With("card2bv", **{
        "pb.solver": "sorting", "keep_cardinality_constraints": False}), "tseitin-cnf")
    result = tactic(goal)
    if len(result) != 1:
        raise ValueError("Expected one CNF goal")
    for clause in result[0]:
        literals = clause.children() if z3.is_or(clause) else [clause]
        for literal in literals:
            atom = literal.arg(0) if z3.is_not(literal) else literal
            if not z3.is_const(atom) or not z3.is_bool(atom):
                raise ValueError("Nonpropositional expression survived CNF conversion")
    return result[0].dimacs() + "\n"


def hole_variables(dimacs):
    mapping = {}
    for line in dimacs.splitlines():
        fields = line.split()
        if len(fields) == 3 and fields[0] == "c" and fields[2].startswith("h_"):
            label = int(fields[2][2:])
            if label in mapping:
                raise ValueError("Repeated original variable mapping")
            mapping[label] = int(fields[1])
    return mapping


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(source, folder, budget, seconds, seed, solver, checker, prefix=None):
    import z3
    if seconds < 1 or seed < 0:
        raise ValueError("Invalid time limit or seed")
    data = json.loads(source.read_text())
    n, rows = read_rows(data)
    if budget is None:
        budget = data["hole_budget"] + 1
    prefix_data = json.loads(prefix.read_text()) if prefix is not None else None
    if prefix_data is not None and prefix_data.get("catalog_sha256") != sha256(source):
        raise ValueError("Prefix and row catalogue hashes differ")
    alternatives = prefix_data["state_sets"] if prefix_data is not None else None
    dimacs = encode(n, rows, budget, alternatives)
    mapping = hole_variables(dimacs)
    if not set(mapping) <= set(range(n)):
        raise ValueError("Unexpected original variable mapping")
    folder.mkdir(parents=True, exist_ok=False)
    cnf, proof, log = (folder / name for name in ("instance.cnf", "proof.drat", "solver.log"))
    cnf.write_text(dimacs)
    header = next(line for line in dimacs.splitlines() if line.startswith("p cnf ")).split()
    command = [str(solver), "--no-colors", "--sat", f"--seed={seed}",
               "-t", str(seconds), str(cnf), str(proof)]
    record = {
        "source": str(source), "source_sha256": sha256(source),
        "script_sha256": sha256(Path(__file__)), "states": n, "rows": len(rows),
        "hole_budget_tested": budget, "seconds_limit": seconds, "seed": seed,
        "encoder": "Z3 " + z3.get_version_string() + ": simplify, card2bv sorting, tseitin-cnf",
        "solver_version": subprocess.check_output([str(solver), "--version"], text=True).strip(),
        "solver_sha256": sha256(solver), "solver_command": command,
        "variables": int(header[2]), "clauses": int(header[3]),
        "scope": "Omission-row relaxation; CNF translation and geometric transfer are not Lean-certified",
        "status": "running", "artifacts": {"cnf": {"path": str(cnf), "sha256": sha256(cnf)}},
    }
    report = folder / "result.json"
    if prefix is not None:
        record["prefix"] = {"path": str(prefix), "sha256": sha256(prefix),
                            "alternatives": len(alternatives),
                            "scope": "Experimental actual-rank prefix restriction; its enumeration and geometric transfer are not certified"}
    report.write_text(json.dumps(record, indent=2) + "\n")
    print(f"{folder.name}: {record['variables']} variables, {record['clauses']} clauses", flush=True)
    started = time.monotonic()
    with log.open("w") as stream:
        try:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                    timeout=seconds + 30)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = None
    text = log.read_text()
    record.update(seconds=time.monotonic() - started, solver_exit_code=code,
                  status="sat" if code == 10 and "s SATISFIABLE" in text else
                  "unsat" if code == 20 and "s UNSATISFIABLE" in text else "unknown")
    if record["status"] == "sat":
        model = read_model(log) if record["variables"] else {}
        record["cnf_clauses_checked"] = check_cnf(cnf, model)
        missing = [i for i in range(n) if i in mapping and model[mapping[i]]]
        if not valid_holes(n, rows, budget, missing):
            raise AssertionError("SAT model fails the original omission rows")
        if alternatives is not None and not any(set(s).isdisjoint(missing) for s in alternatives):
            raise AssertionError("SAT model fails the prefix restriction")
        record.update(holes=missing, occupied=n-len(missing), all_rows_exactly_checked=True)
    if record["status"] == "unsat":
        checker_log = folder / "checker.log"
        with checker_log.open("w") as stream:
            checked = subprocess.run([str(checker), str(cnf), str(proof), "-t", str(seconds)],
                                     stdout=stream, stderr=subprocess.STDOUT, timeout=seconds+30)
        record["drat_verified"] = checked.returncode == 0 and "s VERIFIED" in checker_log.read_text()
        record["checker_sha256"] = sha256(checker)
        record["artifacts"]["checker_log"] = {"path": str(checker_log), "sha256": sha256(checker_log)}
    for name, path in (("proof", proof), ("solver_log", log)):
        if path.exists():
            record["artifacts"][name] = {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}
    report.write_text(json.dumps(record, indent=2) + "\n")
    print(f"{folder.name}: {record['status']}", flush=True)
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--holes", type=int)
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--prefix", type=Path, help="Experimental finite prefix alternatives from prefix_states.py")
    parser.add_argument("--solver", type=Path, default=Path(".cache/cadical/build/cadical"))
    parser.add_argument("--checker", type=Path, default=Path(".cache/drat-trim/drat-trim"))
    args = parser.parse_args()
    run(args.source, args.output_dir, args.holes, args.seconds, args.seed, args.solver, args.checker, args.prefix)
