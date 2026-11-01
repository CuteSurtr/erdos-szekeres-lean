#!/usr/bin/env python3
"""Second check of point sets given as 'x y' lines: distinctness, S = -S with 0 not in S, the largest convex subset by
the cup+cap DP and the angular DP of ../review/refdp.c, and the number of convex subsets of each size (cup x cap
counting DP).  The DPs run on an exact orientation-sign table written by ../review/refdp_io.py (Python integers).
This code shares nothing with check_set.py.  Needs ../review/refdp compiled from ../review/refdp.c.
Usage (from this directory): python3 check_refdp.py FILE...
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'review'))
from refdp_io import run_c  # noqa: E402

for fn in sys.argv[1:]:
    pts = [tuple(int(t) for t in line.split()[:2]) for line in open(fn) if line.strip() and not line.startswith('#')]
    S = set(pts)
    tab = os.path.join(HERE, 'check_refdp_tab.bin')
    out = run_c(pts, tab, counts=True)
    os.remove(tab)
    print('file=%s distinct=%s centrally_symmetric(S=-S, 0 not in S)=%s max|coord|=%.3g' % (
        os.path.basename(fn), len(S) == len(pts), all((-x, -y) in S for x, y in pts) and (0, 0) not in S,
        max(max(abs(x), abs(y)) for x, y in pts)))
    print('  refdp:', out)
