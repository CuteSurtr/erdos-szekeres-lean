#!/usr/bin/env python3
"""Decode a CaDiCaL model of m33k7int.sub.cnf (+units) and check it by brute force.

  checksat.py MODEL [N=33]
X(i,j,k) for i<j<k is variable idx (lex order of triples); the sub CNF uses the smaller index of
the mirror orbit {X(i,j,k), X(N+1-k,N+1-j,N+1-i)} (results/C/scripts/mirgen.py).  Checks:
signotope axioms (every 4-tuple: the sequence X(jkl),X(ikl),X(ijl),X(ijk) changes sign at most
once), mirror symmetry, axis point (N+1)/2 not extreme (some cup and some cap through it), and no
convex 7-gon (no cup of a points and cap of b points with common endpoints, a+b-2 >= 7)."""
import itertools, sys
N = int(sys.argv[2]) if len(sys.argv) > 2 else 33
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
m = N + 1
val = {}
for l in open(sys.argv[1]):
    if l.startswith("v"):
        for x in map(int, l.split()[1:]):
            if x: val[abs(x)] = x > 0
def rep(t):
    i, j, k = t; return min(idx[t], idx[(m - k, m - j, m - i)])
X = {t: val[rep(t)] for t in idx}
bad_sig = 0
for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
    s = [X[(j, k, l)], X[(i, k, l)], X[(i, j, l)], X[(i, j, k)]]
    if sum(s[a] != s[a + 1] for a in range(3)) > 1: bad_sig += 1
bad_mir = sum(X[(i, j, k)] != X[(m - k, m - j, m - i)] for (i, j, k) in idx)
c = (N + 1) // 2
cups = [X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
interior = any(cups) and not all(cups)
def longest(sign):
    # L[(a,b)] = most points of a chain (cup if sign) ending with a<b
    L = {}
    for b in range(1, N + 1):
        for a in range(1, b):
            L[(a, b)] = 2 + 0
            for p in range(1, a):
                if X[(p, a, b)] == sign and L[(p, a)] + 1 > L[(a, b)]: L[(a, b)] = L[(p, a)] + 1
    return L
def best_between(sign):
    # B[(s,e)] = most points of a chain from s to e
    B = {}
    for s in range(1, N + 1):
        L = {}
        for b in range(s + 1, N + 1):
            for a in range(s, b):
                if a == s: L[(a, b)] = 2; continue
                if (s, a) not in L: continue
                v = max((L[(p, a)] + 1 for p in range(s, a) if (p, a) in L and X[(p, a, b)] == sign), default=None)
                if v: L[(a, b)] = v
            B[(s, b)] = max(L[(a, b)] for a in range(s, b) if (a, b) in L)
    return B
cup, cap = best_between(True), best_between(False)
k = max(cup[e] + cap[e] - 2 for e in cup)
print({"signotope_violations": bad_sig, "mirror_violations": bad_mir, "axis_interior": interior,
       "largest_convex_gon": k, "VALID": bad_sig == 0 and bad_mir == 0 and interior and k < 7})
