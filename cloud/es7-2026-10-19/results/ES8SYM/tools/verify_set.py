#!/usr/bin/env python3
"""Exact check of an integer point file ("x y" per line):
distinct points, symmetry (C2: P = -P and origin not in P; M: mirror (x,y)->(-x,y); C3: Eisenstein coordinates,
rotation (a,b)->(-b,a-b)), no three collinear, largest subset in convex position (DP of geom.py).
Writes FILE.orient (n, then n^3 signs) for the independent C checker enum_convex.c.
usage: verify_set.py FILE K [C2|M|C3|none]
For C3 files a line "a b" means a + b*w, w = exp(2 pi i/3); the linear map (a,b) -> (a - b/2, b*sqrt3/2) has positive
determinant, so orientations are those of the integer pairs (a,b) themselves."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import orient_table, max_convex_dp, collinear_triples

path, k = sys.argv[1], int(sys.argv[2])
sym = sys.argv[3] if len(sys.argv) > 3 else "C2"
P = [tuple(map(int, l.split())) for l in open(path) if l.strip() and not l.startswith("#")]
S = set(P)
res = {"points": len(P), "distinct": len(S) == len(P), "max_abs_coord": max(max(abs(x), abs(y)) for x, y in P)}
if sym == "C2":
    res["symmetric"] = all((-x, -y) in S for x, y in P) and (0, 0) not in S
elif sym == "M":
    res["symmetric"] = all((-x, y) in S for x, y in P)
elif sym == "C3":
    res["symmetric"] = all((-b, a - b) in S for a, b in P)
else:
    res["symmetric"] = None
res["collinear_triples"] = len(collinear_triples(P))
T = orient_table(P)
res["largest_convex_subset"] = max_convex_dp(P, T)
print(res)
n = len(P)
with open(path + ".orient", "w") as f:
    f.write(str(n) + "\n")
    for a in range(n):
        f.write(" ".join(str(T[a][b][c]) for b in range(n) for c in range(n)) + "\n")
ok = res["distinct"] and res["symmetric"] is not False and res["collinear_triples"] == 0 \
    and res["largest_convex_subset"] < k
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
