#!/usr/bin/env python3
"""Exact-integer geometry toolkit for testing structural statements on point sets.

All predicates use exact integer (or Fraction) arithmetic.  Points are tuples of ints.
"""
from fractions import Fraction
from functools import cmp_to_key
from itertools import combinations
import sys


def read_points(fn):
    pts = []
    for line in open(fn):
        f = line.split()
        if len(f) >= 2:
            pts.append((int(f[0]), int(f[1])))
    return pts


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(v):
    return (v > 0) - (v < 0)


def general_position(P):
    return len(set(P)) == len(P) and all(orient(a, b, c) != 0 for a, b, c in combinations(P, 3))


def largest_convex_subset(points):
    """Exact size of a largest subset in convex position (general position assumed).
    Dynamic program anchored at the lowest vertex (same algorithm as the repository's
    es_lower_bound_witness.py, re-typed here)."""
    best = min(len(points), 2)
    for p in points:
        above = [q for q in points if (q[1], q[0]) > (p[1], p[0])]
        q = sorted(above, key=cmp_to_key(lambda a, b: -1 if orient(p, a, b) > 0 else 1))
        m = len(q)
        chain = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i):
                value = 3
                for k in range(j):
                    if chain[k][j] and orient(q[k], q[j], q[i]) > 0:
                        value = max(value, chain[k][j] + 1)
                chain[j][i] = value
                if orient(q[j], q[i], p) > 0:
                    best = max(best, value)
    return best


def in_convex_position(Q):
    """Brute force: general-position set Q is in convex position iff no point is inside a triangle."""
    for t in combinations(range(len(Q)), 3):
        a, b, c = (Q[i] for i in t)
        o = sgn(orient(a, b, c))
        for i in range(len(Q)):
            if i in t:
                continue
            p = Q[i]
            if sgn(orient(a, b, p)) == o and sgn(orient(b, c, p)) == o and sgn(orient(c, a, p)) == o:
                return False
    return True


def hull(P):
    """Convex hull vertices in counter-clockwise order (general position)."""
    pts = sorted(P)
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def layers(P):
    rest = list(P)
    out = []
    while rest:
        h = hull(rest)
        out.append(h)
        hs = set(h)
        rest = [p for p in rest if p not in hs]
    return out


def inside_triangle(p, a, b, c):
    o = sgn(orient(a, b, c))
    return sgn(orient(a, b, p)) == o and sgn(orient(b, c, p)) == o and sgn(orient(c, a, p)) == o


# ---------- caps and cups with respect to a "down" point z (finite, outside conv, or at infinity) ----------
# A point z is given homogeneously as (z1, z2, z3) with z3 >= 0 (z3 = 0: point at infinity in direction (z1, z2)).

def orient_h(a, b, z):
    """det [[ax, ay, 1], [bx, by, 1], [z1, z2, z3]]; equals orient(a, b, (z1/z3, z2/z3)) * z3 for z3 > 0,
    and det(b - a, d) for the point at infinity reached by going in direction d (z = (d, 0))."""
    z1, z2, z3 = z
    return (a[0] * (b[1] * z3 - z2) - a[1] * (b[0] * z3 - z1) + (b[0] * z2 - b[1] * z1))


def z_less(z):
    """Comparator for the z-order: p <_z q  iff  orient(z, p, q) < 0 (left-to-right when z is 'below')."""
    def cmp(p, q):
        # orient(z, p, q) for homogeneous z: det[[z],[p,1],[q,1]] = orient_h(p, q, z) (cyclic)
        v = orient_h(p, q, z)
        return -1 if v < 0 else (1 if v > 0 else 0)
    return cmp


def z_sorted(P, z):
    return sorted(P, key=cmp_to_key(z_less(z)))


def z_same_side(p, r, q, z):
    """True iff q and z are strictly on the same side of line pr."""
    return sgn(orient(p, r, q)) == sgn(orient_h(p, r, z)) != 0


def longest_z_chains(P, z):
    """Longest z-cap and z-cup in P.  In z-order p<q<r, the triple is a z-cup iff q is on z's side of
    line pr, a z-cap iff q is on the other side.  Consecutive-triple chains (transitivity holds for
    real point sets)."""
    Q = z_sorted(P, z)
    n = len(Q)
    if n <= 2:
        return n, n
    cup = [[2] * n for _ in range(n)]
    cap = [[2] * n for _ in range(n)]
    bcup = bcap = 2
    for j in range(n):
        for i in range(j):
            for h in range(i):
                if z_same_side(Q[h], Q[j], Q[i], z):
                    if cup[h][i] + 1 > cup[i][j]:
                        cup[i][j] = cup[h][i] + 1
                else:
                    if cap[h][i] + 1 > cap[i][j]:
                        cap[i][j] = cap[h][i] + 1
            bcup = max(bcup, cup[i][j])
            bcap = max(bcap, cap[i][j])
    return bcap, bcup


def longest_xy_chains(P):
    """Longest cap and cup for the vertical direction (z = down at infinity)."""
    return longest_z_chains(P, (0, -1, 0))


if __name__ == "__main__":
    P = read_points(sys.argv[1])
    print(len(P), general_position(P), largest_convex_subset(P), [len(L) for L in layers(P)])
