#!/usr/bin/env python3
"""Compact (DP) version of clsat.py: the same relaxation of Proposition C (i) for an n-point cluster, single orbit.
Instead of one clause per chain, auxiliary variables CU[i,j,l] / CA[i,j,l] mean "some cup / cap with >= l points
ends with the edge (i,j)" (only the forcing direction is encoded, which real configurations satisfy when the
variables are given their true values).  Facts (a)-(e) as in clsat.py; the signotope axiom (c) is optional
(flag sig=1) because it has O(n^4) clauses.  UNSAT => no real cluster of n points satisfies Prop. C (i).
usage: clsat2.py m n sig out.cnf
"""
import sys
from itertools import combinations
m, n, sig, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
B = m - 2
nv = 0
def new():
    global nv; nv += 1; return nv
L = {(i, j, v): new() for i, j in combinations(range(n), 2) for v in range(1, B)}
T = {t: new() for t in combinations(range(n), 3)}
CU = {(i, j, l): new() for i, j in combinations(range(n), 2) for l in range(3, m + 1)}
CA = {(i, j, l): new() for i, j in combinations(range(n), 2) for l in range(3, m + 1)}
G = {(x, a): new() for x in range(1, m) for a in range(2, m + 1)}
H = {(x, a): new() for x in range(1, m) for a in range(2, m + 1)}
cl = []
def le(i, j, v):
    if v <= 0: return None
    if v >= B: return True
    return L[i, j, v]
def notle(i, j, v):
    x = le(i, j, v)
    if x is None: return True
    if x is True: return None
    return -x
def clause(lits):
    o = []
    for l in lits:
        if l is True: return
        if l is None: continue
        o.append(l)
    cl.append(o)
for i, j in combinations(range(n), 2):
    for v in range(1, B - 1):
        cl.append([-L[i, j, v], L[i, j, v + 1]])
for i, j, k in combinations(range(n), 3):
    t = T[i, j, k]
    for v in range(1, B):
        clause([notle(i, j, v), le(j, k, v), t])
        clause([notle(j, k, v), le(i, j, v), -t])
    for v in range(1, B + 1):
        clause([le(i, j, v - 1), le(j, k, v - 1), notle(i, k, v - 1)])
        clause([notle(i, j, v), notle(j, k, v), le(i, k, v)])
    # chain DP: a cup ending with (i,j) extends by k if left turn at j
    clause([-t, CU[j, k, 3]])
    clause([t, CA[j, k, 3]])
    for l in range(4, m + 1):
        clause([-CU[i, j, l - 1], -t, CU[j, k, l]])
        clause([-CA[i, j, l - 1], t, CA[j, k, l]])
if sig:
    for i, j, k, l in combinations(range(n), 4):
        s = [T[i, j, k], T[i, j, l], T[i, k, l], T[j, k, l]]
        for a, b, c in combinations(range(4), 3):
            cl.append([-s[a], s[b], -s[c]]); cl.append([s[a], -s[b], s[c]])
for i, j in combinations(range(n), 2):
    for x in range(1, m):
        clause([notle(i, j, x - 1), G[x, 2]])
        clause([le(i, j, m - x - 1), H[x, 2]])
        for a in range(3, m + 1):
            clause([-CU[i, j, a], notle(i, j, x - 1), G[x, a]])
            clause([-CA[i, j, a], le(i, j, m - x - 1), H[x, a]])
for x in range(1, m):
    for a in range(3, m + 1):
        cl.append([-G[x, a], G[x, a - 1]]); cl.append([-H[x, a], H[x, a - 1]])
    for a in range(2, m + 1):
        if a > x: cl.append([-G[x, a]]); cl.append([-H[x, a]])
        for b in range(2, m + 1):
            if a + b > x + 1: cl.append([-G[x, a], -H[x, b]])
with open(out, 'w') as f:
    f.write('p cnf %d %d\n' % (nv, len(cl)))
    for c in cl:
        f.write(' '.join(map(str, c)) + ' 0\n')
print('m=%d n=%d sig=%d vars=%d clauses=%d' % (m, n, sig, nv, len(cl)))
