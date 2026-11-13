#!/usr/bin/env python3
"""Independent recomputation of all orientation signs of a Z[zeta_m] point file with 110-digit decimals
(own pi via Machin, own Taylor series), compared against an orientation table written by zeta_cert.py.
Error bound: each coordinate error <= sum|w_j| * 1e-100 (trig values accurate to < 1e-100); det error bounded below."""
import sys, itertools
from decimal import Decimal as D, getcontext
getcontext().prec = 120
def arctan_inv(n):
    x = D(1) / n; x2 = x * x; s = x; t = x; k = 1
    while True:
        t *= -x2; k += 2; term = t / k
        if abs(term) < D(10) ** -118: break
        s += term
    return s
PI = 16 * arctan_inv(5) - 4 * arctan_inv(239)
def sincos(a):
    s = D(0); c = D(0); term = D(1); k = 0
    # cos: sum (-1)^k a^(2k)/(2k)!, sin: sum (-1)^k a^(2k+1)/(2k+1)!
    tc = D(1); ts = a; n = 0
    while abs(tc) > D(10) ** -118 or abs(ts) > D(10) ** -118:
        c += tc; s += ts
        tc = -tc * a * a / ((2 * n + 1) * (2 * n + 2))
        ts = -ts * a * a / ((2 * n + 2) * (2 * n + 3))
        n += 1
    return s, c
path, m, tab = sys.argv[1], int(sys.argv[2]), sys.argv[3]
rows = [[int(t) for t in l.split()] for l in open(path) if l.strip() and not l.startswith('#')]
SC = [sincos(2 * PI * j / m) for j in range(m)]
P = [(sum(w[j] * SC[j][1] for j in range(m)), sum(w[j] * SC[j][0] for j in range(m))) for w in rows]
n = len(P)
lines = open(tab).read().split()
assert int(lines[0]) == n
signs = lines[1]
maxw = max(sum(abs(x) for x in w) for w in rows)
err_coord = D(maxw) * D(10) ** -100
mind = None; bad = 0
for idx, (i, j, k) in enumerate(itertools.combinations(range(n), 3)):
    (ax, ay), (bx, by), (cx, cy) = P[i], P[j], P[k]
    det = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    s = '+' if det > 0 else '-'
    if s != signs[idx]: bad += 1
    if mind is None or abs(det) < mind: mind = abs(det)
coordmax = max(max(abs(x), abs(y)) for x, y in P)
err_det = 8 * coordmax * err_coord * 2 + D(10) ** -90
print('n=%d triples=%d sign disagreements=%d  min|det|=%.3E  det error bound=%.3E  -> %s' % (
    n, n * (n - 1) * (n - 2) // 6, bad, mind, err_det, 'CONFIRMED' if bad == 0 and mind > err_det else 'NOT confirmed'))
