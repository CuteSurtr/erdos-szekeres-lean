#!/usr/bin/env python3
"""Round a float 8-fold layered configuration (lr, th per layer) to integer Z[zeta_8] seeds w0 + w1 zeta
(zeta = e^{2 pi i/8}) and write the PRIMEFOLD .pts format: 8 integers per row, row 8o+k = zeta^k * seed_o
(cyclic shift, zeta^8 = 1), layers outermost first.  The exact checks are done separately on the .pts file.
usage: cand2pts.py CAND.json OUT.pts [MIN_INNER_COEFF=1e9]"""
import sys, json, math
from decimal import Decimal, getcontext
getcontext().prec = 60
d = json.load(open(sys.argv[1]))
lr = d['lr']; th = d['th']
mn = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
o = sorted(range(len(lr)), key=lambda i: -lr[i])
lmin = min(lr)
scale = mn / math.exp(lmin)
rows = []
for i in o:
    r = Decimal(scale) * Decimal(math.exp(lr[i] - 0.0))
    x = r * Decimal(math.cos(th[i])); y = r * Decimal(math.sin(th[i]))
    s2 = Decimal(2).sqrt()
    w1 = int((y * s2).to_integral_value())
    w0 = int((x - y).to_integral_value())
    seed = [w0, w1, 0, 0, 0, 0, 0, 0]
    for k in range(8):
        rows.append(seed[8 - k:] + seed[:8 - k])
with open(sys.argv[2], 'w') as f:
    f.write('# m=8 C=0 n=%d layers=%d ; point = sum_j w_j zeta^j, zeta = e^(2 pi i/8); layer o = rows o*m..o*m+m-1 '
            '(outermost first); rounded from %s\n' % (len(rows), len(o), sys.argv[1].split('/')[-1]))
    for r in rows:
        f.write(' '.join(map(str, r)) + '\n')
print('wrote', sys.argv[2], len(rows), 'points, max coeff', max(abs(x) for r in rows for x in r))
