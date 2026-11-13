#!/usr/bin/env python3
"""Exact arithmetic in Z[zeta_m] (m in {3,4,5,6,7,8}) for m-fold symmetric point sets.

A point is an integer vector w = (w_0, ..., w_{m-1}) meaning sum_j w_j zeta^j, zeta = e^{2 pi i/m}.
Multiplication by zeta (rotation by 2 pi/m) = cyclic shift, exact.

Sign of Im(w), method A (algebraic):  Im(w) = sin(2pi/m) * P(c),  c = 2cos(2pi/m),
    P = sum_{j=1}^{h} (w_j - w_{m-j}) U~_{j-1}(c),  h = floor((m-1)/2),  U~_0 = 1, U~_1 = x, U~_{k+1} = x U~_k - U~_{k-1}
(U~_k(2cos t) = sin((k+1)t)/sin t).  P is reduced modulo the minimal polynomial M of c (degree d), so P(c) = 0 iff
the reduced P is the zero polynomial; otherwise its sign is decided exactly:
    d = 1: c rational;  m = 5: c = (sqrt5 - 1)/2;  m = 8: c = sqrt2  (sign of a + b sqrt q by squaring);
    m = 7: exact rational bracket [lo, hi] of c (bisection on M), refined on demand until |P(lo)| exceeds the
           Lipschitz bound of P on the bracket times its width.
Sign of Re(w): 2 Re(w) = 2 w_0 + sum_{j=1}^{h} (w_j + w_{m-j}) V_j(c) [+ w_{m/2} V_{m/2}(c), m even],
    V_0 = 2, V_1 = x, V_{k+1} = x V_k - V_{k-1}  (V_k(2cos t) = 2cos(kt)).

Method B (independent numerical-rigorous): fixed-point interval arithmetic with 2^-PREC resolution and outward
rounding; enclosures of cos(2 pi/m), sin(2 pi/m) obtained from integer square roots (m = 4, 5, 6, 8, 3) or from
bisection on the minimal polynomial 8x^3 + 4x^2 - 4x - 1 of cos(2pi/7) (m = 7); powers by interval angle addition.
"""
from fractions import Fraction
from math import isqrt
import math

MINPOLY = {3: [1, 1], 4: [0, 1], 5: [-1, 1, 1], 6: [-1, 1], 7: [-1, -2, 1, 1], 8: [-2, 0, 1]}  # low degree first


def _pval(P, x):
    s = 0
    for a in reversed(P):
        s = s * x + a
    return s


def _pmod(P, M):
    P = list(P)
    d = len(M) - 1
    while len(P) > d:
        lead = P.pop()
        if lead:
            k = len(P) - d
            for i in range(d):
                P[k + i] -= lead * M[i]
    return P


def _sign_qirr(a, b, q):
    """exact sign of a + b sqrt(q), q a non-square positive integer, a, b integers (or Fractions)"""
    if a >= 0 and b >= 0:
        return 0 if (a == 0 and b == 0) else 1
    if a <= 0 and b <= 0:
        return -1
    # opposite signs
    s = a * a - q * b * b
    if a > 0:
        return 1 if s > 0 else -1     # s != 0 since sqrt q irrational
    return -1 if s > 0 else 1


