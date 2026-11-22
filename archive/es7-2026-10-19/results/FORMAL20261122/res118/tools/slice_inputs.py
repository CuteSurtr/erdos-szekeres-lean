#!/usr/bin/env python3
"""Read-only survey of the six residual slices used by ResidualBound 118 (res118-lean, 22 Nov 2026).

For each slice: extra.json path and sha256, row counts, capacity rows (F, T) and (Lo, B - T) checked against the
states of source-2650.json.gz, and the rhs-1 rows. Then the union of distinct rhs-1 rows over all slices and its
relation to the v169 row set (the 1,990 rows of ES307 T4). Writes data/slice_inputs.json.
"""
import gzip, hashlib, json, sys
from pathlib import Path

W = Path('/home/jay/research/data/es308-20261114')
LO = Path('/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113')
SRC = W / 'inputs/source-2650.json.gz'
raw = gzip.decompress(SRC.read_bytes())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
src = json.loads(raw)
st = src['states']
F = [i for i, s in enumerate(st) if s[0] >= 5]
Lo = [i for i, s in enumerate(st) if s[0] <= 4]
assert len(F) == 84 and len(Lo) == 70

SLICES = [  # (name, budget, T, extra file, packet)
    ('b33s18', 33, 18, LO / 'data/cert_66_55_leanrows/extra_66_55_leanrows.json', LO / 'data/cert_66_55_leanrows'),
    ('b34s18', 34, 18, W / 'inputs/s18-v13/extra.json', W / 'runs/s18/bb'),
    ('b34s19', 34, 19, W / 'inputs/s19/extra.json', W / 'runs/s19/bb'),
    ('b35s18', 35, 18, W / 'inputs/b35s18-v13/extra.json', W / 'runs/b35s18/bb'),
    ('b35s19', 35, 19, W / 'inputs/b35s19-v16/extra.json', W / 'runs/b35s19/bb'),
    ('b35s20', 35, 20, W / 'inputs/b35s20-v169/extra.json', W / 'runs/b35s20/bb-s1'),
]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

out = {'source_gz_sha256': sha(SRC), 'source_raw_sha256': hashlib.sha256(raw).hexdigest(),
       'F': F, 'Lo': Lo, 'slices': {}}
allrows = {}
for name, B, T, ef, pk in SLICES:
    ex = json.loads(Path(ef).read_text())
    rec = {'budget': B, 'T': T, 'extra': str(ef), 'extra_sha256': sha(ef), 'extra_rows': len(ex),
           'total_rows': 2650 + len(ex)}
    assert ex[0] == {'support': F, 'rhs': T}, (name, 'F capacity row')
    assert ex[1] == {'support': Lo, 'rhs': B - T}, (name, 'Lo capacity row')
    rest = ex[2:]
    rhs = sorted({r['rhs'] for r in rest})
    rec['rhs_values_other_rows'] = rhs
    assert all(r['rhs'] == 1 for r in rest), (name, 'non-unit rhs')
    assert all(len(set(r['support'])) == len(r['support']) and all(0 <= i < 154 for i in r['support']) for r in rest)
    keys = [tuple(sorted(r['support'])) for r in rest]
    rec['distinct_unit_rows'] = len(set(keys))
    rec['sorted_supports'] = all(r['support'] == sorted(r['support']) for r in rest)
    m = pk / 'master.json'
    if m.exists():
        mm = json.loads(m.read_text())
        rec['master'] = str(m)
        rec['master_sha256'] = sha(m)
        rec['master_extra'] = mm.get('extra')
        rec['master_budget'] = mm.get('budget')
        assert mm['budget'] == B and Path(mm['extra']) == Path(ef), (name, 'master/extra mismatch')
    for k in keys:
        allrows.setdefault(k, []).append(name)
    out['slices'][name] = rec

v169 = json.loads((W / 'inputs/b35s20-v169/extra.json').read_text())[2:]
v169k = {tuple(sorted(r['support'])) for r in v169}
out['union_unit_rows'] = len(allrows)
out['v169_unit_rows'] = len(v169k)
out['union_minus_v169'] = len(set(allrows) - v169k)
out['union_minus_v169_by_slice'] = {}
for k in set(allrows) - v169k:
    for s in allrows[k]:
        out['union_minus_v169_by_slice'][s] = out['union_minus_v169_by_slice'].get(s, 0) + 1
pool = W / 'inputs/pool812.json'
if pool.exists():
    pj = json.loads(pool.read_text())
    out['pool812_sha256'] = sha(pool)
    out['pool812_type'] = str(type(pj))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('F', 'Lo', 'slices')}, indent=1))
for k, v in out['slices'].items():
    print(k, {a: b for a, b in v.items() if a not in ('extra', 'master', 'master_extra')})
