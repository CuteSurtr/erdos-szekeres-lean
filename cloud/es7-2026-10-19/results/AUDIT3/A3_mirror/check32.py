#!/usr/bin/env python3
"""Exact check of results/SYMMAX/mirror_32points.txt: integer points, mirror-symmetric in the y-axis, no point on the
axis, general position, and largest subset in convex position (exact DP over convex chains with a fixed lowest
vertex).  The DP is cross-validated against brute force (edge-count convexity of every subset) on random sets.
Also checks that adding any axis point or any extra mirror pair... is NOT attempted (that is the theorem)."""
import itertools, os, random, sys

F = os.path.join(os.environ.get("ES7_RESULTS", "."), "SYMMAX/mirror_32points.txt")


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def general_position(P):
    return all(orient(p, q, r) != 0 for p, q, r in itertools.combinations(P, 3))


def largest_convex(P):
    """max size of a subset in convex position (points in general position)."""
    best = min(len(P), 2)
    for p in P:
        # p is the lowest vertex (min y, then min x); others strictly after p in (y, x) order
        Q = [q for q in P if (q[1], q[0]) > (p[1], p[0])]
        # sort by angle around p: all q in the closed upper half-plane minus the left horizontal ray, so the
        # angle lies in [0, pi); compare with cross products
        import functools

        def cmp(a, b):
            o = orient(p, a, b)
            return -1 if o > 0 else (1 if o < 0 else 0)
        Q.sort(key=functools.cmp_to_key(cmp))
        n = len(Q)
        # dp[i][j]: max vertices of a convex chain p -> ... -> Q[i] -> Q[j] (i < j), counting p
        dp = [[0] * n for _ in range(n)]
        for j in range(n):
            for i in range(j):
                v = 3                                # p -> Q[i] -> Q[j]  (turn at Q[i] is left iff ...)
                # chain p -> Q[i] -> Q[j] needs left turn at Q[i]: orient(p, Q[i], Q[j]) > 0, true by angle order
                for h in range(i):
                    if dp[h][i] and orient(Q[h], Q[i], Q[j]) > 0:
                        v = max(v, dp[h][i] + 1)
                dp[i][j] = v
                if orient(Q[i], Q[j], p) > 0:         # closing turn at Q[j]
                    best = max(best, v)
        if n >= 1:
            best = max(best, 2)
    return best


def convex_brute(S):
    n = len(S)
    if n <= 3:
        return True
    e = 0
    for p, q in itertools.combinations(S, 2):
        s = {orient(p, q, r) > 0 for r in S if r != p and r != q}
        e += len(s) == 1
    return e == n


def brute_largest(P):
    for k in range(len(P), 0, -1):
        for S in itertools.combinations(P, k):
            if convex_brute(S):
                return k
    return 0


def main():
    rng = random.Random(5)
    # cross-validation
    tested = 0
    while tested < 300:
        n = rng.randint(5, 11)
        R = rng.choice([5, 30, 1000])
        P = list({(rng.randint(-R, R), rng.randint(-R, R)) for _ in range(n)})
        if rng.random() < 0.5:                      # mirror-symmetric test sets too (shared heights)
            P = list({(x, y) for a, y in P for x in (abs(a) + 1, -abs(a) - 1)})[:12]
        if not general_position(P):
            continue
        a, b = largest_convex(P), brute_largest(P)
        assert a == b, (P, a, b)
        tested += 1
    print("DP cross-validated against brute force on", tested, "random sets (incl. mirror-symmetric ones)")
    P = [tuple(map(int, l.split())) for l in open(F) if l.strip()]
    S = set(P)
    print("points:", len(P), "distinct:", len(S))
    print("mirror-symmetric in the y-axis:", all((-x, y) in S for x, y in P))
    print("points on the axis:", sum(1 for x, y in P if x == 0))
    print("general position:", general_position(P))
    print("distinct pair heights:", len({y for x, y in P}) == len(P) // 2)
    print("largest subset in convex position:", largest_convex(P))


if __name__ == "__main__":
    main()
