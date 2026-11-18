#!/usr/bin/env python3
"""prio.py CNF MODE > file : decision-priority literals for drv/occfirst (occupancy variables).
MODE: asc / desc (state index order, phase 'occupied'), ascneg / descneg (phase 'hole'),
      ascP (occupancy asc, then all order variables P)"""
import sys, pickle
meta = pickle.load(open(sys.argv[1] + '.names.pkl', 'rb'))
names = meta['names']; mode = sys.argv[2]
occ = sorted((k[1], v) for k, v in names.items() if k[0] == 'occ')
if mode.startswith('desc'):
    occ = occ[::-1]
sgn = -1 if 'neg' in mode else 1
out = [sgn * v for _, v in occ]
if mode.endswith('P'):
    out += [v for k, v in sorted(names.items(), key=lambda kv: kv[1]) if k[0] == 'P']
print(' '.join(map(str, out)))
