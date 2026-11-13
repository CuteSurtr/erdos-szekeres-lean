#!/usr/bin/env python3
"""Exploration (evidence only): signs forced on the radius cone for ALL sampled phase vectors of one phase order
(monotone: psi_1 < ... < psi_{t-1}); then SAT-check the phase-order CNF with these units (no thresholds).
usage: univ.py NSAMPLES OUTPREFIX [seed]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lpc8
from pysat.solvers import Solver
N = int(sys.argv[1]); outp = sys.argv[2]; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
rng = np.random.default_rng(seed)
t = 16
base = lpc8.Base(t, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cnf', 'chord_m8t16.clauses'))
U = None
hist = []
for s in range(N):
    ph = np.sort(rng.uniform(0, math.pi / 4, t - 1))
    th = np.concatenate([[0.0], ph])
    fs = base.forced_signs(base.forms(th))
    if U is None:
        U = fs.copy()
    else:
        U[(U != fs)] = 0
    hist.append(int((U != 0).sum()))
    if s % 10 == 0:
        print('sample', s, 'universal forced', hist[-1], flush=True)
np.save(outp + '_U.npy', U)
print('universal forced after', N, ':', hist[-1], flush=True)
# SAT check with these units, all Y true (monotone), gen.py clauses + chord, chain simplified
S = Solver(name='cadical195')
th = np.concatenate([[0.0], np.linspace(1, 44, t - 1) * math.pi / 180])   # only for Y units (monotone)
E = base.E
forced = {v: (v if U[v] > 0 else -v) for v in range(1, base.nt + 1) if U[v]}
for l in forced.values(): S.add_clause([l])
for y in E.Y.values(): S.add_clause([y])
val = {abs(l): l > 0 for l in forced.values()}
val.update({y: True for y in E.Y.values()})
bad = 0
for cl_list in (base.order_cls, base.angle_cls, base.nest_cls, base.chord_cls):
    for cl in cl_list:
        if any(abs(l) in val and val[abs(l)] == (l > 0) for l in cl): continue
        rest = [l for l in cl if abs(l) not in val]
        if not rest: bad += 1
        else: S.add_clause(rest)
E.cls = []; E.ncls = 0; E.nv = base.base_nv; E.body = None; E.forced = dict(forced)
E.add = lambda cl: S.add_clause(cl)
E.fam_chain()
print('conflicts with units', bad, 'built; solving', flush=True)
t0 = time.time()
r = S.solve()
print('RESULT', 'SAT' if r else 'UNSAT', '%.1f s' % (time.time() - t0), flush=True)
