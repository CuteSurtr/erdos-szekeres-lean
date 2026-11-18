#!/usr/bin/env python3
"""mkpat.py BASE PATTERN.json OUT [--order] : BASE.cnf + unit clauses fixing the occupancy pattern
(and with --order also the chronological order) of PATTERN."""
import sys, pickle, json
base, pat, out = sys.argv[1:4]
meta = pickle.load(open(base + '.names.pkl', 'rb')); names = meta['names']
p = json.load(open(pat)); order = p['order']; occ = set(order)
NS = sum(1 for k in names if k[0] == 'occ')
units = [(names[('occ', s)] if s in occ else -names[('occ', s)]) for s in range(NS)]
if '--order' in sys.argv:
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            units.append(names[('P', order[i], order[j])])
with open(base) as f, open(out, 'w') as g:
    hdr = f.readline().split()
    g.write(f'p cnf {hdr[2]} {int(hdr[3]) + len(units)}\n')
    while True:
        c = f.read(1 << 24)
        if not c: break
        g.write(c)
    for u in units: g.write(f'{u} 0\n')
print(int(hdr[3]), len(units))