class ZM:
    def __init__(self, m):
        assert m in MINPOLY
        self.m = m
        self.M = MINPOLY[m]
        self.d = len(self.M) - 1
        self.h = (m - 1) // 2
        U = [[1], [0, 1]]
        V = [[2], [0, 1]]
        for _ in range(m + 2):
            U.append(self._sub(self._shift(U[-1]), U[-2]))
            V.append(self._sub(self._shift(V[-1]), V[-2]))
        self.U = [_pmod(u, self.M) for u in U]
        self.V = [_pmod(v, self.M) for v in V]
        if m == 7:
            # bracket c = 2cos(2pi/7) ~ 1.2469796
            lo, hi = Fraction(12469, 10000), Fraction(12470, 10000)
            assert _pval(self.M, lo) < 0 < _pval(self.M, hi)
            self.lo, self.hi = lo, hi
            self._refine(200)

    @staticmethod
    def _shift(P):
        return [0] + list(P)

    @staticmethod
    def _sub(A, B):
        n = max(len(A), len(B))
        return [(A[i] if i < len(A) else 0) - (B[i] if i < len(B) else 0) for i in range(n)]

    def _refine(self, steps):
        lo, hi = self.lo, self.hi
        for _ in range(steps):
            mid = (lo + hi) / 2
            v = _pval(self.M, mid)
            if v == 0:
                raise ArithmeticError('rational root?')
            if v < 0:
                lo = mid
            else:
                hi = mid
        self.lo, self.hi = lo, hi

    # ---------- ring operations ----------
    def rot(self, w, k=1):
        m = self.m
        k %= m
        return [w[(j - k) % m] for j in range(m)]

    def sub(self, u, v):
        return [a - b for a, b in zip(u, v)]

    def conj(self, u):
        m = self.m
        return [u[(-j) % m] for j in range(m)]

    def mul(self, u, v):
        m = self.m
        w = [0] * m
        for a in range(m):
            ua = u[a]
            if ua:
                for b in range(m):
                    if v[b]:
                        w[(a + b) % m] += ua * v[b]
        return w

    def canon(self, u):
        """reduce modulo the cyclotomic polynomial Phi_m (unique representative)"""
        phi = {3: [1, 1, 1], 4: [1, 0, 1], 5: [1, 1, 1, 1, 1], 6: [1, -1, 1], 7: [1] * 7, 8: [1, 0, 0, 0, 1]}[self.m]
        r = _pmod(list(u), phi)
        return tuple(r + [0] * (len(phi) - 1 - len(r)))

    # ---------- method A ----------
    def _sign_poly(self, P):
        P = list(P)
        while P and P[-1] == 0:
            P.pop()
        if not P:
            return 0
        m = self.m
        if self.d == 1:
            v = _pval(P, Fraction(-self.M[0]))
            return (v > 0) - (v < 0)
        if m == 8:      # c = sqrt2 : P = a + b c
            a = P[0]; b = P[1] if len(P) > 1 else 0
            return _sign_qirr(a, b, 2)
        if m == 5:      # c = (sqrt5 - 1)/2 : a + b c = (2a - b + b sqrt5)/2
            a = P[0]; b = P[1] if len(P) > 1 else 0
            return _sign_qirr(2 * a - b, b, 5)
        # m == 7: bracket
        while True:
            lo, hi = self.lo, self.hi
            B = max(abs(lo), abs(hi)) + 1
            D = sum(abs(k * a) * B ** (k - 1) for k, a in enumerate(P) if k > 0)
            v = _pval(P, lo)
            if abs(v) > D * (hi - lo):
                return 1 if v > 0 else -1
            self._refine(100)

    def im_poly(self, w):
        m = self.m
        P = [0]
        for j in range(1, self.h + 1):
            cj = w[j] - w[m - j]
            if cj:
                u = self.U[j - 1]
                P = [(P[i] if i < len(P) else 0) + (cj * u[i] if i < len(u) else 0) for i in range(max(len(P), len(u)))]
        return _pmod(P, self.M)

    def re2_poly(self, w):
        m = self.m
        P = [2 * w[0]]
        terms = [(w[j] + w[m - j], self.V[j]) for j in range(1, self.h + 1)]
        if m % 2 == 0:
            terms.append((w[m // 2], self.V[m // 2]))
        for cj, v in terms:
            if cj:
                P = [(P[i] if i < len(P) else 0) + (cj * v[i] if i < len(v) else 0) for i in range(max(len(P), len(v)))]
        return _pmod(P, self.M)

    def sign_im(self, w):
        return self._sign_poly(self.im_poly(w))

    def sign_re(self, w):
        return self._sign_poly(self.re2_poly(w))

    def orient(self, p, q, r):
        return self.sign_im(self.mul(self.conj(self.sub(q, p)), self.sub(r, p)))

    def lexcmp(self, p, q):
        """sign of (Im, Re)(p - q) lexicographically"""
        d = self.sub(p, q)
        s = self.sign_im(d)
        return s if s else self.sign_re(d)

    def r2cmp(self, p, q):
        """sign of |p|^2 - |q|^2"""
        a = self.mul(p, self.conj(p))
        b = self.mul(q, self.conj(q))
        return self.sign_re(self.sub(a, b))

    def to_complex(self, w):
        return sum(a * complex(math.cos(2 * math.pi * j / self.m), math.sin(2 * math.pi * j / self.m)) for j, a in enumerate(w))

    def from_complex_Zzeta(self, z):
        """nearest point of the lattice Z + Z zeta to z"""
        m = self.m
        s, c = math.sin(2 * math.pi / m), math.cos(2 * math.pi / m)
        b = z.imag / s
        a = z.real - b * c
        best = None
        for da in (math.floor(a), math.floor(a) + 1):
            for db in (math.floor(b), math.floor(b) + 1):
                w = [0] * m
                w[0], w[1] = int(da), int(db)
                dd = abs(self.to_complex(w) - z)
                if best is None or dd < best[0]:
                    best = (dd, w)
        return best[1]


# ---------------- method B: fixed-point intervals ----------------
PREC = 300
ONE = 1 << PREC


def _fdiv_floor(a, b):
    return a // b


def _fdiv_ceil(a, b):
    return -((-a) // b)


class IV:
    """interval [lo, hi] * 2^-PREC with integer endpoints"""
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi):
        assert lo <= hi
        self.lo, self.hi = lo, hi

    @staticmethod
    def const(k):
        return IV(k * ONE, k * ONE)

    def __add__(s, o):
        return IV(s.lo + o.lo, s.hi + o.hi)

    def __sub__(s, o):
        return IV(s.lo - o.hi, s.hi - o.lo)

    def __mul__(s, o):
        if isinstance(o, int):
            return IV(s.lo * o, s.hi * o) if o >= 0 else IV(s.hi * o, s.lo * o)
        ps = (s.lo * o.lo, s.lo * o.hi, s.hi * o.lo, s.hi * o.hi)
        return IV(_fdiv_floor(min(ps), ONE), _fdiv_ceil(max(ps), ONE))

    __rmul__ = __mul__

    def sign(self):
        if self.lo > 0:
            return 1
        if self.hi < 0:
            return -1
        return None     # undecided


def _sqrt_iv(num, den):
    """enclosure of sqrt(num/den) (num, den positive integers)"""
    # sqrt(num/den) * 2^PREC = sqrt(num * 4^PREC / den)
    x = num * (ONE * ONE) // den      # floor
    lo = isqrt(x)
    hi = isqrt(-((-num * ONE * ONE) // den)) + 1
    return IV(lo, hi)


def trig_enclosures(m):
    """intervals for cos(2 pi j/m), sin(2 pi j/m), j = 0..m-1 (method B; independent of the class ZM)"""
    if m == 4:
        c1, s1 = IV.const(0), IV.const(1)
    elif m == 8:
        h = _sqrt_iv(1, 2)
        c1, s1 = h, h
    elif m == 6:
        c1 = IV(ONE // 2, ONE // 2)
        s1 = _sqrt_iv(3, 4)
    elif m == 3:
        c1 = IV(-ONE // 2, -ONE // 2)
        s1 = _sqrt_iv(3, 4)
    elif m == 5:
        # cos 72 = (sqrt5 - 1)/4 ; sin 72 = sqrt((5 + sqrt5)/8)
        r5 = _sqrt_iv(5, 1)
        c1 = IV(_fdiv_floor(r5.lo - ONE, 4), _fdiv_ceil(r5.hi - ONE, 4))
        # sin^2 = 1 - cos^2, enclose via (5 + sqrt5)/8 bounds
        lo2 = (5 * ONE + r5.lo) // 8; hi2 = -((-(5 * ONE + r5.hi)) // 8)
        s1 = IV(isqrt(lo2 * ONE), isqrt(hi2 * ONE) + 1)
    elif m == 7:
        # cos(2pi/7) is the root of f(x) = 8x^3 + 4x^2 - 4x - 1 in (0.6234, 0.6235)
        f = lambda x: 8 * x ** 3 + 4 * x ** 2 - 4 * x - 1
        lo, hi = Fraction(6234, 10000), Fraction(6235, 10000)
        assert f(lo) < 0 < f(hi)
        for _ in range(PREC + 10):
            mid = (lo + hi) / 2
            if f(mid) < 0:
                lo = mid
            else:
                hi = mid
        c1 = IV(math.floor(lo * ONE), math.ceil(hi * ONE))
        # sin = sqrt(1 - cos^2) : 1 - hi^2 <= sin^2 <= 1 - lo^2
        a = Fraction(1) - hi * hi; b = Fraction(1) - lo * lo
        s1 = IV(isqrt(math.floor(a * ONE * ONE)), isqrt(math.ceil(b * ONE * ONE)) + 1)
    else:
        raise ValueError(m)
    C = [IV.const(1), c1]
    S = [IV.const(0), s1]
    for j in range(2, m):
        C.append(C[-1] * c1 - S[-1] * s1)
        S.append(S[-1] * c1 + C[-2] * s1)
    return C, S


class IntervalGeom:
    def __init__(self, m):
        self.m = m
        self.C, self.S = trig_enclosures(m)

    def xy(self, w):
        x = IV(0, 0); y = IV(0, 0)
        for j, a in enumerate(w):
            if a:
                x = x + self.C[j] * a
                y = y + self.S[j] * a
        return x, y

    @staticmethod
    def orient_xy(P, Q, R):
        (px, py), (qx, qy), (rx, ry) = P, Q, R
        d = (qx - px) * (ry - py) - (qy - py) * (rx - px)
        return d.sign(), d


def self_test(N=2000):
    import random
    random.seed(7)
    for m in (3, 4, 5, 6, 7, 8):
        Z = ZM(m); G = IntervalGeom(m)
        for _ in range(N):
            p, q, r = [[random.randint(-60, 60) for _ in range(m)] for _ in range(3)]
            zp, zq, zr = Z.to_complex(p), Z.to_complex(q), Z.to_complex(r)
            d = ((zq - zp).conjugate() * (zr - zp)).imag
            sA = Z.orient(p, q, r)
            sB, _ = IntervalGeom.orient_xy(G.xy(p), G.xy(q), G.xy(r))
            if abs(d) > 1e-6:
                assert sA == (1 if d > 0 else -1) == sB, (m, p, q, r, d, sA, sB)
            w = [random.randint(-60, 60) for _ in range(m)]
            zw = Z.to_complex(w)
            if abs(zw.real) > 1e-6:
                assert Z.sign_re(w) == (1 if zw.real > 0 else -1)
            if abs(zw.imag) > 1e-6:
                assert Z.sign_im(w) == (1 if zw.imag > 0 else -1)
            assert Z.canon(Z.rot(w, m)) == Z.canon(w)
            assert abs(Z.to_complex(Z.rot(w)) - zw * complex(math.cos(2 * math.pi / m), math.sin(2 * math.pi / m))) < 1e-6
        assert Z.sign_im([1] * m) == 0 and Z.sign_re([1] * m) == 0
        # exact zeros: a vector that is zero modulo Phi_m
        assert all(v == 0 for v in Z.canon([1] * m))
        # collinear triple: p, 2p, 3p
        p = [random.randint(-9, 9) for _ in range(m)]
        assert Z.orient(p, [2 * a for a in p], [3 * a for a in p]) == 0
    print('zm.py self-test passed')


if __name__ == '__main__':
    self_test()
