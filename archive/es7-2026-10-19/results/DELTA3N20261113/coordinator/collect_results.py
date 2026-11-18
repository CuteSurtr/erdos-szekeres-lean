#!/usr/bin/env python3
"""Collect completed frontiers, preserving small logs and large-file references."""
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = Path('/home/jay/research/data/delta3-codex-20261113/encoder')
OUT = HERE/'data'/'frontier'
cases = []
for pattern in ('scheduled*/result.json', 'fallback*/result.json', 'direct*/result.json'):
    for path in sorted(ROOT.glob(pattern)):
        r = json.loads(path.read_text())
        row = dict(case=path.parent.name, status=r['status'], label=r['label'],
                   n=r['parameters']['n'], m=r['parameters']['m'], mode=r['parameters']['mode'],
                   pool=r['parameters']['pool'], directory=str(path.parent),
                   hashes=r['hashes'], runs=r['runs'])
        cases.append(row)
        if r['status'] == 'STARTED':
            continue
        target = OUT/path.parent.name
        target.mkdir(parents=True, exist_ok=True)
        for f in path.parent.iterdir():
            if f.is_file() and (f.name in ('result.json', 'model.log', 'cake.log', 'encode.log') or f.suffix == '.time'):
                shutil.copyfile(f, target/f.name)
        if r['status'] == 'UNSAT_CERTIFIED':
            assert 's VERIFIED UNSAT' in (path.parent/'cake.log').read_text().splitlines()
summary = {'results': cases, 'pending': [r['case'] for r in cases if r['status'] == 'STARTED']}
(HERE/'data'/'frontier_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
for r in cases:
    print(r['case'], r['status'])
print('pending', len(summary['pending']))
