#!/usr/bin/env python3
"""Exact test of the normal-form map of Lemma 0 (finite z): phi(p) = (-u.(p-z)/w(p), -1/w(p)),
w(p) = n.(p-z), u = (-n_y, n_x).  Checks (b) orientation signs, (c) z-order <-> x-order,
(d) q on z's side of line pr <-> phi(q) below line phi(p)phi(r)."""
import random, sys
from fractions import Fraction as F
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from geom import orient, sgn, general_position
def phi(p, z, n):
    u = (-n[1], n[0]); d = (p[0]-z[0], p[1]-z[1]); w = n[0]*d[0] + n[1]*d[1]
    assert w > 0
    return (F(-(u[0]*d[0] + u[1]*d[1]), w), F(-1, w))
rng = random.Random(7); bad = dict(orient=0, order=0, side=0); trials = 0
for t in range(300):
    P = [(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(7)]
    if not general_position(P): continue
    th = rng.random() * 6.283; R = rng.randint(200, 5000)
    import math
    z = (int(R*math.cos(th)), int(R*math.sin(th)))
    if any(orient(a, b, z) == 0 for a, b in combinations(P, 2)): continue
    mx = sum(p[0] for p in P) / len(P); my = sum(p[1] for p in P) / len(P)
    n = (round(mx - z[0]), round(my - z[1]))
    if any(n[0]*(p[0]-z[0]) + n[1]*(p[1]-z[1]) <= 0 for p in P): continue
    trials += 1
    Q = {p: phi(p, z, n) for p in P}
    for a, b, c in combinations(P, 3):
        if sgn(orient(a, b, c)) != sgn(orient(Q[a], Q[b], Q[c])): bad['orient'] += 1
    for a, b in combinations(P, 2):
        if (orient(z, a, b) < 0) != (Q[a][0] < Q[b][0]): bad['order'] += 1
    for p, r in combinations(P, 2):
        for q in P:
            if q in (p, r): continue
            zside = sgn(orient(p, r, q)) == sgn(orient(p, r, z))
            # below the line phi(p)phi(r): compare y at x(phi q)
            (x1, y1), (x2, y2), (xq, yq) = Q[p], Q[r], Q[q]
            yline = y1 + (y2 - y1) * (xq - x1) / (x2 - x1)
            if zside != (yq < yline): bad['side'] += 1
print("trials", trials, "violations", bad)
