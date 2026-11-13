#!/usr/bin/env python3
"""Bind the JSON V2 catalog (sha acaf6323...) to the Lean row systems used by the 311 proof.

(1) Base rows: each Lean module GeometryXXXXX.lean (from balanced-rows-sources.tar.gz, extracted as
    data into ./extract_rows) proves by `decide +kernel` that
        (cycle r).toFinset = support r  and  (cycle r).length - 7 = demand r
    for its row range. We parse the cycles and compare (set, length-7) with JSON rows 0..2684.
(2) Cut rows: parse BalancedCoverCutsV2.lean (support/demand data for the 446 cuts) and compare
    with JSON rows 2685..3130.
(3) State order: compare JSON 'states' with ErdosSzekeres/Omission/BalancedCatalogData.lean.
Exact text parsing only; nothing is executed from the extracted files.
"""
import json, re, os, sys, hashlib

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
CAT = ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
CUTS_LEAN = ROOT + '/experiments/omission-cover-certificates-2026-10-10/BalancedCoverCutsV2.lean'
STATES_LEAN = ROOT + '/ErdosSzekeres/Omission/BalancedCatalogData.lean'

raw = open(CAT, 'rb').read()
assert hashlib.sha256(raw).hexdigest().startswith('acaf6323')
cat = json.loads(raw)
rows = [(frozenset(r['support']), r['rhs']) for r in cat['constraints']]

# (3) states
txt = open(STATES_LEAN).read()
m = re.search(r'def catalog : List \(List Nat\) := (\[.*?\]\])', txt, re.S)
lean_states = json.loads(m.group(1))
print('state order JSON == Lean BalancedCatalog.catalog:', lean_states == cat['states'])

# (1) base rows from cycles
lean_base = {}
mods = sorted(f for f in os.listdir(HERE + '/extract_rows') if f.startswith('Geometry'))
for f in mods:
    t = open(HERE + '/extract_rows/' + f).read()
    cm = re.search(r'def cycles : Array \(List \(Fin 252\)\) := #\[(.*?)\n\]', t, re.S)
    assert cm, f
    cyc = [json.loads(x) for x in re.findall(r'\[[0-9, ]*\]', cm.group(1))]
    off = int(re.search(r'def cycle \(r : Fin 2685\) := cycles\[r\.val - (\d+)\]!', t).group(1))
    lo, hi = map(int, re.search(r'(\d+) ≤ r\.val → r\.val < (\d+) →', t).groups())
    assert lo == off and hi - lo == len(cyc), (f, lo, hi, off, len(cyc))
    assert '(cycle r).toFinset = support r' in t and '(cycle r).length - 7 = demand r' in t
    assert 'decide +kernel' in t
    for k, c in enumerate(cyc):
        lean_base[lo + k] = (frozenset(c), max(len(c) - 7, 0), len(c), len(set(c)))
print('Lean base rows parsed:', len(lean_base), 'covering', min(lean_base), '..', max(lean_base))
assert sorted(lean_base) == list(range(2685))
mism = [k for k in range(2685) if (lean_base[k][0], lean_base[k][1]) != rows[k]]
print('base rows: JSON vs Lean cycle-derived mismatches:', len(mism), mism[:5])
lens = {}
for k in range(2685):
    lens[lean_base[k][2]] = lens.get(lean_base[k][2], 0) + 1
print('cycle length distribution:', dict(sorted(lens.items())))
print('cycles with repeated vertices:', sum(1 for k in range(2685) if lean_base[k][2] != lean_base[k][3]))

# (2) cut rows from BalancedCoverCutsV2.lean
t = open(CUTS_LEAN).read()
print('CutsV2 lean size:', len(t))
# show the definitions that look like support/demand data
for name in ('support', 'demand', 'codes', 'supports', 'demands', 'rowData', 'rows'):
    for mm in re.finditer(r'\ndef ' + name + r'\b[^\n]*', t):
        print('  found def:', mm.group(0)[:160])
open(HERE + '/bind_summary.json', 'w').write(json.dumps({
    'states_match': lean_states == cat['states'], 'base_mismatches': mism}, indent=1))
