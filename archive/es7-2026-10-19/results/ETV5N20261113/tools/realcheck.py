"""End-to-end sanity check of the rows: occupied state sets of real 5-cap-free octagon-free point sets must
violate no row.  Point sets: greedy random (uniform / perturbed parabola / arcs / clusters), plus the
'densest' ones kept.  usage: realcheck.py <seconds> [seed]"""
import json, sys, time, random, math
import etv_common as ec, rowsio
from geom import general, ok_class, states
secs = float(sys.argv[1]); rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 11)
rows = rowsio.load_all()
R = [(sum(1 << i for i in s), d, k) for s, (d, k) in rows.items()]
def cand(kind, Rr):
    if kind == 0: return (rng.randrange(-Rr, Rr), rng.randrange(-Rr, Rr))
    if kind == 1:
        x = rng.uniform(-1, 1); return (int(x * Rr), int((x * x * rng.choice([1, -1]) + rng.gauss(0, 0.05)) * Rr))
    if kind == 2:
        c = rng.choice([(-0.6, 0.3), (0.5, -0.4), (0.0, 0.8), (0.7, 0.7)]); return (int((c[0] + rng.gauss(0, 0.08)) * Rr), int((c[1] + rng.gauss(0, 0.08)) * Rr))
    t = rng.uniform(0, math.pi); r = 1 + rng.gauss(0, 0.02); return (int(r * math.cos(t) * Rr), int(r * math.sin(t) * Rr * rng.choice([1, -1])))
t0 = time.time(); nsets = 0; worst = 0; viol = 0; best_size = 0
while time.time() - t0 < secs:
    Rr = 10**6; P = []; mix = [rng.randrange(4) for _ in range(3)]
    for _ in range(300):
        x = cand(rng.choice(mix), Rr)
        if not general(P, x): continue
        if ok_class(sorted(P + [x])): P = sorted(P + [x])
    st, _, _ = states(P); occ = 0
    for s in st: occ |= 1 << s
    nsets += 1; best_size = max(best_size, len(P))
    for m, d, k in R:
        missing = (m & ~occ).bit_count()
        if missing < d: viol += 1; print('VIOLATED', k, bin(m).count('1'), d, P); sys.exit(1)
        worst = max(worst, bin(m & occ).count('1') / bin(m).count('1'))
print(json.dumps({'rows': len(R), 'sets': nsets, 'largest_set': best_size, 'violations': viol, 'max_row_occupancy_fraction': round(worst, 3), 'seconds': round(time.time() - t0)}))
