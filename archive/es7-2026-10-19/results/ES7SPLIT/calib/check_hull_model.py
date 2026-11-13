#!/usr/bin/env python3
"""Independent check of a gen_hull.py model: decode X(i,j,k) (lexicographic, 1..C(N,3)), check signotope
axioms, count extreme points (p is extreme iff it lies in no triangle of three other points, decided from
the orientations alone), and compute the largest convex subset by the cap/cup DP on the x-order
(valid for signotopes)."""
import itertools, json, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from check_model import read_model, analyse
N = int(sys.argv[1])
sat, vals = read_model(sys.argv[2])
sig = {}
v = 0
for t in itertools.combinations(range(1, N + 1), 3):
    v += 1
    sig[t] = 1 if vals.get(v, False) else -1
def chi(a, b, c):
    t = (a, b, c); s = tuple(sorted(t))
    inv = (a > b) + (a > c) + (b > c)
    return sig[s] * (-1 if inv % 2 else 1)
ext = 0
for p in range(1, N + 1):
    inside = False
    for a, b, c in itertools.combinations([q for q in range(1, N + 1) if q != p], 3):
        o = chi(a, b, c)
        if chi(a, b, p) == o and chi(b, c, p) == o and chi(c, a, p) == o:
            inside = True; break
    ext += not inside
res = analyse(N, sig)
res.update(status=sat, extreme_points=ext)
print(json.dumps(res))
