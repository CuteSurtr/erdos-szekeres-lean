#!/usr/bin/env python3
"""Second, solver-free complete enumeration of all partitions (A, B), |A|,|B| >= 2, satisfying both
one-sidedness conditions (every A-pair has all of B strictly on one side; every B-pair has all of A strictly on one
side).  Plain depth-first search over the points in input order, pruning a partial assignment as soon as an
assigned A-pair sees two assigned B-points on different sides (or one on its line), or vice versa.
Also counts linear partitions (|X|,|Y| >= 2, ordered) by an independent sweep to compare with logs/split_exactness.txt.
"""
import sys, itertools


def read_points(fn):
    return [tuple(int(t) for t in l.split()[:2]) for l in open(fn) if len(l.split()) >= 2]


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


def enumerate_onesided(P):
    n = len(P)
    S = [[[sgn(orient(P[i], P[j], P[k])) for k in range(n)] for j in range(n)] for i in range(n)]
    sols = []
    side = [None] * n  # True: A, False: B
    nodes = [0]

    def consistent(m):
        # check all constraints involving point m with the already assigned points 0..m-1 (and m)
        X = [i for i in range(m + 1) if side[i] == side[m]]
        Y = [i for i in range(m + 1) if side[i] != side[m]]
        # (1) pairs (m, x) with x in X: all of Y strictly on one side
        for x in X:
            if x == m:
                continue
            ss = {S[m][x][y] for y in Y}
            if 0 in ss or len(ss) > 1:
                return False
        # (2) pairs (x, x') in X \ {m}: point m (in Y-role? no: m is in X) -- m is on X's side, so constraints are
        # pairs (y, y') in Y with m: m must be strictly on the same side as the other X-points
        for y, y2 in itertools.combinations(Y, 2):
            ss = {S[y][y2][x] for x in X}
            if 0 in ss or len(ss) > 1:
                return False
        return True

    def rec(m):
        nodes[0] += 1
        if m == n:
            a = sum(1 for s in side if s)
            if a >= 2 and n - a >= 2:
                sols.append(frozenset(i for i in range(n) if side[i]))
            return
        for val in (True, False):
            side[m] = val
            if consistent(m):
                rec(m + 1)
            side[m] = None

    rec(0)
    return sols, nodes[0]


def linear_partitions_count(P):
    """Ordered linear partitions with both sides >= 2, via: for every ordered pair (i, j) the open left side L of
    the directed line P_i -> P_j, and the four ways of adding i, j.  Collect distinct sets X."""
    n = len(P)
    sets = set()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            L = frozenset(k for k in range(n) if k not in (i, j) and orient(P[i], P[j], P[k]) > 0)
            for extra in ((), (i,), (j,), (i, j)):
                X = L | frozenset(extra)
                if 2 <= len(X) <= n - 2:
                    sets.add(X)
    return len(sets)


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        P = read_points(fn)
        sols, nodes = enumerate_onesided(P)
        lp = linear_partitions_count(P)
        n = len(P)
        print(f"{fn.rsplit('/',1)[-1]}: n={n} one-sided partitions={len(sols)} (search nodes {nodes}); "
              f"ordered linear partitions (both sides >=2)={lp}")
        for X in sols:
            print("    A =", sorted(X))
