#!/usr/bin/env python3
"""Fit a near-realisable SAT model of pfenc (orbit-variable signs, no centre) with phases AND radii free (mf.Fit,
scale-free softplus loss), starting from the model's LP point; then a short local N8 anneal.  Evidence only; any
N8 = 0 configuration is written as found_*.json for the exact pipeline.
usage: fitmodel.py BESTMODEL.json OUTDIR TAG [anneal_iters]"""
import sys, os, json, time
import numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mf as MFM
from ptsio import write_cfg

src, out, tag = sys.argv[1], sys.argv[2], sys.argv[3]
iters = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
os.makedirs(out, exist_ok=True)
d = json.load(open(src))
m = d['m']; assert int(d.get('centre', 0)) == 0
lr = np.array(d['lr']); th = np.array(d['th']); t = len(lr)
want = np.array(d['signs'], int)
F = MFM.MF(m, t)
assert F.NT == len(want)
z0 = F.normalise(np.exp(lr + 1j * th))
print('start: wrong', F.nwrong(z0, want), 'N8,N7', F.octs(z0), flush=True)
fit = MFM.Fit(F, want)
t0 = time.time()
R2, w = fit.fit(z0, reps=4)
R2 = F.normalise(R2); w = F.nwrong(R2, want)
o8, o7 = F.octs(R2)
print('fit: wrong %d N8 %d N7 %d (%.1f s)' % (w, o8, o7, time.time() - t0), flush=True)
best = (o8, o7, R2)
if o8 > 0:
    n8, n7, z2 = MFM.anneal(F, R2, iters=iters, seed=1)
    print('anneal: N8 %d N7 %d' % (n8, n7), flush=True)
    if (n8, n7) < best[:2]:
        best = (n8, n7, F.normalise(z2))
fn = os.path.join(out, '%s_fit_N8_%d.json' % (tag, best[0]))
write_cfg(fn, m, np.log(np.abs(best[2])), np.angle(best[2]), 0, None, note='fitmodel from %s' % src)
if best[0] == 0:
    write_cfg(os.path.join(out, 'found_%s.json' % tag), m, np.log(np.abs(best[2])), np.angle(best[2]), 0, None,
              note='fitmodel N8 = 0 (float)')
    print('N8 = 0 FOUND')
