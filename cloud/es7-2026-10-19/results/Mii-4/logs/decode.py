#!/usr/bin/env python3
"""Decode a SAT model of m33k7int.sub.cnf into a .sig file (i j k s) and check mirror identity,
interior axis point and X(1,2,3) unit.  usage: decode.py SAT_x.json out.sig"""
import sys, json, itertools
N = 33; m = N + 1
d = json.load(open(sys.argv[1])); val = {abs(l): l > 0 for l in d["model"] if l}
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
rep = {v: min(v, idx[tuple(sorted((m - k, m - j, m - i)))]) for (i, j, k), v in idx.items()}
X = {t: val[rep[v]] for t, v in idx.items()}
bad = sum(X[(i, j, k)] != X[tuple(sorted((m - k, m - j, m - i)))] for (i, j, k) in idx)
c = 17; cups = [X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
with open(sys.argv[2], "w") as f:
    for t in sorted(idx): f.write(f"{t[0]} {t[1]} {t[2]} {1 if X[t] else -1}\n")
print(json.dumps({"mirror_violations": bad, "axis_interior": any(cups) and not all(cups), "X123": X[(1, 2, 3)]}))
