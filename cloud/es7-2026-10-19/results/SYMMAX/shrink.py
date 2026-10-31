#!/usr/bin/env python3
"""Make the coordinates of a symmetric set small: scale the orbit representatives down and round, rebuild the orbits
exactly, and keep the result while the set stays distinct, in general position and K-gon-free (convex.py).
usage: shrink.py G POINTS.txt K OUT.txt"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convex import collinear_triples, max_convex
G, path, K, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
R = {"2": lambda p: (-p[0], -p[1]), "4": lambda p: (-p[1], p[0]), "3": lambda p: (-p[1], p[0] - p[1]),
     "6": lambda p: (p[0] - p[1], p[0]), "M": lambda p: (-p[0], p[1])}[G]
P = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
seen, reps, fixed = set(), [], []
for p in P:
    if p in seen: continue
    orb = [p]
    while R(orb[-1]) != p: orb.append(R(orb[-1]))
    seen.update(orb)
    (fixed if len(orb) == 1 else reps).append(p)
def build(reps, fixed):
    pts = list(fixed)
    for p in reps:
        q = p
        while True:
            pts.append(q); q = R(q)
            if q == p: break
    return pts
def good(pts):
    return len(set(pts)) == len(pts) and not collinear_triples(pts) and max_convex(pts) < K
assert good(build(reps, fixed))
cur = (reps, fixed)
scale = 1.0
while True:
    lo, hi, best = 0.0, 1.0, None
    for _ in range(14):                       # largest shrink factor that still works, by bisection
        f = (lo + hi) / 2
        nr = [(round(a * f), round(b * f)) for a, b in cur[0]]; nf = [(round(a * f), round(b * f)) for a, b in cur[1]]
        if good(build(nr, nf)): best, hi = (nr, nf), f
        else: lo = f
    if best is None or hi > 0.9: break        # stop once a pass shrinks by less than 10%
    cur = best
pts = build(*cur)
open(out, "w").write("\n".join(f"{a} {b}" for a, b in pts) + "\n")
print(path, "->", out, len(pts), "points, max |coord|", max(max(abs(a), abs(b)) for a, b in pts))
