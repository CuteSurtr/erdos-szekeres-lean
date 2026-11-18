#!/usr/bin/env python3
"""units_scan.py NAME -- progress probe: unit clauses on occupancy variables that the running solver
has already written to run/NAME.lrat (discovery only)."""
import sys, pickle, subprocess, re
name = sys.argv[1]
meta = pickle.load(open(f'run/{name}.cnf.names.pkl', 'rb'))
names = meta['names']
import cat_common
states = cat_common.make(meta['CA'], meta['CB'])[0]
occ = {v: k[1] for k, v in names.items() if k[0] == 'occ'}
out = subprocess.run(['grep', '-a', '-E', '^[0-9]+ -?[0-9]+ 0 ', f'run/{name}.lrat'], capture_output=True, text=True).stdout
holes = []; forced = []; nunits = 0
for line in out.split('\n'):
    p = line.split()
    if len(p) < 3: continue
    nunits += 1
    l = int(p[1])
    if abs(l) in occ:
        (forced if l > 0 else holes).append(states[occ[abs(l)]])
print(name, 'units', nunits, 'occupancy units: holes', len(holes), 'forced occupied', len(forced))
print(' holes:', sorted(set(holes)))
print(' forced:', sorted(set(forced)))
