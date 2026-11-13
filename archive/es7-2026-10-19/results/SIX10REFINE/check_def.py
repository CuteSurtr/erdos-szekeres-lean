#!/usr/bin/env python3
"""Independent exact checker (stdlib only) for face_witness.json.

Representation (independent of the dot/cross table): seed z_i = a_i + b_i*w, w = exp(i*pi/3);
rotation by 60 degrees ccw is (a,b) -> (-b, a+b); det(p,q) = (sqrt3/2)*(p_a q_b - p_b q_a).
Checks: model hash; variable/triple/sign binding against the encoder; positive integer weights;
the weighted sum P of signed (2/sqrt3)*[abc] is a quadratic form with P*W = 0 on the stated
4-dim subspace W, and -P restricted to the coordinate complement is positive definite
(exact rational LDL).  Hence P is negative semidefinite.
"""
import hashlib, importlib.util, json, sys
from fractions import Fraction as F
from pathlib import Path

import os
RES = Path(os.environ['ES_RESULTS'])  # review results directory, read-only
model_path, wit_path = sys.argv[1], sys.argv[2]
raw = Path(model_path).read_bytes(); pos = set(json.loads(raw)); wit = json.loads(Path(wit_path).read_text())
assert hashlib.sha256(raw).hexdigest() == wit['model_sha256']
s = importlib.util.spec_from_file_location('enc', RES / 'C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(6, 8, 10)
NV = 20  # variable index: a_i -> i, b_i -> 10+i


def point(x):
    """linear forms (coef dicts) for the oblique coordinates of point id x = 6*i + k, i.e. R^k z_i"""
    i, k = divmod(x, 6); a = {i: 1}; b = {10 + i: 1}
    for _ in range(k):
        a, b = {j: -c for j, c in b.items()}, {j: a.get(j, 0) + b.get(j, 0) for j in set(a) | set(b)}
    return a, b


def mul(p, q, sign, acc):
    for i, c in p.items():
        for j, d in q.items():
            if c * d:
                key = (min(i, j), max(i, j)); acc[key] = acc.get(key, 0) + sign * c * d


def orient_poly(t, scale, acc):
    """acc += scale * (p_a q_b - p_b q_a) summed cyclically  ( = scale*(2/sqrt3)*[abc] )"""
    P = [point(x) for x in t]
    for (pa, pb), (qa, qb) in zip(P, P[1:] + P[:1]):
        mul(pa, qb, scale, acc); mul(pb, qa, -scale, acc)


acc = {}; nrec = 0
for r in wit['records']:
    t = tuple(r['triple']); assert list(t) == sorted(t) and len(set(t)) == 3
    assert E.tvar[t] == r['variable'], 'triple/variable binding'
    assert r['required_sign'] == (1 if r['variable'] in pos else -1), 'sign binding to model'
    assert isinstance(r['weight'], int) and r['weight'] > 0
    orient_poly(t, r['weight'] * r['required_sign'], acc); nrec += 1
# symmetric matrix S with P(x) = x^T S x
S = [[F(0)] * NV for _ in range(NV)]
for (i, j), c in acc.items():
    if i == j: S[i][i] += c
    else: S[i][j] += F(c, 2); S[j][i] += F(c, 2)
# W in oblique coordinates
def wvec(z0, w):
    z = [(0, 0)] * 10; z[0] = z0; Rw = (-w[1], w[0] + w[1])
    for i in (1, 2, 3, 4): z[i] = Rw
    for i in (5, 6, 7, 8): z[i] = w
    return [p[0] for p in z] + [p[1] for p in z]
Wb = []
for b in Wb:
    assert all(sum(S[r][c] * b[c] for c in range(NV)) == 0 for r in range(NV)), 'P*W != 0'
L = sorted({x // 6 for r in wit['records'] for x in r['triple']}); drop = tuple(k for k in range(NV) if k % 10 not in L)

C = [k for k in range(NV) if k not in drop]
A = [[-S[i][j] for j in C] for i in C]; piv = []
for k in range(len(C)):
    p = A[k][k]; assert p > 0, 'not negative definite on complement'
    piv.append(p)
    for i in range(k + 1, len(C)):
        f = A[i][k] / p
        if f:
            for j in range(k, len(C)): A[i][j] -= f * A[k][j]
clause = sorted([-r['variable'] * r['required_sign'] for r in wit['records']], key=abs)

print(json.dumps({'ok': True, 'records': nrec, 'layers_used': sorted({x // 6 for r in wit['records'] for x in r['triple']}),
                  'kernel_dim_checked': 4, 'complement_pivots_positive': len(piv),
                  'min_pivot_float': float(min(piv)), 'clause_len': len(clause),
                  'witness_sha256': hashlib.sha256(Path(wit_path).read_bytes()).hexdigest()}))
