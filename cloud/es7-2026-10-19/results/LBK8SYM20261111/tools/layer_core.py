#!/usr/bin/env python3
"""Which layers' phase information makes the phase-fixed formula UNSAT?  For a configuration (lr, th), build the
phase-specific units (phase order, threshold and suffix units, threshold implications) and, for each layer i (and each
pair of layers), drop every unit/implication whose form involves layer i (resp. i or j) and re-solve with a conflict
budget.  Evidence only (diagnostic)."""
import sys, os, json, math, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, lpcegar2 as L
m, t, cnf, cfg = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
pairs = len(sys.argv) > 5 and sys.argv[5] == 'pairs'
E = gen.Enc(m, 8, t)
d = json.load(open(cfg)); lr = np.array(d['lr']); th = np.array(d['th'])
o = np.argsort(-lr); lr = lr[o]; th = th[o]; th = (th - th[0]) % (2 * math.pi / m)
A = L.triple_forms(E, th)
cls, nu, ni = L.threshold_clauses(E, A, 10 ** 8)
lay_of = {}
for C, v in E.tvar.items():
    lay_of[v] = set(x // m for x in C)
for (i, j), v in E.Y.items():
    lay_of[v] = {i, j}
for i, v in E.H.items():
    lay_of[v] = {i}
items = []   # (layers, clause)
for x in L.phase_assumptions(E, th):
    items.append((lay_of[abs(x)], [x]))
for cl in cls:
    c = [x for x in cl if x != -10 ** 8]
    ls = set()
    for x in c:
        ls |= lay_of[abs(x)]
    items.append((ls, c))
def solve(drop):
    units = [c[0] for ls, c in items if len(c) == 1 and not (ls & drop)]
    rest = [c for ls, c in items if len(c) > 1 and not (ls & drop)]
    S = L.build_solver([cnf], units, rest)
    S.conf_budget(200000)
    r = S.solve_limited(); S.delete(); return r
print('all units:', solve(set()), flush=True)
for i in range(1, t):
    print('drop layer', i, solve({i}), flush=True)
if pairs:
    for i, j in itertools.combinations(range(1, t), 2):
        r = solve({i, j})
        if r is not False:
            print('drop pair', i, j, r, flush=True)
