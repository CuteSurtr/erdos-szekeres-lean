#!/usr/bin/env python3
"""Negative controls for check_c5.py: perturbed witnesses must be caught.

For each witness we (a) un-hole each single hole in turn (giving 71 / 32 holes) and count how
many of those perturbations violate some row; (b) check the all-occupied vector violates rows;
(c) check the all-missing vector satisfies every row (sanity of row direction d <= |S|).
Also reports whether each witness is inclusion-minimal (every single un-holing breaks a row),
and for the residual side whether any 32-hole un-holing keeps all rows (that would contradict
the repository's kernel-checked exclusion and would itself be a finding).
Usage: python3 -I negative_controls.py
"""
import gzip, json

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
EXP = ROOT + '/experiments'
bal = json.load(open(EXP + '/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
res = json.loads(gzip.decompress(open(EXP + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))
W = json.load(open(TOP + '/witnesses.json'))

B = [(frozenset(c['support']), c['rhs']) for c in bal['constraints']]
R = [(frozenset(c['support']), c['rhs']) for c in res['constraints']]


def nviol(rows, H):
    return sum(1 for s, d in rows if len(s & H) < d)


print('all-occupied balanced violations:', nviol(B, frozenset()), '/ 3131')
print('all-occupied residual violations:', nviol(R, frozenset()), '/ 2650')
print('all-missing balanced violations:', nviol(B, frozenset(range(252))))
print('all-missing residual violations:', nviol(R, frozenset(range(154))))

hb = frozenset(W['balanced_v2_72_hole_witness'])
broken = sum(1 for i in hb if nviol(B, hb - {i}) > 0)
print(f'balanced: {broken}/72 single un-holings violate some row (minimal={broken == 72})')
for k, hr in enumerate(W['residual_2650_33_hole_witnesses_state0_occupied']):
    hr = frozenset(hr)
    broken = sum(1 for i in hr if nviol(R, hr - {i}) > 0)
    print(f'residual {k}: {broken}/33 single un-holings violate some row (32-hole feasible found: {broken < 33})')
# also: moving a hole onto state 0 would break state-0 occupancy; check the witness relies on it or not
for k, hr in enumerate(W['residual_2650_33_hole_witnesses_state0_occupied']):
    print(f'residual {k}: 0 in holes? {0 in hr}')
