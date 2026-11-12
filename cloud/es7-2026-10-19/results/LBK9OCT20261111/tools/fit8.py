#!/usr/bin/env python3
"""Evidence only: fit a real 8-fold layered configuration (lr, th per layer; layer 0 fixed at lr = 0, th = 0) to a
target sign vector of the triple-orbit variables of gen.py Enc(8, 9, t) (scale-free softplus loss as in
<six10-work-dir>/realize/tools/opt.py).  Phase order is free (the target's Y values are reported, not imposed).
usage: fit8.py TARGET.json INIT.json OUT.json [iters]
  TARGET.json: {"t": t, "val": {var: bool}}  (label8.py output or a SAT model dump)
  INIT.json:   {"lr": [...], "th": [...]}     (radial order is taken from -lr)"""
import sys, os, json, math, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen, ev9

M = 8
W = np.exp(2j * np.pi * np.arange(M) / M)


class Problem:
    def __init__(self, t, want):
        E = gen.Enc(M, 9, t)
        self.t = t
        vs = sorted(E.tvar.values())
        inv = {v: C for C, v in E.tvar.items()}
        T = np.array([inv[v] for v in vs])
        self.L = T // M; self.wk = W[T % M]
        self.s = np.array([1.0 if want[v] else -1.0 for v in vs])
        self.vs = vs

    def pts(self, x):
        t = self.t
        rho = np.concatenate([[0.0], x[:t - 1]]); th = np.concatenate([[0.0], x[t - 1:]])
        z = np.exp(rho + 1j * th)
        return z[self.L] * self.wk

    def nwrong(self, x):
        P = self.pts(x)
        a, b, c = P[:, 0], P[:, 1], P[:, 2]
        o = (np.conj(b - a) * (c - a)).imag
        return int((self.s * o <= 0).sum())

    def loss_grad(self, x, tau, margin=0.0):
        t = self.t
        P = self.pts(x)
        a, b, c = P[:, 0], P[:, 1], P[:, 2]
        ab, bc, ca = b - a, c - b, a - c
        o = (np.conj(ab) * (-ca)).imag
        dab, dbc, dca = np.abs(ab), np.abs(bc), np.abs(ca)
        D = np.stack([dab, dbc, dca], 1); im = np.argmax(D, 1); dmax = D[np.arange(len(D)), im]
        g = dmax / (dab * dbc * dca)
        n = self.s * o * g
        u = -(n - margin) / tau
        Lv = np.logaddexp(0, u).sum()
        dLdn = -1.0 / tau * 0.5 * (1 + np.tanh(u / 2))
        cn = dLdn * self.s
        ga = 1j * (c - b) * (cn * g)
        gb = 1j * (a - c) * (cn * g)
        gc = 1j * (b - a) * (cn * g)
        co = cn * o * g
        eab = ab / dab ** 2; ebc = bc / dbc ** 2; eca = ca / dca ** 2
        ga += co * (eab - eca)
        gb += co * (ebc - eab)
        gc += co * (eca - ebc)
        m0 = im == 0; m1 = im == 1; m2 = im == 2
        ga[m0] += co[m0] * (-eab[m0]); gb[m0] += co[m0] * eab[m0]
        gb[m1] += co[m1] * (-ebc[m1]); gc[m1] += co[m1] * ebc[m1]
        gc[m2] += co[m2] * (-eca[m2]); ga[m2] += co[m2] * eca[m2]
        GP = np.stack([ga, gb, gc], 1)
        grho = np.zeros(t); gth = np.zeros(t)
        np.add.at(grho, self.L.ravel(), (np.conj(GP) * P).real.ravel())
        np.add.at(gth, self.L.ravel(), (np.conj(GP) * 1j * P).real.ravel())
        return Lv, np.concatenate([grho[1:], gth[1:]])


def fit(pr, x0, iters=3, log=print):
    x = x0.copy()
    best = (pr.nwrong(x), x.copy())
    for tau in [1e-2, 3e-3, 1e-3, 3e-4, 1e-4][:max(1, iters + 2)]:
        for margin in (0.0, tau):
            r = minimize(lambda y: pr.loss_grad(y, tau, margin), x, jac=True, method='L-BFGS-B',
                         options={'maxiter': 3000})
            x = r.x
            w = pr.nwrong(x)
            log('  tau %.0e margin %.0e: wrong %d' % (tau, margin, w))
            if w < best[0]:
                best = (w, x.copy())
    return best


if __name__ == '__main__':
    tgt = json.load(open(sys.argv[1])); ini = json.load(open(sys.argv[2])); out = sys.argv[3]
    want = {int(k): v for k, v in tgt['val'].items()}
    t = tgt['t']
    lr = np.array(ini['lr'], float); th = np.array(ini['th'], float)
    o = np.argsort(-lr); lr = lr[o] - lr[o][0]; th = (th[o] - th[o][0]) % (2 * math.pi / M)
    pr = Problem(t, want)
    x0 = np.concatenate([lr[1:], th[1:]])
    print('initial wrong', pr.nwrong(x0), 'of', len(pr.vs))
    w, x = fit(pr, x0)
    lr2 = np.concatenate([[0.0], x[:t - 1]]); th2 = np.concatenate([[0.0], x[t - 1:]])
    c9, md = ev9.count_cfg(lr2, th2, 9)
    print('final wrong', w, 'float N9', c9, 'mindet %.2e' % md)
    json.dump({'lr': lr2.tolist(), 'th': th2.tolist(), 'wrong': w, 'N9': int(c9)}, open(out, 'w'))
