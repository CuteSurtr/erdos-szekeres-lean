#!/usr/bin/env python3
"""Extend a hole vector by prefix integer counts, then exec the independent checker."""
import gzip
import json
import os
from pathlib import Path
import resource
import sys

hard = resource.getrlimit(resource.RLIMIT_AS)[1]
ceiling = 300*1024**2 if hard == resource.RLIM_INFINITY else min(hard, 300*1024**2)
resource.setrlimit(resource.RLIMIT_AS, (ceiling, ceiling))
folder, hole_file, out = map(Path, sys.argv[1:])
meta = json.loads((folder/'encoding.json').read_text())
holes = json.loads(hole_file.read_text())
assert len(holes) == 154 and all(type(v) is int and v in (0, 1) for v in holes)
with gzip.open(meta['base'], 'rt') as f:
    base = json.load(f)
pool = json.loads(Path(meta['pool']).read_text())
F = [i for i, s in enumerate(base['states']) if s[0] >= 5]
Lo = [i for i, s in enumerate(base['states']) if s[0] <= 4]
t = meta['slice']
rows = base['constraints'] + pool + [
    {'support': F, 'rhs': t if t else 19},
    {'support': Lo, 'rhs': 34-t if t else 14}]
assert holes[0] == 0 and sum(holes) <= 34
assert all(sum(holes[i] for i in r['support']) >= r['rhs'] for r in rows)
values = holes[:]
for S, threshold in [(r['support'], r['rhs']) for r in rows if r['rhs'] > 1] + [(list(range(154)), 35)]:
    count = 0
    for prefix_len, state in enumerate(S, 1):
        count += holes[state]
        values.extend(int(count >= j) for j in range(1, min(prefix_len, threshold)+1))
assert len(values) == meta['variables']
solution = out/'extended-solution.txt'
with solution.open('w') as f:
    f.write('s SATISFIABLE\n')
    for start in range(0, len(values), 20):
        f.write('v '+' '.join(str((i+1)*(1 if values[i] else -1))
                for i in range(start, min(start+20, len(values))))+' 0\n')
command = [sys.executable, str(Path(__file__).with_name('check_independent.py')),
           'model', '--base', meta['base'], '--pool', meta['pool'],
           '--solution', str(solution), '--cnf', str(folder/'system.cnf'),
           '--out', str(out/'witness.json')]
if t:
    command += ['--slice', str(t)]
os.execv(sys.executable, command)
