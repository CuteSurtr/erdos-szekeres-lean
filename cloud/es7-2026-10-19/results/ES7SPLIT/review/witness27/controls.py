#!/usr/bin/env python3
"""Control runs for the two brute-force checkers (C method A, numpy method B).

1. 10 points (i, i^2): every subset is convex -> expected counts C(10,k).
2. Random integer sets in general position (n = 14..18): methods A and B must agree on all counts
   (and, at k <= 7, at least some sets must contain convex 7-gons, so the 7-gon detection is exercised).
"""
import os
import random
import re
import subprocess
import sys
from itertools import combinations
from math import comb

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from verify_witness import orient, count_convex_numpy  # noqa: E402

BRUTE = os.path.join(HERE, "brute")


def run_brute(fn):
    out = subprocess.run([BRUTE, fn], capture_output=True, text=True, check=True).stdout
    res = {}
    for m in re.finditer(r"k=(\d): subsets (\d+), convex (\d+) \| subsets containing b (\d+), convex containing b (\d+)", out):
        k = int(m.group(1))
        res[k] = tuple(int(m.group(i)) for i in range(2, 6))
    gp = "general position: yes" in out
    return res, gp


def numpy_counts(P):
    n = len(P)
    O = np.zeros((n, n, n), dtype=np.int8)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                v = orient(P[i], P[j], P[k])
                O[i, j, k] = (v > 0) - (v < 0)
    return {k: count_convex_numpy(O, n, k, n - 1) for k in (5, 6, 7)}


def write(P, fn):
    with open(fn, "w") as f:
        for x, y in P:
            f.write(f"{x} {y}\n")


def main():
    # control 1
    P = [(i, i * i) for i in range(10)]
    fn = os.path.join(HERE, "ctrl_parabola10.txt")
    write(P, fn)
    a, gp = run_brute(fn)
    bb = numpy_counts(P)
    print("parabola10: brute", a, "numpy", bb, "gp", gp)
    for k in (5, 6, 7):
        assert a[k][1] == comb(10, k) and bb[k][1] == comb(10, k)
    # control 2
    rng = random.Random(20261101)
    n_sets = 0
    seven_total = 0
    for trial in range(40):
        n = rng.randint(14, 18)
        while True:
            P = [(rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(n)]
            if len(set(P)) == n and all(orient(*t) != 0 for t in combinations(P, 3)):
                break
        fn = os.path.join(HERE, "ctrl_random.txt")
        write(P, fn)
        a, gp = run_brute(fn)
        bb = numpy_counts(P)
        assert gp
        for k in (5, 6, 7):
            assert a[k] == bb[k], (trial, k, a[k], bb[k])
        n_sets += 1
        seven_total += a[7][1]
    print(f"random controls: {n_sets} sets, methods A and B agree on all counts; total convex 7-subsets seen {seven_total}")


if __name__ == "__main__":
    main()
