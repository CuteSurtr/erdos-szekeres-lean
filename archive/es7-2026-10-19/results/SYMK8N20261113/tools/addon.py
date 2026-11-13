#!/usr/bin/env python3
"""Add-on layers: a 4-fold set split into bundles at infinitesimal gaps; try adding one extra square at a new outer
scale (exponent -1) or a new inner scale (exponent max+1), rotated by 2*atan(k/Q), k = 1..Q-1 (angle in (0, 90 deg)).
usage: addon.py FILE.pts cuts(e.g. 1,12) where(outer|inner) Q"""
import sys, math
sys.path.insert(0, '.')
from stack import *
fn, cutspec, where, Q = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
P = read_pts(fn, 4)
L, c = layers4(P)
cuts = set(int(x) for x in cutspec.split(',') if x)
base = []; e = 0
for i, o in enumerate(L):
    if i in cuts: e += 1
    for pt in o: base.append((e, pt[0], pt[1]))
emax = e
sq = [(1, 0), (0, 1), (-1, 0), (0, -1)]
good = []
for k in range(1, Q):
    new = [rotq(p, k, Q) for p in sq]
    ee = -1 if where == 'outer' else emax + 1
    pts = [(ee, x, y) for (x, y) in new] + base
    ml, cnt, z = evaluate(pts, 9)
    ang = 2 * math.degrees(math.atan(k / Q))
    n8 = None if cnt is None else cnt[8]
    if n8 == 0: good.append((k, ang))
    print('k=%d ang=%.3f maxlen=%s n8=%s zero=%d' % (k, ang, ml, n8, z), flush=True)
print('good:', good)
