#!/usr/bin/env python3
"""Randomized realizations of the Erdos-Szekeres 32-point construction, adapted from
results/LBS/L2/gen_bases.py (credit L2): the stacking of ErdosSzekeres/LowerBound with random
extra horizontal gaps and vertical offsets, but milder randomization and no scaling, so that
coordinates stay small; walk.c rescales each axis.  Sets with max |coord| >= 2^24 are redrawn.
Usage: gen_es.py SEED OUTFILE [MILD]  (MILD=0: minimal offsets, 1: mild, 2: L2-like)"""
import math, random, sys
from fractions import Fraction
from itertools import combinations

def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def stack(sign, left, right, rng, mild):
    gx = [0, 1, 3][mild]
    t = max(p[0] for p in left) - min(p[0] for p in right) + 1 + rng.randint(0, gx)
    moved = [(x + t, y) for x, y in right]
    need = Fraction(0)
    for a, a2 in combinations(sorted(left), 2):
        for b in moved:
            need = max(need, Fraction(-sign * orient(a, a2, b), a2[0] - a[0]))
    for a in left:
        for b, b2 in combinations(sorted(moved), 2):
            need = max(need, Fraction(sign * orient(a, b, b2), b2[0] - b[0]))
    mult = [[1], [1, 1, 1, 2], [1, 1, 2, 3]][mild]
    gy = [0, 2, 5][mild]
    m = math.floor(need * Fraction(rng.choice(mult))) + 1 + rng.randint(0, gy)
    return left + [(x, y + sign * m) for x, y in moved]

def ccf(k, l, rng, mild):
    if k == 2 or l == 2:
        return [(0, 0)]
    return stack(1, ccf(k - 1, l, rng, mild), ccf(k, l - 1, rng, mild), rng, mild)

def witness(n, rng, mild):
    pts = ccf(n, 2, rng, mild)
    for j in range(1, n - 1):
        pts = stack(-1, pts, ccf(n - j, j + 2, rng, mild), rng, mild)
    return pts

if __name__ == "__main__":
    seed, out = int(sys.argv[1]), sys.argv[2]
    mild = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    while True:
        pts = witness(7, rng, mild)
        if max(max(abs(x), abs(y)) for x, y in pts) < 2 ** 24:
            break
    with open(out, "w") as f:
        for x, y in pts:
            f.write(f"{x} {y}\n")
