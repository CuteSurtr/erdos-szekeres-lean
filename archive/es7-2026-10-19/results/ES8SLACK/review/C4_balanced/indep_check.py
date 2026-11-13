#!/usr/bin/env python3
"""Independent re-check of claim C4 (balanced 72-hole Boolean witness).

Written from scratch (does not import or reuse ES8SLACK/check_witnesses.py or probes/common.py).
Exact integer arithmetic only. Run with:  python3 -I indep_check.py

Checks
  1. sha256 of the raw bytes of balanced-v2-source.json == acaf6323...3d72
  2. structure: 252 distinct states, 3131 rows, first 2685 rows are the plain (geometric) rows,
     last 446 are 'exact_arithmetic_cover_cut' rows; every support is a set of indices in [0,252)
  3. witness = 72 distinct integers in [0,252)
  4. two independent evaluations of every row  sum_{i in support} h_i >= rhs  (h = 0/1 vector):
     (a) via an explicit 0/1 list and integer sums, (b) via a bitmask popcount
  5. states 0..3 are the profiles [0,0,0,0,0],[1,0,0,0,0],[1,1,0,0,0],[2,0,0,0,0] and are occupied
     (h_0 = h_1 = 0, h_2 + h_3 <= 1)
  6. symmetry: T (conjugate partition), C (complement rotated 180 deg), TC; is the witness invariant?
  7. P1 extra: re-evaluate with P1 constraints added
"""
import hashlib, json, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
CAT = ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
WIT = TOP + '/witnesses.json'
EXPECT = 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72'

raw = open(CAT, 'rb').read()
sha = hashlib.sha256(raw).hexdigest()
print('catalog sha256      :', sha)
assert sha == EXPECT, 'catalog hash mismatch'
cat = json.loads(raw.decode('utf-8'))
states = [tuple(s) for s in cat['states']]
rows = cat['constraints']
N = len(states)
print('states / rows       :', N, len(rows))
assert N == 252 and len(set(states)) == 252
assert len(rows) == 3131
for k, r in enumerate(rows):
    sup = r['support']
    assert isinstance(r['rhs'], int) and not isinstance(r['rhs'], bool)
    assert all(isinstance(i, int) and not isinstance(i, bool) and 0 <= i < N for i in sup), k
    assert len(set(sup)) == len(sup), k
    if k < 2685:
        assert set(r.keys()) == {'support', 'rhs'}, (k, r.keys())
    else:
        assert r.get('kind') == 'exact_arithmetic_cover_cut', k
        assert set(r.keys()) == {'support', 'rhs', 'kind', 'derivation_row'}, k

wj = json.load(open(WIT))
W = wj['balanced_v2_72_hole_witness']
print('witness length      :', len(W))
assert all(isinstance(i, int) and not isinstance(i, bool) for i in W)
assert len(set(W)) == len(W) == 72, 'witness must be 72 distinct indices'
assert all(0 <= i < N for i in W)

# (a) explicit 0/1 vector
h = [0] * N
for i in W:
    h[i] = 1
assert sum(h) == 72
viol_a, tight_a, slack = [], 0, []
for k, r in enumerate(rows):
    s = 0
    for i in r['support']:
        s += h[i]
    d = r['rhs']
    if s < d:
        viol_a.append(k)
    elif s == d:
        tight_a += 1
    slack.append(s - d)
# (b) bitmask popcount
mask = 0
for i in W:
    mask |= 1 << i
viol_b = []
for k, r in enumerate(rows):
    m = 0
    for i in r['support']:
        m |= 1 << i
    if bin(m & mask).count('1') < r['rhs']:
        viol_b.append(k)
print('violated rows (a,b) :', len(viol_a), len(viol_b))
print('violated base rows  :', sum(1 for k in viol_a if k < 2685))
print('tight rows          :', tight_a, '(base:', sum(1 for k in range(2685) if slack[k] == 0), ')')
print('min slack           :', min(slack))
assert viol_a == viol_b

# 5. early states
print('states 0..3         :', states[:4])
assert states[0] == (0, 0, 0, 0, 0) and states[1] == (1, 0, 0, 0, 0)
assert set(states[2:4]) == {(1, 1, 0, 0, 0), (2, 0, 0, 0, 0)}
print('h_0..h_3            :', h[:4], ' P1 ok:', h[0] == 0 and h[1] == 0 and h[2] + h[3] <= 1)

# 6. symmetry maps (independent implementation)
def cells(f):
    return {(c, y) for c in range(5) for y in range(f[c])}  # column c (0-based) has heights f[c]

def prof(cellset):
    return tuple(sum(1 for (c, y) in cellset if c == col) for col in range(5))

def T_map(f):  # transpose the down-set
    return prof({(y, c) for (c, y) in cells(f)})

def C_map(f):  # complement in 5x5 box, rotated by 180 degrees
    comp = {(c, y) for c in range(5) for y in range(5)} - cells(f)
    return prof({(4 - c, 4 - y) for (c, y) in comp})

idx = {s: i for i, s in enumerate(states)}
for f in states:
    assert all(f[c] >= f[c + 1] for c in range(4))
T = [idx[T_map(f)] for f in states]
C = [idx[C_map(f)] for f in states]
TC = [C[T[i]] for i in range(N)]
CT = [T[C[i]] for i in range(N)]
assert sorted(T) == sorted(C) == list(range(N))
print('TC == CT            :', TC == CT)
Hs = set(W)
for name, p in (('T', T), ('C', C), ('TC', TC)):
    print(f'witness invariant under {name:2s}:', {p[i] for i in Hs} == Hs)

# rows invariance (for information): does each permutation map the base row set onto itself?
base = {(tuple(sorted(r['support'])), r['rhs']) for r in rows[:2685]}
for name, p in (('T', T), ('C', C), ('TC', TC)):
    img = {(tuple(sorted(p[i] for i in s)), d) for (s, d) in base}
    print(f'base rows mapped onto themselves by {name:2s}:', img == base)

ok = not viol_a and h[0] == 0 and h[1] == 0 and h[2] + h[3] <= 1
print('RESULT              :', 'WITNESS VALID (72 holes, all 3131 rows, P1)' if ok else 'WITNESS INVALID')
json.dump({'catalog_sha256': sha, 'holes': len(W), 'violated': viol_a, 'tight': tight_a,
           'min_slack': min(slack), 'P1': ok}, open(HERE + '/indep_check_out.json', 'w'), indent=1)
sys.exit(0 if ok else 1)
