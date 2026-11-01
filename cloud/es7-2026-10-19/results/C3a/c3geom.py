#!/usr/bin/env python3
"""Exact geometry for 3-fold rotationally symmetric point sets (task C3a).

Coordinates live in Z[sqrt3]; a number is a pair (a, b) meaning a + b*sqrt3, and every sign
used for chi_S, the x-order and collinearity with the centre is decided exactly.  The
projected set S' = phi(S), phi(x, y) = (y/x, 1/x), is computed independently in mpmath
(120 digits) and every sign taken from it is checked against an explicit margin.

Conventions: the rotation R is by +120 degrees about c = 0.  The line l through c has
integer direction u; the new coordinates are (xt, yt) = (p.n, p.u) with n = (u2, -u1),
an orientation-preserving similarity, so l becomes the y-axis.
"""
import itertools
import random
from functools import cmp_to_key

import mpmath

mpmath.mp.dps = 120
MARGIN = mpmath.mpf(10) ** -60


def zsgn(a, b):
    """sign of a + b*sqrt3 (ints)."""
    if a >= 0 and b >= 0:
        return 1 if (a or b) else 0
    if a <= 0 and b <= 0:
        return -1
    # opposite signs: compare a^2 with 3 b^2
    d = a * a - 3 * b * b
    if d == 0:
        return 0  # impossible for (a,b) != 0, kept for safety
    return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)


def zmul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def zsub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def zadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def zmpf(x):
    return mpmath.mpf(x[0]) + mpmath.mpf(x[1]) * mpmath.sqrt(3)


def rot(p):
    """R p = ((-X - sqrt3 Y)/2, (sqrt3 X - Y)/2) exactly; asserts integrality."""
    X, Y = p
    s3Y = (3 * Y[1], Y[0])
    s3X = (3 * X[1], X[0])
    nx = (-X[0] - s3Y[0], -X[1] - s3Y[1])
    ny = (s3X[0] - Y[0], s3X[1] - Y[1])
    for v in nx + ny:
        assert v % 2 == 0
    return ((nx[0] // 2, nx[1] // 2), (ny[0] // 2, ny[1] // 2))


def orient(p, q, r):
    """exact sign of det(q-p, r-p)."""
    ax, ay = zsub(q[0], p[0]), zsub(q[1], p[1])
    bx, by = zsub(r[0], p[0]), zsub(r[1], p[1])
    return zsgn(*zsub(zmul(ax, by), zmul(ay, bx)))


ZERO = ((0, 0), (0, 0))


def random_c3(m, rng, M=1000, shape="disk"):
    """3m points: m random base points (scaled by 4 so that rotations stay integral),
    with their two rotations.  Returns the list ordered orbit by orbit [p, Rp, R^2 p]."""
    while True:
        base = []
        for _ in range(m):
            while True:
                if shape == "disk":
                    x, y = rng.randint(-M, M), rng.randint(-M, M)
                    if 0 < x * x + y * y <= M * M:
                        break
                elif shape == "ring":
                    x, y = rng.randint(-M, M), rng.randint(-M, M)
                    if (M // 2) ** 2 <= x * x + y * y <= M * M:
                        break
                elif shape == "thin":  # thin radial strip: few points in convex position
                    x, y = rng.randint(M // 2, 3 * M // 2), rng.randint(-M // 400, M // 400)
                    break
                else:  # clustered: a few clusters, makes big convex sets rarer
                    cx, cy = shape
                    x, y = cx + rng.randint(-M // 8, M // 8), cy + rng.randint(-M // 8, M // 8)
                    if x or y:
                        break
            base.append(((4 * x, 0), (4 * y, 0)))
        pts = []
        for p in base:
            q = rot(p)
            r = rot(q)
            assert rot(r) == p
            pts += [p, q, r]
        if general_position(pts):
            return pts


def general_position(pts):
    n = len(pts)
    for i, j in itertools.combinations(range(n), 2):
        if orient(ZERO, pts[i], pts[j]) == 0:
            return False  # collinear with the centre (also catches repeated points)
    for i, j, k in itertools.combinations(range(n), 3):
        if orient(pts[i], pts[j], pts[k]) == 0:
            return False
    return True


def frame(pts, rng, U=50, u=None):
    """Pick an integer direction u for l avoiding S; return xt, yt (Z[sqrt3]) per point."""
    while True:
        u1, u2 = u if u is not None else (rng.randint(-U, U), rng.randint(-U, U))
        if u1 == 0 and u2 == 0:
            continue
        xt = [zadd(zmul((u2, 0), p[0]), zmul((-u1, 0), p[1])) for p in pts]
        yt = [zadd(zmul((u1, 0), p[0]), zmul((u2, 0), p[1])) for p in pts]
        if all(zsgn(*v) != 0 for v in xt) and len(set(xt)) == len(xt):
            return (u1, u2), xt, yt
        assert u is None


class Labelled:
    """All data of item 1-4 for one symmetric set and one line l."""

    def __init__(self, pts, rng, u=None):
        n = len(pts)
        self.n, self.m = n, n // 3
        self.pts = pts
        self.u, xt, yt = frame(pts, rng, u=u)

        # sort by X' = yt/xt exactly
        def cmp(i, j):
            # yt_i/xt_i - yt_j/xt_j has the sign of (yt_i xt_j - yt_j xt_i) * sgn(xt_i xt_j)
            s = zsgn(*zsub(zmul(yt[i], xt[j]), zmul(yt[j], xt[i]))) * zsgn(*xt[i]) * zsgn(*xt[j])
            assert s != 0
            return s

        order = sorted(range(n), key=cmp_to_key(cmp))
        self.orig = order  # label -> index into pts
        self.lab = {o: l for l, o in enumerate(order)}
        self.P = [pts[o] for o in order]
        self.xt = [xt[o] for o in order]
        self.yt = [yt[o] for o in order]
        # rotation on labels
        idx = {pts[i]: i for i in range(n)}
        self.Rlab = [self.lab[idx[rot(pts[order[l]])]] for l in range(n)]
        # sigma
        self.sigma = [1 if zsgn(*v) < 0 else 0 for v in self.xt]
        # S' in mpmath
        X = [zmpf(self.yt[l]) / zmpf(self.xt[l]) for l in range(n)]
        Y = [1 / zmpf(self.xt[l]) for l in range(n)]
        self.Xp, self.Yp = X, Y
        for l in range(n - 1):
            assert X[l + 1] - X[l] > MARGIN
        # chi' (x-sorted S'), chi_S, inv, before
        self.chip = {}
        self.chiS = {}
        for i, j, k in itertools.combinations(range(n), 3):
            d = (X[j] - X[i]) * (Y[k] - Y[i]) - (Y[j] - Y[i]) * (X[k] - X[i])
            assert abs(d) > MARGIN, d
            self.chip[(i, j, k)] = 1 if d > 0 else -1
            self.chiS[(i, j, k)] = orient(self.P[i], self.P[j], self.P[k])
        self.inv = {}
        self.before = {}
        for i, j in itertools.combinations(range(n), 2):
            dy = Y[i] - Y[j]
            assert abs(dy) > MARGIN
            self.inv[(i, j)] = 1 if dy > 0 else 0
            s = zsgn(*zsub(self.xt[i], self.xt[j]))
            assert s != 0
            self.before[(i, j)] = 1 if s < 0 else 0  # i strictly left of j in S


def parity_sort(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(t)), (-1 if inv & 1 else 1)


def ochi(tab, t):
    s, sg = parity_sort(t)
    return sg * tab[s]
