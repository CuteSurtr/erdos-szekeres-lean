#!/usr/bin/env python3
"""Exact check of the C3 / projective-map identities in Q(sqrt 3).

Each sample: random Eisenstein lattice points z = a + b*w (w = e^{2 pi i/3}), Cartesian
(a - b/2, b*sqrt3/2), and their images under the Euclidean rotation R by +120 degrees about
the origin (exact: w*z).  All arithmetic is in Q(sqrt 3) (pairs of Fractions, exact sign test).
The line l is the true y-axis.  Optionally the set is first rotated by a random exact angle
whose cos/sin lie in Q(sqrt3) (rotation by 15*j degrees composed with a rational Pythagorean
rotation) so that l is in a generic position relative to the lattice.

Checked identities (n = 3m points, labels 0..n-1 by increasing y/x):
  I1  R(i) = (i - m) mod n
  I2  chi_S(i,j,k) = chi'(i,j,k) * (-1)^(s_i+s_j+s_k), chi' = orientation of phi(S), phi(x,y) = (y/x, 1/x)
  I3  chi'(Ri,Rj,Rk) = chi'(i,j,k) * e_i e_j e_k, e_i = +1 if i < m else -1
  I4  s_{Ri} = s_i XOR [i >= m]          (s_i = [x_i < 0])
  I5  for i < j: i precedes j in the x-order of S  iff  inv_ij XOR s_i XOR s_j,  inv_ij = [Y'_i > Y'_j]
  I6  per triple i<j<k: inv on (ij,ik,jk) is a prefix of (ij,ik,jk) if chi'(ijk)=+, of (jk,ik,ij) if -
  I7  s_i = 0, s_j = 1 (i<j)  =>  inv_ij = 1 ;  s_i = 1, s_j = 0  =>  inv_ij = 0
  I8  phi(S) has distinct X' (labels well defined) and the centre facts chi_S(c, a, Ra) = +
  I9  the point reflection -S is C3-symmetric with the same labels and all s flipped, same chi_S
usage: identities.py [samples] [seed]
"""
import random
import sys
from fractions import Fraction as F


