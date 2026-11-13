"""(copy of <six10-work-dir>/realize/p2/mfold/tools/mf.py; float evaluator replaced by evm.count_xy)
Generic m-fold helpers for the alternating-projection search (m nested regular m-gons, no centre).
Encoder: C7UPPER/gen.py Enc(m, 8, t).  Point id x = m*i + k is w^k z_i, w = exp(2 pi i/m); theta_0 = 0,
theta_i in (0, 2pi/m); psi_i = theta_i mod (pi/m) (odd m) or theta_i (even m); Y(i,j) = [psi_i < psi_j];
H(i) = [theta_i < pi/m] (odd m)."""
import os, json, importlib.util, itertools, math
import numpy as np
from scipy.optimize import minimize
RES = os.environ.get('ES_RESULTS', '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results')
_s = importlib.util.spec_from_file_location('enc', RES + '/C7UPPER/gen.py'); G = importlib.util.module_from_spec(_s); _s.loader.exec_module(G)
from evm import count_xy as _count_xy
class cvx:
    count_xy = staticmethod(_count_xy)


class MF:
    def __init__(self, m, t):
        self.m, self.t = m, t; self.n = m * t
        self.E = G.Enc(m, 8, t)
        self.C = sorted(self.E.tvar, key=self.E.tvar.get); self.NT = len(self.C)
        self.T = np.array(self.C, np.int64); self.TL = self.T // m; self.TK = self.T % m
        self.w = np.exp(2j * np.pi / m); self.WK = self.w ** np.arange(m)
        self.unit = 2 * np.pi / m

    # ---------------- configuration <-> signs
    def normalise(self, z):
        z = np.asarray(z, complex); z = z[np.argsort(-np.abs(z))]
        z = z * abs(z[0]) / z[0]
        out = []
        for x in z:
            a = np.angle(x) % self.unit; out.append(abs(x) * np.exp(1j * a))
        out = np.array(out); return out / abs(out[0])

    def orient(self, z):
        P = z[self.TL] * self.WK[self.TK]
        a, b, c = P[:, 0], P[:, 1], P[:, 2]
        return (np.conj(b - a) * (c - a)).imag

    def psi(self, z):
        th = np.angle(z) % self.unit; th[0] = 0.0
        return (th % (np.pi / self.m)) if self.m % 2 else th, th

    def lits(self, z):
        o = self.orient(z); L = [(v + 1) if o[v] > 0 else -(v + 1) for v in range(self.NT)]
        ps, th = self.psi(z)
        for (i, j), v in self.E.Y.items(): L.append(v if ps[i] < ps[j] else -v)
        for i, v in self.E.H.items(): L.append(v if th[i] < np.pi / self.m else -v)
        return L, np.where(o > 0, 1, -1)

    def points(self, z):
        return (z[:, None] * self.WK[None, :]).ravel()

    def octs(self, z):
        P = self.points(z); c, _ = cvx.count_xy(P.real.copy(), P.imag.copy()); return int(c[8]), int(c[7])

    def nwrong(self, z, want):
        return int((np.sign(self.orient(z)) != want).sum())


