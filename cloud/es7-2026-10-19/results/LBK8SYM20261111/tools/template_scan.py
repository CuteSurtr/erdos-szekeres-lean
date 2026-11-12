#!/usr/bin/env python3
"""Template phase scan (evidence only).  Phase vectors shaped like the 6- and 7-fold record sets: an outer layer
(phase 0), a spiral arm of n_s layers whose phases drift linearly from phi0 to phi0 + D (units of 2pi/m; optionally
in near-twin pairs), and n_in inner layers at phase psi; the radius order is the index order and ALL radii are left
to the LP of the phase-fixed CEGAR (pfenc + pair cuts).
usage: template_scan.py M T CENTRE NIN OUT TAG TMAX [seed] [nsamples]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pfenc

m, t, centre, nin, out, tag, tmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6], float(sys.argv[7])
seed = int(sys.argv[8]) if len(sys.argv) > 8 else 0
nsamp = int(sys.argv[9]) if len(sys.argv) > 9 else 400
pfenc.PAIRS = True
os.makedirs(out, exist_ok=True)
logf = open(os.path.join(out, 'log_%s.txt' % tag), 'a'); tsv = open(os.path.join(out, 'res_%s.tsv' % tag), 'a')
def log(s):
    logf.write(time.strftime('%H:%M:%S ') + s + '\n'); logf.flush()
U = 2 * math.pi / m
rng = np.random.default_rng(seed)
ns = t - 1 - nin
stop = time.mktime(time.strptime('2026-11-12 03:55', '%Y-%m-%d %H:%M'))
for k in range(nsamp):
    if time.time() > stop:
        break
    phi0 = rng.choice([-1, 1]) * 10 ** rng.uniform(-2, -0.6)
    D = np.sign(phi0) * rng.uniform(0.08, 0.45)
    twins = rng.random() < 0.5
    s = np.linspace(0, 1, ns)
    if twins:
        s = np.repeat(np.linspace(0, 1, (ns + 1) // 2), 2)[:ns] + np.tile([0, 2e-4], ns)[:ns]
    th = np.zeros(t)
    th[1:1 + ns] = (phi0 + D * s) * U + rng.normal(0, 1e-4, ns) * U
    th[1 + ns:] = rng.uniform(0, 1, nin) * U
    th = th % U
    lr = np.concatenate([[0.0], -1.5 - 0.5 * s, -6.0 - np.arange(nin)])[:t]
    name = '%s_%d' % (tag, k)
    t0 = time.time()
    try:
        r = pfenc.run(m, t, centre, th, lr, tmax, log, out, name, conf=int(os.environ.get("CONF", "300000")))
    except ValueError as e:
        r = ('DEGEN', 0, 0, str(e))
    tsv.write('%s\t%.4f\t%.4f\t%d\t%s\t%d\t%.3e\t%.1f\n' % (name, phi0, D, twins, r[0], r[1], r[2], time.time() - t0)); tsv.flush()
    if r[0] in ('TIMEOUT', 'BUDGET'):
        json.dump(dict(m=m, centre=centre, lr=list(map(float, lr)), th=list(map(float, th)), note='live (template)'),
                  open(os.path.join(out, 'live_%s.json' % name), 'w'))
log('done')
