#!/usr/bin/env python3
"""Fixed-phase extension scan (evidence only): keep the phases of a (t-1)-orbit configuration, insert one new orbit at
radius rank p with phase phi (grid), leave ALL radii free, and run the phase-fixed CEGAR of pfenc (with pair cuts).
usage: extscan.py M CFG.json OUT TAG RANKS(lo:hi) PHASESTEP_DEG TMAX [centre]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pfenc

m, cfg, out, tag = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
lo, hi = map(int, sys.argv[5].split(':')); step = float(sys.argv[6]); tmax = float(sys.argv[7])
centre = int(sys.argv[8]) if len(sys.argv) > 8 else 0
pfenc.PAIRS = True
os.makedirs(out, exist_ok=True)
logf = open(os.path.join(out, 'log_%s.txt' % tag), 'a'); tsv = open(os.path.join(out, 'res_%s.tsv' % tag), 'a')
def log(s):
    logf.write(time.strftime('%H:%M:%S ') + s + '\n'); logf.flush()
d = json.load(open(cfg)); lr = np.array(d['lr']); th = np.array(d['th'])
o = np.argsort(-lr); lr = lr[o] - lr[o][0]; th = th[o]
U = 2 * math.pi / m
for p in range(lo, hi + 1):
    if p == 0:
        lnew = 0.3
    elif p == len(lr):
        lnew = lr[-1] - 1.0
    else:
        lnew = 0.5 * (lr[p - 1] + lr[p])
    for phi in np.arange(step / 2, 360.0 / m, step):
        th2 = np.insert(th, p, th[0] + math.radians(phi)); lr2 = np.insert(lr, p, lnew); lr2 = lr2 - lr2[0]
        th2 = (th2 - th2[0]) % U
        name = '%s_p%d_%.2f' % (tag, p, phi)
        t0 = time.time()
        try:
            r = pfenc.run(m, len(lr2), centre, th2, lr2, tmax, log, out, name)
        except ValueError as e:
            r = ('DEGEN', 0, 0, str(e))
        tsv.write('%s\t%d\t%.2f\t%s\t%d\t%.3e\t%.1f\n' % (name, p, phi, r[0], r[1], r[2], time.time() - t0)); tsv.flush()
        if r[0] in ('TIMEOUT',):
            json.dump(dict(m=m, centre=centre, lr=list(map(float, lr2)), th=list(map(float, th2)), note='live (extscan)'),
                      open(os.path.join(out, 'live_%s.json' % name), 'w'))
log('done')
