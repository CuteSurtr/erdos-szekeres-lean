#!/usr/bin/env python3
"""Standard-library-only exact check of the Boolean witnesses in witnesses.json.

For each witness hole set H it recomputes, with Python integers, |S_r & H| for every row r of the
catalog and compares with the demand d_r.  It also re-hashes the catalog files so the check is bound
to the exact inputs used by the 311 / 313 proofs.

Usage (from cloud/es7-2026-10-19/results): python3 -I ES8SLACK/check_witnesses.py"""
import gzip, hashlib, json, os, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = HERE  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
REPO = ROOT + '/experiments'
BAL = REPO + '/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
RES = REPO + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    raw = open(path, 'rb').read()
    data = gzip.decompress(raw) if path.endswith('.gz') else raw
    d = json.loads(data)
    return hashlib.sha256(data).hexdigest(), len(d['states']), [(set(r['support']), int(r['rhs'])) for r in d['constraints']]


def check(rows, n, holes):
    H = set(holes)
    assert len(H) == len(holes) and all(0 <= i < n for i in H)
    bad = [k for k, (s, d) in enumerate(rows) if len(s & H) < d]
    slack0 = sum(1 for s, d in rows if len(s & H) == d)
    return bad, slack0


W = json.load(open(os.path.join(HERE, 'witnesses.json')))
sb, nb, rb = load(BAL)
sr, nr, rr = load(RES)
print('balanced catalog sha256 (decompressed):', sb, 'states', nb, 'rows', len(rb))
print('residual catalog sha256 (decompressed):', sr, 'states', nr, 'rows', len(rr))
assert sb == 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72'
assert sr == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
ok = True
h = W['balanced_v2_72_hole_witness']
bad, tight = check(rb, nb, h)
print(f'balanced witness: {len(h)} holes, violated rows {len(bad)}, tight rows {tight}')
ok &= not bad
for k, h in enumerate(W['residual_2650_33_hole_witnesses_state0_occupied']):
    bad, tight = check(rr, nr, h)
    print(f'residual witness {k}: {len(h)} holes, state 0 occupied {0 not in h}, violated rows {len(bad)}, tight rows {tight}')
    ok &= (not bad) and (0 not in h)
print('ALL WITNESSES VALID' if ok else 'FAILURE')
sys.exit(0 if ok else 1)
