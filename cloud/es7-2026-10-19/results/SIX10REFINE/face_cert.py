#!/usr/bin/env python3
"""Facially reduced negative-SEMIdefinite certificate search for model0090 (triple rows only).

The SDP optimum is a degenerate configuration in the rational subspace
  W = {z_1=z_2=z_3=z_4=R z_5, z_5=z_6=z_7=z_8, z_9=0, z_0 free}   (4 real dims).
We look for lambda >= 0 with Q_lambda W = 0 exactly and -Q_lambda positive definite on a
coordinate complement of W.  Numerical dual only seeds lambda; everything retained is exact.
"""
import json, sys, hashlib
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import importlib.util
s = importlib.util.spec_from_file_location('se', str(Path(__file__).with_name('sdp_ext.py'))); se = importlib.util.module_from_spec(s); s.loader.exec_module(se)

run, model, thr, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), Path(sys.argv[4])
raw, pos, vs, ix, entries, order = se.build(model, list(range(10)), False, False)
dual = np.load(run + '/dual.npy'); n = 10
# W basis in coordinates [u_0..u_9, v_0..v_9], seed = (u, sqrt3 v); R(u,v) = ((u-3v)/2, (u+v)/2)
def wvec(z0, w):
    z = [(F(0), F(0))] * 10; z[0] = z0
    Rw = ((w[0] - 3 * w[1]) / 2, (w[0] + w[1]) / 2)
    for i in (1, 2, 3, 4): z[i] = Rw
    for i in (5, 6, 7, 8): z[i] = w
    return [p[0] for p in z] + [p[1] for p in z]
Wb = [wvec((F(1), F(0)), (F(0), F(0))), wvec((F(0), F(1)), (F(0), F(0))), wvec((F(0), F(0)), (F(1), F(0))), wvec((F(0), F(0)), (F(0), F(1)))]
C = [k for k in range(20) if k not in (0, 10, 5, 15)]  # drop u_0, v_0, u_5, v_5
S = [i for i in range(len(entries)) if dual[i] > thr]
Qs = [se.quad([entries[i]], [1], vs, list(range(10))) for i in S]
# B: equations (Q_lambda b_k)_r = 0
rowsB = []
for b in Wb:
    for r in range(20):
        rowsB.append([sum(F(Qv[r][c]) * b[c] for c in range(20) if b[c]) for Qv in Qs])
# integer-ize
import math
B = [[int(x * 2) for x in row] for row in rowsB]
B = [row for row in B if any(row)]
scale = 10**9
lam0 = [F(int(round(float(dual[i]) * scale))) for i in S]
rhs = [-sum(b * l for b, l in zip(row, lam0)) for row in B]
# solve (B B^T) y = rhs by elimination
m = len(B); BBt = [[F(sum(a * b for a, b in zip(B[p], B[q]))) for q in range(m)] + [rhs[p]] for p in range(m)]
piv = []; r = 0
for c in range(m):
    pr = next((k for k in range(r, m) if BBt[k][c] != 0), None)
    if pr is None: continue
    BBt[r], BBt[pr] = BBt[pr], BBt[r]; f = BBt[r][c]; BBt[r] = [x / f for x in BBt[r]]
    for k in range(m):
        if k != r and BBt[k][c] != 0:
            f = BBt[k][c]; BBt[k] = [a - f * b for a, b in zip(BBt[k], BBt[r])]
    piv.append(c); r += 1
assert all(any(row[:-1]) or row[-1] == 0 for row in BBt), 'inconsistent'
y = [F(0)] * m
for k, c in enumerate(piv): y[c] = BBt[k][-1]
lam = [l + sum(B[p][j] * y[p] for p in range(m)) for j, l in enumerate(lam0)]
neg = sum(1 for l in lam if l <= 0)
print('support', len(S), 'B rows', m, 'rank', len(piv), 'nonpositive after projection', neg, 'min lam', float(min(lam)) / scale, flush=True)
if neg:
    sys.exit(1)
den = math.lcm(*(l.denominator for l in lam)); W = [int(l * den) for l in lam]; g = math.gcd(*W); W = [w // g for w in W]
Q = se.quad([entries[i] for i in S], W, vs, list(range(10)))
for b in Wb:
    assert all(sum(F(Q[r][c]) * b[c] for c in range(20)) == 0 for r in range(20)), 'Q W != 0'
QC = [[Q[a][b] for b in C] for a in C]
p = se.negdef(QC)
print('negdef on complement:', p is not None, flush=True)
if p is None: sys.exit(2)
recs = [{'triple': entries[i]['triple'], 'variable': entries[i]['variable'], 'required_sign': entries[i]['required_sign'], 'weight': w} for i, w in zip(S, W)]
wit = {'model_sha256': hashlib.sha256(raw).hexdigest(), 'method': 'positive combination of signed orientation forms is negative SEMIdefinite; kernel = W',
       'W_basis_uv': [[str(x) for x in b] for b in Wb], 'complement_coords': C, 'records': recs, 'quadratic_matrix_twice': Q,
       'neg_complement_ldl_pivots': [str(x) for x in p], 'candidate_clause': sorted([-r['variable'] * r['required_sign'] for r in recs], key=abs)}
out.mkdir(parents=True, exist_ok=True); data = (json.dumps(wit) + '\n').encode(); (out / 'face_witness.json').write_bytes(data)
print('witness', hashlib.sha256(data).hexdigest(), 'support', len(recs), 'maxw', max(W))
