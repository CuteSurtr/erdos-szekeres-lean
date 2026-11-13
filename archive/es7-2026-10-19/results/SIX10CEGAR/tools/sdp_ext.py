#!/usr/bin/env python3
"""Numerical PSD probe for model0090 with extra valid linear rows; exact rounding attempt.

Extra rows (all valid for the encoding's normalised realisations, see REPORT.md):
  phase rows  : for i<j, sign(theta_j-theta_i)*E_ij > 0, D_ij+E_ij > 0, D_ij-E_ij > 0
  radius rows : D_ii - D_{i+1,i+1} > 0
Numerical output is evidence only; a retained certificate is re-checked exactly by check_cert.py.
"""
import argparse, hashlib, importlib.util, json, sys, time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

import os
RES = Path(os.environ['ES_RESULTS'])  # review results directory, read-only


def load(name, p):
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def build(model_path, layers, use_phase=True, use_radius=True):
    M = load('linear', RES / 'ROTREFINE20261104/math_linear.py'); G = load('encoder', RES / 'C7UPPER/gen.py')
    E = G.Enc(6, 8, 10); raw = Path(model_path).read_bytes(); pos = set(json.loads(raw))
    vs = M.variables(10); ix = {v: j for j, v in enumerate(vs)}; ls = set(layers)
    entries = []
    for q, v in E.tvar.items():
        if {x // 6 for x in q} <= ls:
            sg = 1 if v in pos else -1
            entries.append({'kind': 'triple', 'triple': list(q), 'variable': v, 'required_sign': sg,
                            'row': {j: c * sg for j, c in M.form(q, ix).items()}})
    # phase order: theta_0 = 0 < theta_i (i>=1); Y(i,j) = [theta_i < theta_j]
    def less(i, j):
        if i == 0: return True
        if j == 0: return False
        if i < j: return E.Y[(i, j)] in pos
        return not (E.Y[(j, i)] in pos)
    if use_phase:
        for i in layers:
            for j in layers:
                if i < j:
                    s = 1 if less(i, j) else -1
                    entries.append({'kind': 'phase_sign', 'pair': [i, j], 'row': {ix[('E', i, j)]: s}})
                    entries.append({'kind': 'phase_plus', 'pair': [i, j], 'row': {ix[('D', i, j)]: 1, ix[('E', i, j)]: 1}})
                    entries.append({'kind': 'phase_minus', 'pair': [i, j], 'row': {ix[('D', i, j)]: 1, ix[('E', i, j)]: -1}})
    if use_radius:
        L = sorted(layers)
        for a, b in zip(L, L[1:]):
            entries.append({'kind': 'radius', 'pair': [a, b], 'row': {ix[('D', a, a)]: 1, ix[('D', b, b)]: -1}})
    order = sorted(range(10), key=lambda i: (0 if i == 0 else 1, sum(1 for j in range(1, 10) if j != i and less(j, i))))
    return raw, pos, vs, ix, entries, order


def quad(entries, weights, vs, layers):
    """Twice the symmetric matrix of sum(weight*row) in coordinates (u_i, v_i), seed = (u_i, sqrt3 v_i)."""
    n = len(layers); idx = {i: k for k, i in enumerate(layers)}; Q = [[0] * (2 * n) for _ in range(2 * n)]
    coeff = defaultdict(int)
    for e, w in zip(entries, weights):
        for j, c in e['row'].items(): coeff[j] += w * c
    for j, c in coeff.items():
        if not c: continue
        kind, i, k = vs[j]; i = idx[i]; k = idx[k]
        if kind == 'D':
            if i == k: Q[i][i] += 2 * c; Q[n + i][n + i] += 6 * c
            else: Q[i][k] += c; Q[k][i] += c; Q[n + i][n + k] += 3 * c; Q[n + k][n + i] += 3 * c
        else:
            Q[i][n + k] += c; Q[n + k][i] += c; Q[n + i][k] -= c; Q[k][n + i] -= c
    return Q


def negdef(Q):
    m = len(Q); A = [[-F(x) for x in r] for r in Q]; piv = []
    for k in range(m):
        p = A[k][k]
        if p <= 0: return None
        piv.append(p)
        for i in range(k + 1, m):
            f = A[i][k] / p
            if f:
                for j in range(k, m): A[i][j] -= f * A[k][j]
    return piv


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--model', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--layers', default='all'); ap.add_argument('--no-phase', action='store_true'); ap.add_argument('--no-radius', action='store_true')
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True); t0 = time.monotonic()
    layers = list(range(10)) if a.layers == 'all' else list(map(int, a.layers.split(',')))
    raw, pos, vs, ix, entries, order = build(a.model, layers, not a.no_phase, not a.no_radius)
    import numpy as np, cvxpy as cp
    from scipy.sparse import coo_matrix
    rr = []; cc = []; dd = []
    for k, e in enumerate(entries):
        for j, c in e['row'].items(): rr.append(k); cc.append(j); dd.append(c)
    A = coo_matrix((dd, (rr, cc)), shape=(len(entries), 100)).tocsr(); x = cp.Variable(100); delta = cp.Variable()
    D = cp.bmat([[cp.reshape(x[ix['D', min(i, j), max(i, j)]], (1, 1), order='C') for j in layers] for i in layers])
    EE = cp.bmat([[cp.Constant(np.zeros((1, 1))) if i == j else cp.reshape(x[ix['E', min(i, j), max(i, j)]] * (1 if i < j else -1), (1, 1), order='C') for j in layers] for i in layers])
    mat = cp.bmat([[D, -EE], [EE, D / 3]])
    orient = A @ x >= delta; prob = cp.Problem(cp.Maximize(delta), [orient, mat >> 0, cp.trace(D) == 1])
    prob.solve(solver='CLARABEL', verbose=False, max_threads=1, time_limit=120, max_iter=400, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    res = {'model_sha256': hashlib.sha256(raw).hexdigest(), 'layers': layers, 'rows': len(entries), 'status': prob.status,
           'margin_evidence_only': float(delta.value) if delta.value is not None else None, 'phase_order_theta': order}
    found = False
    if orient.dual_value is not None:
        dual = np.asarray(orient.dual_value).ravel(); res['dual_sum'] = float(dual.sum())
        for scale in (10**2, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**10, 10**12):
            w = [max(0, int(round(float(z) * scale))) for z in dual]; sup = [i for i, v in enumerate(w) if v]
            if not sup: continue
            used = sorted({l for i in sup for l in ([x // 6 for x in entries[i]['triple']] if entries[i]['kind'] == 'triple' else entries[i]['pair'])})
            Q = quad([entries[i] for i in sup], [w[i] for i in sup], vs, used); piv = negdef(Q)
            if piv is not None:
                recs = [dict({k: v for k, v in entries[i].items() if k != 'row'}, weight=w[i], row=sorted([list(vs[j]), c] for j, c in entries[i]['row'].items())) for i in sup]
                wit = {'model_sha256': res['model_sha256'], 'layers': used, 'scale': scale, 'records': recs,
                       'quadratic_matrix_twice': Q, 'neg_ldl_pivots': [str(p) for p in piv]}
                data = (json.dumps(wit, indent=1) + '\n').encode(); (out / 'witness.json').write_bytes(data)
                res.update({'certificate': True, 'support': len(sup), 'scale': scale, 'cert_layers': used, 'witness_sha256': hashlib.sha256(data).hexdigest(),
                            'support_kinds': {k: sum(1 for i in sup if entries[i]['kind'] == k) for k in ('triple', 'phase_sign', 'phase_plus', 'phase_minus', 'radius')}})
                found = True; break
        if not found: res['certificate'] = False
        np.save(out / 'dual.npy', dual)
    if x.value is not None: np.save(out / 'lift.npy', x.value)
    res['seconds'] = round(time.monotonic() - t0, 2)
    (out / 'result.json').write_text(json.dumps(res, indent=1) + '\n'); print(json.dumps(res))


if __name__ == '__main__': main()
