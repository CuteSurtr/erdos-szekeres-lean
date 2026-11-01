"""Probe 1: LP relaxation values of the balanced and residual hole systems.
min sum h  s.t.  A h >= d, 0 <= h <= 1  (plus optional fixings)."""
import sys, time, json
import numpy as np
from scipy.optimize import linprog
from common import *


def lp(n, rows, fix0=(), extra=()):
    A, b = matrix(n, rows)
    bounds = [(0, 1)] * n
    for i in fix0:
        bounds[i] = (0, 0)
    t = time.time()
    res = linprog(np.ones(n), A_ub=-A, b_ub=-b, bounds=bounds, method='highs')
    return res.fun, time.time() - t, res


out = {}
for name, path in [('balanced_v1_2685', BAL_V1), ('balanced_v2_3131', BAL_V2), ('residual_2650', RES_2650)]:
    states, rows = load(path)
    n = len(states)
    v, t, res = lp(n, rows)
    out[name] = {'n': n, 'rows': len(rows), 'lp': v, 'secs': round(t, 2)}
    if name.startswith('residual'):
        v0, t0, _ = lp(n, rows, fix0=[0])
        out[name]['lp_h0_occupied'] = v0
    else:
        v0, _, _ = lp(n, rows, fix0=[0])
        v01, _, _ = lp(n, rows, fix0=[0, 1])
        out[name]['lp_h0_occupied'] = v0
        out[name]['lp_h0_h1_occupied'] = v01
    print(name, out[name], flush=True)
print(json.dumps(out, indent=1))
