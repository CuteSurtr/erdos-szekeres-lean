#!/usr/bin/env python3
"""Diagnostic (evidence only): for a configuration whose phase-fixed formula (pfenc) is UNSAT, find a small set of
LAYER GROUPS whose phase-derived sign units already conflict with "no convex octagon".
Units of pfenc are grouped by the set of layers of their form; each group gets a selector; chain clauses are generated
without unit simplification; a core over the selectors is extracted and shrunk by deletion.
usage: core_groups.py M CFG.json [conf]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pfenc
from pysat.solvers import Solver

m, cfg = int(sys.argv[1]), sys.argv[2]
conf = int(sys.argv[3]) if len(sys.argv) > 3 else 200000
d = json.load(open(cfg)); lr = np.array(d['lr']); th = np.array(d['th']); centre = int(d.get('centre', 0))
o = np.argsort(-lr); lr = lr[o] - lr[o][0]; th = th[o]; th = (th - th[0]) % (2 * math.pi / m)
t = len(lr)
P = pfenc.PF(m, t, centre, th)
units, imps = P.units()
t0 = time.time()
cls = P.chain_clauses({})
print('chain clauses (unsimplified)', len(cls), 'vars', P.nv, '%.1f s' % (time.time() - t0), flush=True)
groups = {}
for v, l in units.items():
    g = frozenset(x // m for x in P.Cof[v])
    groups.setdefault(g, []).append([l])
for c in imps:
    g = frozenset()
    for x in c:
        g |= frozenset(y // m for y in P.Cof[abs(x)])
    groups.setdefault(g, []).append(c)
keys = sorted(groups, key=lambda g: (len(g), sorted(g)))
sel = {}
nv = P.nv
S = Solver(name='cadical195')
for c in cls:
    S.add_clause(c)
for g in keys:
    nv += 1; sel[g] = nv
    for c in groups[g]:
        S.add_clause([-nv] + c)
print('groups', len(keys), flush=True)
assum = [sel[g] for g in keys]
S.conf_budget(conf * 5)
r = S.solve_limited(assumptions=assum)
print('all groups:', r, flush=True)
if r is False:
    core = set(S.get_core())
    cur = [g for g in keys if sel[g] in core]
    print('initial core groups', len(cur), flush=True)
    i = 0
    while i < len(cur):
        trial = cur[:i] + cur[i + 1:]
        S.conf_budget(conf)
        r2 = S.solve_limited(assumptions=[sel[g] for g in trial])
        if r2 is False:
            core2 = set(S.get_core())
            cur = [g for g in trial if sel[g] in core2]
        else:
            i += 1
    print('minimal core: %d groups' % len(cur))
    lay = {}
    for g in cur:
        for x in g:
            lay[x] = lay.get(x, 0) + 1
        print('  layers', sorted(g), 'units/imps', len(groups[g]))
    print('layer frequency', sorted(lay.items()))
    print('phases (deg):', ' '.join('%d:%.4f' % (i, math.degrees(th[i])) for i in range(t)))
    print('log radii   :', ' '.join('%d:%.4f' % (i, lr[i]) for i in range(t)))
