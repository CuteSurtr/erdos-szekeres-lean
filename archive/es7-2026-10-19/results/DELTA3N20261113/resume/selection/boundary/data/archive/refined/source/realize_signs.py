#!/usr/bin/env python3
"""Heuristic realization search; only exact rounded determinants prove success.

SLSQP and linear-program statuses are not mathematical evidence. All numeric
libraries run with one thread, set by the parent unit's environment.
"""
import os
os.environ.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
import argparse
import itertools
import json
from pathlib import Path
import time
import warnings

import numpy as np
from scipy.optimize import minimize, linprog, OptimizeWarning

ap = argparse.ArgumentParser()
ap.add_argument('--input', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--seconds', type=int, default=18)
ap.add_argument('--attempts', type=int, default=300)
args = ap.parse_args()
ROOT = args.out
source = args.input
record = json.loads(source.read_text())
m = record['m']
triples = list(itertools.combinations(range(m), 3))
tr = np.array(triples)
sg = np.array([1 if c == '+' else -1 for c in record['signs']])
nv = 2*(m-2)+1
started = time.monotonic()
rng = np.random.default_rng(20261113)


def coordinates(z):
    return np.r_[0., z[:m-2], 1.], np.r_[0., z[m-2:-1], 0.]


def constraints(z):
    x, y = coordinates(z)
    i, j, k = tr.T
    d = (x[j]-x[i])*(y[k]-y[i])-(y[j]-y[i])*(x[k]-x[i])
    return np.r_[sg*d-z[-1], np.diff(x)-z[-1]]


def jacobian(z):
    x, y = coordinates(z)
    i, j, k = tr.T
    out = np.zeros((len(triples)+m-1, nv))
    out[:, -1] = -1
    for inds, dx, dy in ((i, y[j]-y[k], x[k]-x[j]),
                        (j, y[k]-y[i], x[i]-x[k]),
                        (k, y[i]-y[j], x[j]-x[i])):
        keep = (inds > 0) & (inds < m-1)
        rows = np.flatnonzero(keep)
        out[rows, inds[keep]-1] += sg[keep]*dx[keep]
        out[rows, m-2+inds[keep]-1] += sg[keep]*dy[keep]
    for a in range(m-1):
        if a > 0:
            out[len(triples)+a, a-1] = -1
        if a+1 < m-1:
            out[len(triples)+a, a] = 1
    return out


def exact_candidate(x, y, method, attempt):
    # Translation and uniform positive scaling of each coordinate preserve signs.
    x = np.asarray(x)-x[0]
    y = np.asarray(y)-y[0]
    x /= max(1., np.max(np.abs(x)))
    y /= max(1., np.max(np.abs(y)))
    for scale in (10**6, 10**9, 10**12, 10**14):
        P = [[int(round(a*scale)), int(round(b*scale))] for a, b in zip(x, y)]
        if not all(P[i][0] < P[i+1][0] for i in range(m-1)):
            continue
        dets = [(P[j][0]-P[i][0])*(P[k][1]-P[i][1])-(P[j][1]-P[i][1])*(P[k][0]-P[i][0])
                for i, j, k in triples]
        if all(d and (d > 0) == (s == '+') for d, s in zip(dets, record['signs'])):
            o = dict(record, P=P, realized=True, realization_method=method,
                     attempt=attempt, minimum_absolute_determinant=min(map(abs, dets)))
            (ROOT/'realized.json').write_text(json.dumps(o, indent=2)+'\n')
            print(json.dumps({'status': 'EXACT_INTEGER_REALIZATION', 'attempt': attempt,
                              'method': method, 'min_abs_det': min(map(abs, dets)),
                              'seconds': time.monotonic()-started}), flush=True)
            return True
    return False


def fixed_x(x, attempt):
    rows = np.zeros((len(triples), m))
    for row, ((i, j, k), s) in enumerate(zip(triples, sg)):
        rows[row, i] = -s*(x[k]-x[j])
        rows[row, j] = s*(x[k]-x[i])
        rows[row, k] = -s*(x[j]-x[i])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', OptimizeWarning)
        r = linprog(np.zeros(m), A_ub=rows, b_ub=-np.ones(len(rows)),
                    bounds=[(0, 0)]+[(None, None)]*(m-2)+[(0, 0)], method='highs',
                    options={'threads': 1, 'time_limit': 2})
    return r.x is not None and exact_candidate(x, r.x, 'fixed-x LP, exact integer recheck', attempt)


def main():
    best = -float('inf')
    objective_jac = np.zeros(nv)
    objective_jac[-1] = -1
    for attempt in range(args.attempts):
        if time.monotonic()-started > args.seconds:
            break
        dx = np.exp(rng.normal(0, 1+(attempt % 5), m-1))
        x = np.r_[0, np.cumsum(dx)]
        x /= x[-1]
        if fixed_x(x, attempt):
            return
        y = rng.uniform(-.6, .6, m-2)
        z = np.r_[x[1:-1], y, -1.]
        r = minimize(lambda z: -z[-1], z, jac=lambda z: objective_jac,
                     constraints=[{'type': 'ineq', 'fun': constraints, 'jac': jacobian}],
                     bounds=[(0., 1.)]*(m-2)+[(-1., 1.)]*(m-2)+[(-2., 1.)],
                     method='SLSQP', options={'maxiter': 400, 'ftol': 1e-11})
        x, y = coordinates(r.x)
        if exact_candidate(x, y, 'SLSQP, exact integer recheck', attempt) or fixed_x(x, attempt):
            return
        margin = float(np.min(constraints(np.r_[r.x[:-1], 0.])))
        if margin > best:
            best = margin
            (ROOT/'best_heuristic.json').write_text(json.dumps({'x': list(x), 'y': list(y),
                    'margin': margin, 'attempt': attempt, 'status': 'HEURISTIC_ONLY'})+'\n')
        if attempt % 50 == 0:
            print(json.dumps({'status': 'SEARCHING', 'attempt': attempt,
                              'best_margin': best, 'seconds': time.monotonic()-started}), flush=True)
    print(json.dumps({'status': 'UNRESOLVED_REALIZABILITY', 'best_margin': best,
                      'seconds': time.monotonic()-started}), flush=True)


if __name__ == '__main__':
    ROOT.mkdir(parents=True, exist_ok=True)
    main()
