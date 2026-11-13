#!/usr/bin/env python3
"""addunits.py IN.cnf OUT.cnf lit1 lit2 ...  : copy a DIMACS CNF and append unit clauses"""
import sys
src, dst = sys.argv[1], sys.argv[2]
lits = [int(x) for x in sys.argv[3:]]
with open(src) as f, open(dst, 'w') as g:
    hdr = f.readline().split()
    assert hdr[0] == 'p' and hdr[1] == 'cnf'
    g.write('p cnf %s %d\n' % (hdr[2], int(hdr[3]) + len(lits)))
    while True:
        buf = f.read(1 << 24)
        if not buf:
            break
        g.write(buf)
    for l in lits:
        g.write('%d 0\n' % l)
