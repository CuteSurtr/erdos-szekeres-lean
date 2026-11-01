#!/usr/bin/env python3
"""Exact decision (no floating point) of whether a one-sided partition (A, B) admits a point z making it a z-split.

Reduction: a direction d satisfying all direction constraints implies finite points p + t d (t large) far outside
conv(S) satisfying the same strict constraints; so a z exists iff the open polygon
    F = { z in R^2 : r . (z, 1) > 0 for all constraint rows r }
has a point outside conv(S).  We compute Q = cl(F) cap B0 (B0 a box strictly containing conv(S)) by exact
Sutherland-Hodgman clipping with Fractions.  Then: z exists iff Q has nonempty interior and some vertex of Q is not
in the closed hull conv(S) (Q convex, conv(S) closed convex; and if F left B0 it would cross B0 \\ conv(S)).
"""
import itertools
from fractions import Fraction


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


def rows_for(P, A, B):
    rows = []
    b0, a0 = next(iter(B)), next(iter(A))
    for X, ref, flip in ((A, b0, 1), (B, a0, -1)):
        for p, q in itertools.combinations(sorted(X), 2):
            pa, pb = P[p], P[q]
            s = sgn(orient(pa, pb, P[ref]))
            assert s != 0
            # orient(pa, pb, z) = z1 (ay - by) + z2 (bx - ax) + (ax by - ay bx)
            coef = (pa[1] - pb[1], pb[0] - pa[0], pa[0] * pb[1] - pa[1] * pb[0])
            # (S1): z on ref's (B's) side: s * orient > 0 ; (S2): z opposite A: -s * orient > 0
            rows.append(tuple(flip * s * c for c in coef))
    return rows


def clip(poly, r):
    """Keep the part of convex polygon poly (list of Fraction points, ccw) with r.(z,1) >= 0."""
    def val(p):
        return r[0] * p[0] + r[1] * p[1] + r[2]
    out = []
    m = len(poly)
    for i in range(m):
        p, q = poly[i], poly[(i + 1) % m]
        vp, vq = val(p), val(q)
        if vp >= 0:
            out.append(p)
        if (vp > 0 and vq < 0) or (vp < 0 and vq > 0):
            t = vp / (vp - vq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    # remove consecutive duplicates
    res = []
    for p in out:
        if not res or res[-1] != p:
            res.append(p)
    if len(res) > 1 and res[0] == res[-1]:
        res.pop()
    return res


def area2(poly):
    s = Fraction(0)
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        s += p[0] * q[1] - p[1] * q[0]
    return s


def in_closed_hull(P, z):
    zx, zy = z
    for a, b, c in itertools.combinations(P, 3):
        s = sgn(orient(a, b, c))
        if s == 0:
            continue
        def o(u, v):
            return (v[0] - u[0]) * (zy - u[1]) - (v[1] - u[1]) * (zx - u[0])
        if sgn(o(a, b)) * s >= 0 and sgn(o(b, c)) * s >= 0 and sgn(o(c, a)) * s >= 0:
            return True
    return False


def hull_pts(P):
    pts = sorted(P)
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


def z_exists(P, A, B):
    """Returns (bool, witness or None).  witness: an exact finite point z outside conv(S) satisfying all rows."""
    rows = rows_for(P, A, B)
    M = 10 * max(max(abs(x), abs(y)) for x, y in P) + 10
    M = Fraction(M)
    poly = [(-M, -M), (M, -M), (M, M), (-M, M)]
    for r in rows:
        poly = clip(poly, r)
        if len(poly) < 3:
            return False, None
    if area2(poly) == 0:
        return False, None
    H = hull_pts(P)
    for v in poly:
        if not in_closed_hull(H, v):
            # build an interior witness near v: move v slightly towards the centroid of Q
            cx = sum(p[0] for p in poly) / len(poly)
            cy = sum(p[1] for p in poly) / len(poly)
            eps = Fraction(1, 2)
            for _ in range(200):
                w = (v[0] + eps * (cx - v[0]), v[1] + eps * (cy - v[1]))
                if all(r[0] * w[0] + r[1] * w[1] + r[2] > 0 for r in rows) and not in_closed_hull(H, w):
                    return True, w
                eps /= 2
            raise RuntimeError("could not build interior witness (should not happen)")
    return False, None


def verify(P, A, B, w):
    """Exact re-check of (S1), (S2) and w outside conv(P) for a finite witness w (independent of rows_for)."""
    if in_closed_hull(P, w):
        return False
    def oz(p, q):
        return (q[0] - p[0]) * (w[1] - p[1]) - (q[1] - p[1]) * (w[0] - p[0])
    for a, a2 in itertools.combinations(sorted(A), 2):
        sz = sgn(oz(P[a], P[a2]))
        if sz == 0 or any(sgn(orient(P[a], P[a2], P[b])) != sz for b in B):
            return False
    for b, b2 in itertools.combinations(sorted(B), 2):
        sz = sgn(oz(P[b], P[b2]))
        if sz == 0 or any(sgn(orient(P[b], P[b2], P[a])) != -sz for a in A):
            return False
    return True
