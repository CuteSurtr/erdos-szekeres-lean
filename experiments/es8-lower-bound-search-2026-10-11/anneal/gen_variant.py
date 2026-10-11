#!/usr/bin/env python3
"""Variant of the repository's block construction with randomised stacking offsets:
each stack uses horizontal offset t + extra_t and vertical offset m + extra_m, where
t, m are the least admissible offsets (exactly as in scripts/es_lower_bound_witness.py)
and extra_t, extra_m >= 0 are random. Larger offsets keep every required mixed-triple
sign, so the result is again a 2^(n-2)-point set with no convex n-gon (checked by cgon).
Usage: gen_variant.py n seed"""
import math, random, sys
from fractions import Fraction
from itertools import combinations
def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
n, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
def stack(sign, left, right):
    t = max(p[0] for p in left) - min(p[0] for p in right) + 1 + rng.randint(0, 2)
    moved = [(x + t, y) for x, y in right]
    need = Fraction(0)
    for a, a2 in combinations(sorted(left), 2):
        for b in moved:
            need = max(need, Fraction(-sign * orient(a, a2, b), a2[0] - a[0]))
    for a in left:
        for b, b2 in combinations(sorted(moved), 2):
            need = max(need, Fraction(sign * orient(a, b, b2), b2[0] - b[0]))
    m = math.floor(need) + 1
    m += rng.randint(0, max(1, int(m * rng.choice([0.0, 0.1, 0.4]))))
    return left + [(x, y + sign * m) for x, y in moved]
def ccf(k, l):
    if k == 2 or l == 2:
        return [(0, 0)]
    return stack(1, ccf(k - 1, l), ccf(k, l - 1))
pts = ccf(n, 2)
for j in range(1, n - 1):
    pts = stack(-1, pts, ccf(n - j, j + 2))
assert len(set(pts)) == len(pts) == 2 ** (n - 2)
assert max(max(abs(x), abs(y)) for x, y in pts) < 2 ** 30
for x, y in pts:
    print(x, y)
