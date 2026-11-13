#!/usr/bin/env python3
"""In/out double injection with Hall constraints (balanced catalog).

For a balanced H, every point v has an in-state I(v) (downset of (E_- - 1, E_+ - 1)
over u < v) and an out-state O(v) (downset of (F_- - 1, F_+ - 1) over w > v).  The
out-states are the in-states of the x-reversed configuration, which is balanced, so
both occupied sets satisfy all 3,131 rows, both contain state 0, and both have size n_H.
Compatibility: for u < v < w the triple is a cap or a cup, and the concatenated chains
give a + a' <= 5 or b + b' <= 5 for every in-cell (a,b) of I(v) and out-cell (a',b') of
O(v).  The points give a perfect matching between occupied in- and out-states inside
the compatibility graph, so Hall's condition holds:
  for X = {I contains C}:  #occ_in(X) <= #occ_out(N(X)),  N(X) = {O : comp(down(C), O)},
and symmetrically.  LP with both vectors, equal population, Hall rows for all C of size
1 and 2."""
import itertools, json, sys
import numpy as np, highspy
sys.argv_saved = sys.argv; sys.argv = [sys.argv[0]]
from cap_lp import bal
S, C = bal['states'], bal['constraints']; n = len(S)
cells = [frozenset((a + 1, y) for a in range(5) for y in range(1, s[a] + 1)) for s in S]
def comp_cells(A, B):
    return all(c[0] + d[0] <= 5 or c[1] + d[1] <= 5 for c in A for d in B)
comp = np.array([[comp_cells(cells[i], cells[j]) for j in range(n)] for i in range(n)])
def down(cs):
    return frozenset((a, b) for (x, y) in cs for a in range(1, x + 1) for b in range(1, y + 1))
grid = [(a, b) for a in range(1, 6) for b in range(1, 6)]
hall = []
for k in (1, 2):
    for cs in itertools.combinations(grid, k):
        D = down(cs)
        X = [i for i in range(n) if D <= cells[i]]
        NX = [j for j in range(n) if comp_cells(D, cells[j])]
        if X and len(NX) < n:
            hall.append((X, NX))
print('Hall families', len(hall), 'compatibility density', comp.mean())

def solve(use_hall, integer=False, tl=120, fix0=True):
    h = highspy.Highs(); h.silent(); h.setOptionValue('threads', 1); h.setOptionValue('time_limit', float(tl))
    inf = highspy.kHighsInf
    for k in range(2 * n):                     # 0..n-1 in-holes h, n..2n-1 out-holes g
        h.addVar(0.0, 0.0 if (fix0 and k in (0, n)) else 1.0)
        h.changeColCost(k, 1.0 if k < n else 0.0)
        if integer: h.changeColIntegrality(k, highspy.HighsVarType.kInteger)
    for off in (0, n):
        for r in C:
            sup = np.array(r['support'], dtype=np.int32) + off
            h.addRow(float(r['rhs']), inf, len(sup), sup, np.ones(len(sup)))
    idx = np.arange(2 * n, dtype=np.int32); val = np.r_[np.ones(n), -np.ones(n)]
    h.addRow(0.0, 0.0, 2 * n, idx, val)          # equal populations
    if use_hall:
        for X, NX in hall:
            # |X| - h(X) <= |NX| - g(NX)  <=>  g(NX) - h(X) <= |NX| - |X|   (in -> out)
            ind = np.r_[np.array(NX) + n, np.array(X)].astype(np.int32)
            v = np.r_[np.ones(len(NX)), -np.ones(len(X))]
            h.addRow(-inf, float(len(NX) - len(X)), len(ind), ind, v)
            # out -> in, same families with roles swapped (reversal symmetry of comp)
            ind = np.r_[np.array(NX), np.array(X) + n].astype(np.int32)
            h.addRow(-inf, float(len(NX) - len(X)), len(ind), ind, v)
    h.run(); info = h.getInfo()
    return info.objective_function_value, (info.mip_dual_bound if integer else None), str(h.getModelStatus())

if __name__ == '__main__':
    print('symmetric compatibility:', bool((comp == comp.T).all()))
    print('LP without Hall', solve(False))
    print('LP with Hall', solve(True))
