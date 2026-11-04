#!/usr/bin/env python3
"""realize_opt.py MODEL START.npy [RESTARTS] : smooth numerical realizability search (evidence only).
Seeds z_i = exp(rho_i + i theta_i); every orbit-sign record e gets the scale-free value
n_e = s_e * orient(e) / (product of the two largest radii in e); minimise sum softplus(-n_e / tau) with L-BFGS for a
decreasing tau, from START and from random perturbations of it.  Reports the fewest wrong signs found."""
import sys, json, numpy as np, importlib.util
from pathlib import Path
from scipy.optimize import minimize
RES = Path('<review-results>')
s = importlib.util.spec_from_file_location('enc', RES / 'C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(6, 8, 10)
model = sys.argv[1]; z0 = np.load(sys.argv[2]); restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 6
pos = set(json.loads(open(model).read()))
C = sorted(E.tvar, key=E.tvar.get); T = np.array(C); L = T // 6; K = T % 6
want = np.array([1.0 if E.tvar[c] in pos else -1.0 for c in C])


def vals(p):
    rho, th = p[:10], p[10:]
    r = np.exp(rho[L]); a = th[L] + np.pi / 3 * K
    x, y = r * np.cos(a), r * np.sin(a)
    o = (x[:, 1] - x[:, 0]) * (y[:, 2] - y[:, 0]) - (y[:, 1] - y[:, 0]) * (x[:, 2] - x[:, 0])
    rs = np.sort(r, axis=1); return want * o / (rs[:, 2] * rs[:, 1])


def loss(p, tau):
    v = -vals(p) / tau
    return float(np.sum(np.logaddexp(0, v))) + 1e-3 * float(np.sum((p[:10] - p[0]) ** 2) * 0)


rng = np.random.default_rng(1)
p0 = np.concatenate([np.log(np.abs(z0) + 1e-300), np.angle(z0)])
best = (int((vals(p0) <= 0).sum()), p0)
print('start: %d wrong' % best[0], flush=True)
for rs_ in range(restarts):
    p = best[1] + (0 if rs_ == 0 else 1) * np.concatenate([rng.normal(size=10) * 0.5, rng.normal(size=10) * 0.05])
    for tau in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4):
        res = minimize(loss, p, args=(tau,), method='L-BFGS-B', options={'maxiter': 400})
        p = res.x
        m = int((vals(p) <= 0).sum())
        if m < best[0]: best = (m, p.copy())
    print('restart %d: %d wrong (best %d)' % (rs_, m, best[0]), flush=True)
    if best[0] == 0: break
p = best[1]; v = vals(p)
print('best %d wrong of %d; min scale-free value %.3g; radii' % (best[0], len(C), v.min()),
      np.round(np.exp(p[:10] - p[:10].max()), 8).tolist())
np.save(Path(sys.argv[2]).with_name(Path(sys.argv[2]).stem + '_opt.npy'), np.exp(p[:10] + 1j * p[10:]))