class Fit:
    """scale-free softplus fit of a sign vector (cf. realize/tools/opt.py), params rho_i, theta_i (i >= 1)."""
    def __init__(self, mf, want):
        self.mf = mf; self.s = want.astype(float); self.L = mf.TL; self.wk = mf.WK[mf.TK]; self.t = mf.t

    def z(self, x):
        return np.exp(np.concatenate([[0.0], x[:self.t - 1]]) + 1j * np.concatenate([[0.0], x[self.t - 1:]]))

    def x_of(self, z):
        z = z / z[0]; return np.concatenate([np.log(np.abs(z[1:])), np.angle(z[1:])])

    def values(self, x):
        P = self.z(x)[self.L] * self.wk; a, b, c = P[:, 0], P[:, 1], P[:, 2]
        o = (np.conj(b - a) * (c - a)).imag
        dab, dbc, dca = np.abs(a - b), np.abs(b - c), np.abs(c - a)
        return self.s * o * np.maximum(np.maximum(dab, dbc), dca) / (dab * dbc * dca)

    def nwrong(self, x): return int((self.values(x) <= 0).sum())

    def loss_grad(self, x, tau):
        z = self.z(x); P = z[self.L] * self.wk; a, b, c = P[:, 0], P[:, 1], P[:, 2]
        ab, bc, ca = b - a, c - b, a - c
        o = (np.conj(ab) * (-ca)).imag
        dab, dbc, dca = np.abs(ab), np.abs(bc), np.abs(ca)
        D = np.stack([dab, dbc, dca], 1); im = np.argmax(D, 1); dmax = D[np.arange(len(D)), im]
        g = dmax / (dab * dbc * dca); n = self.s * o * g; u = -n / tau
        Lv = np.logaddexp(0, u).sum(); cn = -1.0 / tau * 0.5 * (1 + np.tanh(u / 2)) * self.s
        ga = 1j * (c - b) * (cn * g); gb = 1j * (a - c) * (cn * g); gc = 1j * (b - a) * (cn * g)
        co = cn * o * g; eab = ab / dab ** 2; ebc = bc / dbc ** 2; eca = ca / dca ** 2
        ga += co * (eab - eca); gb += co * (ebc - eab); gc += co * (eca - ebc)
        m0 = im == 0; m1 = im == 1; m2 = im == 2
        ga[m0] -= co[m0] * eab[m0]; gb[m0] += co[m0] * eab[m0]
        gb[m1] -= co[m1] * ebc[m1]; gc[m1] += co[m1] * ebc[m1]
        gc[m2] -= co[m2] * eca[m2]; ga[m2] += co[m2] * eca[m2]
        GP = np.stack([ga, gb, gc], 1)
        grho = np.zeros(self.t); gth = np.zeros(self.t)
        np.add.at(grho, self.L.ravel(), (np.conj(GP) * P).real.ravel())
        np.add.at(gth, self.L.ravel(), (np.conj(GP) * 1j * P).real.ravel())
        return Lv, np.concatenate([grho[1:], gth[1:]])

    def lbfgs(self, x, taus=(0.03, 0.01, 0.003, 0.001), it=300):
        for tau in taus:
            r = minimize(self.loss_grad, x, args=(tau,), jac=True, method='L-BFGS-B', options={'maxiter': it})
            if np.all(np.isfinite(r.x)): x = r.x
        return x

    def grid_layer(self, x, j, rng, n=24):
        best = self.nwrong(x); bx = x; t = self.t
        lo = x[j - 2] if j >= 2 else 0.0; hi = x[j] if j <= t - 2 else x[j - 1] - 8
        R = np.concatenate([np.linspace(min(lo, hi), max(lo, hi), n // 2), x[j - 1] + rng.normal(size=n // 2) * 2])
        TH = np.linspace(1e-3, self.mf.unit - 1e-3, n)
        for r_ in R:
            for t_ in TH[rng.permutation(n)[:n // 2]]:
                y = x.copy(); y[j - 1] = r_; y[t - 1 + j - 1] = t_
                w = self.nwrong(y)
                if w < best: best, bx = w, y
        return bx, best

    def fit(self, z0, reps=3):
        x = self.x_of(z0); best = (self.nwrong(x), x)
        for rep in range(reps):
            x1 = self.lbfgs(best[1] if rep == 0 else best[1] + np.random.default_rng(rep).normal(size=len(x)) * 0.02)
            for j in range(1, self.t):
                x2, w2 = self.grid_layer(x1, j, np.random.default_rng(rep * 10 + j))
                if w2 < self.nwrong(x1): x1 = x2
            w = self.nwrong(x1)
            if w < best[0]: best = (w, x1)
        return self.z(best[1]), best[0]


def anneal(mf, z, iters=30000, seed=0, T0=0.05, deadline=None):
    """local annealing of log(1+N8) + 0.02 log(1+N7) (cf. realize/tools/anneal8.py), moves on one layer's log-radius or
    phase with log-uniform step 1e-7..1e-1; layer 0 fixed."""
    rng = np.random.default_rng(seed); lr = np.log(np.abs(z)); th = np.angle(z)
    def energy(lr, th):
        zz = np.exp(lr + 1j * th); n8, n7 = mf.octs(zz); return math.log1p(n8) + 0.02 * math.log1p(n7), n8, n7
    E, n8, n7 = energy(lr, th); best = (n8, n7, lr.copy(), th.copy())
    for it in range(iters):
        if deadline and time_now() > deadline: break
        T = T0 * (1 - it / iters) + 1e-4
        i = rng.integers(1, len(lr)); a, b = lr.copy(), th.copy(); st = 10 ** rng.uniform(-7, -1)
        if rng.random() < 0.5: a[i] += rng.normal() * st
        else: b[i] += rng.normal() * st
        E2, m8, m7 = energy(a, b)
        if E2 <= E or rng.random() < math.exp(-(E2 - E) / T):
            lr, th, E, n8, n7 = a, b, E2, m8, m7
            if (n8, n7) < best[:2]: best = (n8, n7, lr.copy(), th.copy())
            if n8 == 0: break
    return best[0], best[1], np.exp(best[2] + 1j * best[3])


def time_now():
    import time; return time.time()


def read_pts(path, m):
    rows = []
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        rows.append([int(x) for x in line.split()])
    zeta = np.exp(2j * np.pi / m)
    return rows, np.array([sum(wj * zeta ** j for j, wj in enumerate(r)) for r in rows])
