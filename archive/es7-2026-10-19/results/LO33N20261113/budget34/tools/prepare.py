#!/usr/bin/env python3
"""Freeze the exact budget34 inputs; do not infer proof acceptance here."""
import gzip
import hashlib
import json
from pathlib import Path
import resource
import shutil

resource.setrlimit(resource.RLIMIT_AS, (150 << 20, 150 << 20))
REPO = Path('/home/jay/research/lean/erdos-szekeres-lean')
WORK = Path('/home/jay/research/data/es308-20261114')
SOURCE = REPO/'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
OLD = Path('/home/jay/research/data/fastbb-20261113/p2')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
raw = gzip.decompress(SOURCE.read_bytes())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
base = json.loads(raw)
assert len(base['states']) == 154 and len(base['constraints']) == 2650
F = [i for i,s in enumerate(base['states']) if s[0] >= 5]
LO = [i for i,s in enumerate(base['states']) if s[0] <= 4]
assert len(F) == 84 and len(LO) == 70 and sorted(F+LO) == list(range(154))
pool = json.loads((OLD/'runs/s23/extra.json').read_text())[2:]
assert len(pool) == 812 and all(r['rhs'] == 1 for r in pool)
assert len({tuple(r['support']) for r in pool}) == 812
inp = WORK/'inputs'
inp.mkdir(exist_ok=True)
shutil.copy2(SOURCE,inp/'source-2650.json.gz')
shutil.copy2(OLD/'runs/s23/extra.json', inp/'source-s23-extra.json')
(inp/'pool812.json').write_text(json.dumps(pool,indent=1)+'\n')
(WORK/'bin').mkdir(exist_ok=True)
shutil.copy2(OLD/'bin/fastbb2',WORK/'bin/fastbb2')
assert sha(WORK/'bin/fastbb2') == '39b724a2b5f5b08b56f3e9aedb24886c08ae2716301008410aaba9a1452b33b5'
manifest = {'label':'COMPUTED input preparation; pool provenance independently audited separately',
            'budget':34,'states':154,'base_rows':2650,'coupled_rows':812,
            'source_sha256':sha(inp/'source-2650.json.gz'),
            'pool_sha256':sha(inp/'pool812.json'),'binary_sha256':sha(WORK/'bin/fastbb2'),
            'source_s23_extra_sha256':sha(inp/'source-s23-extra.json'),'slices':{}}
for t in [19,20]:
    folder = inp/f's{t}';folder.mkdir(exist_ok=True)
    extra = [{'support':F,'rhs':t},{'support':LO,'rhs':34-t}] + pool
    ep = folder/'extra.json';ep.write_text(json.dumps(extra,indent=1)+'\n')
    rows = base['constraints'] + extra
    for r in rows:
        s,d=r['support'],r['rhs']
        assert len(s)==len(set(s)) and all(type(i) is int and 0<=i<154 for i in s)
        assert type(d) is int and 0<=d<=len(s)
    rp=folder/'rows.txt'
    with rp.open('w') as f:
        f.write('FASTBB-ROWS 1\n')
        f.write(f'source {inp/"source-2650.json.gz"}\nsource_sha256 {sha(inp/"source-2650.json.gz")}\n')
        f.write(f'extra {ep}\nextra_sha256 {sha(ep)}\nstates 154\nbase_rows 2650\nrows {len(rows)}\n')
        for r in rows:
            f.write(f'{r["rhs"]} {len(r["support"])} '+' '.join(map(str,r['support']))+'\n')
    manifest['slices'][str(t)]={'capacity_demands':[t,34-t],'extra_sha256':sha(ep),
                               'rows_sha256':sha(rp),'rows':len(rows)}
(inp/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
