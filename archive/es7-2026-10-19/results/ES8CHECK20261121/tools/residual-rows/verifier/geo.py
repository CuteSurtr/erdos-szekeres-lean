"""Exact-integer residual geometry, written independently for the verify-residual-row check (21 Nov 2026).

Conventions (math.md 2.1-2.2, ResidualRanks.labels, ResidualStates.column):
  orient(a,b,c) = det(b-a, c-a); for a_x<b_x<c_x, > 0 is a cup triple, < 0 a cap triple.
  Ep[u][v]  = longest cup ending with the exact pair (u,v)   (E+)
  Em[u][v]  = longest cap ending with the exact pair (u,v)   (E-)
  Fm[u][v]  = longest cap starting with the exact pair (u,v) (F-)
  Fp[u][v]  = longest cup starting with the exact pair (u,v)
  residual label d(u,v) = (6 - Fm[u][v], Ep[u][v] - 1)
  state f_a(v) = max{ d2(u,v) : u<v, d1(u,v) >= a }  (0 if empty), a = 1..4
All predicates use Python integers only.
"""
from math import gcd


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def otable(P):
    n = len(P)
    for i in range(n - 1):
        if not P[i][0] < P[i + 1][0]:
            raise ValueError('x not strictly increasing')
    O = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                s = orient(P[i], P[j], P[k])
                if s == 0:
                    raise ValueError('collinear triple')
                O[i][j][k] = 1 if s > 0 else -1
    return O


def ranks(O, n):
    Ep = [[0] * n for _ in range(n)]
    Em = [[0] * n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            bp = 2
            bm = 2
            for t in range(u):
                if O[t][u][v] > 0:
                    if Ep[t][u] + 1 > bp:
                        bp = Ep[t][u] + 1
                else:
                    if Em[t][u] + 1 > bm:
                        bm = Em[t][u] + 1
            Ep[u][v] = bp
            Em[u][v] = bm
    Fp = [[0] * n for _ in range(n)]
    Fm = [[0] * n for _ in range(n)]
    for u in range(n - 1, -1, -1):
        for v in range(u + 1, n):
            bp = 2
            bm = 2
            for w in range(v + 1, n):
                if O[u][v][w] > 0:
                    if Fp[v][w] + 1 > bp:
                        bp = Fp[v][w] + 1
                else:
                    if Fm[v][w] + 1 > bm:
                        bm = Fm[v][w] + 1
            Fp[u][v] = bp
            Fm[u][v] = bm
    return Ep, Em, Fp, Fm


def max_gon(O, n):
    """Largest convex polygon: max over i<j of maxcap(i->j) + maxcup(i->j) - 2 (chains with first i, last j)."""
    if n <= 2:
        return n
    best = 2
    NEG = -10 ** 9
    for i in range(n):
        capi = {}
        cupi = {}
        for v in range(i + 1, n):
            mc = 2
            mu = 2
            capi[(i, v)] = 2
            cupi[(i, v)] = 2
            for u in range(i + 1, v):
                bc = NEG
                bu = NEG
                for t in range(i, u):
                    s = O[t][u][v]
                    if s < 0:
                        c = capi.get((t, u), NEG)
                        if c + 1 > bc:
                            bc = c + 1
                    else:
                        c = cupi.get((t, u), NEG)
                        if c + 1 > bu:
                            bu = c + 1
                if bc > 0:
                    capi[(u, v)] = bc
                    if bc > mc:
                        mc = bc
                if bu > 0:
                    cupi[(u, v)] = bu
                    if bu > mu:
                        mu = bu
            if mc + mu - 2 > best:
                best = mc + mu - 2
    return best


class Conf:
    def __init__(self, P):
        self.P = list(P)
        self.n = n = len(P)
        self.O = otable(self.P)
        self.Ep, self.Em, self.Fp, self.Fm = ranks(self.O, n)
        Ep, Em, Fp, Fm = self.Ep, self.Em, self.Fp, self.Fm
        self.cupEnd = [max([1] + [Ep[u][v] for u in range(v)]) for v in range(n)]
        self.capEnd = [max([1] + [Em[u][v] for u in range(v)]) for v in range(n)]
        self.cupStart = [max([1] + [Fp[v][w] for w in range(v + 1, n)]) for v in range(n)]
        self.capStart = [max([1] + [Fm[v][w] for w in range(v + 1, n)]) for v in range(n)]
        self.longcup = max(self.cupEnd) if n else 0
        self.longcap = max(self.capEnd) if n else 0
        self._gon = None

    def gon(self):
        if self._gon is None:
            self._gon = max_gon(self.O, self.n)
        return self._gon

    def junction(self):
        return any(self.cupEnd[v] >= 6 and self.capStart[v] >= 5 for v in range(self.n))

    def residual(self):
        return self.longcap <= 5 and not self.junction() and self.gon() <= 7

    def label(self, u, v):
        return (6 - self.Fm[u][v], self.Ep[u][v] - 1)

    def states(self):
        n = self.n
        S = []
        for v in range(n):
            f = [0, 0, 0, 0]
            for u in range(v):
                d1, d2 = self.label(u, v)
                for a in range(1, 5):
                    if d1 >= a and d2 > f[a - 1]:
                        f[a - 1] = d2
            S.append(tuple(f))
        return S


def sub(P, idx):
    return [P[i] for i in sorted(idx)]


def rat_points_to_int(pts):
    """pts: list of (p/q strings); returns integer points scaled by the common denominator (exact)."""
    from fractions import Fraction
    F = [(Fraction(x), Fraction(y)) for x, y in pts]
    L = 1
    for x, y in F:
        for z in (x, y):
            L = L * z.denominator // gcd(L, z.denominator)
    return [(int(x * L), int(y * L)) for x, y in F]
