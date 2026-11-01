#!/usr/bin/env python3
"""Independent cross-check of an orientation table: recompute every orientation sign of the points in PREFIX.pts
(integer coefficient vectors in Z[zeta_m]) with 160-digit decimal arithmetic (pi and sin/cos from the recipes in the
Python `decimal` documentation), and compare with PREFIX.orient(.gz).  Also reports the smallest |orientation
determinant| relative to the arithmetic error bound, so that the decimal signs are themselves certain.
usage: crosscheck_decimal.py PREFIX m"""
import sys, gzip
from decimal import Decimal, getcontext
getcontext().prec = 160


def pi():
    getcontext().prec += 2
    three = Decimal(3)
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    getcontext().prec -= 2
    return +s


def cos(x):
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


def sin(x):
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


def main():
    pref, m = sys.argv[1], int(sys.argv[2])
    P = [list(map(int, l.split())) for l in open(pref + '.pts') if l.strip() and not l.startswith('#')]
    n = len(P)
    PI = pi()
    C = [cos(2 * PI * j / m) for j in range(m)]
    S = [sin(2 * PI * j / m) for j in range(m)]
    X = [sum(w[j] * C[j] for j in range(m)) for w in P]
    Y = [sum(w[j] * S[j] for j in range(m)) for w in P]
    try:
        toks = gzip.open(pref + '.orient.gz', 'rt').read().split()
    except FileNotFoundError:
        toks = open(pref + '.orient').read().split()
    assert int(toks[0]) == n
    O = list(map(int, toks[1:]))
    maxc = max(max(abs(x) for x in w) for w in P)
    # error bound: coordinates have relative error ~1e-155; |coord| <= m*maxc; det = (xb-xa)(yc-ya)-(yb-ya)(xc-xa)
    coordmax = Decimal(m * maxc)
    err = Decimal(10) ** -150 * coordmax * coordmax * 16
    mismatches, minabs = 0, None
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if a == b or b == c or a == c:
                    continue
                if not (a < b < c):
                    continue
                d = (X[b] - X[a]) * (Y[c] - Y[a]) - (Y[b] - Y[a]) * (X[c] - X[a])
                if minabs is None or abs(d) < minabs:
                    minabs = abs(d)
                s = 1 if d > err else (-1 if d < -err else 0)
                if s == 0 or s != O[(a * n + b) * n + c]:
                    mismatches += 1
    print('n=%d points; sorted triples checked; mismatches/undecided: %d; min |det| = %.3E; error bound = %.3E'
          % (n, mismatches, minabs, err))
    print('CROSSCHECK', 'PASS' if mismatches == 0 and minabs > 1000 * err else 'FAIL')


if __name__ == '__main__':
    main()
