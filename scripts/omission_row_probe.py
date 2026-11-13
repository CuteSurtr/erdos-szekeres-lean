#!/usr/bin/env python3
"""Probe a finite omission-row relaxation; this does not prove a planar bound.

Supports the balanced/residual JSON formats in Schroeder's September 2026
archive, DOI 10.5281/zenodo.22842891. A SAT model is checked with exact integer
counts but need not correspond to points. UNSAT still needs a checked certificate
and a geometric necessity proof. The default tests one step beyond the archive's
certified hole budget. Requires the optional z3-solver package.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time


def read_rows(data):
    n = len(data["states"])
    if "cuts" in data and "constraints" not in data:
        k = data["polygon"]
        if type(k) is not int or k < 3:
            raise ValueError("Invalid polygon size")
        rows = [(row, len(row) - (k - 1)) for row in data["cuts"]]
    elif "constraints" in data and "cuts" not in data:
        rows = [(row["support"], row["rhs"]) for row in data["constraints"]]
    else:
        raise ValueError("Expected exactly one row format")
    for support, demand in rows:
        if (len(set(support)) != len(support) or
                not all(type(i) is int and 0 <= i < n for i in support) or
                type(demand) is not int or not 0 <= demand <= len(support)):
            raise ValueError("Invalid omission row")
    return n, rows


def valid_holes(n, rows, budget, holes):
    return (len(holes) == len(set(holes)) and len(holes) <= budget and
            all(type(i) is int and 0 <= i < n for i in holes) and
            all(len(set(support) & set(holes)) >= demand for support, demand in rows))


def run(source, output, budget=None, seconds=180, seed=0):
    import z3
    if output.exists():
        raise FileExistsError(output)
    data = json.loads(source.read_text())
    n, rows = read_rows(data)
    if budget is None:
        budget = data["hole_budget"] + 1
    if type(budget) is not int or not 0 <= budget <= n or seconds <= 0:
        raise ValueError("Invalid budget or time limit")
    holes = [z3.Bool(f"h_{i}") for i in range(n)]
    solver = z3.Solver()
    solver.set(timeout=int(seconds * 1000), random_seed=seed)
    for support, demand in rows:
        solver.add(z3.PbGe([(holes[i], 1) for i in support], demand) if support
                   else z3.BoolVal(demand == 0))
    solver.add(z3.PbLe([(h, 1) for h in holes], budget) if holes else z3.BoolVal(True))
    started = time.monotonic()
    verdict = solver.check()
    result = {
        "source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Boolean omission-row relaxation only; not a planar realization or theorem",
        "states": n, "rows": len(rows), "hole_budget_tested": budget,
        "status": str(verdict), "solver": "Z3 " + z3.get_version_string(),
        "seconds_limit": seconds, "seed": seed, "seconds": time.monotonic() - started,
    }
    if verdict == z3.sat:
        model = solver.model()
        missing = [i for i, h in enumerate(holes)
                   if z3.is_true(model.eval(h, model_completion=True))]
        if not valid_holes(n, rows, budget, missing):
            raise AssertionError("Model failed independent integer row verification")
        result.update(holes=missing, occupied=n-len(missing), all_rows_exactly_checked=True)
    elif verdict == z3.unknown:
        result["reason"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--holes", type=int)
    parser.add_argument("--seconds", type=float, default=180)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    run(args.source, args.output, args.holes, args.seconds, args.seed)
