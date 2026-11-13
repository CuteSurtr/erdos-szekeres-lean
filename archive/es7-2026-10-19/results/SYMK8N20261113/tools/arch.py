#!/usr/bin/env python3
"""Architecture of a 4-fold set: which layer boundaries can be stretched to an infinitesimal gap without creating
octagons (exact limit order type).  Prints radii ratios and, for each cut c (gap between layer c-1 and c), the number
of convex octagons of the stretched set; then tests all free cuts together."""
import sys, math
sys.path.insert(0, '.')
from stack import *
for fn in sys.argv[1:]:
    P = read_pts(fn, 4)
    L, c = layers4(P)
    t = len(L)
    r = [math.sqrt(o[0][0] ** 2 + o[0][1] ** 2) for o in L]
    ph = [math.degrees(math.atan2(o[0][1], o[0][0])) % 90 for o in L]
    def run(cuts):
        e = 0; pts = []
        for i, o in enumerate(L):
            if i in cuts: e += 1
            for pt in o: pts.append((e, pt[0], pt[1]))
        ml, cnt, z = evaluate(pts, 8)
        return cnt[8] if cnt else None
    base = run(set())
    free = [cc for cc in range(1, t) if run({cc}) == base]
    allf = run(set(free))
    print('%s t=%d base_n8=%s free_cuts=%s all_free_n8=%s' % (fn.split('/')[-1], t, base, free, allf))
    print('   ratios', ' '.join('%.3f' % (r[i] / r[i - 1]) for i in range(1, t)))
    print('   phases', ' '.join('%.1f' % p for p in ph), flush=True)
