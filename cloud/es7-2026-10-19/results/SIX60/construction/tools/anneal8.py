"""Local annealing of the convex-octagon count N8 (float evaluator, evidence only) from a given configuration.
E = log(1+N8) + 0.02*log(1+N7); moves: one layer's log-radius or phase, log-uniform step 1e-7..1e-1."""
import numpy as np, math, cvx


def energy(lr, th):
    o = np.argsort(-lr); c, _ = cvx.count6(lr[o], th[o]); return math.log1p(c[8]) + 0.02 * math.log1p(c[7]), c[8], c[7]


def anneal(lr, th, iters=20000, seed=0, T0=0.05):
    rng = np.random.default_rng(seed); lr = np.array(lr, float); th = np.array(th, float)
    E, n8, n7 = energy(lr, th); best = (n8, n7, lr.copy(), th.copy())
    for it in range(iters):
        T = T0 * (1 - it / iters) + 1e-4
        i = rng.integers(1, len(lr)); a, b = lr.copy(), th.copy(); st = 10 ** rng.uniform(-7, -1)
        if rng.random() < 0.5: a[i] += rng.normal() * st
        else: b[i] += rng.normal() * st
        E2, m8, m7 = energy(a, b)
        if E2 <= E or rng.random() < math.exp(-(E2 - E) / T):
            lr, th, E, n8, n7 = a, b, E2, m8, m7
            if (n8, n7) < best[:2]: best = (n8, n7, lr.copy(), th.copy())
            if n8 == 0: break
    return best
