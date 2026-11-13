#!/usr/bin/env python3
"""Exact geometry in Z[zeta_7], written from scratch for the T2d verification (2026-11-02).

A point is w = (w_0..w_6), meaning sum_j w_j zeta^j, zeta = exp(2 pi i / 7).
Im(sum_t e_t zeta^t) = s1 * (D1 + 2 c D2 + (4 c^2 - 1) D3), D_t = e_t - e_{7-t},
with s1 = sin(2pi/7) > 0 and c = cos(2pi/7), a root of 8x^3 + 4x^2 - 4x - 1 (unique root in (1/2, 3/4)).
(sin(4pi/7) = 2 s1 c ; sin(6pi/7) = s1 (4c^2 - 1).)
Re(sum_t e_t zeta^t) = e0 + (e1+e6) c + (e2+e5)(2c^2 - 1) + (e3+e4)(-2c^2 - c + 1/2).
Since c has degree 3, a polynomial of degree <= 2 in c vanishes at c iff all its coefficients vanish.
Signs are decided with a rational enclosure [L/2^K, (L+1)/2^K] of c and an explicit derivative bound.
"""
import sys

M = 7


def _bisect_c(K):
    # integer L with L/2^K <= c < (L+1)/2^K ; f(x) = 8x^3+4x^2-4x-1 increasing on [1/2, 3/4]
    lo, hi = 1 << (K - 1), 3 << (K - 2)  # 1/2, 3/4 scaled by 2^K
    def fsgn(L):  # sign of f(L/2^K) * 2^(3K)
        v = 8 * L ** 3 + 4 * L * L * (1 << K) - 4 * L * (1 << (2 * K)) - (1 << (3 * K))
        return (v > 0) - (v < 0)
    assert fsgn(lo) < 0 and fsgn(hi) > 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        s = fsgn(mid)
        assert s != 0  # c is irrational
        if s < 0:
            lo = mid
        else:
            hi = mid
    return lo


_CACHE = {}


def cbracket(K):
    if K not in _CACHE:
        _CACHE[K] = _bisect_c(K)
    return _CACHE[K]


def sign_quad(a2, a1, a0):
    """exact sign of a2 c^2 + a1 c + a0 at c = cos(2 pi/7); integer (or half-integer scaled) coefficients."""
    if a2 == 0 and a1 == 0 and a0 == 0:
        return 0
    K = 128
    while True:
        L = cbracket(K)
        # value at x0 = L/2^K, times 2^(2K)
        v = a2 * L * L + a1 * L * (1 << K) + a0 * (1 << (2 * K))
        # |Q(c) - Q(x0)| <= (2|a2| + |a1|) * 2^-K  for x0, c in [0, 1]   ->  times 2^(2K)
        err = (2 * abs(a2) + abs(a1)) * (1 << K)
        if abs(v) > err:
            return 1 if v > 0 else -1
        K *= 2
        if K > 1 << 16:
            raise RuntimeError('sign undecided')


def sign_im(e):
    """sign of Im(sum_t e_t zeta^t)"""
    D1, D2, D3 = e[1] - e[6], e[2] - e[5], e[3] - e[4]
    return sign_quad(4 * D3, 2 * D2, D1 - D3)


def sign_re(e):
    """sign of Re(sum_t e_t zeta^t); multiply by 2 to clear the 1/2"""
    A1, A2, A3 = e[1] + e[6], e[2] + e[5], e[3] + e[4]
    # e0 + A1 c + A2 (2c^2 - 1) + A3 (-2c^2 - c + 1/2)
    a2 = 2 * A2 - 2 * A3
    a1 = A1 - A3
    a0 = 2 * e[0] - 2 * A2 + A3  # this is twice the constant term
    return sign_quad(2 * a2, 2 * a1, a0)


def conj_mul(u, v):
    """coefficients of conj(u) * v in the basis zeta^0..zeta^6"""
    e = [0] * M
    for j in range(M):
        uj = u[j]
        if uj == 0:
            continue
        for k in range(M):
            if v[k]:
                e[(k - j) % M] += uj * v[k]
    return e


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def cross_sign(u, v):
    """sign of u_x v_y - u_y v_x = Im(conj(u) v)"""
    return sign_im(conj_mul(u, v))


def orient(a, b, c):
    """+1 if (a, b, c) is counter-clockwise"""
    return cross_sign(sub(b, a), sub(c, a))


def read_pts(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            r = [int(t) for t in line.split()]
            r = r + [0] * (M - len(r))
            assert len(r) == M
            rows.append(r)
    return rows


def to_float(w):
    import cmath, math
    z = cmath.exp(2j * math.pi / M)
    return sum(c * z ** j for j, c in enumerate(w))


if __name__ == '__main__':
    # self-tests against floating point on random inputs
    import random, cmath, math
    random.seed(1)
    z = cmath.exp(2j * math.pi / M)
    bad = 0
    for _ in range(20000):
        e = [random.randint(-50, 50) for _ in range(M)]
        val = sum(c * z ** j for j, c in enumerate(e))
        si, sr = sign_im(e), sign_re(e)
        if abs(val.imag) > 1e-9 and si != (1 if val.imag > 0 else -1):
            bad += 1
        if abs(val.real) > 1e-9 and sr != (1 if val.real > 0 else -1):
            bad += 1
    # exact zeros: e = t*(1,...,1) has value 0; conj-symmetric vectors are real
    for t in range(-3, 4):
        assert sign_im([t] * 7) == 0 and sign_re([t] * 7) == 0
    assert sign_im([5, 2, 3, 1, 1, 3, 2]) == 0  # real element
    print('self-test mismatches:', bad)
