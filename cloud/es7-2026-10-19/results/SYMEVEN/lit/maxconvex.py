#!/usr/bin/env python3
"""Exact size of the largest subset in convex position (points in general position, integer coordinates).
O(n^4) DP: anchor a = lowest vertex (by (y, x)); others sorted by angle around a; f[i][j] = longest convex chain
a -> ... -> v_i -> v_j with all turns left."""
import itertools
from functools import cmp_to_key

def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])

def max_convex(P):
    n = len(P)
    if n <= 3: return n
    best = 3
    for a in P:
        V = [q for q in P if (q[1], q[0]) > (a[1], a[0])]
        if len(V) + 1 <= best: continue
        V.sort(key=cmp_to_key(lambda p, q: -1 if orient(a, p, q) > 0 else 1))
        m = len(V)
        f = [[0]*m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                val = 3
                for h in range(i):
                    if f[h][i] and orient(V[h], V[i], V[j]) > 0 and f[h][i] + 1 > val:
                        val = f[h][i] + 1
                f[i][j] = val
                if val > best and orient(V[i], V[j], a) > 0:
                    best = val
    return best

def brute(P):
    def convex(T):
        for i in range(len(T)):
            for a, b, c in itertools.combinations([j for j in range(len(T)) if j != i], 3):
                o1 = orient(T[a], T[b], T[i]); o2 = orient(T[b], T[c], T[i]); o3 = orient(T[c], T[a], T[i])
                if (o1 > 0) == (o2 > 0) == (o3 > 0): return False
        return True
    for r in range(len(P), 2, -1):
        for T in itertools.combinations(P, r):
            if convex(list(T)): return r
    return min(len(P), 2)

if __name__ == '__main__':
    import random, sys
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    bad = 0; tested = 0
    for trial in range(300):
        n = random.randint(4, 11)
        while True:
            P = list({(random.randint(-30, 30), random.randint(-30, 30)) for _ in range(n)})
            if all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3)): break
        d, b = max_convex(P), brute(P); tested += 1
        if d != b: bad += 1; print('MISMATCH', P, d, b)
    print(f'tested {tested} random general-position sets, mismatches: {bad}')
