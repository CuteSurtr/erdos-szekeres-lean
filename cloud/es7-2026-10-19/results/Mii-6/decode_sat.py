#!/usr/bin/env python3
"""Decode a cadical model of m33k7int.sub.cnf into a 33-point signotope (.sig) and check
mirror consistency, the interior-axis condition and the signotope axioms (Python).
The no-convex-7-gon check is done by tools/trackB/brute_kgon (exhaustive over 7-subsets).

usage: decode_sat.py <model.txt> <out.sig>
"""
import itertools, sys, json
N = 33; m = N + 1; c = 17
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
val = {}
for l in open(sys.argv[1]).read().split():
    l = int(l)
    if l: val[abs(l)] = l > 0
X = {}
for (i, j, k), v in idx.items():
    w = idx[tuple(sorted((m - k, m - j, m - i)))]
    X[(i, j, k)] = val[min(v, w)]
mirror_bad = sum(X[t] != X[tuple(sorted((m - t[2], m - t[1], m - t[0])))] for t in X)
ax = [X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
interior = any(ax) and not all(ax)
sig_bad = 0
for q in itertools.combinations(range(1, N + 1), 4):
    seq = [X[t] for t in itertools.combinations(q, 3)]  # lex order of the 4 triples
    sig_bad += sum(seq[n] != seq[n + 1] for n in range(3)) > 1
with open(sys.argv[2], "w") as f:
    for t in sorted(X): f.write("%d %d %d %d\n" % (*t, 1 if X[t] else -1))
print(json.dumps({"mirror_violations": mirror_bad, "axis_interior": interior,
                  "X123": X[(1, 2, 3)], "signotope_axiom_violations": sig_bad}))
