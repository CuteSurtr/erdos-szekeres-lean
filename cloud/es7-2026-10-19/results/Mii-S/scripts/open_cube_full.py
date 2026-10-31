#!/usr/bin/env python3
"""Measurement only (no proofs): for K random C2 open cubes o, solve F & o & cube(c) for every
open hull case c to completion with one incremental PySAT CaDiCaL 1.9.5 instance per o
(F + o loaded once, the case cube as assumptions).  Reports per-o totals.
  open_cube_full.py CNF CASES_JSONL K SEED"""
import json, os, random, sys, time
from pysat.solvers import Solver
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hullsplit as H
cnf, cj, K, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
_, _, body = H.read_cnf(cnf); F = [list(map(int, l.split()[:-1])) for l in body]
cubes = [(c["case"], H.cube(tuple(c["U"]), tuple(c["L"]))) for c in map(json.loads, open(cj)) if c["status"] == "OPEN"]
opn = [list(map(int, l.split()[:-1])) for l in open(os.path.join(HERE, "../../H3/logs/open_cubes_ii_interior.txt"))]
for o in random.Random(seed).sample(opn, K):
    t0 = time.time(); s = Solver(name="cadical195", bootstrap_with=F)
    for l in o: s.add_clause([l])
    load = time.time() - t0; times = []; sat = []
    for nm, c in cubes:
        t = time.time(); r = s.solve(assumptions=c); times.append(time.time() - t)
        if r: sat.append(nm)
    s.delete()
    print(json.dumps({"open_cube": o, "load_s": round(load, 1), "total_s": round(sum(times), 1), "max_s": round(max(times), 1),
                      "over_1s": sum(t > 1 for t in times), "sat": sat}), flush=True)
