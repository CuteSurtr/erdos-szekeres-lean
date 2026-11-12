"""read/write m-fold .pts files (rows w_0..w_{m-1}: point sum_j w_j zeta^j) as (lr, th, centre) float configurations."""
import math, cmath, json, numpy as np


def read_pts_cfg(fn, m):
    zs = []
    centre = 0
    for l in open(fn):
        l = l.split('#')[0].split()
        if not l:
            continue
        w = list(map(int, l))
        z = sum(c * cmath.exp(2j * math.pi * j / m) for j, c in enumerate(w))
        if all(c == 0 for c in w):
            centre = 1
            continue
        zs.append(z)
    # one representative per orbit: group by radius
    reps = []
    for z in zs:
        if not any(abs(abs(z) - abs(r)) < 1e-12 * abs(z) and abs(((cmath.phase(z) - cmath.phase(r)) * m / (2 * math.pi)) - round((cmath.phase(z) - cmath.phase(r)) * m / (2 * math.pi))) < 1e-9 for r in reps):
            reps.append(z)
    reps.sort(key=lambda z: -abs(z))
    r0 = abs(reps[0])
    lr = np.array([math.log(abs(z) / r0) for z in reps])
    th = np.array([cmath.phase(z) % (2 * math.pi / m) for z in reps])
    return lr, th, centre


def write_cfg(fn, m, lr, th, centre, counts=None, note=''):
    o = np.argsort(-np.asarray(lr))
    d = dict(m=m, centre=int(centre), lr=[float(v) for v in np.asarray(lr)[o]],
             th=[float(v % (2 * math.pi / m)) for v in np.asarray(th)[o]],
             counts=({str(k): int(counts[k]) for k in range(3, 9)} if counts is not None else None), note=note)
    tmp = fn + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(d, f, indent=1)
    import os
    os.replace(tmp, fn)


def read_cfg(fn):
    d = json.load(open(fn))
    return d.get('m'), np.array(d['lr'], float), np.array(d['th'], float), int(d.get('centre', 0))
