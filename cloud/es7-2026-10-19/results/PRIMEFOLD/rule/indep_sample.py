#!/usr/bin/env python3
"""Independent check of a sample of orientation signs written by sym_cvx (SAMPLE_OUT): recompute each sign from the
points file with 120-digit Decimal arithmetic (no shared code with sym_cvx.c). Point index = layer*p + k is
rep_layer * zeta^k; the centre is index p*t.  usage: indep_sample.py points sample"""
import sys
from decimal import Decimal, getcontext
getcontext().prec = 120
def pi():
    getcontext().prec += 2
    three = Decimal(3); lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s; n, na = n + na, na + 8; d, da = d + da, da + 32; t = (t * n) / d; s += t
    getcontext().prec -= 2
    return +s
def cs(x):
    getcontext().prec += 2
    c = s = Decimal(0); term = Decimal(1); i = 0
    while True:
        if i % 4 == 0: c += term
        elif i % 4 == 1: s += term
        elif i % 4 == 2: c -= term
        else: s -= term
        i += 1; term = term * x / i
        if abs(term) < Decimal(10) ** -130: break
    getcontext().prec -= 2
    return +c, +s
lines = [l for l in open(sys.argv[1]) if not l.startswith('#') and l.strip()]
p, t, C = map(int, lines[0].split())
reps = [list(map(int, l.split())) for l in lines[1:1 + t]]
PI = pi()
Z = [cs(2 * PI * j / p) for j in range(p)]
coords = {}
def pt(i):
    if i in coords: return coords[i]
    if i == p * t: v = (Decimal(0), Decimal(0))
    else:
        l, k = divmod(i, p)
        w = reps[l]
        x = sum(Decimal(w[j]) * Z[(j + k) % p][0] for j in range(p) if w[j])
        y = sum(Decimal(w[j]) * Z[(j + k) % p][1] for j in range(p) if w[j])
        v = (x, y)
    coords[i] = v
    return v
maxc = max(abs(x) for w in reps for x in w)
err = Decimal(10) ** -110 * Decimal(maxc) ** 2 * 100     # coordinates carry relative error ~1e-118
mism = 0; minabs = None; cnt = 0
for l in open(sys.argv[2]):
    a, b, c, s = map(int, l.split())
    (xa, ya), (xb, yb), (xc, yc) = pt(a), pt(b), pt(c)
    d = (xb - xa) * (yc - ya) - (yb - ya) * (xc - xa)
    sd = 1 if d > err else (-1 if d < -err else 0)
    if sd != s or sd == 0: mism += 1
    if minabs is None or abs(d) < minabs: minabs = abs(d)
    cnt += 1
print('sample size %d, mismatches/undecided %d, min |det| %.3E, error bound %.3E' % (cnt, mism, minabs, err))
print('INDEPENDENT SAMPLE CHECK', 'PASS' if mism == 0 and minabs > 1000 * err else 'FAIL')
