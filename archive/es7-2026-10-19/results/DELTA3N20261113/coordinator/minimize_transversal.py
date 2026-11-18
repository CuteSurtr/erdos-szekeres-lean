#!/usr/bin/env python3
"""Deletion-minimize a COMPUTED counterexample to the minimum-size strengthening."""
import json
from pathlib import Path
import shutil
from minimum_transversal import check

root = Path('/home/jay/research/data/delta3-codex-20261113/coordinator')
source = root/'counterexample'
out = root/'minimized'
out.mkdir(exist_ok=True)
o = json.loads((source/'witness.json').read_text())
points, n = o['P'], o['n']
while True:
    changed = False
    for i in range(len(points)):
        candidate = points[:i]+points[i+1:]
        if not check(candidate, n, out, f'delete:{len(points)}:{i}'):
            points = candidate
            changed = True
            break
    if not changed:
        break
assert not check(points, n, out, 'deletion_minimal')
print(json.dumps({'status': 'DONE', 'n': n, 'm': len(points), 'P': points}), flush=True)
