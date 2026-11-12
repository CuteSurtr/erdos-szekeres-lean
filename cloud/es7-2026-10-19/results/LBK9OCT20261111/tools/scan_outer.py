"""Evidence only: add one extra octagon (lr, phase grid) to a 15-layer float configuration and count convex 9-gons."""
import sys, math, json
sys.path.insert(0, 'tools'); import ev9
cfg = sys.argv[1]; lo, hi, na, nt = float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
L = [list(map(float, l.split())) for l in open(cfg) if l.strip() and not l.startswith('#')]
L.sort(key=lambda x: -x[0]); th0 = L[0][1]; l0 = L[0][0]
lr = [a - l0 for a, _ in L]; th = [(b - th0) for _, b in L]
best = (1e18, None)
for ia in range(na):
    a = lo + (hi - lo) * (ia + 0.5) / na
    row = []
    for it in range(nt):
        p = 2 * math.pi / 8 * (it + 0.5) / nt
        c, md = ev9.count_cfg(lr + [a], th + [p], 9)
        row.append(c)
        if c < best[0]:
            best = (c, (a, p, md))
    print('lr %8.4f min %d at phase idx %d' % (a, min(row), row.index(min(row))), flush=True)
print('BEST', best, flush=True)
