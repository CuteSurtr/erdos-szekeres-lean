#!/usr/bin/env python3
"""Exact certification of a point set given in Z[zeta_m] coefficient rows (m prime) or integer xy rows (mode 'int').

Written from scratch for the TA verification. Point = sum_j w_j zeta^j, zeta = exp(2 pi i/m).
orient(P,Q,R) = Im( conj(Q-P) * (R-P) ).  For z = sum_t a_t zeta^t:
  Im z = sin(2pi/m) * sum_t a_t U_{t-1}(c),   Re z = sum_t a_t T_t(c),   c = cos(2pi/m)
  exact zero tests (m prime): Im z = 0 iff a_t == a_{-t} for all t;  Re z = 0 iff a_t + a_{-t} == 2 a_0 for all t.
Nonzero signs are decided by rational interval arithmetic with c bracketed to width < 2^-400.
Outputs: general position, m-fold symmetry (exact), largest convex subset by an O(n^4) DP, and an orientation
table file for the independent C enumerator.
"""
import sys, math, itertools
from fractions import Fraction as Fr

def cheb_U_poly_eval_interval(m):
    pass

def U_val(n, x):
    # U_{-1}=0, U_0=1, U_{k+1} = 2x U_k - U_{k-1}; works for Fractions
    if n < 0: return 0 * x
    a, b = 0 * x, 1 + 0 * x
    for _ in range(n):
        a, b = b, 2 * x * b - a
    return b

def bracket_cos(m, bits=420):
    c0 = math.cos(2 * math.pi / m)
    lo, hi = Fr(c0) - Fr(1, 10**9), Fr(c0) + Fr(1, 10**9)
    f = lambda x: U_val(m - 1, x)
    flo, fhi = f(lo), f(hi)
    assert flo != 0 and fhi != 0 and (flo > 0) != (fhi > 0), 'no sign change'
    while hi - lo > Fr(1, 2**bits):
        mid = (lo + hi) / 2
        fm = f(mid)
        assert fm != 0
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return lo, hi

class Iv:
    __slots__ = ('a', 'b')
    def __init__(self, a, b=None):
        self.a = a; self.b = a if b is None else b
    def __add__(s, o):
        if not isinstance(o, Iv): o = Iv(Fr(o))
        return Iv(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o):
        if not isinstance(o, Iv): o = Iv(Fr(o))
        return Iv(s.a - o.b, s.b - o.a)
    def __rsub__(s, o):
        return Iv(Fr(o)) - s
    def __mul__(s, o):
        if not isinstance(o, Iv): o = Iv(Fr(o))
        p = (s.a * o.a, s.a * o.b, s.b * o.a, s.b * o.b)
        return Iv(min(p), max(p))
    __rmul__ = __mul__

class ZetaSigner:
    def __init__(self, m):
        self.m = m
        lo, hi = bracket_cos(m)
        self.c = Iv(lo, hi)
        self.U = [Iv(Fr(0))] + [None] * m   # U[t] = U_{t-1}(c)
        a, b = Iv(Fr(0)), Iv(Fr(1))
        self.U[1] = b
        for t in range(2, m):
            a, b = b, 2 * self.c * b - a
            self.U[t] = b
        self.T = [Iv(Fr(1)), self.c]
        for t in range(2, m):
            self.T.append(2 * self.c * self.T[-1] - self.T[-2])
    def sign_im(self, a):
        m = self.m
        if all(a[t] == a[(-t) % m] for t in range(m)): return 0
        acc = Iv(Fr(0))
        for t in range(1, m):
            if a[t]: acc = acc + self.U[t] * a[t]
        assert acc.a > 0 or acc.b < 0, 'interval contains 0 for nonzero element'
        return 1 if acc.a > 0 else -1
    def sign_re(self, a):
        m = self.m
        if all(a[t] + a[(-t) % m] == 2 * a[0] for t in range(m)): return 0
        acc = Iv(Fr(0))
        for t in range(m):
            if a[t]: acc = acc + self.T[t] * a[t]
        assert acc.a > 0 or acc.b < 0
        return 1 if acc.a > 0 else -1

def conj_mul(u, v, m):
    out = [0] * m
    for j in range(m):
        if u[j] == 0: continue
        uj = u[j]
        for k in range(m):
            if v[k]: out[(k - j) % m] += uj * v[k]
    return out

