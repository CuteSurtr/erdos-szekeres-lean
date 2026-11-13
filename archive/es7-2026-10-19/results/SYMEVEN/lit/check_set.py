#!/usr/bin/env python3
"""Independent checker for a planar point set given as integer coordinates (one 'x y' per line).
Checks: distinct points, central symmetry S = -S with 0 not in S, general position (no collinear triple),
and computes the largest subset in convex position by an exact cup/cap dynamic program:
for every leftmost point q and rightmost point r, the largest convex polygon with these extreme points is
(longest cup from q to r) + (longest cap from q to r) - 2, because a cup from q to r lies below the chord qr and
a cap lies above it.  Points are first expressed in a frame where all abscissae are distinct (a generic
orientation-preserving linear map), so 'leftmost' is well defined.  Exact integer arithmetic throughout.
Usage: python3 -I check_set.py FILE
"""
import sys
from itertools import combinations


def load(fn):
    pts = []
    for line in open(fn):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        a, b = line.replace(',', ' ').split()[:2]
        pts.append((int(a), int(b)))
    return pts


def analyse(P):
    n = len(P)
    assert len(set(P)) == n, 'repeated points'
    Ps = set(P)
    sym = all((-x, -y) in Ps for (x, y) in P) and (0, 0) not in Ps
    # generic frame: (u, v) = (a x + b y, -b x + a y) with a, b chosen so the u are distinct
    a, b = 1, 0
    for cand in [(1, 0), (1000003, 1), (999983, 7919), (104729, 1299709), (15485863, 32452843)]:
        us = [cand[0] * x + cand[1] * y for (x, y) in P]
        if len(set(us)) == n:
            a, b = cand
            break
    else:
        raise SystemExit('could not find a frame with distinct abscissae')
    Q = sorted(((a * x + b * y, -b * x + a * y) for (x, y) in P))
    # orientation sign table
    sg = [[[0] * n for _ in range(n)] for _ in range(n)]
    collinear = 0
    for i, j, k in combinations(range(n), 3):
        (x1, y1), (x2, y2), (x3, y3) = Q[i], Q[j], Q[k]
        o = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        s = (o > 0) - (o < 0)
        if s == 0:
            collinear += 1
        sg[i][j][k] = s
    best = min(n, 2)
    witness = None
    for q in range(n):
        # cup[i][j]: longest cup starting at q whose last edge is (i, j), q <= i < j; cap likewise
        cup = {}
        cap = {}
        for j in range(q + 1, n):
            cup[(q, j)] = 2
            cap[(q, j)] = 2
        for j in range(q + 1, n):
            for i in range(q + 1, j):
                bu = 0
                bc = 0
                for h in range(q, i):
                    v = cup.get((h, i))
                    if v is not None and sg[h][i][j] > 0 and v + 1 > bu:
                        bu = v + 1
                    w = cap.get((h, i))
                    if w is not None and sg[h][i][j] < 0 and w + 1 > bc:
                        bc = w + 1
                if bu:
                    cup[(i, j)] = bu
                if bc:
                    cap[(i, j)] = bc
        bestcup = {}
        bestcap = {}
        for (i, j), v in cup.items():
            if v > bestcup.get(j, 0):
                bestcup[j] = v
        for (i, j), v in cap.items():
            if v > bestcap.get(j, 0):
                bestcap[j] = v
        for r in range(q + 1, n):
            tot = bestcup[r] + bestcap[r] - 2
            if tot > best:
                best = tot
                witness = (q, r)
    return n, sym, collinear, best


if __name__ == '__main__':
    n, sym, collinear, best = analyse(load(sys.argv[1]))
    print(f'file={sys.argv[1]}')
    print(f'  points={n}  centrally_symmetric(S=-S, 0 not in S)={sym}  collinear_triples={collinear}  largest_convex_subset={best}')
