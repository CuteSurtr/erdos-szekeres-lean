#!/usr/bin/env python3
"""For a configuration and a layer i: drop all phase-derived units involving layer i, solve, and report where the
model puts psi_i in the phase order of the other layers (diagnostic, evidence only)."""
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, lpcegar2 as L
m, t, cnf, cfg = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
LI = [int(x) for x in sys.argv[5].split(',')]
seeds = int(sys.argv[6]) if len(sys.argv) > 6 else 1
E = gen.Enc(m, 8, t)
d = json.load(open(cfg)); lr = np.array(d['lr']); th = np.array(d['th'])
o = np.argsort(-lr); lr = lr[o]; th = th[o]; th = (th - th[0]) % (2 * math.pi / m)
A = L.triple_forms(E, th)
cls, nu, ni = L.threshold_clauses(E, A, 10 ** 8)
lay_of = {}
for C, v in E.tvar.items(): lay_of[v] = set(x // m for x in C)
for (i, j), v in E.Y.items(): lay_of[v] = {i, j}
for i, v in E.H.items(): lay_of[v] = {i}
items = []
for x in L.phase_assumptions(E, th): items.append((lay_of[abs(x)], [x]))
for cl in cls:
    c = [x for x in cl if x != -10 ** 8]; ls = set()
    for x in c: ls |= lay_of[abs(x)]
    items.append((ls, c))
units = [c[0] for ls, c in items if len(c) == 1 and not (ls & set(LI))]
rest = [c for ls, c in items if len(c) > 1 and not (ls & set(LI))]
deg = np.degrees(th)
print('phases (deg):', ' '.join('%d:%.3f' % (i, deg[i]) for i in range(t)))
for s in range(seeds):
    S = L.build_solver([cnf], units, rest)
    if s:
        rng = np.random.default_rng(s)
        S.set_phases([int(v if rng.random() < 0.5 else -v) for v in range(1, E.ntriplevars + 1)])
    S.conf_budget(300000)
    r = S.solve_limited()
    if r is not True:
        print('seed', s, 'result', r); S.delete(); continue
    mdl = set(S.get_model()); S.delete()
    for li in LI:
        below = [j for j in range(1, t) if j != li and j not in LI and E.ylit(j, li) in mdl]
        above = [j for j in range(1, t) if j != li and j not in LI and E.ylit(li, j) in mdl]
        lo = max([deg[j] for j in below], default=0.0); hi = min([deg[j] for j in above], default=360.0 / m)
        print('seed', s, 'psi_%d between %.4f and %.4f deg' % (li, lo, hi), 'below', below, 'above', above)
    if len(LI) == 2:
        print('   order of the pair: psi_%d < psi_%d' % ((LI[0], LI[1]) if E.ylit(LI[0], LI[1]) in mdl else (LI[1], LI[0])))
