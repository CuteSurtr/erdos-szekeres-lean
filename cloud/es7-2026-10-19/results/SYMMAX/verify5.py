#!/usr/bin/env python3
"""Exact check of a 5-fold symmetric point set. A line "c0 c1 c2 c3" is the point c0 + c1 z + c2 z^2 + c3 z^3, z = e^(2 pi i/5).
Orientation: cross(u, v) = Im(conj(u) v); for w = sum w_j z^j, Im(w)/sin(72°) = ((2(w1-w4) - (w2-w3)) + (w2-w3) sqrt5)/2,
whose sign is decided with integers. The rotation by 72° is multiplication by z. Checks: distinct, invariant, no three
collinear, largest subset in convex position (the dynamic program of convex.py with exact comparisons); writes FILE.orient.
usage: verify5.py POINTS.txt K"""
import sys
from functools import cmp_to_key
from itertools import combinations

def sgn(A, B):                      # sign of A + B sqrt5
    if A >= 0 and B >= 0: return int(A > 0 or B > 0)
    if A <= 0 and B <= 0: return -int(A < 0 or B < 0)
    a2, b2 = A * A, 5 * B * B
    return (1 if a2 > b2 else -1 if a2 < b2 else 0) * (1 if A > 0 else -1)
def norm(c):
    c = list(c) + [0] * (5 - len(c)); return tuple(x - c[4] for x in c[:4]) + (0,)
def mul(u, v):
    w = [0] * 5
    for a in range(5):
        for b in range(5): w[(a + b) % 5] += u[a] * v[b]
    return w
def conj(u): return [u[(-j) % 5] for j in range(5)]
def orient(p, q, r):
    u = [q[t] - p[t] for t in range(5)]; v = [r[t] - p[t] for t in range(5)]
    w = mul(conj(u), v)
    return sgn(2 * (w[1] - w[4]) - (w[2] - w[3]), w[2] - w[3])
def rot(p): return norm([p[4]] + list(p[:4]))
def key_cmp(p, q):                  # exact (Im, Re) order
    d = [p[t] - q[t] for t in range(5)]
    s = sgn(2 * (d[1] - d[4]) - (d[2] - d[3]), d[2] - d[3])
    if s: return s
    return sgn(4 * d[0] - (d[1] + d[4]) - (d[2] + d[3]), (d[1] + d[4]) - (d[2] + d[3]))
def max_convex(P):
    best = 2
    for a in P:
        up = [p for p in P if key_cmp(p, a) > 0]
        up.sort(key=cmp_to_key(lambda p, q: -1 if orient(a, p, q) > 0 else 1))
        m = len(up); D = [[0] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                v = 3 if orient(a, up[i], up[j]) > 0 else 0
                if v:
                    for h in range(i):
                        if D[h][i] and orient(up[h], up[i], up[j]) > 0 and D[h][i] + 1 > v: v = D[h][i] + 1
                D[i][j] = v
                if v and orient(up[i], up[j], a) > 0 and v > best: best = v
    return best
path, k = sys.argv[1], int(sys.argv[2])
P = [norm(list(map(int, l.split()))) for l in open(path) if l.strip() and not l.startswith(("FOUND", "#"))]
S = set(P)
res = {"group": 5, "points": len(P), "distinct": len(S) == len(P), "invariant": all(rot(p) in S for p in P),
       "fixed_points": sum(1 for p in P if rot(p) == p),
       "collinear_triples": sum(1 for a, b, c in combinations(P, 3) if orient(a, b, c) == 0),
       "largest_convex_subset": max_convex(P)}
print(res)
out = [str(len(P))] + [str(orient(a, b, c)) for a in P for b in P for c in P]
open(path + ".orient", "w").write(" ".join(out))
ok = res["distinct"] and res["invariant"] and res["collinear_triples"] == 0 and res["largest_convex_subset"] < k
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
