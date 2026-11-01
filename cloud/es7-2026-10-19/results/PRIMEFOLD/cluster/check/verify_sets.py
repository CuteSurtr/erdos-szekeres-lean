#!/usr/bin/env python3
"""Exact verification (written from scratch for TE) of the lower-bound point sets.

usage: verify_sets.py int FILE k          (integer coordinates "x y" per line)
       verify_sets.py zeta m FILE k       (rows w_0..w_{m-1}: point = sum w_j zeta^j, zeta = exp(2 pi i/m), m prime)
Checks: distinct points; exact m-fold rotational symmetry (zeta: closure of the canonical forms under the cyclic
shift; int: closure under (x,y) -> (-y,x) when m = 4); no three collinear; largest convex subset (exact DP) < k.

Exact signs for zeta rows: orient(a,b,c) = Im(conj(b-a)(c-a)).  With z = conj(u) v = sum_k z_k zeta^k,
Im z = sum_{k=1}^{(m-1)/2} d_k sin(2 pi k/m), d_k = z_k - z_{m-k}, = sin(2 pi/m) * P(X), X = 2 cos(2 pi/m),
P(X) = sum_k d_k u_{k-1}(X) (u_0 = 1, u_1 = X, u_j = X u_{j-1} - u_{j-2}).  Im z = 0 iff all d_k = 0 (m prime:
zeta^k - zeta^-k, k = 1..(m-1)/2, are linearly independent).  Otherwise the sign of P(X) is decided on a rational
bracket of X (bisection on the minimal polynomial, exact Fractions) with a rigorous mean-value error bound.
"""
import sys
from fractions import Fraction as Fr
from functools import cmp_to_key
from itertools import combinations

MINPOLY = {5: [-1, 1, 1], 7: [-1, -2, 1, 1]}        # coefficients c_0..c_deg of the min. poly of 2cos(2pi/m)
ROOTBOX = {5: (Fr(6, 10), Fr(7, 10)), 7: (Fr(12, 10), Fr(13, 10))}


def peval(c, x):
    r = Fr(0)
    for a in reversed(c):
        r = r * x + a
    return r


def bracket(m, bits):
    lo, hi = ROOTBOX[m]
    c = MINPOLY[m]
    slo = peval(c, lo) > 0
    assert (peval(c, hi) > 0) != slo
    while hi - lo > Fr(1, 2 ** bits):
        mid = (lo + hi) / 2
        v = peval(c, mid)
        assert v != 0
        if (v > 0) == slo:
            lo = mid
        else:
            hi = mid
    return lo, hi


