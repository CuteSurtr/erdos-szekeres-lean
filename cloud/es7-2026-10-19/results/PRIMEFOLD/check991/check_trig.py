#!/usr/bin/env python3
"""Check the claimant's 2^PREC-scaled sin/cos table against values derived from t = 2cos(2pi/p) (Decimal bisection on
m(x) = x^5+x^4-4x^3-3x^2+3x+1, Chebyshev recursions, Decimal sqrt) at 300 digits; reports max |table - 2^PREC*true|."""
import sys
from decimal import Decimal as Dm, getcontext
getcontext().prec = 300
f = open(sys.argv[1]); p, PREC = map(int, f.readline().split())
rows = [tuple(map(int, f.readline().split())) for _ in range(p)]
assert p == 11
m = [1, 3, -3, -4, 1, 1]
def mv(x):
    s = Dm(0)
    for c in reversed(m): s = s * x + c
    return s
lo, hi = Dm(1), Dm(2); assert mv(lo) < 0 < mv(hi)
for _ in range(1000):
    mid = (lo + hi) / 2
    if mv(mid) < 0: lo = mid
    else: hi = mid
tt = (lo + hi) / 2
V = [Dm(2), tt]; U = [Dm(1), tt]
for k in range(2, p + 1): V.append(tt * V[-1] - V[-2]); U.append(tt * U[-1] - U[-2])
s1 = (1 - tt * tt / 4).sqrt(); sc = Dm(2) ** PREC
mx = Dm(0)
for k in range(p):
    c = V[k] / 2; s = s1 * U[k - 1] if k else Dm(0)
    es = abs(Dm(rows[k][0]) - sc * s); ec = abs(Dm(rows[k][1]) - sc * c)
    mx = max(mx, es, ec)
print('p=%d PREC=%d: max |table entry - 2^PREC * exact| = %.6f (certificate needs < 1)' % (p, PREC, mx))
