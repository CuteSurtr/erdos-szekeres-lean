#!/usr/bin/env python3
"""Completeness audit: for every orbit, sign s and total phase order, the optimal margin
t* = min over 0 <= lambda <= M of lambda_max(S_triple(s) + sum lambda_k S_k) (all rows incl. nesting, all sign rows of
the order).  t* <= 0: certificate exists (numerically); t* > 0 clearly: no certificate within the box.
Small positive t* flags a possibly missed (weakly feasible / boundary) case."""
import os, sys, json, itertools, math
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, scipy.sparse as sp, clarabel
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lr_core as C
from lr_scan import build, total_orders

def margin(S0, Ss, M=100.0):
    n = S0.shape[0]; m = len(Ss); d = n*(n+1)//2
    A1 = np.column_stack([C.svec(X) for X in Ss] + [-C.svec(np.eye(n))])
    A = np.vstack([A1, np.hstack([-np.eye(m), np.zeros((m,1))]), np.hstack([np.eye(m), np.zeros((m,1))])])
    b = np.concatenate([C.svec(-S0), np.zeros(m), M*np.ones(m)])
    q = np.zeros(m+1); q[-1] = 1
    st = clarabel.DefaultSettings(); st.verbose = False
    sol = clarabel.DefaultSolver(sp.csc_matrix((m+1,m+1)), q, sp.csc_matrix(A), b, [clarabel.PSDTriangleConeT(n), clarabel.NonnegativeConeT(2*m)], st).solve()
    return str(sol.status), float(sol.x[-1])

def run(t):
    L = sorted({x//6 for x in t}); out = []
    for s in (1, -1):
        for o in total_orders(L):
            trip, recs, S0F, SsF = build(t, s, o, True)
            st, tv = margin(C.tofloat(S0F), [C.tofloat(X) for X in SsF])
            out.append((s, sorted(['%d,%d' % k for k, v in o.items() if v == 1]), st, tv))
    return {'t': list(t), 'var': C.E.tvar[t], 'res': out}

if __name__ == '__main__':
    ts = sorted(C.E.tvar, key=lambda T: C.E.tvar[T])
    with Pool(4) as P, open(sys.argv[1], 'w') as f:
        for r in P.imap_unordered(run, ts, chunksize=8):
            f.write(json.dumps(r) + '\n')
