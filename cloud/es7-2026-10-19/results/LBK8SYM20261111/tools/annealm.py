#!/usr/bin/env python3
"""Multi-scale simulated annealing for m-fold configurations (t orbits of m points, optional centre) without a
convex octagon.  Generic-m adaptation of <six10-work-dir>/search/py/anneal.py.

Float evaluator (src/libcvxm.so, long-double orientation signs): evidence only.  Every configuration with N8 = 0
is written to OUT/found_*.json for exact verification.

State: orbits (lr_i, th_i), lr = log radius, th = phase (radians, mod 2pi/m when written).
Energy E = log(1 + N8) + w7 * log(1 + N7).

usage: annealm.py --m 4 --t 14 [--centre] --out DIR --seed S [--init FILE.json|.pts] [--ansatz NAME] [--hours H]
"""
import sys, os, json, math, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evm import countm, pointsm, enum_k
from ptsio import read_pts_cfg, write_cfg, read_cfg


def ansatz(name, rng, m, t):
    U = 2 * math.pi / m
    lr = np.zeros(t); th = np.zeros(t)
    if name == 'free':
        lr[1:] = -np.sort(rng.uniform(0, 12, t - 1))
        th[:] = rng.uniform(0, U, t)
    elif name.startswith('needle'):
        n_out = int(name[6]) if len(name) > 6 else 1
        n_in = int(name[7]) if len(name) > 7 else 0
        n_cl = t - n_out - n_in
        lr[:n_out] = -np.sort(rng.uniform(0, 2.0, n_out)); lr[0] = 0
        th[:n_out] = rng.uniform(0, U, n_out)
        base = lr[n_out - 1] - rng.uniform(0.3, 5)
        width = 10 ** rng.uniform(-2, 0.3)
        tc = rng.uniform(0, U); tw = 10 ** rng.uniform(-3, -0.5)
        lr[n_out:n_out + n_cl] = base - np.sort(rng.uniform(0, width, n_cl))
        th[n_out:n_out + n_cl] = tc + np.sort(rng.normal(0, tw, n_cl)) * (1 if rng.random() < 0.5 else -1)
        if n_in:
            b2 = lr[n_out + n_cl - 1] - rng.uniform(1.0, 8)
            lr[t - n_in:] = b2 - np.sort(rng.uniform(0, 10 ** rng.uniform(-2, 0.5), n_in))
            th[t - n_in:] = rng.uniform(0, U, n_in)
    elif name.startswith('spiral'):
        # outer layer(s) + a spiral arm (radius decreasing, phase drifting monotonically) + tiny inner layers;
        # spiralAB: A outer layers, B inner layers (shape of the 6- and 7-fold record sets)
        n_out = int(name[6]) if len(name) > 6 else 1
        n_in = int(name[7]) if len(name) > 7 else 0
        n_s = t - n_out - n_in
        lr[:n_out] = -np.sort(rng.uniform(0, 1.0, n_out)); lr[0] = 0
        th[:n_out] = rng.uniform(0, U, n_out)
        a0 = rng.uniform(0.3, 3.0); w = rng.uniform(0.15, 1.2)
        ph0 = rng.uniform(0, U); dph = rng.uniform(0.05, 0.45) * U * (1 if rng.random() < 0.5 else -1)
        s = np.sort(rng.uniform(0, 1, n_s))
        if rng.random() < 0.5:          # twin pairs
            s = np.repeat(s[: (n_s + 1) // 2], 2)[:n_s] + rng.normal(0, 1e-3, n_s)
            s = np.sort(s)
        lr[n_out:n_out + n_s] = lr[n_out - 1] - a0 - w * s
        th[n_out:n_out + n_s] = ph0 + dph * s + rng.normal(0, 10 ** rng.uniform(-4, -2), n_s)
        if n_in:
            b2 = lr[n_out + n_s - 1] - rng.uniform(1.0, 8)
            lr[t - n_in:] = b2 - np.sort(rng.uniform(0, 10 ** rng.uniform(-2, 0.5), n_in))
            th[t - n_in:] = rng.uniform(0, U, n_in)
    elif name == 'clusters':
        c = int(rng.integers(2, 6))
        cuts = np.sort(rng.choice(np.arange(1, t), c - 1, replace=False))
        sizes = np.diff(np.concatenate([[0], cuts, [t]]))
        pos = 0; base = 0.0
        for s in sizes:
            w = 10 ** rng.uniform(-3, 0)
            tc = rng.uniform(0, U); tw = 10 ** rng.uniform(-3, -0.3)
            lr[pos:pos + s] = base - np.sort(rng.uniform(0, w, s))
            th[pos:pos + s] = tc + rng.normal(0, tw, s)
            base = lr[pos + s - 1] - 10 ** rng.uniform(-1.5, 0.8)
            pos += s
        lr -= lr.max()
    elif name == 'orbit':
        w = 10 ** rng.uniform(-4, -1.5)
        lr[:] = -np.sort(rng.uniform(0, w, t)); lr[0] = 0
        th[:] = rng.normal(0, w / 2, t)
    elif name == 'twoorbit':
        k = int(rng.integers(2, t - 1))
        w = 10 ** rng.uniform(-4, -1.5)
        lr[:k] = -np.sort(rng.uniform(0, w, k)); lr[0] = 0
        th[:k] = rng.normal(0, w / 2, k)
        b = -rng.uniform(0.05, 1.5); tc = rng.uniform(0, U)
        lr[k:] = b - np.sort(rng.uniform(0, w, t - k))
        th[k:] = tc + rng.normal(0, w / 2, t - k)
    else:
        raise ValueError(name)
    return lr, th


class Annealer:
    def __init__(self, m, centre, lr, th, rng, w7=0.02, out='.', tag='a', T0=0.3, Tmin=0.01, fixlayers=()):
        self.m = m; self.centre = centre
        self.rng = rng
        self.lr = np.array(lr, float); self.th = np.array(th, float)
        self.w7 = w7
        self.out = out; self.tag = tag
        self.fix = np.zeros(len(lr), bool)
        for i in fixlayers:
            self.fix[i] = True
        c, _ = countm(m, self.lr, self.th, centre)
        self.c = c
        self.E = self.en(c)
        self.best = (self.E, self.lr.copy(), self.th.copy(), list(c))
        self.T = T0; self.T0 = T0; self.Tmin = Tmin
        self.nev = 0; self.nacc = 0; self.nab = 0
        self.found = 0
        self.focus = []
        self.pfocus = 0.0

    def update_focus(self):
        if self.c[8] == 0 or self.c[8] > 5000:
            self.focus = []; return
        x, y = pointsm(self.m, self.lr, self.th, self.centre)
        tot, octs = enum_k(x, y, 8, 3000)
        n = self.m * len(self.lr)
        lay = set()
        for P in octs:
            for p in P:
                if int(p) < n:
                    lay.add(int(p) // self.m)
        self.focus = sorted(lay)

    def en(self, c):
        return math.log1p(c[8]) + self.w7 * math.log1p(c[7])

    def propose(self):
        rng = self.rng
        lr = self.lr.copy(); th = self.th.copy(); t = len(lr)
        o = np.argsort(-lr)
        mv = rng.random()
        if mv < 0.45:
            i = rng.integers(t)
            if self.focus and rng.random() < self.pfocus:
                i = self.focus[rng.integers(len(self.focus))]
            s = 10 ** rng.uniform(-7, -0.3)
            which = rng.random()
            if which < 0.4:
                lr[i] += rng.normal(0, s)
            elif which < 0.8:
                th[i] += rng.normal(0, s)
            else:
                lr[i] += rng.normal(0, s); th[i] += rng.normal(0, s)
        elif mv < 0.65:
            a = rng.integers(t); b = rng.integers(a, t)
            idx = o[a:b + 1]
            s = 10 ** rng.uniform(-6, -0.3)
            if rng.random() < 0.5:
                lr[idx] += rng.normal(0, s)
            else:
                th[idx] += rng.normal(0, s)
        elif mv < 0.80:
            a = rng.integers(t); b = rng.integers(a, t)
            if b == a:
                b = min(t - 1, a + 1)
            idx = o[a:b + 1]
            f = math.exp(rng.normal(0, 10 ** rng.uniform(-4, -0.5)))
            if rng.random() < 0.5:
                mm = lr[idx].mean(); lr[idx] = mm + f * (lr[idx] - mm)
            else:
                mm = th[idx].mean(); th[idx] = mm + f * (th[idx] - mm)
        elif mv < 0.88:
            a = rng.integers(t - 1)
            i, j = o[a], o[a + 1]
            th[i], th[j] = th[j], th[i]
        elif mv < 0.94:
            s = 10 ** rng.uniform(-7, -2)
            lr += rng.normal(0, s, t); th += rng.normal(0, s, t)
        else:
            i = rng.integers(t); j = rng.integers(t)
            s = 10 ** rng.uniform(-5, 0)
            lr[i] = lr[j] + rng.normal(0, s); th[i] = th[j] + rng.normal(0, s)
        if self.fix.any():
            lr[self.fix] = self.lr[self.fix]; th[self.fix] = self.th[self.fix]
        if getattr(self, 'fixphase', False):
            th = self.th.copy()
        lr -= lr.max()
        return lr, th

    def step(self):
        lr, th = self.propose()
        u = self.rng.random()
        thr_E = self.E - self.T * math.log(max(u, 1e-300))
        lim = math.exp(thr_E) - 1
        ab = 0 if lim > 1e18 else int(lim) + 1
        c, r = countm(self.m, lr, th, self.centre, ab)
        self.nev += 1
        if r == 1:
            self.nab += 1
            return
        E = self.en(c)
        if E <= thr_E:
            self.lr, self.th, self.c, self.E = lr, th, c, E
            self.nacc += 1
            if E < self.best[0]:
                self.best = (E, lr.copy(), th.copy(), list(c))
            if c[8] == 0:
                self.save_found(lr, th, c)

    def save_found(self, lr, th, c):
        self.found += 1
        if self.found > 5 and c[7] >= getattr(self, 'best_found_n7', 1 << 62):
            return
        self.best_found_n7 = min(c[7], getattr(self, 'best_found_n7', 1 << 62))
        fn = os.path.join(self.out, 'found_%s_%d.json' % (self.tag, self.found))
        write_cfg(fn, self.m, lr, th, self.centre, c, note='N8=0 (float)')


def load_init(fn, m, t, centre, rng):
    if fn.endswith('.pts'):
        lr, th, c0 = read_pts_cfg(fn, m)
    else:
        _, lr, th, c0 = read_cfg(fn)
    lr = list(lr); th = list(th)
    while len(lr) > t:          # drop random orbits
        k = int(rng.integers(1, len(lr))); lr.pop(k); th.pop(k)
    while len(lr) < t:          # add random orbits near existing ones or at random radii
        if rng.random() < 0.5:
            j = int(rng.integers(len(lr)))
            s = 10 ** rng.uniform(-5, 0)
            lr.append(lr[j] + rng.normal(0, s)); th.append(th[j] + rng.normal(0, s))
        else:
            lr.append(rng.uniform(min(lr) - 3, 0)); th.append(rng.uniform(0, 2 * math.pi / m))
    lr = np.array(lr); th = np.array(th)
    lr -= lr.max()
    return lr, th


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--centre', action='store_true')
    ap.add_argument('--out', required=True)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--init', default=None)
    ap.add_argument('--ansatz', default='needle1')
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('--hours', type=float, default=1.0)
    ap.add_argument('--steps-per-T', type=int, default=4000)
    ap.add_argument('--T0', type=float, default=0.5)
    ap.add_argument('--Tmin', type=float, default=0.02)
    ap.add_argument('--alpha', type=float, default=0.93)
    ap.add_argument('--w7', type=float, default=0.02)
    ap.add_argument('--restart-evals', type=int, default=600000)
    ap.add_argument('--tag', default=None)
    ap.add_argument('--perturb', type=float, default=0.0)
    ap.add_argument('--fixphase', action='store_true', help='radii-only moves (phases frozen)')
    ap.add_argument('--pfocus', type=float, default=0.0, help='probability that a single-layer move picks a layer of a current octagon')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = a.tag or ('s%d' % a.seed)
    rng = np.random.default_rng(a.seed)
    stop = a.stop_at if a.stop_at else time.time() + 3600 * a.hours
    logf = open(os.path.join(a.out, 'log_%s.txt' % tag), 'a')
    centre = 1 if a.centre else 0
    ansatze = a.ansatz.split(',')

    def log(*x):
        s = time.strftime('%H:%M:%S ') + ' '.join(str(v) for v in x)
        logf.write(s + '\n'); logf.flush()

    log('start', vars(a))
    gbest = None
    rnum = 0
    while time.time() < stop:
        rnum += 1
        if a.init:
            inits = a.init.split(',')
            lr, th = load_init(inits[rnum % len(inits)], a.m, a.t, centre, rng)
            if a.perturb > 0:
                lr = lr + rng.normal(0, a.perturb, len(lr)) * (rng.random(len(lr)) < 0.5)
                th = th + rng.normal(0, a.perturb, len(th)) * (rng.random(len(th)) < 0.5)
                lr -= lr.max()
            an = 'init'
        else:
            an = ansatze[rnum % len(ansatze)]
            lr, th = ansatz(an, rng, a.m, a.t)
        A = Annealer(a.m, centre, lr, th, rng, w7=a.w7, out=a.out, tag='%s_r%d' % (tag, rnum), T0=a.T0, Tmin=a.Tmin)
        A.pfocus = a.pfocus
        A.fixphase = a.fixphase
        log('restart', rnum, an, 'init N8', A.c[8], 'N7', A.c[7])
        last = time.time()
        while time.time() < stop and A.nev < a.restart_evals:
            if A.pfocus > 0:
                A.update_focus()
            for _ in range(a.steps_per_T):
                A.step()
            A.T = max(A.Tmin, A.T * a.alpha)
            if A.T <= A.Tmin * 1.0001 and A.E > A.best[0] + 1e-12 and rng.random() < 0.3:
                A.lr, A.th = A.best[1].copy(), A.best[2].copy(); A.c = list(A.best[3]); A.E = A.best[0]
                A.T = A.T0 * 0.3
            if time.time() - last > 60:
                last = time.time()
                log('r%d ev %d acc %.3f ab %.3f T %.4f cur N8 %d N7 %d | best N8 %d N7 %d' % (
                    rnum, A.nev, A.nacc / max(1, A.nev), A.nab / max(1, A.nev), A.T, A.c[8], A.c[7],
                    A.best[3][8], A.best[3][7]))
                write_cfg(os.path.join(a.out, 'best_%s_r%d.json' % (tag, rnum)), a.m, A.best[1], A.best[2], centre, A.best[3])
        write_cfg(os.path.join(a.out, 'best_%s_r%d.json' % (tag, rnum)), a.m, A.best[1], A.best[2], centre, A.best[3])
        log('end restart', rnum, an, 'evals', A.nev, 'best N8', A.best[3][8], 'N7', A.best[3][7], 'found', A.found)
        if gbest is None or A.best[0] < gbest[0]:
            gbest = A.best
            write_cfg(os.path.join(a.out, 'gbest_%s.json' % tag), a.m, gbest[1], gbest[2], centre, gbest[3])
    log('done', 'gbest N8', gbest[3][8] if gbest else None)


if __name__ == '__main__':
    main()