def load(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'): continue
        rows.append([int(t) for t in line.split()])
    return rows

def main():
    path = sys.argv[1]; mode = sys.argv[2]; tabout = sys.argv[3] if len(sys.argv) > 3 else None
    rows = load(path)
    n = len(rows)
    if mode == 'int':
        P = [tuple(r) for r in rows]
        def orient(i, j, k):
            (ax, ay), (bx, by), (cx, cy) = P[i], P[j], P[k]
            v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
            return (v > 0) - (v < 0)
        lexkey = lambda i: P[i]
        def lexless(i, j): return P[i] < P[j]
        # symmetry: rotation by 90 degrees
        S = set(P)
        rot = [(-y, x) for (x, y) in P]
        sym = set(rot) == S and len(S) == n
        perm = [P.index(q) for q in rot]
        msym = 4
    else:
        m = int(mode)
        assert all(len(r) == m for r in rows)
        Z = ZetaSigner(m)
        def orient(i, j, k):
            u = [rows[j][t] - rows[i][t] for t in range(m)]
            v = [rows[k][t] - rows[i][t] for t in range(m)]
            return Z.sign_im(conj_mul(u, v, m))
        def cmp_coord(i, j):
            d = [rows[i][t] - rows[j][t] for t in range(m)]
            sx = Z.sign_re(d)
            if sx: return sx
            return Z.sign_im(d)
        def canon(w):
            return tuple(wj - w[m - 1] for wj in w)
        C = [canon(r) for r in rows]
        assert len(set(C)) == n, 'repeated point'
        rot = [canon([r[(j - 1) % m] for j in range(m)]) for r in rows]
        sym = set(rot) == set(C)
        perm = [C.index(q) for q in rot] if sym else None
        msym = m
    # orientation table
    O = {}
    zero = 0
    for i, j, k in itertools.combinations(range(n), 3):
        s = orient(i, j, k)
        if s == 0: zero += 1
        O[(i, j, k)] = s
    def ori(i, j, k):
        if i < j < k: return O[(i, j, k)]
        a = [i, j, k]; s = 1
        # sort with parity
        for x in range(3):
            for y in range(2 - x):
                if a[y] > a[y + 1]: a[y], a[y + 1] = a[y + 1], a[y]; s = -s
        return s * O[tuple(a)]
    print('file', path, 'n', n, 'collinear triples', zero)
    print('exact %d-fold rotation symmetry of the point set:' % msym, sym)
    if sym:
        # also check the orientation table is invariant (consistency)
        bad = sum(1 for (i, j, k), s in O.items() if ori(perm[i], perm[j], perm[k]) != s)
        print('orientation table invariant under rotation permutation: bad =', bad)
    # lexicographic order
    import functools
    if mode == 'int':
        order = sorted(range(n), key=lexkey)
    else:
        order = sorted(range(n), key=functools.cmp_to_key(cmp_coord))
    rank = {p: r for r, p in enumerate(order)}
    best = 2; bestpoly = None
    for p in order:
        Q = [q for q in range(n) if rank[q] > rank[p]]
        Q.sort(key=functools.cmp_to_key(lambda a, b: -ori(p, a, b)))
        k = len(Q)
        # verify sortedness consistency (strict ccw order)
        for a in range(k - 1):
            assert ori(p, Q[a], Q[a + 1]) > 0
        dp = [[0] * k for _ in range(k)]
        par = [[-1] * k for _ in range(k)]
        for j in range(k):
            for i in range(j):
                val = 3; pr = -1
                for h in range(i):
                    if dp[h][i] + 1 > val and ori(Q[h], Q[i], Q[j]) > 0:
                        val = dp[h][i] + 1; pr = h
                dp[i][j] = val; par[i][j] = pr
                if ori(Q[i], Q[j], p) > 0 and val > best:
                    best = val
                    # reconstruct
                    poly = [Q[j], Q[i]]; a, b = i, j
                    while par[a][b] >= 0:
                        h = par[a][b]; poly.append(Q[h]); a, b = h, a
                    poly.append(p); bestpoly = poly[::-1]
    print('largest convex subset (DP):', best, 'witness (0-based rows):', bestpoly)
    # verify witness independently: every 4-subset convex
    if bestpoly:
        def in_tri(a, b, c, x):
            s1, s2, s3 = ori(a, b, x), ori(b, c, x), ori(c, a, x)
            return s1 == s2 == s3
        okw = all(not in_tri(*[q for q in quad if q != x], x) for quad in itertools.combinations(bestpoly, 4) for x in quad)
        print('witness in convex position (4-point test):', okw)
    if tabout:
        with open(tabout, 'w') as f:
            f.write('%d\n' % n)
            f.write(''.join('+' if O[t] > 0 else '-' for t in itertools.combinations(range(n), 3)))
            f.write('\n')
        print('wrote orientation table', tabout)

if __name__ == '__main__':
    main()
