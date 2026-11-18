#!/usr/bin/env python3
"""Freeze slice inputs whose coupled rows are the union (in first-seen order) of several row versions.

Every coupled row of every source version was accepted by cake_lpr before it was appended (and audited per batch);
coupled rows are slice-independent relaxations of actual residual owners, so the union is valid for any slice.
Usage: prepare_union.py B T OUT_VERSION SRC_VERSION [SRC_VERSION ...]   e.g. 35 21 b35s21-u1 s20-v13 b35s19-v16 b35s20-v128
"""
import gzip
import hashlib
import json
from pathlib import Path
import sys

W = Path('/home/jay/research/data/es308-20261114')
B, t, out_v, srcs = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4:]
assert B in (34, 35) and 14 <= t <= 21 and out_v.startswith(f'b{B}s{t}-u') and srcs
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = W / 'inputs/source-2650.json.gz'
raw = gzip.decompress(source.read_bytes())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
base = json.loads(raw)
F = [i for i, s in enumerate(base['states']) if s[0] >= 5]
LO = [i for i, s in enumerate(base['states']) if s[0] <= 4]
coupled, seen, per_src = [], set(), {}
for v in srcs:
    ex = json.loads((W / 'inputs' / v / 'extra.json').read_text())
    assert ex[0]['support'] == F and ex[1]['support'] == LO
    added = 0
    for r in ex[2:]:
        assert r['rhs'] == 1
        key = tuple(r['support'])
        if key not in seen:
            seen.add(key); coupled.append(r); added += 1
    per_src[v] = {'extra_sha256': sha(W / 'inputs' / v / 'extra.json'), 'coupled_rows': len(ex) - 2, 'new_in_union': added}
extra = [{'support': F, 'rhs': t}, {'support': LO, 'rhs': B - t}] + coupled
folder = W / 'inputs' / out_v
folder.mkdir(exist_ok=False)
ep = folder / 'extra.json'
ep.write_text(json.dumps(extra, indent=1) + '\n')
rows = base['constraints'] + extra
for r in rows:
    s, d = r['support'], r['rhs']
    assert len(s) == len(set(s)) and all(type(i) is int and 0 <= i < 154 for i in s) and type(d) is int and 0 <= d <= len(s)
rp = folder / 'rows.txt'
with rp.open('x') as f:
    f.write('FASTBB-ROWS 1\n')
    f.write(f'source {source}\nsource_sha256 {sha(source)}\n')
    f.write(f'extra {ep}\nextra_sha256 {sha(ep)}\nstates 154\nbase_rows 2650\nrows {len(rows)}\n')
    for r in rows:
        f.write(f'{r["rhs"]} {len(r["support"])} ' + ' '.join(map(str, r['support'])) + '\n')
manifest = {'label': 'COMPUTED input preparation (union of certified coupled rows)', 'budget': B, 'slice': t,
            'capacity_demands': [t, B - t], 'sources': per_src, 'coupled_rows': len(coupled), 'rows': len(rows),
            'extra_sha256': sha(ep), 'rows_sha256': sha(rp), 'tool_sha256': sha(Path(__file__))}
(folder / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print(json.dumps(manifest, indent=1))
