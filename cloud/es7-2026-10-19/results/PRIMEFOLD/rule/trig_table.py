#!/usr/bin/env python3
"""Fixed-point tables: round(2^PREC * sin(2 pi j/p)), round(2^PREC * cos(2 pi j/p)), j = 0..p-1, from 200-digit Decimal
arithmetic (pi by the Python-docs recipe, sin/cos by Taylor series). |error| <= 1/2 + 2^PREC * 1e-190 < 1 unit.
usage: trig_table.py p PREC out"""
import sys
from decimal import Decimal, getcontext
getcontext().prec = 200
def pi():
    getcontext().prec += 2
    three = Decimal(3); lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s; n, na = n + na, na + 8; d, da = d + da, da + 32; t = (t * n) / d; s += t
    getcontext().prec -= 2
    return +s
def cos(x):
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
    while s != lasts:
        lasts = s; i += 2; fact *= i * (i - 1); num *= x * x; sign *= -1; s += num / fact * sign
    getcontext().prec -= 2
    return +s
def sin(x):
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    while s != lasts:
        lasts = s; i += 2; fact *= i * (i - 1); num *= x * x; sign *= -1; s += num / fact * sign
    getcontext().prec -= 2
    return +s
p, PREC, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
PI = pi(); sc = Decimal(2) ** PREC
with open(out, 'w') as f:
    f.write('%d %d\n' % (p, PREC))
    for j in range(p):
        x = 2 * PI * j / p
        f.write('%d %d\n' % (int((sin(x) * sc).to_integral_value()), int((cos(x) * sc).to_integral_value())))
print('wrote', out)
