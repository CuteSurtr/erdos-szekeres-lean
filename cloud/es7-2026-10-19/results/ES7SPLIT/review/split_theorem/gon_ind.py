#!/usr/bin/env python3
"""Exact largest subset in convex position (general position assumed), O(n^4) DP over the lowest vertex,
cross-checked against brute force on random small sets when run with --selftest."""
import random
import sys
from functools import cmp_to_key
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from igeom import orient, in_convex_position, general_position


def gon(S):
    S = [tuple(p) for p in S]
    n = len(S)
    if n <= 3:
        return n
    best_all = 3
    for p in S:
        above = [q for q in S if (q[1], q[0]) > (p[1], p[0])]

        def cmp(a, b):
            o = orient(p, a, b)
            return -1 if o > 0 else 1
        Q = sorted(above, key=cmp_to_key(cmp))
        m = len(Q)
        if m < 2:
            continue
        best = [[0] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                v = 3
                for k in range(i):
                    if best[k][i] + 1 > v and orient(Q[k], Q[i], Q[j]) > 0:
                        v = best[k][i] + 1
                best[i][j] = v
                if v > best_all:
                    best_all = v
    return best_all


def gon_brute(S):
    for r in range(len(S), 2, -1):
        for T in combinations(S, r):
            if in_convex_position(T):
                return r
    return min(len(S), 2)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        rng = random.Random(3)
        bad = 0
        for t in range(400):
            n = rng.randint(4, 10)
            while True:
                S = list({(rng.randint(0, 60), rng.randint(0, 60)) for _ in range(n)})
                if len(S) == n and general_position(S):
                    break
            if gon(S) != gon_brute(S):
                bad += 1
        print('selftest 400 random sets, mismatches:', bad)
    else:
        for path in sys.argv[1:]:
            pts = [tuple(map(int, l.split()[:2])) for l in open(path) if l.strip() and not l.startswith('#')]
            print(path.rsplit('/', 1)[-1], len(pts), 'general_position', general_position(pts), 'gon', gon(pts))
