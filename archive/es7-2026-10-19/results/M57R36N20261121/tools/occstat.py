#!/usr/bin/env python3
"""occstat.py CNF NAMESPKL: occurrence counts of the 56 occupancy literals; unit clauses on them."""
import sys, pickle, collections
cnf, pk = sys.argv[1], sys.argv[2]
names = pickle.load(open(pk, 'rb'))['names']
occ = {v: k[1] for k, v in names.items() if k[0] == 'occ'}
pos = collections.Counter(); neg = collections.Counter(); units = {}
with open(cnf) as f:
    for line in f:
        if line[0] in 'pc': continue
        lits = line.split()[:-1]
        if len(lits) == 1:
            l = int(lits[0])
            if abs(l) in occ: units[occ[abs(l)]] = l > 0
        for x in lits:
            l = int(x); a = abs(l)
            if a in occ:
                (pos if l > 0 else neg)[occ[a]] += 1
for s in sorted(occ.values()):
    print(s, pos[s], neg[s], units.get(s, ''))
