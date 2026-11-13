#!/usr/bin/env python3
"""Does an octagon-free (t-1)-layer configuration extend abstractly by one layer?  (m-fold, nested layers; evidence /
diagnostic; a SAT answer is an abstract model only.)
For a configuration C with t-1 layers (float, N8 = 0) and each insertion rank p = 1..t-1 (new layer strictly inside the
outermost one), fix in gen.py's Enc(m, 8, t) every orbit variable of a triple of old points to C's sign and every
phase-order literal between old layers, and solve (conflict budget).  For a SAT answer, report the phase interval of
the new layer in the model's phase order.
usage: ext_test.py M T CNF CFG.json [conf]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'py'))
import gen
from pysat.solvers import Solver
from evm import countm, pointsm

m, t, cnf, cfg = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
conf = int(sys.argv[5]) if len(sys.argv) > 5 else 500000
E = gen.Enc(m, 8, t)
d = json.load(open(cfg)); lr = np.array(d['lr']); th = np.array(d['th'])
o = np.argsort(-lr); lr = lr[o] - lr[o][0]; th = th[o]; th = (th - th[0]) % (2 * math.pi / m)
assert len(lr) == t - 1
c, _ = countm(m, lr, th, 0)
print('config', cfg, 'layers', len(lr), 'N8', c[8], flush=True)
x, y = pointsm(m, lr, th, 0)
P = x + 1j * y
U = 2 * math.pi / m
psi = th % (math.pi / m) if m % 2 else th
clauses = []
for line in open(cnf):
    if line[0] in 'pc' or not line.strip():
        continue
    clauses.append([int(v) for v in line.split()[:-1]])
deg = np.degrees(th)
for p in range(1, t):
    newid = lambda j: j if j < p else j + 1
    units = set()
    old = [i for i in range(t) if i != p]
    oldidx = {newid(j): j for j in range(t - 1)}
    for C, v in E.tvar.items():
        Ls = [q // m for q in C]
        if p in Ls:
            continue
        a, b, cc = [P[oldidx[q // m] * m + q % m] for q in C]
        val = ((b - a).conjugate() * (cc - a)).imag
        units.add(v if val > 0 else -v)
    for (i, j), v in E.Y.items():
        if p in (i, j):
            continue
        oi, oj = oldidx[i], oldidx[j]
        units.add(v if psi[oi] < psi[oj] else -v)
    for i, v in E.H.items():
        if i == p:
            continue
        units.add(v if th[oldidx[i]] < math.pi / m else -v)
    S = Solver(name='cadical195')
    for cl in clauses:
        if any(l in units for l in cl):
            continue
        S.add_clause([l for l in cl if -l not in units])
    for u in units:
        S.add_clause([u])
    S.conf_budget(conf)
    t0 = time.time()
    r = S.solve_limited()
    msg = 'insert rank %d: %s (%.1f s)' % (p, r, time.time() - t0)
    if r is True:
        mdl = set(S.get_model())
        below = [j for j in range(1, t) if j != p and E.ylit(j, p) in mdl]
        above = [j for j in range(1, t) if j != p and E.ylit(p, j) in mdl]
        lo = max([deg[oldidx[j]] for j in below], default=0.0); hi = min([deg[oldidx[j]] for j in above], default=360.0 / m)
        msg += '  new phase in (%.4f, %.4f) deg' % (lo, hi)
        json.dump(sorted(l for l in mdl if 0 < abs(l) <= E.ntriplevars + len(E.Y) + len(E.H)),
                  open(cfg.replace('.json', '_ext_p%d_model.json' % p), 'w'))
    print(msg, flush=True)
    S.delete()
