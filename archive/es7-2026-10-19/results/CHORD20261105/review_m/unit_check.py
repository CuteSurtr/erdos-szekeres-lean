#!/usr/bin/env python3
"""Step 5: stream a gen.py CNF, collect its unit clauses, and check chord clause files against them:
 - chord clause whose orientation literal is FALSIFIED by a base unit (would force a condition / signal a conflict)
 - chord clause fully falsified by base units (direct contradiction)
 - chord unit literal whose negation is a base unit
 - clauses already satisfied by base units (redundant; informational)
Then unit-propagate (base units + all chord clauses of the file) to fixpoint and report any conflict.
Usage: unit_check.py CNF NTRIPLE CHORDFILE [CHORDFILE...]"""
import sys
cnf, ntr = sys.argv[1], int(sys.argv[2])
units = set()
ncl = 0
with open(cnf) as f:
    for line in f:
        if line[0] in 'pc':
            continue
        ncl += 1
        sp = line.split()
        if len(sp) == 2:
            units.add(int(sp[0]))
conf_units = [x for x in units if -x in units]
print('%s: %d clauses, %d unit clauses (%d triple-var units), self-contradictory units: %d' %
      (cnf, ncl, len(units), sum(1 for x in units if abs(x) <= ntr), len(conf_units)))
for fn in sys.argv[3:]:
    cls = [[int(x) for x in l.split()[:-1]] for l in open(fn)]
    olit_false = [c for c in cls if -[x for x in c if abs(x) <= ntr][0] in units]
    falsified = [c for c in cls if all(-x in units for x in c)]
    unit_conf = [c for c in cls if len(c) == 1 and -c[0] in units]
    satisfied = [c for c in cls if any(x in units for x in c)]
    anyfalse = [c for c in cls if any(-x in units for x in c)]
    print(' %s: %d clauses; orientation literal falsified by a base unit: %d; fully falsified: %d; '
          'chord unit vs base unit conflicts: %d; already satisfied by base units: %d; some literal falsified: %d' %
          (fn, len(cls), len(olit_false), len(falsified), len(unit_conf), len(satisfied), len(anyfalse)))
    for c in olit_false[:5]:
        print('   olit-false', c)
    # unit propagation to fixpoint
    assign = set(units)
    changed = True
    conflict = None
    while changed and conflict is None:
        changed = False
        for c in cls:
            if any(x in assign for x in c):
                continue
            free = [x for x in c if -x not in assign]
            if not free:
                conflict = c
                break
            if len(free) == 1:
                assign.add(free[0])
                changed = True
    print('   unit propagation (base units + this file): %s; literals forced beyond base units: %d' %
          ('CONFLICT at %s' % conflict if conflict else 'no conflict', len(assign) - len(units)))
