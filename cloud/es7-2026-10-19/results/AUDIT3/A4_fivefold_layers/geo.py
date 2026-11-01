#!/usr/bin/env python3
"""Exact plane geometry for m-fold symmetric configurations (written for audit A4, independent of project code).

Rings:
  m = 4 : Gaussian integers, points (x, y) with integer x, y; rotation by +90 deg: (x, y) -> (-y, x).
  m = 5 : Z[zeta5], zeta = exp(2 pi i / 5); an element is a 5-tuple (b0..b4) meaning sum b_k zeta^k
          (redundant since 1 + zeta + ... + zeta^4 = 0; normalised so that b4 = 0); rotation by +72 deg = * zeta.
Exact signs:  sin(144)/sin(72) = 2 cos(72) = (sqrt5 - 1)/2,  cos(72) = (sqrt5 - 1)/4,  cos(144) = -(sqrt5 + 1)/4,
so Im z and Re z are positive multiples of A + B sqrt5 with integer A, B, whose sign is decided exactly.
Orientation chi(p, q, r) = sign det(q - p, r - p) = sign Im(conj(q - p) (r - p)).
"""
import cmath, math


def sign_ab5(A, B):
    """exact sign of A + B*sqrt(5) for integers A, B"""
    if A >= 0 and B >= 0:
        return 0 if (A == 0 and B == 0) else 1
    if A <= 0 and B <= 0:
        return -1
    d = A * A - 5 * B * B          # never 0 here (sqrt5 irrational, A, B nonzero of opposite signs)
    assert d != 0
    if A > 0:                      # A > 0 > B
        return 1 if d > 0 else -1
    return -1 if d > 0 else 1      # A < 0 < B


class Z5:
    m = 5
    zero = (0, 0, 0, 0, 0)

    @staticmethod
    def norm(b):
        return tuple(x - b[4] for x in b)

    @staticmethod
    def add(p, q):
        return Z5.norm(tuple(x + y for x, y in zip(p, q)))

    @staticmethod
    def sub(p, q):
        return Z5.norm(tuple(x - y for x, y in zip(p, q)))

    @staticmethod
    def mul(p, q):
        c = [0] * 5
        for i in range(5):
            if p[i]:
                for j in range(5):
                    c[(i + j) % 5] += p[i] * q[j]
        return Z5.norm(tuple(c))

    @staticmethod
    def conj(p):
        return Z5.norm((p[0], p[4], p[3], p[2], p[1]))

    @staticmethod
    def rot(p, k=1):
        k %= 5
        return Z5.norm(tuple(p[(i - k) % 5] for i in range(5)))

    @staticmethod
    def im_sign(z):
        b = z
        return sign_ab5(2 * (b[1] - b[4]) - (b[2] - b[3]), b[2] - b[3])

    @staticmethod
    def re_sign(z):
        b = z
        return sign_ab5(4 * b[0] - b[1] - b[4] - b[2] - b[3], b[1] + b[4] - b[2] - b[3])

    @staticmethod
    def orient(p, q, r):
        return Z5.im_sign(Z5.mul(Z5.conj(Z5.sub(q, p)), Z5.sub(r, p)))

    @staticmethod
    def to_complex(p):
        w = cmath.exp(2j * math.pi / 5)
        return sum(p[k] * w ** k for k in range(5))

    @staticmethod
    def from_complex(z, scale):
        """an element close to scale*z (error O(1) in coefficient units), with two random-ish free coefficients"""
        w = cmath.exp(2j * math.pi / 5)
        z = z * scale
        a1 = round(z.imag / math.sin(2 * math.pi / 5))
        a0 = round(z.real - a1 * math.cos(2 * math.pi / 5))
        return Z5.norm((a0, a1, 0, 0, 0))

    @staticmethod
    def less_yx(p, q):
        """exact lexicographic (y, x) comparison p < q"""
        d = Z5.sub(p, q)
        s = Z5.im_sign(d)
        if s:
            return s < 0
        return Z5.re_sign(d) < 0


class Z4:
    m = 4
    zero = (0, 0)

    @staticmethod
    def sub(p, q):
        return (p[0] - q[0], p[1] - q[1])

    @staticmethod
    def rot(p, k=1):
        k %= 4
        x, y = p
        for _ in range(k):
            x, y = -y, x
        return (x, y)

    @staticmethod
    def orient(p, q, r):
        d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (d > 0) - (d < 0)

    @staticmethod
    def to_complex(p):
        return complex(p[0], p[1])

    @staticmethod
    def from_complex(z, scale):
        return (round(z.real * scale), round(z.imag * scale))

    @staticmethod
    def less_yx(p, q):
        return (p[1], p[0]) < (q[1], q[0])


RING = {4: Z4, 5: Z5}


def orbit(ring, p):
    return [ring.rot(p, k) for k in range(ring.m)]


class Config:
    """points = list of orbits (each a list of m points, orbit[r] = R^r orbit[0]); centre = ring.zero (not a set point)"""

    def __init__(self, ring, reps):
        self.ring = ring
        self.m = ring.m
        self.orbits = [orbit(ring, p) for p in reps]
        self.pts = [q for o in self.orbits for q in o]
        self.n = len(self.pts)
        self._chi = {}

    def chi(self, i, j, k):
        """orientation of set points with indices i, j, k (index = position in self.pts); exact, cached"""
        key = (i, j, k)
        v = self._chi.get(key)
        if v is None:
            v = self.ring.orient(self.pts[i], self.pts[j], self.pts[k])
            self._chi[key] = v
        return v

    def general_position(self):
        n = self.n
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if self.chi(i, j, k) == 0:
                        return False
        return True

    def centre_general(self):
        """odd m only: the centre is not on any line through two set points"""
        c = self.ring.zero
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.ring.orient(c, self.pts[i], self.pts[j]) == 0:
                    return False
        return True


