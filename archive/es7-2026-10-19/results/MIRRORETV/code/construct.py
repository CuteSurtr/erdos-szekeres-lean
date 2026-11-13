#!/usr/bin/env python3
"""Explicit integer constructions (exact arithmetic throughout).

1. Erdos-Szekeres cups-caps sets G(a,b) (no a-cup, no b-cap, C(a+b-4,a-2) points) as (+)-trees:
      G(a,b) = G(a-1,b) (+) G(a,b-1),   G(a,b) = one point if a <= 2 or b <= 2.
   X (+) Y means: Y entirely to the right of X and every slope between a point of X and a point of Y is
   larger than every slope inside X and every slope inside Y.
2. The Erdos-Tuza-Valtr set for (a,b,n) = (j, k, k), k = 2j (no j-cap, no k-cup, no convex k-gon):
      R = T_{j-2} (+) ( T_{j-3} (+) ( ... (+) (T_1 (+) T_0) ) ),   T_s = G(k-s, s+2),  |T_s| = C(k-2, s),
   so |R| = sum_{s=0}^{j-2} C(k-2, s).
3. The mirror-symmetric set: R_H = R + (0,H), S = R_H u mu(R_H) u {(-1,0), (-2,0)}, mu(x,y) = (x,-y), with
   H > s_R (W+2) (s_R = largest |slope| inside R, W = largest abscissa of R, smallest abscissa = 0), H increased
   until S is in general position.  |S| = 2|R| + 2.

For odd k = 2j - 1 the same R (T_s = G(k-s, s+2), s = 0..j-2, |R| = 2^(k-3)) is used and NO axis points are
added: S = R_H u mu(R_H), |S| = 2^(k-2).
Usage: construct.py k [gapfactor] [outdir]
Writes outdir/etv_R_k{k}.txt (one "x y" per line, x-sorted) and outdir/mirror_S_k{k}.txt.
"""
import sys
import os
from fractions import Fraction
from math import comb, floor


def G(a, b):
    """(+)-tree of the cups-caps set with no a-cup and no b-cap.  Leaf = None."""
    if a <= 2 or b <= 2:
        return None
    return (G(a - 1, b), G(a, b - 1))


def etv_tree(j, k):
    t = G(k, 2)                      # T_0, one point
    for s in range(1, j - 1):        # T_s (+) (previous)
        t = (G(k - s, s + 2), t)
    return t


def tree_type(t):
    """(size, longest cap, longest cup, largest convex subset) by the (+) recurrences:
       cap(X+Y) = max(cap X, 1 + cap Y), cup(X+Y) = max(cup X + 1, cup Y),
       conv(X+Y) = max(conv X, conv Y, cup X + cap Y)."""
    if t is None:
        return (1, 1, 1, 1)
    nX, capX, cupX, cvX = tree_type(t[0])
    nY, capY, cupY, cvY = tree_type(t[1])
    return (nX + nY, max(capX, 1 + capY), max(cupX + 1, cupY), max(cvX, cvY, cupX + capY))


def realize(t, gapf):
    """Integer realization of a (+)-tree.  Returns (points sorted by x starting at (0,0), max slope as Fraction).
    All slopes are positive."""
    if t is None:
        return [(0, 0)], Fraction(0)
    PX, sX = realize(t[0], gapf)
    PY, sY = realize(t[1], gapf)
    s = max(sX, sY)
    wX = PX[-1][0]
    wY = PY[-1][0]
    g = max(1, int(gapf * (wX + wY)))
    dx = wX + g
    # need  yq + D - yp > s*(xq + dx - xp)  for all p in PX, q in PY
    m1 = max(s * x - y for (x, y) in PY)
    m2 = max(y - s * x for (x, y) in PX)
    D = floor(s * dx + m1 + m2) + 1
    P = PX + [(x + dx, y + D) for (x, y) in PY]
    snew = s
    for (xp, yp) in PX:
        for (xq, yq) in PY:
            sl = Fraction(yq + D - yp, xq + dx - xp)
            assert sl > s
            if sl > snew:
                snew = sl
    return P, snew


def max_abs_slope(P):
    s = Fraction(0)
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            dx = P[j][0] - P[i][0]
            assert dx != 0
            sl = abs(Fraction(P[j][1] - P[i][1], dx))
            if sl > s:
                s = sl
    return s


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def collinear_count(P):
    """Exact count of collinear triples, O(n^2 log n) via slope classes around each point."""
    n = len(P)
    bad = 0
    from math import gcd
    for i in range(n):
        seen = {}
        for j in range(n):
            if j == i:
                continue
            dx = P[j][0] - P[i][0]
            dy = P[j][1] - P[i][1]
            g = gcd(dx, dy)
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            seen[(dx, dy)] = seen.get((dx, dy), 0) + 1
        for c in seen.values():
            bad += c * (c - 1) // 2
    return bad // 3   # each collinear triple counted at each of its 3 points


def mirror_set(R, sR, axis=True):
    W = max(x for x, _ in R)
    assert min(x for x, _ in R) == 0
    H = floor(sR * (W + 2)) + 1
    while True:
        RH = [(x, y + H) for x, y in R]
        S = RH + [(x, -y) for x, y in RH] + ([(-1, 0), (-2, 0)] if axis else [])
        if collinear_count(S) == 0:
            return S, H
        H += 1


def main():
    k = int(sys.argv[1])
    gapf = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    outdir = sys.argv[3] if len(sys.argv) > 3 else "."
    assert k >= 4
    j = (k + 1) // 2            # even k = 2j; odd k = 2j - 1 (then no axis points: |S| = 2|R| = 2^(k-2))
    t = etv_tree(j, k)
    n, cap, cup, cv = tree_type(t)
    pred = sum(comb(k - 2, i) for i in range(j - 1))
    print(f"k={k} j={j}: tree size {n} (ETV value {pred}), recurrence: longest cap {cap}, cup {cup}, conv {cv}")
    assert n == pred and cap <= j - 1 and cv <= k - 1
    R, sR = realize(t, gapf)
    assert len(R) == n and len(set(x for x, _ in R)) == n
    assert all(R[i][0] < R[i + 1][0] for i in range(n - 1))
    sR2 = max_abs_slope(R)
    assert sR2 == sR, (sR2, sR)
    print(f"R: {n} points, max x {R[-1][0]}, max y {max(y for _, y in R)}, max slope {float(sR):.6g}")
    cR = collinear_count(R)
    print("collinear triples in R:", cR)
    assert cR == 0
    S, H = mirror_set(R, sR, axis=(k % 2 == 0))
    print(f"S: {len(S)} points, H = {H}, max |coord| = {max(max(abs(x), abs(y)) for x, y in S)}")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, f"etv_R_k{k}.txt"), "w") as f:
        f.write("".join(f"{x} {y}\n" for x, y in R))
    with open(os.path.join(outdir, f"mirror_S_k{k}.txt"), "w") as f:
        f.write("".join(f"{x} {y}\n" for x, y in S))


if __name__ == "__main__":
    main()
