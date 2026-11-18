#!/usr/bin/env python3
"""Freeze the inputs of a further budget-34 slice from an existing row version (no proof acceptance inferred here).

Usage: prepare_slice.py T SOURCE_VERSION OUT_VERSION   e.g. 18 s20-v13 s18-v13
Rows: the 2,650 Lean rows, then (F, T) and (Lo, 34 - T), then every coupled row of SOURCE_VERSION in order
(each already accepted by cake_lpr; coupled rows are slice-independent relaxations of actual residual owners).
"""
import gzip
import hashlib
import json
from pathlib import Path
import sys

W = Path('/home/jay/research/data/es308-20261114')
t, src_v, out_v = int(sys.argv[1]), sys.argv[2], sys.argv[3]
assert 14 <= t <= 20 and out_v.startswith(f's{t}-v')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = W / 'inputs/source-2650.json.gz'
raw = gzip.decompress(source.read_bytes())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
base = json.loads(raw)
F = [i for i, s in enumerate(base['states']) if s[0] >= 5]
LO = [i for i, s in enumerate(base['states']) if s[0] <= 4]
assert len(F) == 84 and len(LO) == 70 and sorted(F + LO) == list(range(154))
old = json.loads((W / 'inputs' / src_v / 'extra.json').read_text())
assert old[0]['support'] == F and old[1]['support'] == LO and old[0]['rhs'] + old[1]['rhs'] == 34
coupled = old[2:]
assert all(r['rhs'] == 1 for r in coupled) and len({tuple(r['support']) for r in coupled}) == len(coupled)
extra = [{'support': F, 'rhs': t}, {'support': LO, 'rhs': 34 - t}] + coupled
folder = W / 'inputs' / out_v
folder.mkdir(exist_ok=False)
ep = folder / 'extra.json'
ep.write_text(json.dumps(extra, indent=1) + '\n')
rows = base['constraints'] + extra
for r in rows:
    s, d = r['support'], r['rhs']
    assert len(s) == len(set(s)) and all(type(i) is int and 0 <= i < 154 for i in s)
    assert type(d) is int and 0 <= d <= len(s)
rp = folder / 'rows.txt'
with rp.open('x') as f:
    f.write('FASTBB-ROWS 1\n')
    f.write(f'source {source}\nsource_sha256 {sha(source)}\n')
    f.write(f'extra {ep}\nextra_sha256 {sha(ep)}\nstates 154\nbase_rows 2650\nrows {len(rows)}\n')
    for r in rows:
        f.write(f'{r["rhs"]} {len(r["support"])} ' + ' '.join(map(str, r['support'])) + '\n')
manifest = {'label': 'COMPUTED input preparation', 'slice': t, 'capacity_demands': [t, 34 - t],
            'source_version': src_v, 'source_extra_sha256': sha(W / 'inputs' / src_v / 'extra.json'),
            'coupled_rows': len(coupled), 'rows': len(rows), 'extra_sha256': sha(ep), 'rows_sha256': sha(rp),
            'tool_sha256': sha(Path(__file__))}
(folder / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print(json.dumps(manifest, indent=1))
