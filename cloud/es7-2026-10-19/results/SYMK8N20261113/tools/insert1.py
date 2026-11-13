#!/usr/bin/env python3
"""Insert one extra square as a NEW scale level at every level position of a stack (blocks given by cuts),
rotation 2 atan(k/Q), k = 0..Q-1 (k = 0 means aligned with the x-axis).  Exact limit evaluation.
usage: insert1.py FILE.pts cuts Q"""
import sys, math
sys.path.insert(0, '.')
from stack import *
fn, cutspec, Q = sys.argv[1], sys.argv[2], int(sys.argv[3])
P = read_pts(fn, 4)
L, c = layers4(P)
cuts = sorted(set(int(x) for x in cutspec.split(',') if x))
blocks = []; prev = 0
for cc in cuts + [len(L)]:
    blocks.append(L[prev:cc]); prev = cc
sq = [(1, 0), (0, 1), (-1, 0), (0, -1)]
best = None
for pos in range(len(blocks) + 1):
    res = []
    for k in range(0, Q):
        new = [rotq(p, k, Q) for p in sq]
        bl = blocks[:pos] + [[new]] + blocks[pos:]
        pts = []
        for e, b in enumerate(bl):
            for o in b:
                for pt in o: pts.append((2 * e, pt[0], pt[1]))
        ml, cnt, z = evaluate(pts, 8)
        n8 = cnt[8] if cnt else None
        res.append((n8 if n8 is not None else 10**12, k))
        if n8 == 0: print('FOUND', fn, 'pos', pos, 'k', k, flush=True)
    res.sort()
    print('%s pos=%d best n8=%s at k=%d (angle %.2f)  worst %s' % (fn.split('/')[-1], pos, res[0][0], res[0][1], 2 * math.degrees(math.atan(res[0][1] / Q)), res[-1][0]), flush=True)
