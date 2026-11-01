#!/usr/bin/env python3
"""Exact check of the central 32-point example that the finding's fix ('update the C2 row to 32') relies on.

Usage: python3 -I c2_example_check.py <points file>

Checks with integer / Fraction arithmetic only:
  - 32 distinct points;
  - invariant under the half-turn about the centroid c (2c - p in S for all p), and c not in S;
  - no three collinear;
  - largest subset in convex position (O(n^4) dynamic program over a lowest vertex), expected 6;
the DP is validated against brute force over all subsets on random small integer sets first.
"""
import itertools
import random
import sys
from fractions import Fraction


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def in_convex_position(pts):
    """Brute force: no point lies in a triangle of three others (points in general position)."""
    n = len(pts)
    if n <= 3:
        return True
    for i in range(n):
        for a, b, c in itertools.combinations([j for j in range(n) if j != i], 3):
            A, B, C, X = pts[a], pts[b], pts[c], pts[i]
            d1, d2, d3 = cross(A, B, X), cross(B, C, X), cross(C, A, X)
            if (d1 > 0 and d2 > 0 and d3 > 0) or (d1 < 0 and d2 < 0 and d3 < 0):
                return False
    return True


def largest_convex(pts):
    """Largest convex-position subset of a set in general position (exact)."""
    n = len(pts)
    best = min(n, 2)
    for s in range(n):
        p = pts[s]
        # points above p (lexicographic by (y, x)) so that p is the lowest vertex
        up = [q for q in pts if (q[1], q[0]) > (p[1], p[0])]
        # sort by angle around p, counterclockwise from direction (1, 0): all are in the upper half-plane
        # (or on the ray to the right), so compare with cross products.
        import functools

        def cmp(a, b):
            c = cross(p, a, b)
            return -1 if c > 0 else (1 if c < 0 else 0)

        up.sort(key=functools.cmp_to_key(cmp))
        m = len(up)
        # L[i][j]: max number of vertices of a convex chain p -> ... -> up[i] -> up[j] (i < j), counterclockwise
        NEG = -10 ** 9
        L = [[NEG] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                v = 3  # p, up[i], up[j]  (left turn p, up[i], up[j] holds since angles increase)
                for k in range(i):
                    if L[k][i] > NEG and cross(up[k], up[i], up[j]) > 0:
                        v = max(v, L[k][i] + 1)
                L[i][j] = v
                # closing edge up[j] -> p must turn left at up[j] and at p
                if cross(up[i], up[j], p) > 0:
                    best = max(best, v)
    return best


def selftest():
    rng = random.Random(1)
    tested = 0
    while tested < 60:
        n = rng.randint(6, 10)
        pts = list({(rng.randint(-30, 30), rng.randint(-30, 30)) for _ in range(n)})
        if any(cross(a, b, c) == 0 for a, b, c in itertools.combinations(pts, 3)):
            continue
        bf = max(k for k in range(len(pts) + 1) for sub in itertools.combinations(pts, k) if in_convex_position(list(sub)))
        dp = largest_convex(pts)
        assert bf == dp, (pts, bf, dp)
        tested += 1
    return tested


def main():
    print("DP self-test against brute force:", selftest(), "random sets agree")
    pts = []
    for line in open(sys.argv[1]):
        line = line.split("#")[0].strip()
        if line:
            x, y = map(int, line.split())
            pts.append((x, y))
    n = len(pts)
    S = set(pts)
    print("points:", n, "distinct:", len(S))
    cx = Fraction(sum(x for x, _ in pts), n)
    cy = Fraction(sum(y for _, y in pts), n)
    sym = all((2 * cx - x, 2 * cy - y) in {(Fraction(a), Fraction(b)) for a, b in pts} for x, y in pts)
    print("centroid:", cx, cy, "| half-turn invariant:", sym, "| centre in S:", (cx, cy) in {(Fraction(a), Fraction(b)) for a, b in pts})
    col = sum(1 for a, b, c in itertools.combinations(pts, 3) if cross(a, b, c) == 0)
    print("collinear triples:", col)
    lc = largest_convex(pts)
    print("largest convex subset:", lc)
    ok = n == 32 and len(S) == 32 and sym and col == 0 and lc == 6
    print("CENTRAL 32-POINT EXAMPLE OK" if ok else "CHECK FAILED")
    sys.exit(0 if ok else 1)


main()
