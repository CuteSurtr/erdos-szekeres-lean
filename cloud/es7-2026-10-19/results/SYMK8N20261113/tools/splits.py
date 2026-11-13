#!/usr/bin/env python3
"""Stretch the radial gaps of a 4-fold set: put an infinitesimal scale gap at chosen layer boundaries and evaluate
the limit order type exactly.  usage: splits.py FILE.pts [all|list of cut positions like 1,12]"""
import sys, itertools, time
sys.path.insert(0, '.')
from stack import *
fn = sys.argv[1]
P = read_pts(fn, 4)
L, c = layers4(P)
t = len(L)
def run(cuts):
    e = 0; pts = []
    for i, o in enumerate(L):
        if i in cuts: e += 1
        for pt in o: pts.append((e, pt[0], pt[1]))
    ml, cnt, z = evaluate(pts, 9)
    return ml, (cnt or {}).get(8), z
if len(sys.argv) > 2 and sys.argv[2] != 'all':
    for spec in sys.argv[2:]:
        cuts = set(int(x) for x in spec.split(',') if x)
        print(sorted(cuts), run(cuts), flush=True)
else:
    good = []
    for r in range(1, t):
        for cuts in itertools.combinations(range(1, t), r):
            res = run(set(cuts))
            if res[1] == 0: good.append(cuts)
            print(cuts, res, flush=True)
    print('octagon-free cut sets:', len(good))
