#!/usr/bin/env python3
"""Evaluate a CNF (or clause file) on the exact assignment of label8.py.
Clauses whose variables are all assigned (triple-orbit and Y variables) must be satisfied by a real configuration
(soundness test).  Clauses with other (chain) variables are counted only; optionally write the assignment as unit
clauses (--units OUT) so that a SAT solver can decide CNF + units (chain variables free).
usage: check_cnf.py ASSIGN.json FILE [FILE...] [--units OUT]"""
import sys, json
args = sys.argv[1:]
units = None
if '--units' in args:
    i = args.index('--units'); units = args[i + 1]; del args[i:i + 2]
d = json.load(open(args[0]))
val = {int(k): v for k, v in d['val'].items()}
tot_bad = 0
for fn in args[1:]:
    n = nfull = bad = other = 0
    first = None
    with open(fn) as f:
        for line in f:
            if not line.strip() or line[0] in 'cp':
                continue
            lits = [int(x) for x in line.split()[:-1]]
            n += 1
            if all(abs(l) in val for l in lits):
                nfull += 1
                if not any(val[abs(l)] == (l > 0) for l in lits):
                    bad += 1
                    if first is None:
                        first = line.strip()
            else:
                other += 1
    tot_bad += bad
    print('%s: clauses %d, fully assigned %d, VIOLATED %d, with other vars %d %s' % (
        fn, n, nfull, bad, other, ('first violated: ' + first) if first else ''), flush=True)
if units:
    with open(units, 'w') as f:
        for v in sorted(val):
            f.write('%d 0\n' % (v if val[v] else -v))
    print('wrote %d units to %s' % (len(val), units))
print('TOTAL VIOLATED', tot_bad)
