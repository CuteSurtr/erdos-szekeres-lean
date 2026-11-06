#!/usr/bin/env python3
"""Exact arithmetic for points of Z[zeta_7] (written from scratch for the E8 check).

A point is w = (w_0..w_6), meaning sum_j w_j zeta^j with zeta = exp(2 pi i / 7).

Cross product a x b = Im(conj(a) b).  conj(a) b = sum_k c_k zeta^k with c_k = sum_j a_j b_{j+k} (mod 7).
Im = sum_{k=1..3} (c_k - c_{7-k}) sin(2 pi k/7)
   = sin(theta) * (e1 + e2 t + e3 (t^2 - 1)),   t = 2 cos(theta), theta = 2 pi/7,
using sin 2x = sin x * 2cos x and sin 3x = sin x * (4 cos^2 x - 1).  sin(theta) > 0, so
sign(a x b) = sign(P(t)) with P(t) = e3 t^2 + e2 t + (e1 - e3).
t is the unique root in [1.2, 1.3] of f(x) = x^3 + x^2 - 2x - 1 (min. poly of zeta + zeta^-1).
We bracket t as T/2^K < t < (T+1)/2^K by integer bisection and certify each sign with an explicit
error bound; anything not certified raises an exception.  1, t, t^2 are Q-linearly independent
(t has degree 3), so P(t) = 0 iff (e1, e2, e3) = 0.
"""
import sys

K = 320
ONE = 1 << K


def f_scaled(T):
    # 2^(3K) * f(T / 2^K)
    return T ** 3 + T * T * ONE - 2 * T * ONE * ONE - ONE ** 3


def bracket_t():
    lo = (12 * ONE) // 10      # 1.2 (rounded down) -> f < 0
    hi = (13 * ONE) // 10 + 1  # 1.3 (rounded up)   -> f > 0
    assert f_scaled(lo) < 0 < f_scaled(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if f_scaled(mid) < 0:
            lo = mid
        else:
            hi = mid
    assert f_scaled(lo) < 0 < f_scaled(lo + 1)
    return lo  # t in (lo/2^K, (lo+1)/2^K)


T = bracket_t()


def sign_poly(e0, e1, e2):
    """Certified sign of Q(t) = e0 + e1 t + e2 t^2 at t = 2cos(2pi/7)."""
    if e0 == 0 and e1 == 0 and e2 == 0:
        return 0
    # N = 2^(2K) Q(T/2^K); |2^(2K)(Q(t) - Q(T/2^K))| <= 2^K (|e1| + |e2| (2 T/2^K + 2^-K)) * 1
    N = e2 * T * T + e1 * T * ONE + e0 * ONE * ONE
    err = ONE * (abs(e1) + abs(e2) * 3) + abs(e2) * 4  # generous (t < 1.3, so 2t + 2^-K < 3)
    if abs(N) <= err:
        raise ArithmeticError("sign not certified: %r" % ((e0, e1, e2),))
    return 1 if N > 0 else -1


def cross_e(a, b):
    """(e1,e2,e3) with Im(conj(a) b) = sin(theta) (e1 + e2 t + e3 (t^2-1))."""
    c = [0] * 7
    for j in range(7):
        aj = a[j]
        if aj:
            for k in range(7):
                c[k] += aj * b[(j + k) % 7]
    return (c[1] - c[6], c[2] - c[5], c[3] - c[4])


def poly_from_e(e):
    e1, e2, e3 = e
    return (e1 - e3, e2, e3)


def read_pts(path):
    pts = []
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            v = [int(x) for x in s.split()]
            assert len(v) == 7, (path, line)
            pts.append(tuple(v))
    return pts


def canon(w):
    """Unique representative in Z[zeta]: subtract w_6 * (1,...,1) (since 1+zeta+...+zeta^6 = 0)."""
    return tuple(x - w[6] for x in w)


def rot(w):
    """Multiplication by zeta: coefficient of zeta^{j+1} becomes w_j."""
    return (w[6],) + tuple(w[:6])


def sign_im_diff(a, b):
    """sign Im(a - b) = sign sum_k d_k sin(2 pi k/7), d = a - b."""
    d = [x - y for x, y in zip(a, b)]
    e = (d[1] - d[6], d[2] - d[5], d[3] - d[4])
    return sign_poly(*poly_from_e(e))


def sign_re_diff(a, b):
    """sign Re(a - b). 2Re = 2 d0 + (d1+d6) t + (d2+d5)(t^2-2) + (d3+d4)(t^3-3t), t^3 = -t^2+2t+1."""
    d = [x - y for x, y in zip(a, b)]
    s1, s2, s3 = d[1] + d[6], d[2] + d[5], d[3] + d[4]
    # (t^3 - 3t) = -t^2 - t + 1
    e0 = 2 * d[0] - 2 * s2 + s3
    e1 = s1 - s3
    e2 = s2 - s3
    return sign_poly(e0, e1, e2)


def orient_table(pts):
    """Return dict-free 3D list O[i][j][k] in {-1,0,1} (exact, certified)."""
    n = len(pts)
    E = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                E[i][j] = cross_e(pts[i], pts[j])
    O = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            Eij = E[i][j]
            for k in range(j + 1, n):
                Ejk = E[j][k]
                Eki = E[k][i]
                e = (Eij[0] + Ejk[0] + Eki[0], Eij[1] + Ejk[1] + Eki[1], Eij[2] + Ejk[2] + Eki[2])
                s = sign_poly(*poly_from_e(e))
                O[i][j][k] = O[j][k][i] = O[k][i][j] = s
                O[j][i][k] = O[i][k][j] = O[k][j][i] = -s
    return O


if __name__ == '__main__':
    print('T/2^K =', T / ONE)
