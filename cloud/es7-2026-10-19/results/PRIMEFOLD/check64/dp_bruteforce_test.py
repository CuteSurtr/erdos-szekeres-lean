#!/usr/bin/env python3
"""Validate the anchor DP (as used in verify64.py) against brute force on random subsets.

Brute force: a subset Q (general position) is in convex position iff no point of Q lies strictly inside a
triangle of three other points of Q.  We count convex k-subsets of random 13-point subsets by brute force
and by the DP, and also compare the largest convex subset.
"""
import sys, random, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import z7exact as Z
from functools import cmp_to_key

path = sys.argv[1]
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
size = int(sys.argv[3]) if len(sys.argv) > 3 else 13
pts = Z.read_pts(path)
n = len(pts)
O = Z.orient_table(pts)


def cmp_yx(a, b):
    if a == b:
        return 0
    s = Z.sign_im_diff(pts[a], pts[b])
    if s != 0:
        return s
    return Z.sign_re_diff(pts[a], pts[b])


order = sorted(range(n), key=cmp_to_key(cmp_yx))
rank = {i: r for r, i in enumerate(order)}


def dp_counts(sub, KMAX=12):
    counts = [0] * (KMAX + 1)
    for p in sub:
        above = [q for q in sub if rank[q] > rank[p]]
        above.sort(key=cmp_to_key(lambda q, r: -O[p][q][r]))
        m = len(above)
        prev = [[1 if i < j else 0 for j in range(m)] for i in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                if O[above[i]][above[j]][p] > 0:
                    counts[3] += 1
        for k in range(4, KMAX + 1):
            cur = [[0] * m for _ in range(m)]
            for j in range(m):
                for i in range(j):
                    s = 0
                    for h in range(i):
                        if prev[h][i] and O[above[h]][above[i]][above[j]] > 0:
                            s += prev[h][i]
                    cur[i][j] = s
                    if s and O[above[i]][above[j]][p] > 0:
                        counts[k] += s
            prev = cur
    return counts


def inside(x, a, b, c):
    # x strictly inside triangle abc (general position)
    s1 = O[a][b][x]; s2 = O[b][c][x]; s3 = O[c][a][x]
    return s1 == s2 == s3


def convex_position(Q):
    for x in Q:
        others = [y for y in Q if y != x]
        for a, b, c in itertools.combinations(others, 3):
            if inside(x, a, b, c):
                return False
    return True


def brute_counts(sub, KMAX=12):
    counts = [0] * (KMAX + 1)
    for k in range(3, min(KMAX, len(sub)) + 1):
        c = 0
        for Q in itertools.combinations(sub, k):
            if convex_position(Q):
                c += 1
        counts[k] = c
        if c == 0:
            break
    return counts


random.seed(12345)
bad = 0
for t in range(trials):
    # bias some trials toward one or two clusters plus random others to get dense configurations
    if t % 3 == 0:
        sub = random.sample(range(n), size)
    elif t % 3 == 1:
        base = random.randrange(7)
        cl = [base * 6 + i for i in range(6)] + [42 + base * 3 + i for i in range(3)]
        rest = [x for x in range(n) if x not in cl]
        sub = cl + random.sample(rest, size - len(cl))
    else:
        sub = random.sample(range(n), size)
    a = dp_counts(sub)
    b = brute_counts(sub)
    if a != b:
        bad += 1
        print('MISMATCH', sub, a, b)
print('trials', trials, 'size', size, 'mismatches', bad)
print('example counts', a)
