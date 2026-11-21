#!/usr/bin/env python3
"""rows-search: 'witness' (predecessor) implication rows at the root of catalog + Z + Z* (h0 = h1 = 0).
Claim (own, written in the report): if state s is occupied by v and (a,b) is a corner of s (b = s(a-1) >= 1 and
(a = 5 or s(a) < b)), some u < v has labels (capLabel, cupLabel)(u,v) = (a,b), and its state t = f_u satisfies
  R_1(t) >= a-1,  t(0) >= b-1,  t(a-1) <= b-1  (every incoming edge of u with capLabel >= a makes a cup turn).
Row: (1 - h_s) <= sum_{t in W(s,a,b)} (1 - h_t)  i.e.  h_s - sum_W h_t >= 1 - |W|.
Also: distinct corners of s use distinct u, so (#corners)(1 - h_s) <= sum_{t in union W} (1 - h_t)."""
import sys
import numpy as np, highspy
sys.path.insert(0, '<scratch>/agents/rows-search')
import chainrows as cr
N = cr.N; S = cr.S
R = lambda f, k: sum(1 for x in f if x >= k)

def corners(s):
    out = []
    for a in range(1, 6):
        b = s[a - 1]
        if b >= 1 and (a == 5 or s[a] < b):
            out.append((a, b))
    return out

def W(si, a, b):
    return [ti for ti, t in enumerate(S) if ti != si and R(t, 1) >= a - 1 and t[0] >= b - 1 and t[a - 1] <= b - 1]

rows = [({s: 1 for s in sup}, r) for sup, r in cr.ROWS] + [({s: 1 for s in cr.Z}, 15), ({s: 1 for s in cr.Zs}, 15)]
wrows = []; minW = 999; forced = []
for si, s in enumerate(S):
    if si == 0: continue
    cs = corners(s); U = set()
    for a, b in cs:
        w = W(si, a, b); U |= set(w); minW = min(minW, len(w))
        if not w: forced.append(si)
        co = {si: 1}
        for t in w: co[t] = co.get(t, 0) - 1
        wrows.append((co, 1 - len(w)))
    k = len(cs)
    co = {si: k}
    for t in U: co[t] = co.get(t, 0) - 1
    wrows.append((co, k - len(U)))
print('witness rows %d, min |W| %d, states with an empty W (forced holes): %s' % (len(wrows), minW, forced), flush=True)

def solve(rows):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    inf = highspy.kHighsInf
    for j in range(N):
        h.addVar(0.0, 0.0 if j in (0, 1) else 1.0); h.changeColCost(j, 1.0)
    for co, r in rows:
        idx = np.array(sorted(co), dtype=np.int32); val = np.array([float(co[i]) for i in idx])
        h.addRow(float(r), inf, len(idx), idx, val)
    h.run(); return h.getInfo().objective_function_value, np.array(h.getSolution().col_value)

v0, x0 = solve(rows)
v1, x1 = solve(rows + wrows)
print('root LP catalog+Z+Z*: %.6f ; + witness rows: %.6f' % (v0, v1), flush=True)
viol = [r - sum(c * x0[s] for s, c in co.items()) for co, r in wrows]
print('max violation of witness rows at the base optimum: %.4f' % max(viol), flush=True)
