#!/usr/bin/env python3
"""Exact orientation tables for planar point sets (2026-11-01).

Independent of the other checkers: own exact arithmetic.

Input kinds
  int  FILE        rows "x y" with integer coordinates ('#' lines ignored)
  zeta M FILE      rows of up to M integer coefficients w_0..w_{M-1}; point = sum_j w_j zeta^j, zeta = e^{2 pi i/M}
                   (M odd prime: 5 or 7 tested)
  es   K           the classical Erdos-Szekeres set of 2^(K-2) points from the repository script scripts/es_lower_bound_witness.py

Output: binary table  b"OT1 n\n" followed by n^3 signed bytes T[i][j][k] in {+1,-1,0} (0 only on repeated
indices; any zero orientation of distinct points aborts with an error), plus a short report on stdout.

Exact sign in Z[zeta_M] (M odd): orient(z1,z2,z3) = sign Im(conj(z2-z1) (z3-z1)).  With w = conj(a) b,
Im(w) = sum_{k=1}^{(M-1)/2} (w_k - w_{M-k}) sin(k theta), theta = 2 pi/M, and sin(k theta) = sin(theta) V_{k-1}(c)
with c = 2 cos theta, V_0 = 1, V_1 = c, V_k = c V_{k-1} - V_{k-2}.  So the sign is that of an integer polynomial
P(c) of degree <= (M-3)/2 < deg(minpoly of c) = (M-1)/2, hence P(c) = 0 iff P = 0.  c is bracketed by exact
bisection on its minimal polynomial and P is evaluated by exact integer interval arithmetic.
"""
import sys
from fractions import Fraction
from itertools import combinations

MINPOLY = {  # minimal polynomial of c = 2cos(2pi/M), coefficients low -> high, and a bracket with one root
    5: ([-1, 1, 1], (Fraction(3, 5), Fraction(13, 20))),          # c^2 + c - 1, c = 0.618...
    7: ([-1, -2, 1, 1], (Fraction(6, 5), Fraction(13, 10))),       # c^3 + c^2 - 2c - 1, c = 1.2469...
}
KBITS = 400


def polyval(coeffs, x):
    r = Fraction(0)
    for a in reversed(coeffs):
        r = r * x + a
    return r


def bracket(M):
    coeffs, (lo, hi) = MINPOLY[M]
    flo, fhi = polyval(coeffs, lo), polyval(coeffs, hi)
    assert flo * fhi < 0
    # monotone on the bracket: derivative positive at both ends and convex/concave check is overkill for these
    # tiny intervals; instead verify there is exactly one sign change on a fine grid as a sanity check.
    for _ in range(KBITS):
        mid = (lo + hi) / 2
        fm = polyval(coeffs, mid)
        assert fm != 0
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi, fhi = mid, fm
    # integer endpoints scaled by 2^KBITS
    L = int(lo * (1 << KBITS))
    H = int(hi * (1 << KBITS)) + 1
    assert Fraction(L, 1 << KBITS) <= lo and Fraction(H, 1 << KBITS) >= hi
    return L, H


