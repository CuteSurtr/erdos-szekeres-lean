"""Exact integer geometry helpers (written independently; no code shared with results/SYM2).

orient(p,q,r) > 0  <=>  p -> q -> r turns left (counterclockwise).
max_convex_dp(P): size of the largest subset of P in convex position (P in general position), by the standard
  O(n^4) dynamic program anchored at the lowest vertex: chains a -> p_i -> p_j with left turns, closed at a.
"""
from functools import cmp_to_key
from itertools import combinations


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(v):
    return (v > 0) - (v < 0)


def collinear_triples(P):
    return [(a, b, c) for a, b, c in combinations(range(len(P)), 3) if orient(P[a], P[b], P[c]) == 0]


def orient_table(P):
    n = len(P)
    T = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if b == a:
                continue
            for c in range(n):
                if c == a or c == b:
                    continue
                T[a][b][c] = sgn(orient(P[a], P[b], P[c]))
    return T


def max_convex_dp(P, T=None):
    n = len(P)
    if T is None:
        T = orient_table(P)
    best = min(n, 2)
    idx = list(range(n))
    for a in idx:
        up = [i for i in idx if (P[i][1], P[i][0]) > (P[a][1], P[a][0])]
        up.sort(key=cmp_to_key(lambda i, j: -1 if T[a][i][j] > 0 else 1))
        m = len(up)
        D = [[0] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                if T[a][up[i]][up[j]] <= 0:
                    continue
                v = 3
                for h in range(i):
                    if D[h][i] and D[h][i] + 1 > v and T[up[h]][up[i]][up[j]] > 0:
                        v = D[h][i] + 1
                D[i][j] = v
                if T[up[i]][up[j]][a] > 0 and v > best:
                    best = v
    return best


def in_convex_position(S):
    """Brute-force criterion (general position assumed): no point of S inside a triangle of three others."""
    for t in range(len(S)):
        others = S[:t] + S[t + 1:]
        for x, y, z in combinations(others, 3):
            o1, o2, o3 = sgn(orient(x, y, S[t])), sgn(orient(y, z, S[t])), sgn(orient(z, x, S[t]))
            if o1 == o2 == o3:
                return False
    return True
