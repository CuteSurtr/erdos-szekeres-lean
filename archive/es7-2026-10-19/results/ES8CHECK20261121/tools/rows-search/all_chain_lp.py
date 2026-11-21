#!/usr/bin/env python3
"""rows-search: (i) max size of a maximal (a-cap, b-cup)-chain-free class vs. its capacity, for 3 <= a,b <= 7;
(ii) root LP with catalog + Z + Z* + ALL (6,6) chain rows h(C) >= |C| - 55 (|C| >= 56), h0 = h1 = 0."""
import sys
from math import comb
import numpy as np
sys.path.insert(0, '<scratch>/agents/rows-search')
import chainrows as cr
from witness_rows import solve
N = cr.N
fam = {}
for a in range(3, 8):
    fam[('cap', a)] = list(cr.chain_free_classes(a, cr.S)); fam[('cup', a)] = list(cr.chain_free_classes(a, cr.ST))
M = {k: np.array([[1.0 if j in c else 0.0 for j in range(N)] for c in v]) for k, v in fam.items()}
for a in range(3, 8):
    line = []
    for b in range(3, 8):
        if a == 7 and b == 7: continue
        cap = 55 if (a, b) == (6, 6) else comb(a + b - 4, a - 2)
        mx = int((M[('cap', a)] @ M[('cup', b)].T).max())
        line.append('(%d,%d): max %d cap %d' % (a, b, mx, cap))
    print('; '.join(line), flush=True)
A6, B6 = fam[('cap', 6)], fam[('cup', 6)]
SZ = M[('cap', 6)] @ M[('cup', 6)].T
bits = set()
for i, j in zip(*np.where(SZ >= 56)):
    bits.add(frozenset(A6[i] & B6[j]))
rows = [({s: 1 for s in sup}, r) for sup, r in cr.ROWS] + [({s: 1 for s in cr.Z}, 15), ({s: 1 for s in cr.Zs}, 15)]
extra = [({s: 1 for s in C}, len(C) - 55) for C in bits]
print('distinct (6,6) chain-free intersections with >= 56 states: %d (rows added)' % len(extra), flush=True)
v0, _ = solve(rows); v1, _ = solve(rows + extra)
print('root LP catalog+Z+Z*: %.6f ; + all chain rows: %.6f' % (v0, v1), flush=True)
