"""Second reading of cone_rules.py and thr_rules2.py on t = 4 (evidence): dense random sampling of phases (all orders)
and radii (including near-generator extremes); every emitted clause must hold at every sample."""
import sys, os, math, importlib.util
import numpy as np
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools')
def load(n, f):
    s = importlib.util.spec_from_file_location(n, os.path.join(T, f)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
CR = load('cone', 'cone_rules.py'); T2 = load('thr2', 'thr_rules2.py'); G = load('gen', 'gen.py')
t = int(sys.argv[1]) if len(sys.argv) > 1 else 4
E, cone, nu = CR.build(8, t)
_, thr, st = T2.build(8, t)
cls = list(cone) + list(thr)
print('t=%d cone %d thr %d' % (t, len(cone), len(thr)))
vs = sorted(E.tvar.values()); inv = {v: C for C, v in E.tvar.items()}
Tr = np.array([inv[v] for v in vs]); L = Tr // 8; K = Tr % 8
rng = np.random.default_rng(7)
bad = 0; n = 0
for s in range(20000):
    th = np.concatenate([[0.0], rng.uniform(0, math.pi / 4, t - 1)])
    mode = s % 3
    if mode == 0:
        lr = -np.sort(rng.uniform(0, 3, t)); lr -= lr[0]
    elif mode == 1:
        lr = -np.cumsum(np.concatenate([[0], rng.choice([1e-6, 1e-3, 3.0, 15.0], t - 1)]))
    else:
        lr = -np.cumsum(np.concatenate([[0], rng.exponential(1.0, t - 1)]))
    if np.any(np.diff(lr) >= 0): continue
    z = np.exp(lr + 1j * th); P = z[L] * np.exp(2j * np.pi * K / 8)
    a, b, c = P[:, 0], P[:, 1], P[:, 2]
    o = (np.conj(b - a) * (c - a)).imag
    sc = np.maximum(np.maximum(abs(b - a), abs(c - b)), abs(a - c)) ** 2
    if np.min(np.abs(o) / sc) < 1e-12: continue
    val = {v: bool(o[q] > 0) for q, v in enumerate(vs)}
    for (i, j), y in E.Y.items(): val[y] = bool(th[i] < th[j])
    n += 1
    for cl in cls:
        if not any(val[abs(l)] == (l > 0) for l in cl):
            bad += 1
            if bad < 4: print('VIOLATED', cl, th, lr)
print('samples %d violations %d' % (n, bad))
