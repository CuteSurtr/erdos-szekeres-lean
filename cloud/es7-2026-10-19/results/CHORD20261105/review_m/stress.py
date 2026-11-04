#!/usr/bin/env python3
"""High-precision stress test of chord clause families on real configurations in gen.py normal form.
Config: t layers, radii strictly decreasing, theta_0 = 0, theta_i in (0, 360/m); vertex (i,k) at theta_i + 360k/m.
Assignment: triple var v := [orient(canonical sorted C) > 0] (80 digits), Y(i,j) := [psi_i < psi_j],
H(i) := [theta_i < 180/m] (odd m), psi_i = theta_i mod (180/m) (odd) / theta_i (even).
Checks every clause of the chord family; every NBASE-th config also checks gen.py's order+angle+nest clauses (semantic
cross-check of the assignment).  Usage: stress.py m t CHORDFILE BASECNF NCONF SEED NBASE"""
import sys, random, itertools, time
import mpmath as mp
sys.path.insert(0, '<rot45-work-dir>/review_m')
from verify_exact import numbering
mp.mp.dps = 80

m, t, chf, basecnf, NCONF, SEED, NBASE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
m, t, NCONF, SEED, NBASE = int(m), int(t), int(NCONF), int(SEED), int(NBASE)
odd = m % 2 == 1
tv, inv, Y, H = numbering(m, t)
ntr = len(tv)
chord = [[int(x) for x in l.split()[:-1]] for l in open(chf)]
# base clauses: order + angle + nest ranges
import json
meta = json.load(open(basecnf + '.json'))
nbase = meta['ranges']['nest'][1]
base = []
with open(basecnf) as f:
    f.readline()
    for _ in range(nbase):
        base.append([int(x) for x in f.readline().split()[:-1]])
need_ch = sorted({abs(x) for c in chord for x in c if abs(x) <= ntr})
need_all = sorted({abs(x) for c in base for x in c if abs(x) <= ntr} | set(need_ch))
print('m=%d t=%d chord clauses %d (triple vars %d); base clauses %d (triple vars %d)' %
      (m, t, len(chord), len(need_ch), len(base), len(need_all)), flush=True)

u = mp.mpf(180) / m
W = mp.mpf(360) / m
DEG = mp.pi / 180


def gen_config(rng, mode):
    eps = lambda: mp.mpf(10) ** (-rng.uniform(9, 12)) * (1 + rng.random())
    th = [mp.mpf(0)]
    anchors = [mp.mpf(0), u, W]                        # interval ends for psi / H
    extra = [W * q / 24 for q in range(1, 24)]        # rational points (chord boundaries etc.)
    if mode == 'uniform':
        for i in range(1, t):
            th.append(W * mp.mpf(rng.random()))
    elif mode == 'boundary':
        for i in range(1, t):
            a = rng.choice(anchors)
            sgn = 1 if a == 0 else (-1 if a == W else rng.choice([-1, 1]))
            th.append(a + sgn * eps() if rng.random() < 0.8 else W * mp.mpf(rng.random()))
    elif mode == 'cluster':      # all psi within ~1e-9 of a common value, random H
        c = (u if odd else W) * mp.mpf(rng.choice([rng.random(), 1e-3, 1 - 1e-3]))
        if rng.random() < 0.3:
            c = eps() if rng.random() < 0.5 else (u if odd else W) - eps()
        for i in range(1, t):
            v = c + (rng.random() - 0.5) * mp.mpf(10) ** -9
            if odd and rng.random() < 0.5:
                v += u
            th.append(v % W)
    elif mode == 'pairs':        # psi_i ~ psi_j with H different, plus near-zero/near-u psi
        base_ = []
        for i in range(1, t):
            if base_ and rng.random() < 0.6:
                b = rng.choice(base_) + (rng.random() - 0.5) * 2 * eps()
                v = b + (u if (odd and rng.random() < 0.5) else 0)
                v = v % W
            else:
                v = rng.choice(anchors[:2] + extra) + rng.choice([-1, 1]) * eps()
                v = v % W
            base_.append(v % (u if odd else W))
            th.append(v)
    elif mode == 'rational':
        for i in range(1, t):
            th.append((rng.choice(extra) + rng.choice([-1, 1]) * eps()) % W)
    # radii
    rmode = rng.choice(['uniform', 'tiny', 'near1', 'mixed', 'nested_tight', 'nested_tight', 'wild'])
    r = [mp.mpf(1)]
    for i in range(1, t):
        if rmode == 'uniform':
            q = mp.mpf(rng.uniform(0.05, 0.999))
        elif rmode == 'tiny':
            q = mp.mpf(10) ** (-rng.uniform(6, 12))
        elif rmode == 'near1':
            q = 1 - mp.mpf(10) ** (-rng.uniform(6, 12))
        elif rmode == 'mixed':
            q = rng.choice([mp.mpf(10) ** (-12), 1 - mp.mpf(10) ** -12, mp.mpf(rng.random()) * 0.999 + 1e-6])
        elif rmode == 'nested_tight':
            # largest ratio keeping layer i inside conv(layer i-1), times (1 - tiny) or a random fraction of it
            qmax = mp.inf
            for k in range(m):
                al = (th[i] - th[i - 1]) % W
                qmax = min(qmax, mp.cos(u * DEG) / mp.cos((al - u) * DEG))
            q = qmax * (1 - mp.mpf(10) ** (-rng.uniform(3, 12))) if rng.random() < 0.7 else qmax * mp.mpf(rng.uniform(1e-3, 1))
        if rmode == 'wild':
            r.append(mp.mpf(10) ** (-rng.uniform(0, 8)))      # NOT monotone: chord clauses are radius-free
        else:
            r.append(r[-1] * q)
    return th, r


