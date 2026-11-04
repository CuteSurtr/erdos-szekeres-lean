#!/usr/bin/env python3
"""face_sparse_g.py MODEL OUT ROUNDS SPEC (face from SPEC). Reweighted-L1 search (numerical, evidence only) for a sparse lambda with Q_lambda W = 0 and
-Q_lambda[C,C] >= I.  Output dual.npy is fed to face_cert.py, which makes everything exact."""
import sys, numpy as np, cvxpy as cp, importlib.util
from pathlib import Path
from scipy.sparse import coo_matrix
s = importlib.util.spec_from_file_location('se', str(Path(__file__).with_name('sdp_ext.py'))); se = importlib.util.module_from_spec(s); s.loader.exec_module(se)
model, out, rounds = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
raw, pos, vs, ix, entries, order = se.build(model, list(range(10)), False, False)
N = len(entries); rr = []; cc = []; dd = []
for v, e in enumerate(entries):
    Q = se.quad([e], [1], vs, list(range(10)))
    for a in range(20):
        for b in range(20):
            if Q[a][b]: rr.append(a * 20 + b); cc.append(v); dd.append(Q[a][b])
Mm = coo_matrix((dd, (rr, cc)), shape=(400, N)).tocsr()
import json
spec = json.load(open(sys.argv[4]))
def Rk(p, k):
    for _ in range(k % 6): p = ((p[0] - 3 * p[1]) / 2, (p[0] + p[1]) / 2)
    return p
def bvec(g, e):
    z = [(0, 0)] * 10
    for (i, k) in g: z[i] = Rk(e, k)
    return [p[0] for p in z] + [p[1] for p in z]
Wb = np.array([bvec(g, e) for g in spec['groups'] for e in ((1, 0), (0, 1))], float).T
drop = [d for g in spec['groups'] for d in (g[0][0], g[0][0] + 10)]
C = [k for k in range(20) if k not in drop]
lam = cp.Variable(N, nonneg=True); Qv = cp.reshape(Mm @ lam, (20, 20), order='C')
cons = [Qv @ Wb == 0, -Qv[np.ix_(C, C)] >> np.eye(len(C))]
c = np.ones(N)
for r in range(rounds):
    prob = cp.Problem(cp.Minimize(c @ lam), cons); prob.solve(solver='CLARABEL', max_threads=1)
    x = np.maximum(lam.value, 0); print(r, prob.status, 'support>1e-6*max', int((x > 1e-6 * x.max()).sum()), flush=True)
    c = 1.0 / (x + 1e-4 * x.max())
out.mkdir(parents=True, exist_ok=True); x = x / x.sum(); x[x < 1e-7] = 0; np.save(out / 'dual.npy', x)
print('nonzero', int((x > 0).sum()), 'min nonzero', float(x[x > 0].min()))