class Q3:
    """a + b*sqrt(3), a,b rational"""
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(s, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return Q3(s.a + o.a, s.b + o.b)

    def __sub__(s, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return Q3(s.a - o.a, s.b - o.b)

    def __neg__(s):
        return Q3(-s.a, -s.b)

    def __mul__(s, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return Q3(s.a * o.a + 3 * s.b * o.b, s.a * o.b + s.b * o.a)

    def inv(s):
        d = s.a * s.a - 3 * s.b * s.b
        assert d != 0
        return Q3(s.a / d, -s.b / d)

    def __truediv__(s, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return s * o.inv()

    def sign(s):
        sa = (s.a > 0) - (s.a < 0)
        sb = (s.b > 0) - (s.b < 0)
        if sa == sb or sb == 0:
            return sa
        if sa == 0:
            return sb
        # opposite signs: compare a^2 with 3 b^2
        d = s.a * s.a - 3 * s.b * s.b
        return sa if d > 0 else (sb if d < 0 else 0)


S3 = Q3(0, 1)
HALF = F(1, 2)


def orient(p, q, r):
    return ((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])).sign()


def rotate(p, c, s):
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def random_set(m, rng, R=30):
    pts = []
    while len(pts) < m:
        a, b = rng.randint(-R, R), rng.randint(-R, R)
        if (a, b) != (0, 0):
            pts.append((a, b))
    orbit = []
    for a, b in pts:
        z = (a, b)
        for _ in range(3):
            orbit.append(z)
            z = (-z[1], z[0] - z[1])           # multiplication by w
    cart = [(Q3(a - F(b, 2)), Q3(0, F(b, 2))) for a, b in orbit]
    # generic exact rotation: Pythagorean (u^2-v^2, 2uv)/(u^2+v^2) times 15j degrees
    u, v = rng.randint(1, 9), rng.randint(1, 9)
    h = u * u + v * v
    c1, s1 = Q3(F(u * u - v * v, h)), Q3(F(2 * u * v, h))
    j = rng.randrange(24)
    # cos/sin of 15 j degrees in Q(sqrt3)? only multiples of 30 are; use 30*j
    import math
    tab = {0: (Q3(1), Q3(0)), 30: (Q3(0, HALF), Q3(HALF)), 60: (Q3(HALF), Q3(0, HALF)),
           90: (Q3(0), Q3(1))}
    ang = (30 * j) % 360
    q, r = divmod(ang, 90)
    c2, s2 = tab[r]
    for _ in range(q):                       # rotate by 90 q
        c2, s2 = -s2, c2
    cart = [rotate(rotate(p, c1, s1), c2, s2) for p in cart]
    return cart          # cart[3o + t] = R^t(cart[3o])


def check(m, rng):
    n = 3 * m
    P = random_set(m, rng)
    O = (Q3(0), Q3(0))
    # genericity
    for p in P:
        if p[0].sign() == 0:
            return None
    for i in range(n):
        for j in range(i + 1, n):
            if orient(O, P[i], P[j]) == 0:
                return None
            if P[i][0] .sign() * 0 == 1:
                pass
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if orient(P[i], P[j], P[k]) == 0:
                    return None
    # x-coordinates distinct (for the x-order)
    xs = [p[0] for p in P]
    for i in range(n):
        for j in range(i + 1, n):
            if (xs[i] - xs[j]).sign() == 0:
                return None
    slope = [p[1] / p[0] for p in P]
    import functools
    order = sorted(range(n), key=functools.cmp_to_key(lambda i, j: (slope[i] - slope[j]).sign()))
    lab = {orig: L for L, orig in enumerate(order)}
    pts = [P[o] for o in order]                          # by label
    Rmap = [lab[3 * (o // 3) + (o % 3 + 1) % 3] for o in order]   # label -> label of R(point)
    phi = [(slope[o], Q3(1) / P[o][0]) for o in order]
    s = [1 if p[0].sign() < 0 else 0 for p in pts]
    e = [1 if i < m else -1 for i in range(n)]
    bad = []
    for i in range(n):
        if Rmap[i] != (i - m) % n:
            bad.append(("I1", i))
        if s[Rmap[i]] != s[i] ^ (1 if i >= m else 0):
            bad.append(("I4", i))
        if orient(O, pts[i], pts[Rmap[i]]) != 1:
            bad.append(("I8c", i))
    for i in range(n - 1):
        if (phi[i + 1][0] - phi[i][0]).sign() <= 0:
            bad.append(("I8", i))
    chiS = lambda i, j, k: orient(pts[i], pts[j], pts[k])
    chip = lambda i, j, k: orient(phi[i], phi[j], phi[k])
    inv = {}
    for i in range(n):
        for j in range(i + 1, n):
            inv[i, j] = 1 if (phi[i][1] - phi[j][1]).sign() > 0 else 0
            prec = 1 if (pts[i][0] - pts[j][0]).sign() < 0 else 0
            if prec != inv[i, j] ^ s[i] ^ s[j]:
                bad.append(("I5", i, j))
            if s[i] == 0 and s[j] == 1 and inv[i, j] != 1:
                bad.append(("I7", i, j))
            if s[i] == 1 and s[j] == 0 and inv[i, j] != 0:
                bad.append(("I7", i, j))
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                cp = chip(i, j, k)
                if chiS(i, j, k) != cp * (-1) ** (s[i] + s[j] + s[k]):
                    bad.append(("I2", i, j, k))
                if chip(Rmap[i], Rmap[j], Rmap[k]) != cp * e[i] * e[j] * e[k]:
                    bad.append(("I3", i, j, k))
                seq = [inv[i, j], inv[i, k], inv[j, k]] if cp > 0 else [inv[j, k], inv[i, k], inv[i, j]]
                if seq not in ([0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]):
                    bad.append(("I6", i, j, k))
    # I9: point reflection
    neg = [(-p[0], -p[1]) for p in pts]
    for i in range(n - 1):
        if ((neg[i + 1][1] / neg[i + 1][0]) - (neg[i][1] / neg[i][0])).sign() <= 0:
            bad.append(("I9lab", i))
    for i, j, k in [(0, 1, 2), (0, m, 2 * m), (1, n - 2, n - 1)]:
        if orient(neg[i], neg[j], neg[k]) != chiS(i, j, k):
            bad.append(("I9chi", i, j, k))
    return bad


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    done = 0
    nbad = 0
    per_m = {}
    while done < N:
        m = 3 + done % 9
        b = check(m, rng)
        if b is None:
            continue
        done += 1
        per_m[m] = per_m.get(m, 0) + 1
        if b:
            nbad += 1
            print("FAIL m=%d" % m, b[:10])
    print("samples", done, "per_m", per_m, "failures", nbad)
    sys.exit(1 if nbad else 0)


if __name__ == "__main__":
    main()
