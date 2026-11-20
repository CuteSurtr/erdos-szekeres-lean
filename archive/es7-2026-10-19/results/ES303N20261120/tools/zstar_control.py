#!/usr/bin/env python3
"""Exact control for the Z*-row lemma (own code from the Lean definitions, as lemmaz_control.py):
  capLabel(u,v) = (points of the longest cap ending with edge (u,v)) - 1, cupLabel likewise;
  f_v(i) = max{cupLabel(u,v) : u < v, capLabel(u,v) >= i+1}, else 0.
Claim (THEORY310N Lemma B, both halves): in a set with no 7-cap and no 7-cup, the owners of
  Z* = {f(0) = 5, f(4) >= 1} (a 6-cup and a 6-cap end at the point) contain no 6-cap and no 6-cup.
Test sets: the Erdos-Szekeres cup-cap construction X(7,7) (252 points, exact integers) and random subsets of it.
Also re-checks injectivity and Lemma Z, and runs negative controls (each half of the condition alone is not enough).
usage: zstar_control.py SUBSETS SEED"""
import random, sys
from math import comb

def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def es(k, l):
    """X(k,l): C(k+l-4, k-2) points, distinct x, general position, no k-cup, no l-cap (exact integers)."""
    if k == 2 or l == 2: return [(0, 0)]
    L, R = es(k - 1, l), es(k, l - 1)
    def flat(P):
        ys = [y for _, y in P]; F = 2 * (max(ys) - min(ys)) + 2
        return [(x * F, y) for x, y in P]
    L, R = flat(L), flat(R)
    xL = max(x for x, _ in L) - min(x for x, _ in L); xR0 = max(x for x, _ in L) + 1 - min(x for x, _ in R)
    Y = max(abs(y) for _, y in L + R); W = xL + (max(x for x, _ in R) - min(x for x, _ in R)) + 2
    D = 4 * Y + 2 * W + 2
    return L + [(x + xR0, y + D) for x, y in R]

def chains(P):
    n = len(P); cap = [[0] * n for _ in range(n)]; cup = [[0] * n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            cap[u][v] = cup[u][v] = 2
            for t in range(u):
                o = orient(P[t], P[u], P[v])
                if o < 0: cap[u][v] = max(cap[u][v], cap[t][u] + 1)
                elif o > 0: cup[u][v] = max(cup[u][v], cup[t][u] + 1)
                else: raise ValueError('collinear')
    return cap, cup

def longest(S, P, kind):
    best = {}; m = 1 if S else 0
    for j, v in enumerate(S):
        for i in range(j):
            u = S[i]; best[(u, v)] = 2
            for t in S[:i]:
                if orient(P[t], P[u], P[v]) * kind > 0: best[(u, v)] = max(best[(u, v)], best[(t, u)] + 1)
            m = max(m, best[(u, v)])
    return m

def check(P, stats):
    P = sorted(P); n = len(P)
    assert len({x for x, _ in P}) == n
    cap, cup = chains(P)
    assert max(max(r) for r in cap) <= 6 and max(max(r) for r in cup) <= 6, 'class violated'
    F = []
    for v in range(n):
        f = []
        for i in range(5):
            vals = [cup[u][v] - 1 for u in range(v) if cap[u][v] - 1 >= i + 1]
            f.append(max(vals) if vals else 0)
        F.append(tuple(f))
    assert len(set(F)) == n, 'states not injective'
    own = lambda p: [v for v in range(n) if p(F[v])]
    Zs, Z = own(lambda f: f[0] == 5 and f[4] >= 1), own(lambda f: f[0] <= 4 and f[4] == 0)
    for name, O in (('Z*', Zs), ('Z', Z)):
        lc, lu = longest(O, P, -1), longest(O, P, +1)
        assert lc <= 5 and lu <= 5, '%s lemma fails: cap %d cup %d' % (name, lc, lu)
    stats['sets'] += 1; stats['zstar_owners_max'] = max(stats['zstar_owners_max'], len(Zs)); stats['zstar_owners_sum'] += len(Zs)
    # negative controls: one half of the condition alone
    if longest(own(lambda f: f[0] == 5), P, +1) >= 6: stats['neg_cupend_has_6cup'] += 1
    if longest(own(lambda f: f[4] >= 1), P, -1) >= 6: stats['neg_capend_has_6cap'] += 1
    if longest(own(lambda f: f[0] >= 4 and f[4] >= 1), P, +1) >= 6: stats['neg_wider_has_6cup'] += 1
    return len(set(F))

subsets, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
X = es(7, 7); assert len(X) == comb(10, 5) == 252
stats = dict(sets=0, zstar_owners_max=0, zstar_owners_sum=0, neg_cupend_has_6cup=0, neg_capend_has_6cap=0, neg_wider_has_6cup=0)
nstates = check(X, stats); print('ES(7,7): %d points, %d distinct states, Z* owners %d' % (len(X), nstates, stats['zstar_owners_max']), flush=True)
for t in range(subsets):
    keep = rng.uniform(0.35, 0.95)
    P = [p for p in X if rng.random() < keep]
    if len(P) >= 8: check(P, stats)
    if (t + 1) % 25 == 0: print(stats, flush=True)
print('DONE', stats, flush=True)
