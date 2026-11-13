#!/usr/bin/env python3
"""Check that the clsat2.py formula (m, n, sig) is invariant under the y-reflection sigma:
L[i,j,v] -> -L[i,j,B-v], T[i,j,k] -> -T[i,j,k], CU[i,j,l] <-> CA[i,j,l], G[x,a] <-> H[x,a] (B = m-2).
usage: sigma.py m n CNF   -> prints 'INVARIANT' if sigma maps the clause multiset onto itself; writes sigma map (json)."""
import sys, json
from itertools import combinations
from collections import Counter
m, n, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
B = m - 2; nv = 0
def new():
    global nv; nv += 1; return nv
L = {(i, j, v): new() for i, j in combinations(range(n), 2) for v in range(1, B)}
T = {t: new() for t in combinations(range(n), 3)}
CU = {(i, j, l): new() for i, j in combinations(range(n), 2) for l in range(3, m + 1)}
CA = {(i, j, l): new() for i, j in combinations(range(n), 2) for l in range(3, m + 1)}
G = {(x, a): new() for x in range(1, m) for a in range(2, m + 1)}
H = {(x, a): new() for x in range(1, m) for a in range(2, m + 1)}
sig = [0] * (nv + 1)
for (i, j, v), x in L.items(): sig[x] = -L[i, j, B - v]
for t, x in T.items(): sig[x] = -x
for k, x in CU.items(): sig[x] = CA[k]
for k, x in CA.items(): sig[x] = CU[k]
for k, x in G.items(): sig[x] = H[k]
for k, x in H.items(): sig[x] = G[k]
assert all(sig[1:]) and sorted(abs(s) for s in sig[1:]) == list(range(1, nv + 1))
def s(l): return sig[l] if l > 0 else -sig[-l]
cls = []
with open(path) as f:
    hdr = f.readline().split(); assert int(hdr[2]) == nv, (hdr, nv)
    for line in f:
        c = list(map(int, line.split()))[:-1]; cls.append(tuple(sorted(c)))
A = Counter(cls); Bc = Counter(tuple(sorted(s(l) for l in c)) for c in cls)
print('vars', nv, 'clauses', len(cls), 'INVARIANT' if A == Bc else 'NOT invariant')
json.dump({'sigma': sig, 'G': {'%d,%d' % k: v for k, v in G.items()}, 'H': {'%d,%d' % k: v for k, v in H.items()}}, open(path + '.sigma.json', 'w'))
