#!/usr/bin/env python3
"""Try fixed-abscissa linear realization of an upstream SAT model.

Inspired by arXiv:2604.20120, section 5.2. UNSAT here concerns the chosen
abscissae only. Successful coordinates are independently checked with integers.
Requires optional z3-solver; all geometric verification uses the standard library.
"""
import argparse
from fractions import Fraction
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import time

from search import convex_subset, general_position, orient


def read_model(path):
    values = {}
    for line in path.read_text().splitlines():
        if line.startswith("v "):
            for literal in map(int, line.split()[1:]):
                if literal:
                    values[abs(literal)] = literal > 0
    if not values:
        raise ValueError("No SAT assignment found")
    return values


def check_cnf(path, model):
    count = expected = None
    clause = []
    with path.open() as stream:
        for line in stream:
            if line.startswith("c") or not line.strip():
                continue
            if line.startswith("p cnf "):
                _, _, variables, expected = line.split()
                expected, count = int(expected), 0
                if set(model) != set(range(1, int(variables) + 1)):
                    raise ValueError("Incomplete or extra model variables")
                continue
            for literal in map(int, line.split()):
                if literal:
                    clause.append(literal)
                else:
                    if not any(model[abs(x)] == (x > 0) for x in clause):
                        raise ValueError(f"Unsatisfied clause {count}")
                    count += 1
                    clause.clear()
    if clause or count != expected or expected is None:
        raise ValueError("Malformed DIMACS clause count")
    return count


def realize(manifest, seconds, base):
    import z3
    root = Path(__file__).resolve().parents[1]
    info = json.loads(manifest.read_text())
    if info["status"] != "sat":
        raise ValueError("A SAT result is required")
    out = root / info["artifacts"]["cnf"]["path"]
    folder = out.parent
    model = read_model(folder / "solver.log")
    clause_count = check_cnf(out, model)
    n = info["points"]
    signs = {(0, b, c): True for b, c in combinations(range(1, n), 2)}
    for variable, line in enumerate((folder / "variables.txt").read_text().splitlines(), 1):
        fields = list(map(int, line.split()))
        if fields[:2] == [0, 0]:
            a, b, c = fields[2:]
            signs[a+1, b+1, c+1] = model[variable]
    if set(signs) != set(combinations(range(n), 3)):
        raise ValueError("Unexpected orientation variable map")
    if base < 1:
        raise ValueError("Require base >= 1")
    xs = list(range(n)) if base == 1 else [base**i for i in range(n)]
    ys = [z3.Real(f"y{i}") for i in range(n)]
    solver = z3.Solver()
    solver.set(timeout=seconds * 1000)
    solver.add(ys[0] == 0, ys[1] == 0)
    for (a, b, c), positive in signs.items():
        area = (xs[b]-xs[a])*(ys[c]-ys[a]) - (ys[b]-ys[a])*(xs[c]-xs[a])
        solver.add(area >= 1 if positive else area <= -1)
    started = time.monotonic()
    status = solver.check()
    result = {"scope": "one abstract model and one fixed x-grid",
              "source_manifest": str(manifest.relative_to(root)), "points": n,
              "gon": info["gon"], "x_grid_base": base,
              "cnf_clauses_independently_checked": clause_count,
              "z3_version": z3.get_version_string(), "status": str(status),
              "seconds": time.monotonic() - started}
    if status == z3.sat:
        solution = solver.model()
        rational = [Fraction(str(solution.eval(y))) for y in ys]
        denominator = lcm(*(y.denominator for y in rational))
        points = [(x, int(y*denominator)) for x, y in zip(xs, rational)]
        sign_check = all((orient(*(points[i] for i in triple)) > 0) == sign
                         for triple, sign in signs.items())
        gp = general_position(points)
        polygon = convex_subset(points, info["gon"])
        result.update(coordinates=points, general_position=gp,
                      all_orientation_signs_match=sign_check, forbidden_polygon=polygon,
                      exact_witness_verified=gp and sign_check and polygon is None,
                      verification="independent exact Python integers; not yet Lean-certified")
        if not result["exact_witness_verified"]:
            raise RuntimeError("Realization failed independent geometric verification")
    elif status == z3.unknown:
        result["reason"] = solver.reason_unknown()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--base", type=int, default=1)
    args = parser.parse_args()
    print(json.dumps(realize(args.manifest.resolve(), args.seconds, args.base), indent=2))
