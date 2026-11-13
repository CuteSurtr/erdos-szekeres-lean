#!/usr/bin/env python3
"""Validate a7lib.max_convex_dp against exhaustive brute force (Andrew hull test on every subset) on random
general-position integer sets, including sets with large convex subsets (points near a circle), Eisenstein and Z[zeta5]
random sets (exercising the exact Q(sqrt5) arithmetic), and mutated copies of the examples.
usage: python3 -I test_dp_random.py"""
import os, random, sys
from functools import cmp_to_key
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7lib as L

def true_max(pts, fmt):
    cmpf = L.lex_key_cmp(fmt)
    cross = lambda o, a, b: L.orient_A(o, a, b, fmt)
    n = len(pts)
    best = min(n, 2)
    for k in range(3, n + 1):
        if any(L.hull_is_convex_position(list(c), cmpf, cross) for c in combinations(pts, k)):
            best = k
        else:
            break
    return best

def gen_position(pts, fmt):
    for a, b, c in combinations(pts, 3):
        if L.orient_A(a, b, c, fmt) == 0:
            return False
    return len(set(pts)) == len(pts)

def dp(pts, fmt):
    n = len(pts)
    O = L.orient_table(pts, fmt)
    cmpf = L.lex_key_cmp(fmt)
    order = sorted(range(n), key=cmp_to_key(lambda i, j: cmpf(pts[i], pts[j])))
    d, w = L.max_convex_dp(O, order)
    d2, _ = L.max_convex_dp(O, order[::-1])
    assert L.convex_position_halfplane(w, O), "witness not convex"
    return d, d2

def main():
    rng = random.Random(12345)
    stats = {}
    fails = 0
    tests = 0
    # 1) random integer sets, uniform and near a circle
    for t in range(400):
        n = rng.randint(5, 13)
        mode = t % 3
        while True:
            if mode == 0:
                pts = [(rng.randint(-60, 60), rng.randint(-60, 60)) for _ in range(n)]
            elif mode == 1:
                import math
                pts = []
                for _ in range(n):
                    a = rng.random() * 2 * math.pi
                    r = 1000 + rng.randint(-120, 120)
                    pts.append((int(r * math.cos(a)), int(r * math.sin(a))))
            else:
                pts = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]
            if gen_position(pts, "Z2"):
                break
        d, d2 = dp(pts, "Z2")
        tm = true_max(pts, "Z2")
        tests += 1
        stats[("Z2", tm)] = stats.get(("Z2", tm), 0) + 1
        if not (d == d2 == tm):
            fails += 1
            print("FAIL Z2", pts, d, d2, tm)
    # 2) random Eisenstein sets
    for t in range(150):
        n = rng.randint(5, 12)
        while True:
            pts = [(rng.randint(-40, 40), rng.randint(-40, 40)) for _ in range(n)]
            if gen_position(pts, "EIS"):
                break
        d, d2 = dp(pts, "EIS")
        tm = true_max(pts, "EIS")
        tests += 1
        stats[("EIS", tm)] = stats.get(("EIS", tm), 0) + 1
        if not (d == d2 == tm):
            fails += 1
            print("FAIL EIS", pts, d, d2, tm)
    # 3) random Z[zeta5] sets (small coefficients: many near-degenerate configurations)
    for t in range(150):
        n = rng.randint(5, 11)
        while True:
            pts = [tuple(rng.randint(-6, 6) for _ in range(4)) for _ in range(n)]
            if gen_position(pts, "Z5"):
                break
        d, d2 = dp(pts, "Z5")
        tm = true_max(pts, "Z5")
        tests += 1
        stats[("Z5", tm)] = stats.get(("Z5", tm), 0) + 1
        if not (d == d2 == tm):
            fails += 1
            print("FAIL Z5", pts, d, d2, tm)
    # 4) regular polygons in Z[zeta5]: orbit of a point is a regular pentagon (5 in convex position);
    #    two concentric pentagons rotated: 10 points, check DP vs brute force
    for t in range(40):
        while True:
            p = tuple(rng.randint(-9, 9) for _ in range(4))
            q = tuple(rng.randint(-9, 9) for _ in range(4))
            pts = []
            for base in (p, q):
                x = base
                for _ in range(5):
                    pts.append(x)
                    x = L.MAPS["C5"](x)
            if gen_position(pts, "Z5"):
                break
        d, d2 = dp(pts, "Z5")
        tm = true_max(pts, "Z5")
        tests += 1
        stats[("Z5-2pent", tm)] = stats.get(("Z5-2pent", tm), 0) + 1
        if not (d == d2 == tm):
            fails += 1
            print("FAIL Z5 pentagons", pts, d, d2, tm)
    print("tests=%d fails=%d" % (tests, fails))
    for k in sorted(stats, key=str):
        print("  %s true_max=%d : %d sets" % (k[0], k[1], stats[k]))

if __name__ == "__main__":
    main()
