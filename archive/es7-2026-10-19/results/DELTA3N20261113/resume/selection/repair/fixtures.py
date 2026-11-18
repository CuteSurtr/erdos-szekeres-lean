#!/usr/bin/env python3
"""Snapshot real input coordinates, provenance and source hashes, then emit text."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parents[3]
D3 = RES / 'DELTA3N20261113'
OUT = HERE / 'data'
OUT.mkdir(exist_ok=True)
records = []

def add(name, n, path, key=None):
    raw = json.loads(path.read_text())
    data = raw[key] if key is not None else raw
    points = data.get('P', data.get('points'))
    if points is None:
        raise ValueError(path)
    records.append(dict(name=name, n=n, P=points, source=str(path.relative_to(RES)),
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest(), key=key))

for n in (7, 8):
    add(f'old-ends-n{n}', n, RES / f'DELTA2N20261113/data/cex/restr_ends_weak_a5_n{n}_m{n+5}_real.json')
    add(f'minimum16-n{n}', n, D3 / 'resume/compact/real_n7m16.json')
add('targeted-n8m16', 8, D3 / 'resume/compact/real_n8m16_targeted.json')
for n in (7,8):
    add(f'star12-n{n}', n, D3 / 'resume/pool/data/maximal/real-star.json')
rawpath = D3 / 'resume/weak_theory/findings.json'
for obj in json.loads(rawpath.read_text())['obstructions']:
    records.append(dict(name=f'monotone-min-n{obj["n"]}', n=obj['n'], P=obj['P'],
                        source=str(rawpath.relative_to(RES)), sha256=hashlib.sha256(rawpath.read_bytes()).hexdigest()))
fp = D3 / 'search/fixtures.json'
for key, obj in json.loads(fp.read_text()).items():
    if len(obj['P'])<=16:
        for n in (7,8): add(f'{key}-n{n}', n, fp, key)
(OUT/'fixtures.json').write_text(json.dumps(records,indent=2)+'\n')
with (OUT/'fixtures.txt').open('w') as f:
    for rec in records:
        f.write(f'{rec["name"]} {rec["n"]} {len(rec["P"])}\n')
        for x,y in rec['P']: f.write(f'{x} {y}\n')
print(json.dumps({'fixtures':len(records),'output':str(OUT/'fixtures.txt')}))
