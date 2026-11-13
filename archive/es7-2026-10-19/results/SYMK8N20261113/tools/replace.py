#!/usr/bin/env python3
"""Stack an outer part X (layers of one set, with its own infinitesimal cuts) over a candidate inner block Y (a
contiguous layer range of another set), Y rotated by 2 atan(k/Q), k = 1..Q-1, at a new infinitesimal scale.
usage: replace.py XFILE XRANGE(a:b) XCUTS YLIST(file:a:b,...) Q"""
import sys, math
sys.path.insert(0, '.')
from stack import *
xf, xr, xc, ylist, Q = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
a, b = map(int, xr.split(':'))
LX, _ = layers4(read_pts(xf, 4))
LX = LX[a:b]
xcuts = set(int(x) - a for x in xc.split(',') if x)
base = []; e = 0
for i, o in enumerate(LX):
    if i in xcuts: e += 1
    for pt in o: base.append((2 * e, pt[0], pt[1]))
ey = 2 * e + 2
for spec in ylist.split(','):
    f, ya, yb = spec.split(':'); ya, yb = int(ya), int(yb)
    LY, _ = layers4(read_pts(f, 4))
    LY = LY[ya:yb]
    res = []
    for k in range(1, Q):
        pts = list(base)
        for o in LY:
            for pt in o:
                q = rotq(pt, k, Q); pts.append((ey, q[0], q[1]))
        ml, cnt, z = evaluate(pts, 8)
        n8 = cnt[8] if cnt else 10 ** 12
        res.append((n8, k))
        if n8 == 0: print('FOUND', spec, k, flush=True)
    res.sort()
    print('%s Y=%s best n8=%d k=%d ang=%.2f' % (xf.split('/')[-1], spec.split('/')[-1], res[0][0], res[0][1], 2 * math.degrees(math.atan(res[0][1] / Q))), flush=True)
