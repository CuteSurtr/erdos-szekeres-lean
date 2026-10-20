#!/usr/bin/env python3
"""Decode and brute-force check a SAT leaf of hm33k7.sub.cnf (sub-case (i), hull frame).

usage: check_sat.py <SAT_model.json> <out.sig>

The model assigns the orbit representatives; every X(i,j,k) (lex index, 1<=i<j<k<=33) is read
through its mirror orbit {X(i,j,k), X(35-k,35-j,35-i)} (i >= 2).  Checks, independently of the CNF:
signotope axioms on all quadruples, mirror consistency, X(1,i,j) true (point 1 = axis point at
vertical infinity), and the largest convex subset (4-point test, exact DFS) is < 7.
Writes the 33-point chirotope as .sig lines "a b c s" (0-based) for tools/realizer.
"""
import sys, os, json, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../tools/trackB"))
from sigcheck import is_signotope, max_convex_4pt
N = 33
d = json.load(open(sys.argv[1]))
val = {abs(l): l > 0 for l in d["model"]}
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
def rep(t):
    i, j, k = t
    if i < 2: return idx[t]
    return min(idx[t], idx[tuple(sorted((N + 2 - k, N + 2 - j, N + 2 - i)))])
sig = {t: (1 if val[rep(t)] else -1) for t in idx}
res = {"model_file": sys.argv[1], "cube": d["cube"]}
res["signotope"] = is_signotope(sig, N)
res["mirror_violations"] = sum(sig[(i, j, k)] != sig[tuple(sorted((N + 2 - k, N + 2 - j, N + 2 - i)))]
                               for (i, j, k) in idx if i >= 2)
res["axis_point_at_vertical_infinity"] = all(sig[(1, j, k)] == 1 for j, k in itertools.combinations(range(2, N + 1), 2))
mc = max_convex_4pt(sig, N)
res["max_convex"] = mc if isinstance(mc, int) else (len(mc) if hasattr(mc, "__len__") else str(mc))
with open(sys.argv[2], "w") as f:
    for (i, j, k), s in sig.items(): f.write(f"{i-1} {j-1} {k-1} {s}\n")
print(json.dumps(res))
