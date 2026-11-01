#!/usr/bin/env python3
"""Validate the exact algorithms of geom_check.py against brute force on random sets in general position
(including sets with repeated x-coordinates, to exercise the lexicographic tie-breaking)."""
import random
import sys
from itertools import combinations
from geom_check import (general_position_violations, largest_convex_angular, largest_convex_cupcap,
                        brute_largest, in_convex_position, count_convex_by_size, longest_cup_cap, orient)


def random_gp_set(n, box, rng):
    while True:
        P = list({(rng.randint(-box, box), rng.randint(-box, box)) for _ in range(n)})
        if len(P) == n and not general_position_violations(P):
            return P


def brute_counts(P, maxlen):
    c = [0] * (maxlen + 1)
    for L in range(3, maxlen + 1):
        c[L] = sum(1 for s in combinations(P, L) if in_convex_position(s))
    return c


def brute_cup_cap(P):
    V = sorted(P)
    bu = bc = min(2, len(V))
    for L in range(3, len(V) + 1):
        for s in combinations(V, L):
            o = [orient(s[i], s[i + 1], s[i + 2]) for i in range(L - 2)]
            if all(x > 0 for x in o):
                bu = max(bu, L)
            if all(x < 0 for x in o):
                bc = max(bc, L)
    return bu, bc


def main(trials, seed):
    rng = random.Random(seed)
    fails = 0
    for t in range(trials):
        n = rng.randint(5, 12)
        box = rng.choice([4, 6, 10, 50, 1000])
        P = random_gp_set(n, box, rng)
        a, wit = largest_convex_angular(P)
        b = largest_convex_cupcap(P)
        c = brute_largest(P)
        okw = len(wit) == a and in_convex_position(wit) and len(set(wit)) == a and set(wit) <= set(P)
        cc = count_convex_by_size(P, n)
        bc = brute_counts(P, n)
        cup = longest_cup_cap(P)
        bcup = brute_cup_cap(P)
        if not (a == b == c and okw and cc[3:] == bc[3:] and cup == bcup):
            fails += 1
            print("MISMATCH", P, a, b, c, okw, cc, bc, cup, bcup)
    print("trials=%d seed=%d failures=%d" % (trials, seed, fails))
    return fails


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    sys.exit(1 if main(trials, seed) else 0)