def assignment(th, r, vars_):
    rmax, rmin = max(r), min(r)
    rng_digits = int(mp.ceil(mp.log10(rmax / rmin))) if rmin < rmax else 0
    dps = 60 + 3 * rng_digits
    with mp.workdps(dps):
        thp = [mp.mpf(x) for x in th]
        pts = []
        for i in range(t):
            for k in range(m):
                a = (thp[i] + mp.mpf(360) / m * k) * mp.pi / 180
                pts.append((r[i] * mp.cos(a), r[i] * mp.sin(a)))
        val = {}
        degenerate = False
        thr = mp.mpf(10) ** (-(dps - 20)) * rmax ** 2
        def orient(a, b, c):
            (ax, ay), (bx, by), (cx, cy) = pts[a], pts[b], pts[c]
            return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        for v in vars_:
            o = orient(*inv[v])
            if abs(o) < thr:
                degenerate = True
            val[v] = o > 0
        # nesting: every vertex of layer i+1 strictly inside conv(layer i) (strictly left of every ccw edge)
        nested = all(orient(i * m + k, i * m + (k + 1) % m, (i + 1) * m + l) > thr
                     for i in range(t - 1) for k in range(m) for l in range(m))
    if odd:
        psi = [x % u for x in th]
    else:
        psi = list(th)
    for (i, j), v in Y.items():
        val[v] = psi[i] < psi[j]
    for i, v in H.items():
        val[v] = th[i] < u
    # phase genericity / normal form (required for the encoder's labelling)
    gen_ok = all(abs(psi[i] - psi[j]) > mp.mpf(10) ** -30 for i in range(t) for j in range(i)) \
        and all(p > mp.mpf(10) ** -30 for p in psi[1:]) and all(0 < x < W for x in th[1:])
    return val, degenerate, gen_ok, nested


def sat(c, val):
    return any(val[abs(x)] == (x > 0) for x in c)


rng = random.Random(SEED)
modes = ['uniform', 'boundary', 'cluster', 'pairs', 'rational']
viol = 0
nbase_checked = 0
basefail = 0
skipped = 0
t0 = time.time()
from collections import Counter
mc = Counter()
for it in range(NCONF):
    mode = modes[it % len(modes)]
    th, r = gen_config(rng, mode)
    dobase = (it % NBASE == 0)
    val, degenerate, gen_ok, nested = assignment(th, r, need_all if dobase else need_ch)
    if not gen_ok or degenerate:
        skipped += 1
        continue
    if nested:
        mc['nested'] += 1
    mc[mode] += 1
    for c in chord:
        if not sat(c, val):
            viol += 1
            if viol <= 10:
                print('VIOLATION clause', c, 'mode', mode, 'theta', [mp.nstr(x, 25) for x in th],
                      'r', [mp.nstr(x, 25) for x in r], flush=True)
    if dobase and nested:
        nbase_checked += 1
        for c in base:
            if not sat(c, val):
                basefail += 1
                if basefail <= 5:
                    print('BASE CLAUSE VIOLATED (semantic mismatch?)', c, mode, flush=True)
    if (it + 1) % 200 == 0:
        print('%d configs, %d chord violations, %d base checks (%d base violations), skipped %d, %.0fs' %
              (it + 1, viol, nbase_checked, basefail, skipped, time.time() - t0), flush=True)
print('DONE m=%d t=%d seed=%d: configs used %d %s, chord clause evaluations %d, chord violations %d; '
      'base-CNF semantic checks %d configs x %d clauses, base violations %d; skipped %d' %
      (m, t, SEED, sum(v for k, v in mc.items() if k != 'nested'), dict(mc), sum(v for k, v in mc.items() if k != 'nested') * len(chord), viol, nbase_checked, len(base),
       basefail, skipped), flush=True)
