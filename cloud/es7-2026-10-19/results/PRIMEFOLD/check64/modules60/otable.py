#!/usr/bin/env python3
"""Exact orientation table of a Z[zeta_7] point file (own code, z7.py), plus an independent numeric cross-check:
coordinates from a Decimal Taylor-series evaluation of cos/sin(2 pi j/7) (pi by Machin's formula) at PREC digits,
with an explicit error bound.  Writes OUT.npyless binary: header 'OTV n\n' then n^3 signed bytes (index (a*n+b)*n+c).
Usage: otable.py PTS OUT"""
import sys, hashlib, itertools
from decimal import Decimal, getcontext
sys.path.insert(0, sys.path[0])
import z7

PREC = 120


def dec_pi():
    getcontext().prec = PREC + 20
    def arctan_inv(x):  # arctan(1/x)
        x = Decimal(x)
        x2 = x * x
        term = 1 / x
        s = term
        k = 1
        while True:
            term = -term / x2
            t = term / (2 * k + 1)
            if abs(t) < Decimal(10) ** (-(PREC + 15)):
                break
            s += t
            k += 1
        return s
    return 4 * (4 * arctan_inv(5) - arctan_inv(239))


def dec_cos_sin(theta):
    getcontext().prec = PREC + 20
    c = Decimal(0); s = Decimal(0)
    term = Decimal(1)  # theta^k / k!
    k = 0
    eps = Decimal(10) ** (-(PREC + 15))
    while True:
        if k % 4 == 0: c += term
        elif k % 4 == 1: s += term
        elif k % 4 == 2: c -= term
        else: s -= term
        k += 1
        term = term * theta / k
        if abs(term) < eps and k > 10:
            break
    return c, s


def main():
    rows = z7.read_pts(sys.argv[1])
    n = len(rows)
    # exact table
    T = bytearray(n * n * n)
    zeros = 0
    for a, b, c in itertools.combinations(range(n), 3):
        s = z7.orient(rows[a], rows[b], rows[c])
        if s == 0:
            zeros += 1
        for (x, y, z), sg in (((a, b, c), s), ((b, c, a), s), ((c, a, b), s), ((b, a, c), -s), ((a, c, b), -s), ((c, b, a), -s)):
            T[(x * n + y) * n + z] = sg & 0xff
    with open(sys.argv[2], 'wb') as f:
        f.write(b'OTV %d\n' % n)
        f.write(bytes(T))
    print('n=%d exact zero orientations: %d' % (n, zeros))
    print('sha256(table bytes) = %s' % hashlib.sha256(bytes(T)).hexdigest())
    # numeric cross-check
    pi = dec_pi()
    cs = [dec_cos_sin(2 * pi * j / 7) for j in range(7)]
    X = [sum(Decimal(w[j]) * cs[j][0] for j in range(7)) for w in rows]
    Y = [sum(Decimal(w[j]) * cs[j][1] for j in range(7)) for w in rows]
    W = max(max(abs(v) for v in w) for w in rows)
    # coordinates have absolute error <= 7 * W * 10^-(PREC+10) (generous); |coord| <= 7W
    ecoord = Decimal(7 * W) * Decimal(10) ** (-(PREC + 10))
    R = Decimal(7 * W)
    # det = (bx-ax)(cy-ay) - (by-ay)(cx-ax): |error| <= 2 * [2R * 2e * 2 + (2e)^2 * ...] ; bound 32 R e
    edet = 32 * (2 * R) * ecoord + 64 * ecoord * ecoord
    mism = 0; mindet = None
    for a, b, c in itertools.combinations(range(n), 3):
        d = (X[b] - X[a]) * (Y[c] - Y[a]) - (Y[b] - Y[a]) * (X[c] - X[a])
        if mindet is None or abs(d) < mindet:
            mindet = abs(d)
        if abs(d) <= edet:
            mism += 1
            continue
        s = 1 if d > 0 else -1
        t = T[(a * n + b) * n + c]
        t = t - 256 if t > 127 else t
        if s != t:
            mism += 1
    print('decimal cross-check (%d digits): mismatches/undecided = %d ; min |det| = %.4E ; error bound = %.3E' % (PREC, mism, mindet, edet))


if __name__ == '__main__':
    main()
