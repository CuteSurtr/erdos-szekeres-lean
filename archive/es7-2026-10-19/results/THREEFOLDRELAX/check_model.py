#!/usr/bin/env python3
"""check_model.py CNF MODEL : every clause of CNF has a true literal under the 'v' lines of MODEL (exact)."""
import sys
val = set()
for line in open(sys.argv[2]):
    if line.startswith('v'):
        val.update(int(x) for x in line.split()[1:] if x != '0')
bad = n = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line[0] in 'pc': continue
        lits = line.split()[:-1]
        n += 1
        if not any(int(l) in val for l in lits): bad += 1
print({'clauses': n, 'falsified': bad, 'model_lits': len(val)})
