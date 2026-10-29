#!/usr/bin/env python3
"""Test of the mirror reduction for sgn.py --par --rs. For random real centrally symmetric sets S with a parallelogram
hull, label S and its mirror image R(S) in the normal form (edge pair chosen by --rs, edge V1 -> V2 counter-clockwise,
direction tilted towards V2). Claim: the orientation vectors satisfy o_R(i,j,k) = -chi_S(t(i),t(j),t(k)) with t swapping
labels 1<->2 and n-1<->n; in particular o_R = -o_S on every triple of inner points (labels 3..n-2), so exactly one of
S, R(S) has o(3,4,5) false.  usage: mirrortest.py TRIALS SEED"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sgnval import det, general
def hull(Q):
    def chain(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and det(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    Q = sorted(Q); lo, up = chain(Q), chain(Q[::-1]); return lo[:-1] + up[:-1]
def label(P):
    H = hull(P); assert len(H) == 4
    inner = [p for p in P if p not in H]; reps = [q for q in inner if q < (-q[0], -q[1])]; m = len(reps)
    O = (0, 0)
    def cls(e0, e1): return sum(1 for q in reps if (det(O, e0, q) > 0) == (det(O, q, e1) > 0))
    c0, c1 = H[0], H[1]
    if cls(c0, c1) < (m + 1) // 2: c0, c1 = c1, H[2]
    nv = (c1[1] - c0[1], -(c1[0] - c0[0])); t = (c1[0] - c0[0], c1[1] - c0[1])
    key = lambda p: (nv[0] * p[0] + nv[1] * p[1], t[0] * p[0] + t[1] * p[1])
    S = sorted(P, key=key)
    keys = [key(p)[0] for p in S[2:-2]]; generic = len(set(keys)) == len(keys)
    return S, generic
rng = random.Random(int(sys.argv[2])); T = int(sys.argv[1]); ok = gen = 0; bad = 0
while ok < T:
    while True:
        A = (rng.randint(-9, 9), rng.randint(-9, 9)); B = (rng.randint(-9, 9), rng.randint(-9, 9))
        if A[0] * B[1] - A[1] * B[0] > 0: break
    D = 1000; c0 = (D * (A[0] + B[0]), D * (A[1] + B[1])); c1 = (D * (B[0] - A[0]), D * (B[1] - A[1]))
    P = [c0, c1, (-c0[0], -c0[1]), (-c1[0], -c1[1])]
    for _ in range(rng.choice([3, 5, 7])):
        u, v = rng.randint(-D + 1, D - 1), rng.randint(-D + 1, D - 1)
        p = (u * A[0] + v * B[0], u * A[1] + v * B[1]); P += [p, (-p[0], -p[1])]
    if len(set(P)) != len(P) or not general(P): continue
    S, g1 = label(P); RS, g2 = label([(-x, y) for x, y in P])
    if not (g1 and g2): continue
    n = len(S); tmap = {1: 2, 2: 1, n - 1: n, n: n - 1}; tt = lambda i: tmap.get(i, i)
    o = lambda L, i, j, k: det(L[i - 1], L[j - 1], L[k - 1]) > 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            for k in range(j + 1, n + 1):
                if o(RS, i, j, k) != (not o(S, tt(i), tt(j), tt(k))): bad += 1
    if o(S, 3, 4, 5) == o(RS, 3, 4, 5): bad += 1
    ok += 1
print({"trials": T, "inner_pairs": "odd (3, 5, 7)", "violations": bad})
