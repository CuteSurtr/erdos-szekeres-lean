#!/usr/bin/env python3
"""Randomized realizations of the Erdos-Szekeres 32-point construction
(the stacking of ErdosSzekeres/LowerBound, as in scripts/es_lower_bound_witness.py),
with random extra horizontal gaps and vertical offsets, then scaled.
Usage: gen_bases.py COUNT OUTDIR SEED"""
import math, random, sys
from fractions import Fraction
from itertools import combinations

def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def stack(sign, left, right, rng):
    t = max(p[0] for p in left) - min(p[0] for p in right) + 1 + rng.randint(0, 3)
    moved = [(x + t, y) for x, y in right]
    need = Fraction(0)
    for a, a2 in combinations(sorted(left), 2):
        for b in moved:
            need = max(need, Fraction(-sign * orient(a, a2, b), a2[0] - a[0]))
    for a in left:
        for b, b2 in combinations(sorted(moved), 2):
            need = max(need, Fraction(sign * orient(a, b, b2), b2[0] - b[0]))
    m = math.floor(need * Fraction(rng.choice([1, 1, 2, 3]))) + 1 + rng.randint(0, 5)
    return left + [(x, y + sign * m) for x, y in moved]

def ccf(k, l, rng):
    if k == 2 or l == 2:
        return [(0, 0)]
    return stack(1, ccf(k - 1, l, rng), ccf(k, l - 1, rng), rng)

def witness(n, rng):
    pts = ccf(n, 2, rng)
    for j in range(1, n - 1):
        pts = stack(-1, pts, ccf(n - j, j + 2, rng), rng)
    return pts

class Minimal:
    def randint(self, a, b): return a
    def choice(self, s): return 1

if __name__ == "__main__":
    cnt, out, seed = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    rng = random.Random(seed)
    for i in range(cnt):
        # base000 is the canonical witness (minimal offsets)
        pts = witness(7, rng if i else Minimal())
        sx, sy = rng.choice([256, 1024, 4096]), rng.choice([16, 64, 256])
        with open(f"{out}/base{i:03d}.txt", "w") as f:
            for x, y in pts:
                f.write(f"{x * sx} {y * sy}\n")
