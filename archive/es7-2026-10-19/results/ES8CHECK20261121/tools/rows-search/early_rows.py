#!/usr/bin/env python3
"""rows-search: 'early point' packing rows. The j-th point (x-order) of H has a state whose corners (a,b) all satisfy
a + b <= j (the cap and the cup attaining a corner end with the same edge (u,v), their other points lie on opposite
sides of line uv, so they use a + b distinct points among the first j). The first j points have distinct states, so
|occupied cap E_j| >= j, i.e. h(E_j) <= |E_j| - j (n >= j). LP test at the root of catalog + Z + Z* (h0 = h1 = 0)."""
import sys
import numpy as np, highspy
sys.path.insert(0, '<scratch>/agents/rows-search')
import chainrows as cr
from witness_rows import corners, solve
N = cr.N; S = cr.S
rows = [({s: 1 for s in sup}, r) for sup, r in cr.ROWS] + [({s: 1 for s in cr.Z}, 15), ({s: 1 for s in cr.Zs}, 15)]
v0, x0 = solve(rows)
er = []
for j in range(2, 11):
    E = [i for i, s in enumerate(S) if all(a + b <= j for a, b in corners(s))]
    co = {i: -1 for i in E}; er.append((co, j - len(E)))
    print('j=%d |E_j|=%d  x*(E_j)=%.3f  row h(E_j) <= %d' % (j, len(E), x0[E].sum(), len(E) - j), flush=True)
v1, _ = solve(rows + er)
print('root LP %.6f -> with early rows %.6f' % (v0, v1), flush=True)
