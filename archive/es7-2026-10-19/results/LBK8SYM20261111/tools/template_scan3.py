#!/usr/bin/env python3
"""Cluster (blow-up) template phase scan (evidence only; a CAND is a candidate for the exact pipeline).
B base orbits with phases psi_b (psi_1 = 0) carry clusters of n_b consecutive layers in radius order; within a cluster
the phases are psi_b + eps * N(0, 1) (eps log-uniform, units of 2pi/m); all radii are left to the LP of the
phase-fixed CEGAR (pfenc + pair cuts), so the LP chooses the radial shape of each cluster and the base radii.
usage: template_scan3.py M T CENTRE OUT TAG TMAX SEED NSAMPLES [B list e.g. 2,3] [sizes e.g. 6,5 or -]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pfenc

m, t, centre, out, tag, tmax, seed, nsamp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], float(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
Bs = [int(x) for x in sys.argv[9].split(',')] if len(sys.argv) > 9 else [2, 3]
fixed_sizes = None if len(sys.argv) <= 10 or sys.argv[10] == '-' else [int(x) for x in sys.argv[10].split(',')]
pfenc.PAIRS = True
os.makedirs(out, exist_ok=True)
logf = open(os.path.join(out, 'log_%s.txt' % tag), 'a'); tsv = open(os.path.join(out, 'res_%s.tsv' % tag), 'a')
def log(s):
    logf.write(time.strftime('%H:%M:%S ') + s + '\n'); logf.flush()
U = 2 * math.pi / m
rng = np.random.default_rng(seed)
stop = time.mktime(time.strptime('2026-11-12 03:55', '%Y-%m-%d %H:%M'))
for k in range(nsamp):
    if time.time() > stop:
        break
    if fixed_sizes:
        sizes = list(fixed_sizes); B = len(sizes)
    else:
        B = int(rng.choice(Bs))
        cuts = np.sort(rng.choice(np.arange(1, t), B - 1, replace=False))
        sizes = list(np.diff(np.concatenate([[0], cuts, [t]])))
    psi = np.concatenate([[0.0], rng.uniform(0, 1, B - 1)])
    eps = 10 ** rng.uniform(-4, -1.5)
    th = np.zeros(t); pos = 0
    for b, n in enumerate(sizes):
        th[pos:pos + n] = (psi[b] + eps * rng.normal(0, 1, n)) * U
        pos += n
    th = (th - th[0]) % U
    lr = -np.arange(t) * 0.01
    name = '%s_%d' % (tag, k)
    t0 = time.time()
    try:
        r = pfenc.run(m, t, centre, th, lr, tmax, log, out, name)
    except ValueError as e:
        r = ('DEGEN', 0, 0, str(e))
    tsv.write('%s\t%s\t%s\t%.2e\t%s\t%d\t%.3e\t%.1f\n' % (name, sizes, np.round(psi, 3).tolist(), eps, r[0], r[1], r[2], time.time() - t0)); tsv.flush()
    if r[0] == 'TIMEOUT':
        json.dump(dict(m=m, centre=centre, lr=list(map(float, lr)), th=list(map(float, th)), note='live (template3)'),
                  open(os.path.join(out, 'live_%s.json' % name), 'w'))
log('done')