def extreme_points(cfg, idx):
    """indices in idx that are vertices of conv(points idx) (general position assumed): p is a vertex iff some
    other point q has every remaining point strictly on one side of the line pq"""
    idx = list(idx)
    if len(idx) <= 2:
        return list(idx)
    V = []
    for p in idx:
        ok = False
        for q in idx:
            if q == p:
                continue
            sides = {cfg.chi(p, q, r) for r in idx if r != p and r != q}
            if len(sides) == 1:
                ok = True
                break
        if ok:
            V.append(p)
    return V


def convex_layers(cfg):
    rest = list(range(cfg.n))
    layers = []
    while rest:
        V = extreme_points(cfg, rest)
        layers.append(sorted(V))
        rest = [x for x in rest if x not in V]
    return layers


def convex_counts(cfg, kmax=8):
    """exact numbers of k-subsets in convex position, k = 3..kmax, by the lowest-vertex angular DP
    (independent of the 4-point criterion). Returns dict k -> count, and the size of a largest convex subset."""
    ring, P, n = cfg.ring, cfg.pts, cfg.n
    counts = {k: 0 for k in range(3, kmax + 1)}
    best = 2 if n >= 2 else n
    for b in range(n):
        U = [u for u in range(n) if u != b and ring.less_yx(P[b], P[u])]
        # sort U counter-clockwise around b (all in the upper half-plane at b, so chi(b,u,v) is a total order)
        import functools
        U.sort(key=functools.cmp_to_key(lambda u, v: -1 if cfg.chi(b, u, v) > 0 else 1))
        L = len(U)
        # cnt[i][j][k]: number of convex chains b -> ... -> U[i] -> U[j] with k vertices, all left turns so far
        cnt = [[None] * L for _ in range(L)]
        mx = [[0] * L for _ in range(L)]
        for j in range(L):
            for i in range(j):
                c = [0] * (kmax + 2)
                c[3] = 1                         # chain b, U[i], U[j]  (chi(b,U[i],U[j]) > 0 by the order)
                m_ = 3
                for h in range(i):
                    if cfg.chi(U[h], U[i], U[j]) > 0:
                        ch = cnt[h][i]
                        for k in range(3, kmax + 1):
                            if ch[k]:
                                c[k + 1] += ch[k]
                        m_ = max(m_, mx[h][i] + 1)
                cnt[i][j] = c
                mx[i][j] = m_
        for j in range(L):
            for i in range(j):
                if cfg.chi(U[i], U[j], b) > 0:   # closing turn at U[j]
                    c = cnt[i][j]
                    for k in range(3, kmax + 1):
                        counts[k] += c[k]
                    best = max(best, mx[i][j])
    return counts, best


if __name__ == "__main__":
    # self-test of the exact predicates against floating point on random inputs
    import random
    rnd = random.Random(12345)
    bad = 0
    for trial in range(20000):
        p = tuple(rnd.randint(-50, 50) for _ in range(4)) + (0,)
        q = tuple(rnd.randint(-50, 50) for _ in range(4)) + (0,)
        r = tuple(rnd.randint(-50, 50) for _ in range(4)) + (0,)
        s = Z5.orient(p, q, r)
        a, b_, c = Z5.to_complex(p), Z5.to_complex(q), Z5.to_complex(r)
        d = ((b_ - a).conjugate() * (c - a)).imag
        if abs(d) > 1e-6 and (d > 0) != (s > 0):
            bad += 1
        z = Z5.sub(p, q)
        zc = Z5.to_complex(z)
        if abs(zc.imag) > 1e-6 and (zc.imag > 0) != (Z5.im_sign(z) > 0):
            bad += 1
        if abs(zc.real) > 1e-6 and (zc.real > 0) != (Z5.re_sign(z) > 0):
            bad += 1
        # rotation is multiplication by zeta
        if abs(Z5.to_complex(Z5.rot(p)) - Z5.to_complex(p) * cmath.exp(2j * math.pi / 5)) > 1e-6:
            bad += 1
        # multiplication and conjugation
        if abs(Z5.to_complex(Z5.mul(p, q)) - Z5.to_complex(p) * Z5.to_complex(q)) > 1e-6 * (1 + abs(Z5.to_complex(p) * Z5.to_complex(q))):
            bad += 1
        if abs(Z5.to_complex(Z5.conj(p)) - Z5.to_complex(p).conjugate()) > 1e-6:
            bad += 1
    # exact zero detection: collinear triples p, q, p + t (q - p)
    for trial in range(2000):
        p = tuple(rnd.randint(-50, 50) for _ in range(4)) + (0,)
        q = tuple(rnd.randint(-50, 50) for _ in range(4)) + (0,)
        t = rnd.randint(-5, 5)
        r = Z5.add(p, tuple(t * x for x in Z5.sub(q, p)))
        if Z5.orient(p, q, r) != 0:
            bad += 1
        # rotations preserve orientation
        if p != q and Z5.orient(p, q, Z5.zero) != Z5.orient(Z5.rot(p), Z5.rot(q), Z5.zero):
            bad += 1
    print("geo self-test mismatches:", bad)
