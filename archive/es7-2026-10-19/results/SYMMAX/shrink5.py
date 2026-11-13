#!/usr/bin/env python3
"""shrink.py for 5-fold sets in Z[z] coordinates (see verify5.py): scale the orbit representatives down and round while
the set stays distinct, in general position and K-gon-free.  usage: shrink5.py POINTS.txt K OUT.txt"""
import sys, types
from itertools import combinations
src = open(__file__.replace("shrink5.py", "verify5.py")).read().split("path, k = sys.argv[1]")[0]
V = types.ModuleType("v5"); exec(src, V.__dict__)
path, K, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
P = [V.norm(list(map(int, l.split()))) for l in open(path) if l.strip()]
seen, reps, fixed = set(), [], []
for p in P:
    if p in seen: continue
    orb = [p]
    while V.rot(orb[-1]) != p: orb.append(V.rot(orb[-1]))
    seen.update(orb); (fixed if len(orb) == 1 else reps).append(p)
def build(reps):
    pts = list(fixed)
    for p in reps:
        q = p
        for _ in range(5): pts.append(q); q = V.rot(q)
    return pts
def good(pts):
    if len(set(pts)) != len(pts): return False
    if any(V.orient(a, b, c) == 0 for a, b, c in combinations(pts, 3)): return False
    return V.max_convex(pts) < K
cur = reps
while True:
    lo, hi, best = 0.0, 1.0, None
    for _ in range(14):
        f = (lo + hi) / 2
        nr = [V.norm([round(x * f) for x in p]) for p in cur]
        if good(build(nr)): best, hi = nr, f
        else: lo = f
    if best is None or hi > 0.9: break
    cur = best
pts = build(cur)
open(out, "w").write("\n".join(" ".join(map(str, p[:4])) for p in pts) + "\n")
print(out, len(pts), "points, max |coef|", max(max(abs(x) for x in p) for p in pts))
