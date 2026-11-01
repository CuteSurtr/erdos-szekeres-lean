#!/usr/bin/env python3
"""Compare the 446 cut rows of the JSON V2 catalog with BalancedCoverCutsV2.lean (text parse only).
Also check that each Lean cut theorem's stated target equals the `demand` list entry."""
import json, re, hashlib

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
CAT = ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
LEAN = ROOT + '/experiments/omission-cover-certificates-2026-10-10/BalancedCoverCutsV2.lean'
raw = open(CAT, 'rb').read()
assert hashlib.sha256(raw).hexdigest().startswith('acaf6323')
rows = json.loads(raw)['constraints']
t = open(LEAN).read()
sup = {}
for m in re.finditer(r'^def support(\d+) : Finset \(Fin 252\) := \{([0-9, ]*)\}$', t, re.M):
    k = int(m.group(1))
    lst = [int(x) for x in m.group(2).split(',')]
    assert k not in sup
    sup[k] = lst
print('Lean cut supports parsed:', len(sup))
assert sorted(sup) == list(range(446))
dm = re.search(r'^def demand : Fin 446 → ℕ := !\[([0-9, ]*)\]$', t, re.M)
dem = [int(x) for x in dm.group(1).split(',')]
assert len(dem) == 446
tgt = {}
for m in re.finditer(r'^    (\d+) ≤ ∑ i ∈ support(\d+), holes i := by$', t, re.M):
    tgt[int(m.group(2))] = int(m.group(1))
print('cut theorem targets parsed:', len(tgt), '| targets == demand list:', all(tgt[k] == dem[k] for k in range(446)))
sm = re.search(r'^def support : Fin 446 → Finset \(Fin 252\) := !\[([^\]]*)\]$', t, re.M)
order = [s.strip() for s in sm.group(1).split(',')]
print('support vector is support0..support445 in order:', order == [f'support{k}' for k in range(446)])
mism = []
for k in range(446):
    r = rows[2685 + k]
    if set(r['support']) != set(sup[k]) or len(set(sup[k])) != len(sup[k]) or r['rhs'] != dem[k]:
        mism.append(k)
print('JSON rows 2685..3130 vs Lean cuts mismatches:', len(mism), mism[:5])
# every cut theorem uses rounded_cover_cut with base rows only (OmissionBalanced.*) or earlier cuts?
uses_cut = len(re.findall(r'apply rounded_cover_cut ![^\n]*support\d+', t))
print('cut proofs whose weighted premises mention earlier derived supports (textual):', uses_cut)
print('distinct theorem headers cutK:', len(set(re.findall(r'^theorem cut(\d+) ', t, re.M))))
