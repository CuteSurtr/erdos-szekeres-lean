#!/usr/bin/env python3
"""Measurement only (no proofs): for sampled C2 open cubes o, how many of the open hull cases
c give a quickly refuted F & o & cube(c)?  Uses PySAT CaDiCaL 1.9.5 incrementally: F + o is
loaded once, each case cube is passed as assumptions with a conflict budget.
  hybrid_grid.py CNF CASES_JSONL NOPEN SEED BUDGET
Prints one JSON line per open cube: counts of UNSAT within budget / unknown / SAT, and time."""
import json, os, random, sys, time
from pysat.solvers import Solver
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hullsplit as H
cnf, cj, K, seed, B = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
_, _, body = H.read_cnf(cnf); F = [list(map(int, l.split()[:-1])) for l in body]
openc = [json.loads(l) for l in open(cj) if json.loads(l)["status"] == "OPEN"]
cubes = [(c["case"], H.cube(tuple(c["U"]), tuple(c["L"]))) for c in openc]
opn = [list(map(int, l.split()[:-1])) for l in open(os.path.join(HERE, "../../H3/logs/open_cubes_ii_interior.txt"))]
rng = random.Random(seed)
for o in rng.sample(opn, K):
    s = Solver(name="cadical195", bootstrap_with=F)
    for l in o: s.add_clause([l])
    t0 = time.time(); res = {"unsat": 0, "unknown": [], "sat": []}
    for nm, c in cubes:
        s.conf_budget(B); r = s.solve_limited(assumptions=c)
        if r is False: res["unsat"] += 1
        elif r is None: res["unknown"].append(nm)
        else: res["sat"].append(nm)
    s.delete()
    print(json.dumps({"open_cube": o, "cases": len(cubes), "unsat": res["unsat"], "unknown": res["unknown"],
                      "sat": res["sat"], "budget": B, "s": round(time.time() - t0, 1)}), flush=True)