class ZetaSign:
    def __init__(self, m, bits=400):
        self.m = m
        self.lo, self.hi = bracket(m, bits)
        self.mid = (self.lo + self.hi) / 2
        self.rad = (self.hi - self.lo) / 2
        h = (m - 1) // 2
        # u_{k-1}(X) as coefficient lists
        us = [[1], [0, 1]]
        while len(us) < h:
            a, b = us[-1], us[-2]
            nxt = [0] + a
            for i, cf in enumerate(b):
                nxt[i] -= cf
            us.append(nxt)
        self.us = us[:h]
        self.undecided = 0

    def sign_im(self, z):
        """sign of Im(sum z_k zeta^k)."""
        m = self.m
        d = [z[k] - z[m - k] for k in range(1, (m - 1) // 2 + 1)]
        if all(v == 0 for v in d):
            return 0
        deg = max(len(u) for u in self.us)
        P = [0] * deg
        for dk, u in zip(d, self.us):
            for i, cf in enumerate(u):
                P[i] += dk * cf
        val = peval(P, self.mid)
        R = max(abs(self.lo), abs(self.hi))
        dbound = sum(abs(P[i]) * i * R ** (i - 1) for i in range(1, len(P)))
        err = dbound * self.rad
        if abs(val) > err:
            return 1 if val > 0 else -1
        self.undecided += 1
        raise RuntimeError('sign undecided at this precision')


def zmul_conj(u, v, m):
    """coefficients of conj(u) * v in Z[zeta_m] (length m, exponents mod m)."""
    z = [0] * m
    for i, ui in enumerate(u):
        if ui == 0:
            continue
        for j, vj in enumerate(v):
            if vj:
                z[(j - i) % m] += ui * vj
    return z


def load_zeta(path, m):
    rows = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        w = [int(t) for t in line.split()]
        assert len(w) == m
        rows.append(w)
    return rows


def canon(w, m):
    return tuple(w[j] - w[m - 1] for j in range(m - 1))


def largest_convex(N, O, height_cmp):
    best = min(N, 2)
    for p in range(N):
        Q = [q for q in range(N) if q != p and height_cmp(q, p) > 0]
        Q.sort(key=cmp_to_key(lambda a, b: -O(p, a, b)))
        L = len(Q)
        dp = [[0] * L for _ in range(L)]
        for j in range(L):
            qj = Q[j]
            for i in range(j):
                qi = Q[i]
                v = 3
                for k in range(i):
                    if dp[k][i] + 1 > v and O(Q[k], qi, qj) > 0:
                        v = dp[k][i] + 1
                dp[i][j] = v
                if v > best and O(qi, qj, p) > 0:
                    best = v
    return best


def run_zeta(m, path, k):
    rows = load_zeta(path, m)
    N = len(rows)
    cf = [canon(w, m) for w in rows]
    assert len(set(cf)) == N, 'repeated point'
    shift = lambda w: [w[(j - 1) % m] for j in range(m)]          # multiplication by zeta
    S = set(cf)
    closed = all(canon(shift(w), m) in S for w in rows)
    zs = ZetaSign(m)
    sgn = {}
    for a, b, c in combinations(range(N), 3):
        u = [rows[b][t] - rows[a][t] for t in range(m)]
        v = [rows[c][t] - rows[a][t] for t in range(m)]
        s = zs.sign_im(zmul_conj(u, v, m))
        if s == 0:
            print('COLLINEAR', a, b, c)
            return
        sgn[a, b, c] = s

    def O(a, b, c):
        if a < b < c:
            return sgn[a, b, c]
        if b < c < a:
            return sgn[b, c, a]
        if c < a < b:
            return sgn[c, a, b]
        if a < c < b:
            return -sgn[a, c, b]
        if b < a < c:
            return -sgn[b, a, c]
        return -sgn[c, b, a]
    # height = Im(conj(gamma) * P) with gamma = 1 (y-coordinate); exact comparison
    gamma = [1] + [0] * (m - 1)

    def hcmp(a, b):
        diff = [rows[a][t] - rows[b][t] for t in range(m)]
        s = zs.sign_im(zmul_conj(gamma, diff, m))
        if s == 0:
            raise RuntimeError('height tie')
        return s
    try:
        mc = largest_convex(N, O, hcmp)
    except RuntimeError:
        gamma = [7, 3, 1] + [0] * (m - 3)
        mc = largest_convex(N, O, hcmp)
    print('%s: N=%d m=%d  distinct=yes  zeta-closed=%s  collinear triples=0  largest convex subset=%d  (need < %d): %s' % (
        path.split('/')[-1], N, m, closed, mc, k, 'OK' if (closed and mc < k) else 'FAIL'))


def run_int(path, k):
    pts = []
    for line in open(path):
        line = line.strip()
        if line and not line.startswith('#'):
            x, y = map(int, line.split())
            pts.append((x, y))
    N = len(pts)
    assert len(set(pts)) == N
    S = set(pts)
    closed4 = all((-y, x) in S for (x, y) in pts)

    def O(a, b, c):
        (ax, ay), (bx, by), (cx, cy) = pts[a], pts[b], pts[c]
        d = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        return (d > 0) - (d < 0)
    col = sum(1 for a, b, c in combinations(range(N), 3) if O(a, b, c) == 0)

    def hcmp(a, b):
        ha = pts[a][1] * 1000003 + pts[a][0]
        hb = pts[b][1] * 1000003 + pts[b][0]
        assert ha != hb
        return (ha > hb) - (ha < hb)
    mc = largest_convex(N, O, hcmp)
    print('%s: N=%d  4-fold closed=%s  collinear triples=%d  largest convex subset=%d (need < %d): %s' % (
        path.split('/')[-1], N, closed4, col, mc, k, 'OK' if (closed4 and col == 0 and mc < k) else 'FAIL'))


if __name__ == '__main__':
    if sys.argv[1] == 'int':
        run_int(sys.argv[2], int(sys.argv[3]))
    else:
        run_zeta(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
