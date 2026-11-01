#!/usr/bin/env python3
"""Cross-validation of the two C checkers (maxconv_a: angular DP, 128-bit; maxconv_b: cap+cup DP, GMP)
against a pure-Python brute force (method C: every subset, convex hull by Andrew's monotone chain, exact ints).

Usage: test_methods.py NRANDOM [pointfile ...]
  - NRANDOM random sets (general position, 6..15 points; half of them mirror-symmetric with 0..2 axis points);
  - for every pointfile: random subsets of 9..15 points (brute force) and of 25..45 points (A vs B vs
    Python cap+cup DP), 60 subsets per file.
"""
import sys
import os
import random
import subprocess
import tempfile
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def hull_size(P):
    P = sorted(P)
    if len(P) <= 2:
        return len(P)
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return len(lo) + len(up) - 2


def brute_max_convex(P):
    n = len(P)
    for s in range(n, 2, -1):
        for c in combinations(P, s):
            if hull_size(c) == s:
                return s
    return min(n, 2)


def capcup_py(P):
    """Python cap+cup DP (lexicographic order), O(n^4)."""
    P = sorted(P)
    n = len(P)
    best = min(n, 2)
    for a in range(n):
        LA = {}
        LU = {}
        for i in range(a + 1, n):
            LA[(a, i)] = 2
            LU[(a, i)] = 2
            for h in range(a + 1, i):
                mA = mU = 0
                for g in range(a, h):
                    o = orient(P[g], P[h], P[i])
                    if o < 0:
                        mA = max(mA, LA.get((g, h), 0))
                    elif o > 0:
                        mU = max(mU, LU.get((g, h), 0))
                LA[(h, i)] = mA + 1 if mA else 0
                LU[(h, i)] = mU + 1 if mU else 0
            cm = max(LA[(h, i)] for h in range(a, i))
            um = max(LU[(h, i)] for h in range(a, i))
            best = max(best, cm + um - 2)
    return best


def general_position(P):
    return all(orient(p, q, r) != 0 for p, q, r in combinations(P, 3)) and len(set(P)) == len(P)


def run(prog, P):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("".join(f"{x} {y}\n" for x, y in P))
        fn = f.name
    out = subprocess.run([os.path.join(HERE, prog), fn, "-q"] if prog == "maxconv_a" else
                         [os.path.join(HERE, prog), fn], capture_output=True, text=True).stdout
    os.unlink(fn)
    for line in out.splitlines():
        if line.startswith("LARGEST SUBSET IN CONVEX POSITION"):
            return int(line.split(":")[1].split()[0])
    raise RuntimeError(out)


def random_set(rng):
    while True:
        n = rng.randint(6, 15)
        C = rng.choice([6, 12, 40, 1000])
        if rng.random() < 0.5:
            m = (n - rng.randint(0, 2)) // 2
            R = [(rng.randint(-C, C), rng.randint(1, C)) for _ in range(m)]
            P = R + [(x, -y) for x, y in R] + [(rng.randint(-C, C), 0) for _ in range(n - 2 * m)]
        else:
            P = [(rng.randint(-C, C), rng.randint(-C, C)) for _ in range(n)]
        if general_position(P):
            return P


def main():
    rng = random.Random(20261102)
    N = int(sys.argv[1])
    fails = 0
    tested = 0
    for t in range(N):
        P = random_set(rng)
        b = brute_max_convex(P)
        a = run("maxconv_a", P)
        c = run("maxconv_b", P)
        d = capcup_py(P)
        tested += 1
        if not (a == b == c == d):
            fails += 1
            print("MISMATCH random", P, a, b, c, d)
    print(f"random sets: {tested} tested, {fails} mismatches")
    for fn in sys.argv[2:]:
        S = [tuple(map(int, l.split())) for l in open(fn) if l.strip() and not l.startswith("#")]
        f1 = f2 = 0
        for t in range(60):
            m = rng.randint(9, 15)
            P = rng.sample(S, m)
            b = brute_max_convex(P)
            a = run("maxconv_a", P)
            c = run("maxconv_b", P)
            if not (a == b == c):
                f1 += 1
                print("MISMATCH small subset", fn, P, a, b, c)
            m = rng.randint(25, 45)
            P = rng.sample(S, m)
            a = run("maxconv_a", P)
            c = run("maxconv_b", P)
            d = capcup_py(P)
            if not (a == c == d):
                f2 += 1
                print("MISMATCH medium subset", fn, a, c, d)
        print(f"{fn}: 60 small subsets (brute force) mismatches {f1}; 60 medium subsets (A/B/Py) mismatches {f2}")
        fails += f1 + f2
    print("TOTAL MISMATCHES:", fails)


if __name__ == "__main__":
    main()
