#!/usr/bin/env python3
"""Brute-force check of `sat test`: largest convex polygon through an extra point p.

Random integer sets S (general position) and random extra points p; the
largest subset of S+{p} in convex position that contains p is found by
enumerating subsets and testing convex position with the independent
criterion "no point lies in a triangle of three others".
"""
import random, subprocess, sys, os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
# Directory holding the compiled `sat`/`verify` binaries and temporary files
# (run_all.sh sets it; default: the ignored .cache/ build directory).
BUILD = os.environ.get("BUILD_DIR") or os.path.join(
    HERE, "..", "..", "..", ".cache", "es8-lower-bound-search-2026-10-11", "saturation")


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def in_triangle(p, a, b, c):
    s1, s2, s3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
    return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)


def convex_position(pts):
    for i, p in enumerate(pts):
        others = pts[:i] + pts[i + 1:]
        for a, b, c in combinations(others, 3):
            if in_triangle(p, a, b, c):
                return False
    return True


def gp(pts):
    return all(orient(a, b, c) != 0 for a, b, c in combinations(pts, 3))


def best_through(S, p):
    best = 2
    for k in range(3, len(S) + 2):
        found = any(convex_position(list(sub) + [p]) for sub in combinations(S, k - 1))
        if not found:
            break
        best = k
    return best


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    mismatches = 0
    hist = {}
    for t in range(trials):
        n = rng.randint(5, 10)
        R = rng.choice([6, 20, 1000])
        while True:
            S = [(rng.randint(-R, R), rng.randint(-R, R)) for _ in range(n)]
            if len(set(S)) == n and gp(S):
                break
        ps = []
        while len(ps) < 6:
            p = (rng.randint(-2 * R, 2 * R), rng.randint(-2 * R, 2 * R))
            if p not in S and gp(S + [p]):
                ps.append(p)
        path = os.path.join(BUILD, "tmp_test_pts.txt")
        with open(path, "w") as f:
            f.write("".join(f"{x} {y}\n" for x, y in S))
        out = subprocess.run([os.path.join(BUILD, "sat"), "test", path, "5"],
                             input="".join(f"{x} {y}\n" for x, y in ps),
                             capture_output=True, text=True, check=True).stdout.split()
        for p, o in zip(ps, out):
            b = best_through(S, p)
            hist[b] = hist.get(b, 0) + 1
            if int(o) != b:
                mismatches += 1
                print("MISMATCH", S, p, o, b)
    print(f"trials={trials} points_tested={sum(hist.values())} mismatches={mismatches} "
          f"histogram_of_true_values={dict(sorted(hist.items()))}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
