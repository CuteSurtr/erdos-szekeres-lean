#!/usr/bin/env python3
"""Triple check of a point set (for any set claimed heptagon-free).

1. general position: every triple has nonzero orientation (Python integers /
   Fractions, exact);
2. convex k-gon counts by cups and caps (verify_exact.py);
3. convex k-gon counts by a depth-first search over convex-position subsets
   using the triangle criterion (a set is in convex position iff no point lies
   in a triangle spanned by three others) -- no angular sorting, no cups;
4. cgon.c count (angular DP), on integer input only.

usage: triple_check.py FILE [K]     (FILE: "x y" lines; or --json FILE KEY)
"""
import sys, os, json, itertools
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_exact
import dlib


def dfs_counts(P, K):
    n = len(P)
    O = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and j != k and i != k:
                    v = verify_exact.orient(P[i], P[j], P[k])
                    O[i][j][k] = 1 if v > 0 else -1

    def in_tri(x, a, b, c):
        s1 = O[a][b][x]; s2 = O[b][c][x]; s3 = O[c][a][x]
        return s1 == s2 == s3

    counts = {k: 0 for k in range(3, K + 1)}

    def ext(C, q):
        for a, b_, c in itertools.combinations(C, 3):
            if in_tri(q, a, b_, c):
                return False
        for x in C:
            others = [y for y in C if y != x]
            for a, b_ in itertools.combinations(others, 2):
                if in_tri(x, q, a, b_):
                    return False
        return True

    def rec(C, start):
        s = len(C)
        if s >= 3:
            counts[s] += 1
        if s == K:
            return
        for q in range(start, n):
            if s < 3 or ext(C, q):
                C.append(q)
                rec(C, q + 1)
                C.pop()
    rec([], 0)
    return counts


def main():
    a = sys.argv[1:]
    if a[0] == "--json":
        d = json.load(open(a[1]))
        P = [(Fraction(x), Fraction(y)) for x, y in d[a[2]]]
        K = int(a[3]) if len(a) > 3 else 8
    else:
        P = verify_exact.read_points(a[0])
        K = int(a[1]) if len(a) > 1 else 8
    gp, why = verify_exact.general_position(P)
    res = {"n": len(P), "general_position": gp, "why": why}
    if gp:
        res["cups_caps"] = verify_exact.count_convex(P, K)
        res["dfs_triangle"] = dfs_counts(P, K)
        if all(x.denominator == 1 and y.denominator == 1 for x, y in P):
            res["cgon"] = dlib.cgon_count([(int(x), int(y)) for x, y in P], K)
        res["agree"] = (res["cups_caps"] == res["dfs_triangle"] and
                        ("cgon" not in res or all(res["cgon"][k] == res["cups_caps"][k] for k in range(3, K + 1))))
    print(json.dumps(res, default=str))


if __name__ == "__main__":
    main()
