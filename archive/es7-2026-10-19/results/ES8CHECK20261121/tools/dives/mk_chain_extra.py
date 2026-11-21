#!/usr/bin/env python3
"""mk_chain_extra.py CHAIN70 ZZS OUT: the Z- and Z*-rows plus the 70-state (6,6)-chain classes, as one FASTBB row list.

CHAIN70 is logs/rows-search/chain70_rows.json (classes of 70 states, one common rhs); ZZS is
ES303N20261120/data/zzs_rows.json.  Z and Z* come first; a class whose support is already present is dropped.
"""
import json, sys

c = json.load(open(sys.argv[1]))
z = json.load(open(sys.argv[2]))
base = {tuple(sorted(r['support'])) for r in z}
extra = list(z)
for cl in c['classes']:
    s = tuple(sorted(cl if isinstance(cl, list) else cl['support']))
    if s in base:
        continue
    base.add(s)
    extra.append({'support': list(s), 'rhs': int(c['rhs'])})
print('extra rows', len(extra), 'sizes', sorted({len(r['support']) for r in extra}))
json.dump(extra, open(sys.argv[3], 'w'))
