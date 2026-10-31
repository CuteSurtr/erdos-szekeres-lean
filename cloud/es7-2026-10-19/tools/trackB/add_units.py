#!/usr/bin/env python3
"""Diversify models: append k random unit clauses on X(i,j,k) with 2<=i (triples not fixed by --hull).
Any model of the result is a model of the input. usage: add_units.py in.cnf out.cnf N k seed"""
import itertools, random, sys
inp, out, N, k, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
rng = random.Random(seed)
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
cands = [v for t, v in idx.items() if t[0] >= 2]
units = [v if rng.random() < 0.5 else -v for v in rng.sample(cands, k)]
lines = open(inp).read().split("\n")
with open(out, "w") as f:
    for l in lines:
        if l.startswith("p cnf"):
            _, _, nv, nc = l.split(); l = f"p cnf {nv} {int(nc) + k}"
        if l.strip():
            f.write(l + "\n")
    for u in units:
        f.write(f"{u} 0\n")
