"""Robustify an octagon-free configuration (float, evidence only; the result is re-verified exactly):
maximise the smallest scale-free orientation value min_t |sin(largest angle of triangle t)| over all C(60,3) triples,
subject to N8 = 0 (float evaluator), by a constrained local annealing.  Usage: robustify.py IN.json OUT.json SECONDS"""
import sys, json, time, math, numpy as np, itertools, cvx
cfg = json.load(open(sys.argv[1])); lr = np.array(cfg['lr'], float); th = np.array(cfg['th'], float); sec = float(sys.argv[3])
I = np.array(list(itertools.combinations(range(60), 3)))
W6 = np.exp(1j * np.pi / 3 * np.arange(6))
def pts(lr, th): return (np.exp(lr + 1j * th)[:, None] * W6[None, :]).ravel()
def minval(lr, th):
    P = pts(lr, th); a, b, c = P[I[:, 0]], P[I[:, 1]], P[I[:, 2]]
    o = np.abs((np.conj(b - a) * (c - a)).imag); d = np.sort(np.stack([abs(a - b), abs(b - c), abs(c - a)], 1), 1)
    return (o / (d[:, 0] * d[:, 1])).min()
def n8(lr, th):
    o = np.argsort(-lr); c, _ = cvx.count6(lr[o], th[o]); return c[8]
assert n8(lr, th) == 0
cur = minval(lr, th); best = (cur, lr.copy(), th.copy()); rng = np.random.default_rng(1); t0 = time.time(); it = 0
print('start min sine %.3e' % cur, flush=True)
while time.time() - t0 < sec:
    it += 1; a, b = lr.copy(), th.copy(); i = rng.integers(1, 10); st = 10 ** rng.uniform(-6, -2)
    if rng.random() < 0.5: a[i] += rng.normal() * st
    else: b[i] += rng.normal() * st
    v = minval(a, b)
    if v >= cur * (1 - 1e-3 * rng.random()) and n8(a, b) == 0:
        lr, th, cur = a, b, v
        if cur > best[0]: best = (cur, lr.copy(), th.copy())
    if it % 2000 == 0: print('it', it, 'min sine %.3e' % best[0], flush=True)
json.dump({'lr': best[1].tolist(), 'th': best[2].tolist(), 'min_sine': best[0]}, open(sys.argv[2], 'w'))
print('FINAL min sine %.3e' % best[0], flush=True)
