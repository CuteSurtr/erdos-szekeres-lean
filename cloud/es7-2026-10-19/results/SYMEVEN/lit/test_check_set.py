#!/usr/bin/env python3
"""Validate check_set.analyse against brute force on random small sets (exact arithmetic)."""
import random, sys, os
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_set import analyse

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def in_convex_position(T):
    for p in T:
        others = [q for q in T if q != p]
        for a, b, c in combinations(others, 3):
            s = orient(a, b, c)
            if (orient(a, b, p) > 0) == (s > 0) and (orient(b, c, p) > 0) == (s > 0) and (orient(c, a, p) > 0) == (s > 0):
                return False
    return True

def brute(P):
    n = len(P)
    for size in range(n, 2, -1):
        for T in combinations(P, size):
            if in_convex_position(T):
                return size
    return min(n, 2)

random.seed(20261101)
bad = 0
trials = 0
while trials < 300:
    n = random.randint(6, 11)
    if random.random() < 0.5:
        half = [(random.randint(-60, 60), random.randint(-60, 60)) for _ in range(n // 2)]
        P = list(set(half + [(-x, -y) for (x, y) in half]))
    else:
        P = list(set((random.randint(-60, 60), random.randint(-60, 60)) for _ in range(n)))
    if any(orient(a, b, c) == 0 for a, b, c in combinations(P, 3)) or (0, 0) in P:
        continue
    trials += 1
    _, _, col, best = analyse(P)
    bf = brute(P)
    if best != bf:
        bad += 1
        print('MISMATCH', P, best, bf)
print(f'{trials} random sets in general position, mismatches: {bad}')
