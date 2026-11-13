#!/usr/bin/env python3
"""Check a point file (one "x y" integer pair per line) exactly: distinct points, central symmetry about the origin
(P = -P, origin not in P), no three collinear, and the largest subset in convex position (dynamic program of convex.py).
Also writes FILE.orient (orientation signs) for the independent brute force brute.c.
usage: verify.py POINTS.txt K   (exit 0 iff all checks pass and no K points are in convex position)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convex import collinear_triples, max_convex

path, k = sys.argv[1], int(sys.argv[2])
P = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
S = set(P)
res = {"points": len(P), "distinct": len(S) == len(P), "centrally_symmetric": all((-x, -y) in S for x, y in P),
       "origin_not_a_point": (0, 0) not in S}
res["collinear_triples"] = len(collinear_triples(P))
res["largest_convex_subset"] = max_convex(P)
print(res)
if len(P) <= 40:
    out = [str(len(P))]
    for a in P:
        for b in P:
            for c in P:
                v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]); out.append(str((v > 0) - (v < 0)))
    open(path + ".orient", "w").write(" ".join(out))
ok = res["distinct"] and res["centrally_symmetric"] and res["origin_not_a_point"] and res["collinear_triples"] == 0 \
     and res["largest_convex_subset"] < k
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
