#!/usr/bin/env python3
"""Free cuts (infinitesimal scale gaps between consecutive orbits in radius order) of 3-fold sets; the centre, if
present, stays at the origin.  usage: arch3.py FILES"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from double_exact import peval, read_set, orbits_of
for fn in sys.argv[1:]:
    P = read_set(fn, 3)
    orbs, centre = orbits_of(P, 3)
    t = len(orbs)
    def run(cuts):
        pts = []; e = 0
        for i, o in enumerate(orbs):
            if i in cuts:
                e += 1
            for p in o:
                pts.append([(e, p[0], p[1])])
        if centre:
            pts.append([(0, 0, 0)])
        ml, cnt, nz = peval(pts, 8)
        return None if nz else cnt[8]
    base = run(set())
    free = [c for c in range(1, t) if run({c}) == base]
    print('%s orbits=%d centre=%s n8=%s free_cuts=%s all_free_n8=%s' % (os.path.basename(fn), t, centre, base, free,
          run(set(free)) if free else '-'), flush=True)
