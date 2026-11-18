#!/usr/bin/env python3
"""geom.py -- exact helpers for real point sets (integer coordinates), used for positive controls.

orient(P)            : dict (i,j,k) -> +1 (cup: k above line ij ... i.e. counterclockwise) / -1
brute_convex_gon(P,G): independent brute-force test "G points in convex position" (4-point
                       Caratheodory table), not using caps/cups
longest_cap_cup(P)   : longest cap, longest cup (DP on pairs)
upper_hull(P)        : indices of the upper hull (monotone chain)
"""
import itertools, json, sys


def load(path):
    P = [tuple(p) for p in json.load(open(path))]
    P = sorted(P)
    assert len({p[0] for p in P}) == len(P), 'distinct x required'
    return P


def det(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def orient(P):
    n = len(P)
    S = {}
    for i, j, k in itertools.combinations(range(n), 3):
        d = det(P[i], P[j], P[k])
        assert d != 0, 'general position required'
        S[(i, j, k)] = 1 if d > 0 else -1
    return S


def mirror(P):
    return sorted((-x, y) for x, y in P)


def longest_cap_cup(P, S=None):
    n = len(P)
    S = S or orient(P)
    best = {}
    for sgn in (1, -1):
        L = {}
        for j in range(n):
            for k in range(j + 1, n):
                L[(j, k)] = 2
        for k in range(n):
            for j in range(k):
                for i in range(j):
                    if S[(i, j, k)] == sgn and L[(i, j)] + 1 > L[(j, k)]:
                        L[(j, k)] = L[(i, j)] + 1
        best[sgn] = max(L.values()) if L else min(n, 1)
    return best[-1], best[1]      # (cap, cup)


def brute_convex_gon(P, G, S=None):
    """True iff some G points are in convex position.  Independent of cap/cup logic:
    4 points are in convex position iff none is inside the triangle of the other three;
    G points are in convex position iff all their 4-subsets are (Caratheodory)."""
    n = len(P)
    S = S or orient(P)

    def sg(a, b, c):
        t = tuple(sorted((a, b, c)))
        s = S[t]
        # parity of the permutation taking sorted order to (a,b,c)
        perm = [t.index(a), t.index(b), t.index(c)]
        inv = sum(1 for x in range(3) for y in range(x + 1, 3) if perm[x] > perm[y])
        return s if inv % 2 == 0 else -s

    def inside(p, a, b, c):
        s1, s2, s3 = sg(a, b, p), sg(b, c, p), sg(c, a, p)
        return s1 == s2 == s3
    conv4 = set()
    for q in itertools.combinations(range(n), 4):
        ok = True
        for x in q:
            a, b, c = [y for y in q if y != x]
            if inside(x, a, b, c):
                ok = False
                break
        if ok:
            conv4.add(q)
    # grow convex k-sets level by level (every 4-subset convex)
    level = conv4
    for size in range(5, G + 1):
        nxt = set()
        for q in level:
            for x in range(q[-1] + 1, n):
                r = q + (x,)
                if all(tuple(sub) in level for sub in itertools.combinations(r, size - 1)):
                    nxt.add(r)
        level = nxt
        if not level:
            return False
    return bool(level)


def upper_hull(P):
    H = []
    for i, p in enumerate(P):
        while len(H) >= 2 and det(P[H[-2]], P[H[-1]], p) >= 0:
            H.pop()
        H.append(i)
    return tuple(H)


if __name__ == '__main__':
    P = load(sys.argv[1])
    G = int(sys.argv[2])
    S = orient(P)
    print('n', len(P), 'cap,cup', longest_cap_cup(P, S), 'has convex %d-gon:' % G, brute_convex_gon(P, G, S),
          'upper hull', upper_hull(P))
