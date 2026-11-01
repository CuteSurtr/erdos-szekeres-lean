#!/usr/bin/env python3
"""Independent exact verification of the 27-point witness of Proposition 8(b).

Written from scratch (does not import tools/geom.py).  All geometry uses Python integers.

Checks:
  (1) 27 distinct points, general position (every triple has nonzero orientation).
  (2) Convex hull by gift wrapping (Jarvis march); b = last point is a hull vertex.
  (3) Convex layers by repeated gift wrapping -> layer profile.
  (4) Method B: for k = 5, 6, 7 count k-subsets in convex position with the hull-edge criterion
      (in general position, #hull vertices of Q = #ordered pairs (i, j) of Q with every other point of Q
      strictly left of i->j; Q convex iff that number equals |Q|), vectorised with numpy over an exact
      int8 orientation-sign table; also the counts restricted to subsets containing b.
  (5) Method C (pure Python, a third test): every 6-subset containing b; sort the 5 other points by angle
      around b (b is a hull vertex, so they lie in an open half-plane at b) and test that b, q1..q5 is a
      strictly convex polygon (all consecutive turns left, including the wrap-around).
"""
import sys
from itertools import combinations
from math import comb
import numpy as np


def read_points(fn):
    pts = []
    for line in open(fn):
        f = line.split()
        if len(f) >= 2:
            pts.append((int(f[0]), int(f[1])))
    return pts


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def jarvis(P):
    """Hull vertices (CCW) by gift wrapping; general position assumed."""
    if len(P) <= 2:
        return list(P)
    start = min(P)  # leftmost (then lowest): a hull vertex
    hull = [start]
    cur = start
    while True:
        cand = None
        for q in P:
            if q == cur:
                continue
            if cand is None or orient(cur, cand, q) < 0:  # q is right of cur->cand: wrap tighter
                cand = q
        # now every point is left of (or on) cur->cand
        if cand == start:
            break
        hull.append(cand)
        cur = cand
        if len(hull) > len(P):
            raise RuntimeError("gift wrapping did not terminate")
    # sanity: every other point strictly left of each hull edge
    for i in range(len(hull)):
        a, b2 = hull[i], hull[(i + 1) % len(hull)]
        for q in P:
            if q not in (a, b2):
                assert orient(a, b2, q) > 0, "hull edge check failed"
    return hull


def layers(P):
    rest = list(P)
    out = []
    while rest:
        h = jarvis(rest)
        out.append(h)
        hs = set(h)
        rest = [p for p in rest if p not in hs]
    return out


def all_combos(n, k):
    return np.array(list(combinations(range(n), k)), dtype=np.int16)


def count_convex_numpy(Osgn, n, k, b, chunk=10000):
    """Method B: hull-edge counting, vectorised."""
    C = all_combos(n, k)
    pairs = [(i, j) for i in range(k) for j in range(k) if i != j]
    total_convex = 0
    convex_b = 0
    total_b = 0
    for s in range(0, len(C), chunk):
        Q = C[s:s + chunk].astype(np.int64)
        nh = np.zeros(len(Q), dtype=np.int64)
        for (i, j) in pairs:
            others = [m for m in range(k) if m not in (i, j)]
            ok = np.ones(len(Q), dtype=bool)
            for m in others:
                ok &= Osgn[Q[:, i], Q[:, j], Q[:, m]] > 0
            nh += ok
        isconv = nh == k
        hasb = (Q == b).any(axis=1)
        total_convex += int(isconv.sum())
        convex_b += int((isconv & hasb).sum())
        total_b += int(hasb.sum())
        # consistency: every subset has at least 3 hull vertices
        assert (nh >= 3).all()
    return len(C), total_convex, total_b, convex_b


def convex_through_b_angular(P, b, r=5):
    """Method C: count 6-subsets {b} + 5 others in convex position via angular sort around b."""
    others = [p for i, p in enumerate(P) if i != b]  # (fixed: an earlier version compared a tuple to an index)
    bp = P[b]
    assert len(others) == len(P) - 1 and bp not in others
    from functools import cmp_to_key
    cnt = 0
    tested = 0
    for Q in combinations(others, r):
        tested += 1
        # angular order around the hull vertex bp: q1 before q2 iff orient(bp, q1, q2) > 0
        R = sorted(Q, key=cmp_to_key(lambda u, v: -1 if orient(bp, u, v) > 0 else 1))
        poly = [bp] + R
        m = len(poly)
        if all(orient(poly[i], poly[(i + 1) % m], poly[(i + 2) % m]) > 0 for i in range(m)):
            cnt += 1
    return tested, cnt


def main():
    fn = sys.argv[1]
    P = read_points(fn)
    n = len(P)
    b = n - 1
    print(f"file {fn}: {n} points; designated b = index {b} = {P[b]}")
    assert len(set(P)) == n
    gp = all(orient(P[i], P[j], P[k]) != 0 for i, j, k in combinations(range(n), 3))
    print("general position:", gp)
    H = jarvis(P)
    print("hull (gift wrapping):", len(H), "vertices:", H)
    print("b is a hull vertex:", P[b] in H)
    L = layers(P)
    print("layer profile:", [len(l) for l in L])
    for t, l in enumerate(L):
        print(f"  layer {t + 1}: {l}")
    # exact orientation sign table
    Osgn = np.zeros((n, n, n), dtype=np.int8)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                v = orient(P[i], P[j], P[k])
                Osgn[i, j, k] = (v > 0) - (v < 0)
    for k in (5, 6, 7):
        tot, conv, totb, convb = count_convex_numpy(Osgn, n, k, b)
        assert tot == comb(n, k) and totb == comb(n - 1, k - 1)
        print(f"method B k={k}: subsets {tot}, convex {conv} | containing b {totb}, convex containing b {convb}")
    for r in (4, 5, 6):
        tested, cnt = convex_through_b_angular(P, b, r)
        assert tested == comb(n - 1, r)
        print(f"method C: {r + 1}-subsets through b tested {tested}, convex {cnt}")


if __name__ == "__main__":
    main()
