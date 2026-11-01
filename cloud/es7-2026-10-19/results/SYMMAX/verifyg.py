#!/usr/bin/env python3
"""Exact check of a symmetric point set. G = 2, 4: ordinary integer coordinates, rotation by 180 / 90 degrees about 0;
G = 3, 6: Eisenstein coordinates, (a, b) = a + b*w with w = e^(2 pi i/3), i.e. the plane point (a - b/2, b*sqrt(3)/2) (a linear
invertible map, so collinearity and convex position are decided on the integer pairs), rotation by 120 / 60 degrees;
G = M: mirror (a, b) -> (-a, b) in ordinary coordinates. Checks: distinct, invariant, no three collinear, largest subset in
convex position (convex.py). Writes FILE.orient for brute.c.   usage: verifyg.py G POINTS.txt K"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convex import collinear_triples, max_convex
G, path, k = sys.argv[1], sys.argv[2], int(sys.argv[3])
R = {"2": lambda p: (-p[0], -p[1]), "4": lambda p: (-p[1], p[0]), "3": lambda p: (-p[1], p[0] - p[1]),
     "6": lambda p: (p[0] - p[1], p[0]), "M": lambda p: (-p[0], p[1])}[G]
P = [tuple(map(int, l.split())) for l in open(path) if l.strip() and not l.startswith(("FOUND", "#"))]
S = set(P)
res = {"group": G, "points": len(P), "distinct": len(S) == len(P), "invariant": all(R(p) in S for p in P),
       "fixed_points": sum(1 for p in P if R(p) == p), "collinear_triples": len(collinear_triples(P)),
       "largest_convex_subset": max_convex(P)}
print(res)
out = [str(len(P))]
for a in P:
    for b in P:
        for c in P:
            v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]); out.append(str((v > 0) - (v < 0)))
open(path + ".orient", "w").write(" ".join(out))
ok = res["distinct"] and res["invariant"] and res["collinear_triples"] == 0 and res["largest_convex_subset"] < k
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
