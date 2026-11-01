#!/usr/bin/env python3
"""Second, independently derived arithmetic path for ALL orientation signs of the 253-point set:
pi from Machin's formula, cos/sin(2 pi k/9) from Taylor series, 150-digit Decimal coordinates, plain determinant.
Compares every sign with orient_upper.bin (from exact_orient.py); also compares with the explorer's own sampled
signs (p9_sample.txt) and reports the smallest |det| with an explicit error estimate.
usage: decimal_crosscheck.py points.pts outdir_p9 [sample.txt]"""
import sys, os
from decimal import Decimal as D, getcontext
getcontext().prec = 150

def arctan_inv(x):  # arctan(1/x)
    x = D(x); x2 = x * x; term = 1 / x; s = term; k = 1
    eps = D(10) ** (-148)
    while abs(term) > eps:
        term = -term / x2; k += 2; s += term / k
    return s

def taylor_cos_sin(a):
    eps = D(10) ** (-148)
    c = D(0); s = D(0); term = D(1); k = 0
    while True:   # term = a^k/k!
        if k % 4 == 0: c += term
        elif k % 4 == 1: s += term
        elif k % 4 == 2: c -= term
        else: s -= term
        k += 1; term = term * a / k
        if abs(term) < eps and k > 10: break
    return c, s

def main():
    path, d = sys.argv[1], sys.argv[2]
    sample = sys.argv[3] if len(sys.argv) > 3 else None
    lines = [l.split() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    p, t, cflag = map(int, lines[0]); reps = [list(map(int, l)) for l in lines[1:]]
    pi = 16 * arctan_inv(5) - 4 * arctan_inv(239)
    assert str(pi).startswith('3.14159265358979323846264338327950288419716939937510')
    cs = [taylor_cos_sin(2 * pi * k / p) for k in range(p)]
    pts = []
    for l in range(t):
        for s in range(p):
            v = [reps[l][(j - s) % p] for j in range(p)]
            pts.append((sum(D(v[k]) * cs[k][0] for k in range(p)), sum(D(v[k]) * cs[k][1] for k in range(p))))
    if cflag: pts.append((D(0), D(0)))
    n = len(pts)
    tab = open(os.path.join(d, 'orient_upper.bin'), 'rb').read()
    assert len(tab) == n ** 3
    n2 = n * n
    mism = 0; minabs = None; arg = None
    for i in range(n):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            dxj = pts[j][0] - xi; dyj = pts[j][1] - yi
            base = i * n2 + j * n
            for k in range(j + 1, n):
                det = dxj * (pts[k][1] - yi) - dyj * (pts[k][0] - xi)
                sgn = 1 if det > 0 else (-1 if det < 0 else 0)
                tv = tab[base + k]; ts = 1 if tv == 1 else (-1 if tv == 255 else 0)
                if sgn != ts: mism += 1
                a = abs(det)
                if minabs is None or a < minabs: minabs = a; arg = (i, j, k)
    print('Decimal(150) recomputation of all %d triples: sign mismatches vs exact table = %d' % (n * (n - 1) * (n - 2) // 6, mism))
    print('smallest |det| = %.6E at %s ; coordinate magnitudes <= %.3E ; estimated arithmetic error < 1E-90' % (minabs, arg, max(max(abs(x), abs(y)) for x, y in pts)))
    if sample:
        def ori(a, b, c):
            s = 1
            if a > b: a, b = b, a; s = -s
            if b > c: b, c = c, b; s = -s
            if a > b: a, b = b, a; s = -s
            v = tab[a * n2 + b * n + c]
            return s if v == 1 else (-s if v == 255 else 0)
        cnt = 0; bad = 0
        for line in open(sample):
            a, b, c, sg = map(int, line.split())
            cnt += 1
            if ori(a, b, c) != sg: bad += 1
        print('explorer sample file %s: %d signs, disagreements with my exact table: %d' % (os.path.basename(sample), cnt, bad))

if __name__ == '__main__':
    main()
