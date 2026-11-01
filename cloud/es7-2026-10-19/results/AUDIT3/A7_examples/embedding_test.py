#!/usr/bin/env python3
"""Informational: the Z[zeta5] files only define a planar set once an embedding zeta -> exp(2 pi i j/5) is fixed.
The README fixes j = 1.  j = 4 is the complex conjugate (a mirror image: same convexity).  j = 2, 3 are the Galois
conjugates (sqrt5 -> -sqrt5), a genuinely different planar set.  Re-run general position and the DP for each j."""
import os, sys
from functools import cmp_to_key
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7lib as L
R = os.environ.get("ES7_RESULTS", ".")

def emb(p, j):
    """the tuple of sum c_t zeta^(j t), re-expressed in the basis 1, zeta, zeta^2, zeta^3"""
    v = [0] * 5
    for t in range(4):
        v[(j * t) % 5] += p[t]
    return tuple(v[t] - v[4] for t in range(4))

for name, path, K in [("c5_30", R + "/SYMMAX/c5_30points.txt", 7), ("c5_31", R + "/SYMMAX/c5_31points.txt", 7),
                      ("k6_c5_16", R + "/SYMMAX/k6/c5_16points.txt", 6)]:
    pts0, _ = L.parse(path, "Z5")
    for j in (1, 2, 3, 4):
        pts = [emb(p, j) for p in pts0]
        n = len(pts)
        O = L.orient_table(pts, "Z5")
        col = sum(1 for a, b, c in combinations(range(n), 3) if O[a][b][c] == 0)
        cmpf = L.lex_key_cmp("Z5")
        order = sorted(range(n), key=cmp_to_key(lambda a, b: cmpf(pts[a], pts[b])))
        d, w = L.max_convex_dp(O, order) if col == 0 else (None, None)
        inv = set(L.MAPS["C5"](p) for p in pts) == set(pts)
        print("%-9s embedding zeta->exp(2pi i*%d/5): C5-invariant=%s collinear=%d max_convex=%s %s" % (
            name, j, inv, col, d, "(< K)" if d is not None and d < K else "(>= K: has a convex K-gon)"))