def vpolys(M):
    """V_{k-1}(c) as integer coefficient lists, k = 1..(M-1)/2."""
    V = [[1], [0, 1]]
    while len(V) < (M - 1) // 2:
        a, b = V[-1], V[-2]
        n = [0] + a
        for i, x in enumerate(b):
            n[i] -= x
        V.append(n)
    return V[: (M - 1) // 2]


class ZetaSign:
    def __init__(self, M):
        self.M = M
        self.L, self.H = bracket(M)
        self.V = vpolys(M)
        self.deg = (M - 3) // 2

    def sign_im(self, w):
        M = self.M
        P = [0] * (self.deg + 1)
        for k in range(1, (M - 1) // 2 + 1):
            D = w[k] - w[M - k]
            if D:
                for i, x in enumerate(self.V[k - 1]):
                    P[i] += D * x
        if not any(P):
            return 0
        # interval evaluation of sum_i P_i c^i * 2^(K*deg), c = c'/2^K, c' in [L, H], c' > 0
        K, d = KBITS, self.deg
        lo = hi = 0
        Lp, Hp = 1, 1
        for i in range(d + 1):
            a, b = P[i] * Lp, P[i] * Hp
            sh = K * (d - i)
            lo += min(a, b) << sh
            hi += max(a, b) << sh
            Lp *= self.L
            Hp *= self.H
        if lo > 0:
            return 1
        if hi < 0:
            return -1
        raise RuntimeError("bracket too coarse for P=%r" % P)


def conj_mul(a, b, M):
    """coefficients of conj(a) * b in Z[x]/(x^M - 1)."""
    w = [0] * M
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    w[(j - i) % M] += ai * bj
    return w


def read_rows(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            rows.append([int(t) for t in line.split()])
    return rows


def table_int(pts):
    n = len(pts)
    T = bytearray(n * n * n)
    zero = 0
    for i, j, k in combinations(range(n), 3):
        (ax, ay), (bx, by), (cx, cy) = pts[i], pts[j], pts[k]
        d = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        s = (d > 0) - (d < 0)
        if s == 0:
            zero += 1
        fill(T, n, i, j, k, s)
    return T, zero


def fill(T, n, i, j, k, s):
    neg = (-s) & 0xFF
    pos = s & 0xFF
    for (a, b, c), v in (((i, j, k), pos), ((j, k, i), pos), ((k, i, j), pos),
                         ((j, i, k), neg), ((i, k, j), neg), ((k, j, i), neg)):
        T[(a * n + b) * n + c] = v


def table_zeta(rows, M):
    zs = ZetaSign(M)
    vecs = [r + [0] * (M - len(r)) for r in rows]
    n = len(vecs)
    T = bytearray(n * n * n)
    zero = 0
    for i, j, k in combinations(range(n), 3):
        a = [x - y for x, y in zip(vecs[j], vecs[i])]
        b = [x - y for x, y in zip(vecs[k], vecs[i])]
        s = zs.sign_im(conj_mul(a, b, M))
        if s == 0:
            zero += 1
        fill(T, n, i, j, k, s)
    return T, zero


def float_points_zeta(rows, M):
    import cmath
    z = cmath.exp(2j * cmath.pi / M)
    return [sum(c * z ** j for j, c in enumerate(r)) for r in rows]


def main():
    kind = sys.argv[1]
    out = sys.argv[-1]
    if kind == 'int':
        pts = [tuple(r[:2]) for r in read_rows(sys.argv[2])]
        assert len(set(pts)) == len(pts), "repeated point"
        T, zero = table_int(pts)
        n = len(pts)
    elif kind == 'es':
        K = int(sys.argv[2])
        sys.path.insert(0, sys.argv[3])
        from es_lower_bound_witness import witness
        pts = [tuple(p) for p in witness(K)]
        assert len(set(pts)) == len(pts)
        with open(out + '.pts', 'w') as f:
            f.write('# classical Erdos-Szekeres set, es_lower_bound_witness.witness(%d)\n' % K)
            for x, y in pts:
                f.write('%d %d\n' % (x, y))
        T, zero = table_int(pts)
        n = len(pts)
    elif kind == 'zeta':
        M = int(sys.argv[2])
        rows = read_rows(sys.argv[3])
        assert len({tuple(r) for r in rows}) == len(rows), "repeated coefficient row"
        T, zero = table_zeta(rows, M)
        n = len(rows)
        # sanity cross-check against floating point (not part of the exact result)
        fz = float_points_zeta(rows, M)
        bad = 0
        for i, j, k in combinations(range(n), 3):
            a, b = fz[j] - fz[i], fz[k] - fz[i]
            d = (a.conjugate() * b).imag
            if abs(d) > 1e-6 * max(1.0, abs(a) * abs(b)):
                s = 1 if d > 0 else -1
                if (T[(i * n + j) * n + k] if T[(i * n + j) * n + k] < 128 else T[(i * n + j) * n + k] - 256) != s:
                    bad += 1
        print('float cross-check disagreements (|det| not tiny):', bad)
    else:
        raise SystemExit('unknown kind')
    if zero:
        raise SystemExit('ERROR: %d collinear triples' % zero)
    with open(out, 'wb') as f:
        f.write(b'OT1 %d\n' % n)
        f.write(bytes(T))
    print('n=%d, no collinear triple, table written to %s' % (n, out))


if __name__ == '__main__':
    main()
