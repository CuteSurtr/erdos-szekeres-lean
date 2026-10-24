#!/usr/bin/env python3
"""Hybrid case CNF: F + cube(case) units + {-k : k a closed C2 cube} (C2's 749 closed cubes of
results/C2/logs/cnc_ii_interior/closed.txt, all cake_lpr-verified by H3 against F).
UNSAT of this CNF plus UNSAT of each F + k gives UNSAT of F + cube(case) (the blocked-cover
lemma of shard_plan.md, with P = cube(case) and the cubes k).
  hybrid_case.py CNF SPEC OUT.cnf"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hullsplit as H
cnf, sp, out = sys.argv[1:4]
U, L = sp.split("/"); U = tuple(int(x) for x in U.split(",") if x); L = tuple(int(x) for x in L.split(",") if x)
cube = H.cube(U, L)
closed = []
for line in open(os.path.join(HERE, "../../C2/logs/cnc_ii_interior/closed.txt")):
    k = tuple(int(x) for x in line.split()[1:-1])
    if k not in closed: closed.append(k)
nv, nc, body = H.read_cnf(cnf)
cl = [f"{l} 0\n" for l in cube] + [" ".join(str(-l) for l in k) + " 0\n" for k in closed]
with open(out, "w") as f:
    f.write(f"p cnf {nv} {nc + len(cl)}\n"); f.writelines(body); f.writelines(cl)
print(len(cube), len(closed))
