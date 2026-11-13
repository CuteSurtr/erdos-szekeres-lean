#!/usr/bin/env python3
"""Brute force on a few points of a set: for the given point indices (0-based), count the subsets in convex position
of every size and report the largest, from an orientation table in text form ("n", then the n^3 signs, a major).
A set of points in general position is in convex position iff no point lies inside a triangle of three others.
usage: subset_convex.py TABLE i1 i2 ...
"""
import sys
from itertools import combinations

toks = open(sys.argv[1]).read().split()
n = int(toks[0])
O = list(map(int, toks[1:]))
assert len(O) == n ** 3


def o(a, b, c):
    return O[(a * n + b) * n + c]


def inside(x, a, b, c):
    s = o(a, b, c)
    return o(a, b, x) == s and o(b, c, x) == s and o(c, a, x) == s


idx = [int(t) for t in sys.argv[2:]]
assert all(o(a, b, c) != 0 for a, b, c in combinations(idx, 3)), 'collinear triple'
count = {}
best = None
for k in range(3, len(idx) + 1):
    for sub in combinations(idx, k):
        if not any(inside(x, a, b, c) for x in sub for a, b, c in combinations([y for y in sub if y != x], 3)):
            count[k] = count.get(k, 0) + 1
            best = sub
print('points', idx)
print('convex subsets by size:', {k: count.get(k, 0) for k in range(3, len(idx) + 1)})
print('largest convex subset: %d, e.g. %s' % (len(best), list(best)))
