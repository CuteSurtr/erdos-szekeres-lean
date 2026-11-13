#!/usr/bin/env python3
"""Cross-checks of the limit evaluator.
(1) Realization: a limit configuration (ES8SYM 52-point set + a twin orbit) is exported with eps = 2^-s to plain
    integer coordinates and its convex k-gon counts are recomputed by stack.py (independent orientation code on big
    integers, single scale) -- they must equal the limit counts for s large enough.
(2) Arc completeness (sampling): for a twin family, 2,000 random directions are evaluated; none may have fewer
    octagons than the minimum over the arc representatives (the order type is constant on each open arc)."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from double_exact import peval, read_set, orbits_of, critical_arcs
import stack

P = read_set(os.path.join(os.path.dirname(__file__), '..', 'sets', 'lib4', 'es8sym_52.pts'), 4)
orbs, centre = orbits_of(P, 4)
reps = [[(0, o[0][0], o[0][1])] for o in orbs]


def config(reps):
    pts = []
    for r in reps:
        cur = r
        for _ in range(4):
            pts.append(cur)
            cur = [(e, -y, x) for (e, x, y) in cur]
    return pts


l = 8
p0 = reps[l]
allp = config(reps)
dirs = []
for q in allp:
    if q == p0:
        continue
    v = (q[0][1] - p0[0][1], q[0][2] - p0[0][2])
    dirs += [v, (-v[0], -v[1])]
arcs = critical_arcs(dirs)
vals = []
for d in arcs:
    ml, cnt, nz = peval(config(reps + [p0 + [(1, d[0], d[1])]]), 8)
    vals.append((cnt[8], d))
vals.sort()
best, dbest = vals[0]
print('twin of layer %d: %d arcs, min octagons %d at d=%s' % (l, len(arcs), best, dbest))
# (1) realization at eps = 2^-s
for s in (20, 40, 60):
    pts = config(reps + [p0 + [(1, dbest[0], dbest[1])]])
    flat = []
    for p in pts:
        X = sum(x << (s * (1 - e)) for (e, x, y) in p)
        Y = sum(y << (s * (1 - e)) for (e, x, y) in p)
        flat.append((0, X, Y))
    ml, cnt, z = stack.evaluate(flat, 8)
    print('  realized with eps = 2^-%d: zero orientations %d, octagons %s (limit: %d)' % (s, z, cnt[8] if cnt else None, best))
# (2) sampling
random.seed(7)
mn = None
for _ in range(2000):
    import math
    a = random.uniform(0, 2 * math.pi)
    d = (int(10 ** 9 * math.cos(a)), int(10 ** 9 * math.sin(a)))
    ml, cnt, nz = peval(config(reps + [p0 + [(1, d[0], d[1])]]), 8)
    if nz:
        continue
    mn = cnt[8] if mn is None else min(mn, cnt[8])
print('  2000 random directions: min octagons %s (must be >= %d)' % (mn, best))
