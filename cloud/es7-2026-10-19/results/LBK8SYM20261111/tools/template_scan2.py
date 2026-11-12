#!/usr/bin/env python3
"""Random multi-arm template phase scan (evidence only; a CAND is a candidate for the exact pipeline).
Phase vector: outer layer at phase 0; G arms (G = 1..3) of consecutive layers in radius order, arm g with start phase
phi_g and linear drift D_g (units of 2pi/m), optionally in near-twin pairs; then nin inner layers with random phases.
All radii are left to the LP of the phase-fixed CEGAR (pfenc + pair cuts).
usage: template_scan2.py M T CENTRE OUT TAG TMAX SEED NSAMPLES [ninmax] [Gmax]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pfenc

m, t, centre, out, tag, tmax, seed, nsamp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], float(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
ninmax = int(sys.argv[9]) if len(sys.argv) > 9 else 2
gmax = int(sys.argv[10]) if len(sys.argv) > 10 else 3
pfenc.PAIRS = True
CONF = int(os.environ.get("CONF", "300000"))
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
    nin = int(rng.integers(0, ninmax + 1))
    G = int(rng.integers(1, gmax + 1))
    nrest = t - 1 - nin
    if nrest < G:
        G = 1
    cuts = np.sort(rng.choice(np.arange(1, nrest), G - 1, replace=False)) if G > 1 else np.array([], int)
    sizes = np.diff(np.concatenate([[0], cuts, [nrest]]))
    th = np.zeros(t); desc = []
    pos = 1
    for g, n in enumerate(sizes):
        phi = rng.uniform(-0.5, 0.5) if g > 0 or rng.random() < 0.5 else rng.choice([-1, 1]) * 10 ** rng.uniform(-2, -0.6)
        D = rng.choice([-1, 1]) * rng.uniform(0.0, float(os.environ.get("DMAX", "0.45")))
        tw = rng.random() < 0.5
        s = np.linspace(0, 1, n) if n > 1 else np.zeros(1)
        if tw and n > 1:
            s = np.repeat(np.linspace(0, 1, (n + 1) // 2), 2)[:n] + np.tile([0, 2e-4], n)[:n]
        th[pos:pos + n] = (phi + D * s) * U + rng.normal(0, 1e-4, n) * U
        desc.append('%d:%.3f%+.3f%s' % (n, phi, D, 't' if tw else ''))
        pos += n
    th[pos:] = rng.uniform(0, 1, nin) * U
    th = th % U
    lr = -np.arange(t) * 0.3
    name = '%s_%d' % (tag, k)
    t0 = time.time()
    try:
        r = pfenc.run(m, t, centre, th, lr, tmax, log, out, name, conf=CONF)
    except ValueError as e:
        r = ('DEGEN', 0, 0, str(e))
    tsv.write('%s\tnin%d\t%s\t%s\t%d\t%.3e\t%.1f\n' % (name, nin, ' '.join(desc), r[0], r[1], r[2], time.time() - t0)); tsv.flush()
    if r[0] in ('TIMEOUT', 'BUDGET'):
        json.dump(dict(m=m, centre=centre, lr=list(map(float, lr)), th=list(map(float, th)), note='live (template2 %s)' % ' '.join(desc)),
                  open(os.path.join(out, 'live_%s.json' % name), 'w'))
log('done')
