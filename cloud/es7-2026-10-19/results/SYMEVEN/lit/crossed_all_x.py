#!/usr/bin/env python3
"""Check, for every x = 0..X, that the half-turn-symmetric parameter choice with labelling LEFTPOS on base S along
sweep direction (a,b) satisfies Baek-Balko Lemma 14 (a), (b) with k = m + 2x, and compute the Lemma 14 size.
Brute-force s-values (exact).  Usage: python3 -I crossed_all_x.py BASE m a b LEFTPOS X"""
import sys
from math import comb
from itertools import combinations


def load(fn):
    pts = []
    for line in open(fn):
        line = line.strip()
        if line and not line.startswith('#'):
            u, v = line.replace(',', ' ').split()[:2]
            pts.append((int(u), int(v)))
    return pts


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def convex(T):
    for p in T:
        o = [q for q in T if q != p]
        for a, b, c in combinations(o, 3):
            s = orient(a, b, c) > 0
            if (orient(a, b, p) > 0) == s and (orient(b, c, p) > 0) == s and (orient(c, a, p) > 0) == s:
                return False
    return True


base = load(sys.argv[1]); m = int(sys.argv[2]); a = int(sys.argv[3]); b = int(sys.argv[4])
L = [int(t) - 1 for t in sys.argv[5].split(',')]; XMAX = int(sys.argv[6])
N = len(base)
R = sorted((a * x + b * y, -b * x + a * y) for (x, y) in base)
assert all((-R[i][0], -R[i][1]) == R[N - 1 - i] for i in range(N))
assert sorted(L + [N - 1 - i for i in L]) == list(range(N))
maxc = max(len(T) for r in range(1, 7) for T in combinations(range(N), r) if r < 3 or convex([R[t] for t in T]))
assert maxc < m, 'base has an m-gon'


def best(pool, fixed):
    for r in range(len(pool), -1, -1):
        for T in combinations(pool, r):
            if convex([R[t] for t in T] + [R[f] for f in fixed]):
                return r + len(fixed)


sL = {i: best(list(range(i)), [i]) for i in range(N)}           # largest left-gon at p_i
sR = {i: best(list(range(i + 1, N)), [i]) for i in range(N)}     # largest right-gon at p_i
sij = {(i, j): best(list(range(i + 1, j)), [i, j]) for i, j in combinations(range(N), 2)}
s = {i: (sL[i] if i in L else sR[i]) for i in range(N)}
print('labels', ''.join('L' if i in L else 'R' for i in range(N)), 's', [s[i] for i in range(N)])
crossed = [(i, j) for i, j in combinations(range(N), 2) if i not in L and j in L]
print('crossed pairs (right-labelled i < left-labelled j):', [(i + 1, j + 1, s[i], s[j], sij[(i, j)]) for i, j in crossed])
for x in range(0, XMAX + 1):
    k = m + 2 * x
    X = {}; Y = {}
    for i in range(N):
        if i in L:
            X[i] = x; Y[i] = (k - 1 - x - s[i]) if i > 0 else 0
        else:
            Y[i] = x; X[i] = (k - 1 - x - s[i]) if i < N - 1 else 0
    ok_a = all(X[i] >= 0 and Y[i] >= 0 and X[i] + Y[i] <= k - 1 for i in range(N))
    viol = [(i + 1, j + 1) for i, j in combinations(range(N), 2) if X[i] + Y[j] > k - 1 - sij[(i, j)]]
    sym = all((X[N - 1 - i], Y[N - 1 - i]) == (Y[i], X[i]) for i in range(N))
    size = sum(comb(k - 2, l) for l in range(X[0] + 1)) + sum(comb(X[i] + Y[i], X[i]) for i in range(1, N - 1)) \
        + sum(comb(k - 2, l) for l in range(Y[N - 1] + 1))
    print(f'x={x} k={k}: (a) ok={ok_a}, (b) violations={viol}, half-turn-compatible={sym}, size={size}, 2^(k-2)={2**(k-2)}')
