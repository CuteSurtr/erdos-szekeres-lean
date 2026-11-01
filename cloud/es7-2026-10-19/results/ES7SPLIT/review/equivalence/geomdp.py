#!/usr/bin/env python3
"""Exact cap/cup/gon computations for point sets with distinct x-coordinates
(integer or Fraction coordinates).  gon(P) = max over l<r of maxcup(l,r)+maxcap(l,r)-2,
using that a set with distinct x-coordinates is in convex position iff it is the union
of a cup and a cap with common first and last points."""
import itertools

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def general_position(P):
    return all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))

def distinct_x(P):
    return len({p[0] for p in P}) == len(P)

def chain_table(P, sign):
    """M[l][r] = longest chain from P[l] to P[r] (P sorted by x) all of whose triples have
    orientation sign `sign` (+1: cup, -1: cap). M[l][r] >= 2 for l < r."""
    n = len(P)
    M = [[0]*n for _ in range(n)]
    for l in range(n):
        f = {}
        for j in range(l+1, n):
            f[(l, j)] = 2
        for i in range(l+1, n):
            for j in range(i+1, n):
                best = 0
                for k in range(l, i):
                    v = f.get((k, i), 0)
                    if v and v + 1 > best and sign * orient(P[k], P[i], P[j]) > 0:
                        best = v + 1
                if best:
                    f[(i, j)] = best
        for r in range(l+1, n):
            M[l][r] = max(f.get((i, r), 0) for i in range(l, r))
    return M

def analyse(P):
    P = sorted(P)
    assert distinct_x(P)
    n = len(P)
    cup = chain_table(P, +1); cap = chain_table(P, -1)
    maxcup = max(cup[l][r] for l in range(n) for r in range(l+1, n))
    maxcap = max(cap[l][r] for l in range(n) for r in range(l+1, n))
    g = max(cup[l][r] + cap[l][r] - 2 for l in range(n) for r in range(l+1, n))
    return {'n': n, 'gon': g, 'maxcap': maxcap, 'maxcup': maxcup}

def brute_gon(P):
    def conv(Q):
        for i, p in enumerate(Q):
            o = Q[:i] + Q[i+1:]
            for a, b, c in itertools.combinations(o, 3):
                s = (orient(a, b, p), orient(b, c, p), orient(c, a, p))
                if all(x > 0 for x in s) or all(x < 0 for x in s):
                    return False
        return True
    for r in range(len(P), 0, -1):
        for c in itertools.combinations(P, r):
            if conv(list(c)):
                return r
    return 0

if __name__ == '__main__':
    # self-test against brute force on random small sets
    import random
    rng = random.Random(5)
    bad = 0
    for t in range(300):
        n = rng.randint(3, 9)
        while True:
            P = list({(rng.randint(-30, 30), rng.randint(-30, 30)) for _ in range(n)})
            if len(P) == n and general_position(P) and distinct_x(P):
                break
        a = analyse(P)
        b = brute_gon(P)
        # brute cap/cup
        Ps = sorted(P)
        bc = max(len(c) for r in range(1, n+1) for c in itertools.combinations(Ps, r)
                 if all(orient(c[i], c[j], c[k]) < 0 for i, j, k in itertools.combinations(range(len(c)), 3)))
        bu = max(len(c) for r in range(1, n+1) for c in itertools.combinations(Ps, r)
                 if all(orient(c[i], c[j], c[k]) > 0 for i, j, k in itertools.combinations(range(len(c)), 3)))
        if a['gon'] != b or a['maxcap'] != bc or a['maxcup'] != bu:
            bad += 1; print('MISMATCH', P, a, b, bc, bu)
    print('self-test 300 random sets, mismatches:', bad)
