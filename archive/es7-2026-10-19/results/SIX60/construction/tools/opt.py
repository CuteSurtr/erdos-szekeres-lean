"""Smooth scale-free realizability search (evidence only).
Per record t the scale-free value n_t = s_t * orient_t / (d1 d2), d1 <= d2 the two shortest sides
= s_t * sin(largest angle of the triangle): similarity invariant, near 0 only for genuinely flat triangles, so
hierarchical (multi-scale) configurations are not penalised.  Loss = sum softplus(-(n_t - margin)/tau).
Parameters: rho_i = log r_i, theta_i (layer 0: rho=0, theta=0 fixed)."""
import numpy as np, common as cm
from scipy.optimize import minimize

W6 = cm.W ** np.arange(6)


class Problem:
    def __init__(self, want, mask):
        self.idx = np.nonzero(mask)[0]
        self.T = cm.T[self.idx]; self.L = self.T // 6; self.K = self.T % 6
        self.s = want[self.idx].astype(float)
        self.wk = W6[self.K]

    def pts(self, x):
        rho = np.concatenate([[0.0], x[:9]]); th = np.concatenate([[0.0], x[9:]])
        z = np.exp(rho + 1j * th)
        return z, z[self.L] * self.wk

    def values(self, x):
        z, P = self.pts(x)
        a, b, c = P[:, 0], P[:, 1], P[:, 2]
        o = (np.conj(b - a) * (c - a)).imag
        dab, dbc, dca = np.abs(a - b), np.abs(b - c), np.abs(c - a)
        dmax = np.maximum(np.maximum(dab, dbc), dca)
        g = dmax / (dab * dbc * dca)
        return self.s * o * g

    def nwrong(self, x):
        return int((self.values(x) <= 0).sum())

    def loss_grad(self, x, tau, margin=0.0):
        z, P = self.pts(x)
        a, b, c = P[:, 0], P[:, 1], P[:, 2]
        ab, bc, ca = b - a, c - b, a - c
        o = (np.conj(ab) * (-ca)).imag
        dab, dbc, dca = np.abs(ab), np.abs(bc), np.abs(ca)
        D = np.stack([dab, dbc, dca], 1); im = np.argmax(D, 1); dmax = D[np.arange(len(D)), im]
        g = dmax / (dab * dbc * dca)
        n = self.s * o * g
        u = -(n - margin) / tau
        L = np.logaddexp(0, u).sum()
        dLdn = -1.0 / tau * 0.5 * (1 + np.tanh(u / 2))   # -sigmoid(u)/tau
        # dn = s*(g do + o dg); log g = log dmax - log dab - log dbc - log dca
        cn = dLdn * self.s
        # orient gradient wrt complex point: do/dp as complex (dx + i dy)
        # o = Im(conj(b-a)(c-a)); do/da = i*(c-b)?? derive: o = ax*by - ay*bx + bx*cy - by*cx + cx*ay - cy*ax
        # do/dax = by-cy, do/day = cx-bx  -> complex (by-cy) + i(cx-bx) = -i*(cx-bx + i(cy-by))... = -1j*(c-b)?
        # -1j*(c-b) = -1j*(cx-bx) + (cy-by) -> real cy-by: sign flip; so do/da = 1j*(c-b)
        ga = 1j * (c - b) * (cn * g)
        gb = 1j * (a - c) * (cn * g)
        gc = 1j * (b - a) * (cn * g)
        # dg/dp: g * (dlog dmax - sum dlog d)
        co = cn * o * g
        # d log dab / da = (a-b)/dab^2
        eab = ab / dab ** 2; ebc = bc / dbc ** 2; eca = ca / dca ** 2
        # log dab depends on a (-eab) and b (+eab)
        ga += co * (eab - eca)
        gb += co * (ebc - eab)
        gc += co * (eca - ebc)
        # dmax term
        sel = [(0, 'ab'), (1, 'bc'), (2, 'ca')]
        m0 = im == 0; m1 = im == 1; m2 = im == 2
        ga[m0] += co[m0] * (-eab[m0]); gb[m0] += co[m0] * eab[m0]
        gb[m1] += co[m1] * (-ebc[m1]); gc[m1] += co[m1] * ebc[m1]
        gc[m2] += co[m2] * (-eca[m2]); ga[m2] += co[m2] * eca[m2]
        GP = np.stack([ga, gb, gc], 1)
        # chain to layer params: dP/drho = P, dP/dtheta = iP ; dL = Re(conj(GP) dP)
        grho = np.zeros(10); gth = np.zeros(10)
        np.add.at(grho, self.L.ravel(), (np.conj(GP) * P).real.ravel())
        np.add.at(gth, self.L.ravel(), (np.conj(GP) * 1j * P).real.ravel())
        return L, np.concatenate([grho[1:], gth[1:]])


def check_grad():
    k = cm.core('c11110'); pr = Problem(k['want'], ~k['free'])
    rng = np.random.default_rng(0); x = np.concatenate([-np.sort(rng.random(9)) * 3, rng.random(9)])
    f, g = pr.loss_grad(x, 0.1)
    gn = np.zeros_like(x); h = 1e-6
    for i in range(len(x)):
        e = np.zeros_like(x); e[i] = h
        gn[i] = (pr.loss_grad(x + e, 0.1)[0] - pr.loss_grad(x - e, 0.1)[0]) / (2 * h)
    print('grad rel err', np.abs(g - gn).max() / np.abs(gn).max())


if __name__ == '__main__':
    check_grad()
