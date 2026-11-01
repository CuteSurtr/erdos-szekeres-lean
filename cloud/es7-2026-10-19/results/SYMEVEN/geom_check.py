#!/usr/bin/env python3
"""
Exact (integer) verification routines, independent of construct.py.
  - orient, general position, central symmetry
  - (A) largest convex subset: angular DP around the lowest vertex (with witness)
  - (B) largest convex subset: lower cup + upper cap DP over lexicographic order
  - (C) brute force: enumerate subsets, convex position via Andrew monotone-chain hull
  - counting DP: number of convex j-gons for every j (angular DP with counts)
  - longest cup / longest cap (for cluster parameters)
"""
from functools import cmp_to_key
from itertools import combinations


def read_points(path):
    pts, lab = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            t = line.split()
            pts.append((int(t[0]), int(t[1])))
            lab.append(int(t[2]) if len(t) > 2 else None)
    return pts, lab


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def general_position_violations(P):
    bad = []
    n = len(P)
    for i in range(n):
        a = P[i]
        for j in range(i + 1, n):
            b = P[j]
            bx, by = b[0] - a[0], b[1] - a[1]
            for l in range(j + 1, n):
                c = P[l]
                if bx * (c[1] - a[1]) - by * (c[0] - a[0]) == 0:
                    bad.append((i, j, l))
    return bad


def symmetry_report(P):
    S = set(P)
    return dict(n=len(P), distinct=len(S) == len(P), centrally_symmetric=all((-x, -y) in S for (x, y) in P),
                origin_absent=(0, 0) not in S)


# ---------------------------------------------------------------- (A) angular DP
def largest_convex_angular(P):
    """Max number of points of P in convex position (P in general position).
    For each p as lowest vertex (lexicographically smallest (y,x)), sort the points above p by angle
    and run dp[i][j] = max #vertices of a convex chain p,...,v_i,v_j with all left turns.
    Returns (size, witness list)."""
    n = len(P)
    if n < 3:
        return n, list(P)
    best, wit = 2, list(P[:2])
    for p in P:
        above = [q for q in P if (q[1], q[0]) > (p[1], p[0])]
        if len(above) + 1 <= best:
            continue

        def cmp(q1, q2, p=p):
            o = orient(p, q1, q2)
            return -1 if o > 0 else (1 if o < 0 else 0)

        above.sort(key=cmp_to_key(cmp))
        t = len(above)
        dp = [[0] * t for _ in range(t)]
        par = [[-1] * t for _ in range(t)]
        for j in range(t):
            vj = above[j]
            for i in range(j):
                vi = above[i]
                bv, bp = 3, -1
                dpi = [dp[h][i] for h in range(i)]
                for h in range(i):
                    if dpi[h] + 1 > bv and orient(above[h], vi, vj) > 0:
                        bv, bp = dpi[h] + 1, h
                dp[i][j] = bv
                par[i][j] = bp
                if bv > best and orient(vi, vj, p) > 0:
                    best = bv
                    chain = [j, i]
                    a, b = i, j
                    while par[a][b] != -1:
                        h = par[a][b]
                        chain.append(h)
                        a, b = h, a
                    wit = [p] + [above[x] for x in reversed(chain)]
    return best, wit


# ---------------------------------------------------------------- (B) cup + cap DP
def largest_convex_cupcap(P):
    """Sort lexicographically (= x-order after an infinitesimal rotation). A set is in convex position iff
    it is the union of a cup and a cap with common first point a and last point b.
    For each a: Cu[i][j] = longest cup a,...,v_i,v_j ; Ca similarly; answer max_b fcup(b)+fcap(b)-2."""
    V = sorted(P)
    n = len(V)
    if n < 3:
        return n
    best = 2
    NEG = -10 ** 9
    for a in range(n):
        idx = list(range(a + 1, n))
        Cu = {}
        Ca = {}
        for j in idx:
            vj = V[j]
            fu = 2
            fc = 2
            Cu[(a, j)] = 2
            Ca[(a, j)] = 2
            for i in range(a + 1, j):
                vi = V[i]
                bu, bc = NEG, NEG
                for h in range(a, i):
                    o = orient(V[h], vi, vj)
                    if o > 0:
                        x = Cu[(h, i)]
                        if x > 0 and x + 1 > bu:
                            bu = x + 1
                    elif o < 0:
                        x = Ca[(h, i)]
                        if x > 0 and x + 1 > bc:
                            bc = x + 1
                Cu[(i, j)] = bu if bu > 0 else 0
                Ca[(i, j)] = bc if bc > 0 else 0
                if bu > fu:
                    fu = bu
                if bc > fc:
                    fc = bc
            if fu + fc - 2 > best:
                best = fu + fc - 2
    return best


# ---------------------------------------------------------------- (C) brute force
def hull_size(Q):
    """Andrew monotone chain with strict turns; returns number of hull vertices."""
    Q = sorted(set(Q))
    if len(Q) <= 2:
        return len(Q)
    lower = []
    for p in Q:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(Q):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower) + len(upper) - 2


def in_convex_position(Q):
    return hull_size(Q) == len(Q)


def brute_largest(Q):
    Q = list(Q)
    for s in range(len(Q), 2, -1):
        for c in combinations(Q, s):
            if in_convex_position(c):
                return s
    return min(len(Q), 2)


# ---------------------------------------------------------------- counting DP
def count_convex_by_size(P, maxlen):
    """cnt[L] = number of L-subsets of P in convex position, for 3 <= L <= maxlen (angular DP with counts)."""
    tot = [0] * (maxlen + 1)
    for p in P:
        above = [q for q in P if (q[1], q[0]) > (p[1], p[0])]

        def cmp(q1, q2, p=p):
            o = orient(p, q1, q2)
            return -1 if o > 0 else (1 if o < 0 else 0)

        above.sort(key=cmp_to_key(cmp))
        t = len(above)
        # C[i][j][L]: number of convex chains p,...,v_i,v_j with L vertices, all left turns
        C = [[None] * t for _ in range(t)]
        for j in range(t):
            vj = above[j]
            for i in range(j):
                vi = above[i]
                arr = [0] * (maxlen + 1)
                arr[3] = 1
                for h in range(i):
                    if orient(above[h], vi, vj) > 0:
                        src = C[h][i]
                        for L in range(3, maxlen):
                            if src[L]:
                                arr[L + 1] += src[L]
                C[i][j] = arr
                if orient(vi, vj, p) > 0:
                    for L in range(3, maxlen + 1):
                        tot[L] += arr[L]
    return tot


# ---------------------------------------------------------------- cups and caps
def longest_cup_cap(P):
    """Longest cup and longest cap of P (lexicographic order)."""
    V = sorted(P)
    n = len(V)
    if n <= 2:
        return n, n
    cu = [[2] * n for _ in range(n)]
    ca = [[2] * n for _ in range(n)]
    bu = bc = 2
    for j in range(n):
        for i in range(j):
            for h in range(i):
                o = orient(V[h], V[i], V[j])
                if o > 0 and cu[h][i] + 1 > cu[i][j]:
                    cu[i][j] = cu[h][i] + 1
                elif o < 0 and ca[h][i] + 1 > ca[i][j]:
                    ca[i][j] = ca[h][i] + 1
            bu = max(bu, cu[i][j])
            bc = max(bc, ca[i][j])
    return bu, bc
