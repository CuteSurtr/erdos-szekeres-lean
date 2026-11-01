#!/usr/bin/env python3
"""Coverage check for a cube file: base CNF plus one clause (negation of the cube) per cube
must be UNSAT.  Together with an LRAT-verified UNSAT for every cube this shows the base CNF
is UNSAT (cube leaves cover everything march_cu refuted internally as well).
usage: cover.py base.cnf cubes.icnf [extra.icnf ...]   (cubes replaced by their split children
are covered recursively if the children files are listed; here we use the final leaf list)"""
import sys, subprocess, os, json
CAD = '/tmp/claude-0/sw/cadical/build/cadical'; LC = '/tmp/claude-0/sw/drat-trim/lrat-check'
base, leaves = sys.argv[1], sys.argv[2]
cubes = []
if leaves.endswith('.jsonl'):
    for l in open(leaves):
        d = json.loads(l)
        if d['status'] == 'UNSAT' and d.get('lrat') == 'VERIFIED': cubes.append(d['cube'])
else:
    cubes = [[int(x) for x in l.split()[1:] if x != '0'] for l in open(leaves) if l.startswith('a')]
lines = open(base).read().split('\n')
h = [i for i, l in enumerate(lines) if l.startswith('p cnf')][0]
nv, nc = map(int, lines[h].split()[2:4])
p = '/tmp/claude-0/mx/cover.cnf'
with open(p, 'w') as f:
    f.write('p cnf %d %d\n' % (nv, nc + len(cubes)))
    f.write('\n'.join(l for i, l in enumerate(lines) if i > h and l and not l.startswith('c')) + '\n')
    for c in cubes: f.write(' '.join(str(-x) for x in c) + ' 0\n')
r = subprocess.run([CAD, '-q', '--lrat', '--binary=false', p, p + '.lrat'], capture_output=True, text=True)
st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'UNKNOWN')
res = dict(base=base, leaves=leaves, ncubes=len(cubes), status=st)
if st == 'UNSAT':
    o = subprocess.run([LC, p, p + '.lrat'], capture_output=True, text=True).stdout
    res['lrat'] = 'VERIFIED' if 'c VERIFIED' in o else 'NOT VERIFIED'
for q in (p, p + '.lrat'):
    if os.path.exists(q): os.remove(q)
print(json.dumps(res))
