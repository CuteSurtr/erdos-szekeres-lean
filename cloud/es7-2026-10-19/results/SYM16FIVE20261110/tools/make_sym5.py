#!/usr/bin/env python3
"""SYM16FIVE20261110: write, for each F/data/sym16/m5/model*.pts (3 orbits of 5 in rotation order, then the centre),
the exactly 5-fold symmetric set with orbit representatives a + b*zeta (zeta = e^{2 pi i/5}, a, b integers nearest to
the file's first point of each orbit), in the input format of PRIMEFOLD/rule/sym_cvx.c.
usage: make_sym5.py F_M5_DIR OUTDIR"""
import sys, os, glob, math
c1, sn1 = math.cos(2 * math.pi / 5), math.sin(2 * math.pi / 5)
src, out = sys.argv[1], sys.argv[2]
for f in sorted(glob.glob(os.path.join(src, 'model*.pts'))):
    P = [tuple(int(x) for x in l.split()) for l in open(f) if l.strip()]
    assert len(P) == 16 and P[15] == (0, 0)
    with open(os.path.join(out, os.path.basename(f)), 'w') as g:
        g.write('# exact 5-fold version of F/data/sym16/m5/%s: orbit representatives a + b zeta, then the centre\n'
                % os.path.basename(f))
        g.write('5 3 1\n')
        for j in range(3):
            x, y = P[5 * j]; b = round(y / sn1); a = round(x - b * c1)
            g.write('%d %d 0 0 0\n' % (a, b))
