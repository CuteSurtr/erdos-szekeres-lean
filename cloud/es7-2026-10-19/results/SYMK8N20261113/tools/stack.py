#!/usr/bin/env python3
"""Exact evaluator for *stacked* (multi-scale) m-fold configurations, m = 3, 4.

A point is (e, x, y): the plane point eps^e * (x, y) with integers x, y and a symbolic infinitesimal eps > 0.
Every orientation det(b - a, c - a) = cr(a,b) + cr(b,c) + cr(c,a) with cr(eps^e1 z1, eps^e2 z2) = eps^(e1+e2) cr(z1, z2)
is a polynomial in eps; its sign for all sufficiently small eps > 0 is the sign of its lowest-order nonzero coefficient.
So the order type of the configuration for small eps (the 'limit order type') is computed exactly.  Coordinate
comparisons (for the (y, x) anchor order of the DP) are done the same way.

m = 4: .pts rows w0..w3 -> (x, y) = (w0 - w2, w1 - w3);  m = 3: (a, b) = (w0 - w2, w1 - w2) oblique coordinates
(orientation preserving linear image), rotation (a, b) -> (-b, a - b).
Rotations of a bundle by a rational angle: (x, y) -> ((q^2 - p^2) x - 2pq y, 2pq x + (q^2 - p^2) y), i.e. by
2 atan(p/q) up to the positive factor p^2 + q^2 (irrelevant for orientations inside a bundle and, because the
scales are separated by eps, for all orientations).  For m = 3 the rotation is applied in Cartesian form: we only
use m = 4 rotations here.
"""
import ctypes, os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_lib = None


def lib():
    global _lib
    if _lib is None:
        so = os.path.join(HERE, 'libcvxdp.so')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(os.path.join(HERE, 'cvxdp.c')):
            os.system('gcc -O2 -shared -fPIC -o %s %s' % (so, os.path.join(HERE, 'cvxdp.c')))
        _lib = ctypes.CDLL(so)
        _lib.cvx_dp.restype = ctypes.c_int
        _lib.cvx_dp.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
    return _lib


def read_pts(fn, m):
    P = []
    for line in open(fn):
        line = line.split('#')[0].strip()
        if not line:
            continue
        w = list(map(int, line.split()))
        if m == 4:
            P.append((w[0] - w[2], w[1] - w[3]))
        elif m == 3:
            P.append((w[0] - w[2], w[1] - w[2]))
        else:
            raise ValueError
    return P


def layers4(P):
    """group a 4-fold set into orbits; returns list of orbits (each 4 points (x, y)), outermost first, and centre flag"""
    orb = {}
    centre = False
    for (x, y) in P:
        if x == 0 and y == 0:
            centre = True
            continue
        orb.setdefault(x * x + y * y, []).append((x, y))
    out = [orb[k] for k in sorted(orb, reverse=True)]
    for o in out:
        assert len(o) == 4, len(o)
    return out, centre


def rot4(pt, k):
    x, y = pt
    for _ in range(k % 4):
        x, y = -y, x
    return (x, y)


def rotq(pt, p, q):
    x, y = pt
    c, s = q * q - p * p, 2 * p * q
    return (c * x - s * y, s * x + c * y)


def lowsign(terms):
    """terms: dict exponent -> integer coefficient; sign of lowest-order nonzero coefficient"""
    for e in sorted(terms):
        v = terms[e]
        if v:
            return 1 if v > 0 else -1
    return 0


def orient(a, b, c):
    t = {}
    for (u, v) in ((a, b), (b, c), (c, a)):
        e = u[0] + v[0]
        t[e] = t.get(e, 0) + u[1] * v[2] - u[2] * v[1]
    return lowsign(t)


def cmp_coord(a, b, idx):
    t = {}
    t[a[0]] = t.get(a[0], 0) + a[idx]
    t[b[0]] = t.get(b[0], 0) - b[idx]
    return lowsign(t)


def sign_table(pts):
    n = len(pts)
    S = np.zeros((n, n, n), dtype=np.int8)
    zero = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                s = orient(pts[i], pts[j], pts[k])
                if s == 0:
                    zero.append((i, j, k))
                S[i, j, k] = S[j, k, i] = S[k, i, j] = s
                S[j, i, k] = S[i, k, j] = S[k, j, i] = -s
    return S, zero


def ranks(pts):
    from functools import cmp_to_key
    def cmp(i, j):
        c = cmp_coord(pts[i], pts[j], 2)
        if c == 0:
            c = cmp_coord(pts[i], pts[j], 1)
        return c
    order = sorted(range(len(pts)), key=cmp_to_key(cmp))
    r = [0] * len(pts)
    for pos, i in enumerate(order):
        r[i] = pos
    return np.array(r, dtype=np.int32)


def evaluate(pts, kmax=9):
    """pts: list of (e, x, y).  Returns (maxlen, counts dict L->#convex L-gons for L<=kmax, #zero triples)"""
    S, zero = sign_table(pts)
    if zero:
        return None, None, len(zero)
    R = ranks(pts)
    cnt = np.zeros(kmax + 1, dtype=np.int64)
    S = np.ascontiguousarray(S)
    ml = lib().cvx_dp(len(pts), S.ctypes.data, R.ctypes.data, cnt.ctypes.data, kmax)
    return ml, {L: int(cnt[L]) for L in range(3, kmax + 1)}, 0


def build_stack(bundles):
    """bundles: list of (list of 4-fold orbits [(x,y)*4], exponent, (p,q) rotation or None).  Returns pts."""
    pts = []
    for orbits, e, rq in bundles:
        for o in orbits:
            for pt in o:
                if rq is not None:
                    pt = rotq(pt, rq[0], rq[1])
                pts.append((e, pt[0], pt[1]))
    return pts


if __name__ == '__main__':
    m = int(sys.argv[1]); fn = sys.argv[2]
    P = read_pts(fn, m)
    pts = [(0, x, y) for (x, y) in P]
    print(fn, len(pts), evaluate(pts))
