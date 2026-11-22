#!/usr/bin/env python3
"""Reviewer's own freshness / one-provider check for n66-l15-rows (reads only; writes review/own_fresh.json).

1. One provider per module on the worker's LEAN_PATH (tools/env.sh, with OLEAN unset): every .olean path relative to
   its store root, counted over all stores of the path (first store wins in Lean's search).
2. For every olean of the worker's store: source exists, olean newer than its source, and newer than the olean of
   every import (wherever it is found on the path).
3. IR C files (build/ir) vs oleans: each .c was written in the same compile as its olean (|mtime difference| small)
   and is older than the object compiled from it (build/obj).
"""
import json, os, re, subprocess
from pathlib import Path

D = Path('/home/jay/research/data/formalize-20261122/n66-l15-rows')
env = subprocess.run(['bash', '-c', f'unset OLEAN; source {D}/tools/env.sh; echo "$LEAN_PATH"'],
                     capture_output=True, text=True, check=True).stdout.strip()
stores = env.split(':')
res = {'stores': stores}
prov = {}
for s in stores:
    p = Path(s)
    if not p.is_dir():
        res.setdefault('missing_stores', []).append(s)
        continue
    for f in p.rglob('*.olean'):
        mod = str(f.relative_to(p))[:-6].replace('/', '.')
        prov.setdefault(mod, []).append(s)
dups = {m: v for m, v in prov.items() if len(v) > 1}
res['modules_on_path'] = len(prov)
res['modules_with_two_or_more_providers'] = len(dups)
res['dups_sample'] = dict(list(dups.items())[:20])
key = ['LemmaZ', 'EncB.Render', 'EncB.Dimacs', 'N66E15.Full', 'N66E15.Bridge', 'N66E15.Cover', 'N66G15.End',
       'N66G15.Assembly', 'N66R15Geo.Final', 'N66R15Enc.RowList', 'N66R15Enc.Bridge', 'N66R15Chk.RowsAll',
       'N66Enc.Rows', 'N66Geo.End', 'RowEnc.Gen', 'RowGeo.End', 'RowChk.Check', 'N66E15.Rows']
res['key_providers'] = {m: prov.get(m, []) for m in key}

ws = D / 'build/olean'
lean = D / 'lean'
def olean_of(mod):
    for s in stores:
        f = Path(s) / (mod.replace('.', '/') + '.olean')
        if f.exists():
            return f
    return None
bad = []
n = 0
for f in sorted(ws.rglob('*.olean')):
    mod = str(f.relative_to(ws))[:-6].replace('/', '.')
    n += 1
    src = lean / (mod.replace('.', '/') + '.lean')
    if not src.exists():
        bad.append((mod, 'no source'))
        continue
    mo = f.stat().st_mtime
    if src.stat().st_mtime > mo:
        bad.append((mod, 'source newer than olean'))
    if olean_of(mod) != f:
        bad.append((mod, f'shadowed by {olean_of(mod)}'))
    for imp in re.findall(r'^import (\S+)', src.read_text(), re.M):
        g = olean_of(imp)
        if g is None:
            bad.append((mod, f'import {imp} not found'))
        elif g.stat().st_mtime > mo:
            bad.append((mod, f'import {imp} newer ({g})'))
res['worker_oleans'] = n
res['freshness_problems'] = bad
# IR C vs olean vs object
ir = D / 'build/ir'
irp = []
nc = 0
for c in sorted(ir.rglob('*.c')):
    mod = str(c.relative_to(ir))[:-2]
    nc += 1
    o = ws / (mod + '.olean')
    if not o.exists():
        irp.append((mod, 'no olean'))
        continue
    dt = abs(c.stat().st_mtime - o.stat().st_mtime)
    if dt > 60:
        irp.append((mod, f'c vs olean mtime differ by {dt:.0f} s'))
    obj = D / 'build/obj' / (mod.replace('/', '_') + '.o')
    if obj.exists() and obj.stat().st_mtime < c.stat().st_mtime:
        irp.append((mod, 'object older than its C'))
res['ir_c_files'] = nc
res['ir_problems'] = irp
(D / 'review/own_fresh.json').write_text(json.dumps(res, indent=1) + '\n')
for k in ['modules_on_path', 'modules_with_two_or_more_providers', 'worker_oleans', 'freshness_problems',
          'ir_c_files', 'ir_problems', 'key_providers', 'dups_sample', 'missing_stores']:
    print(k, res.get(k))
