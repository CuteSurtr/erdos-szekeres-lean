#!/usr/bin/env python3
"""Export the extremal needles (3-fold ES profile, 4-fold profile needle4_n10.json) to exact integer point sets with
eps = 2^-S, for the independent verifier of LBK8SYM (tools/verify_indep.py)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from needle_test import es_set
S = int(sys.argv[1]) if len(sys.argv) > 1 else 40
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sets')
E = sorted((x + 1, y) for (x, y) in es_set(4, 5))
# 3-fold: arm point r + eps*y*omega -> oblique (a, b) = (r * 2^S, y); rotation (a, b) -> (-b, a - b); rows 'w0 w1 w2' with
# a = w0 - w2, b = w1 - w2: write (a, b, 0)
rows = []
for (r, y) in E:
    p = (r << S, y)
    for _ in range(3):
        rows.append(p); p = (-p[1], p[0] - p[1])
with open(os.path.join(W, 'needle3_es10_S%d.pts' % S), 'w') as f:
    f.write('# m=3 n=%d 3-fold strict needle, ES profile cup 3 cap 4, eps = 2^-%d\n' % (len(rows), S))
    for (a, b) in rows:
        f.write('%d %d 0\n' % (a, b))
B = [tuple(p) for p in json.load(open(os.path.join(W, 'needle4_n10.json')))]
rows = []
for (r, y) in B:
    p = (r << S, y)
    for _ in range(4):
        rows.append(p); p = (-p[1], p[0])
with open(os.path.join(W, 'needle4_n10_S%d.pts' % S), 'w') as f:
    f.write('# m=4 n=%d 4-fold strict needle, profile needle4_n10.json, eps = 2^-%d\n' % (len(rows), S))
    for (x, y) in rows:
        f.write('%d %d 0 0\n' % (x, y))
print('written')
