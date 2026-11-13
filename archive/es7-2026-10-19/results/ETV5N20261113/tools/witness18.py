"""Recover the 18-hole vector of the SAT cube 10111 (states 22,37,45,53,67) over final19/rows_all.json and check
it exactly against every row: the minimum over that row set is then exactly 18 (lower bound certified)."""
import json, subprocess, os, hashlib
import etv_common as ec
from pbcnf5 import build
rows = json.load(open('final19/rows_all.json'))
top, cls = build(rows, 18, ec.N, ec.FIXED_OCC)
br = [22, 37, 45, 53, 67]; bits = [1, 0, 1, 1, 1]
cls = cls + [[(s + 1) if b else -(s + 1)] for s, b in zip(br, bits)]
p = 'final19/witness_cube.cnf'
with open(p, 'w') as f:
    f.write(f'p cnf {top} {len(cls)}\n')
    for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
r = subprocess.run(['cadical', '-q', p], capture_output=True, text=True); os.remove(p)
assert r.returncode == 10, r.returncode
vals = set(int(x) for line in r.stdout.splitlines() if line.startswith('v') for x in line.split()[1:])
H = [i for i in range(ec.N) if (i + 1) in vals]
viol = sum(1 for s, d in rows if len(set(s) & set(H)) < d)
print(json.dumps({'rows': len(rows), 'rows_sha256': hashlib.sha256(open('final19/rows_all.json', 'rb').read()).hexdigest(),
                  'holes': H, 'n_holes': len(H), 'fixed_states_occupied': not (set(H) & set(ec.FIXED_OCC)), 'violated_rows': viol,
                  'hole_states': [ec.STATES[i] for i in H]}))
