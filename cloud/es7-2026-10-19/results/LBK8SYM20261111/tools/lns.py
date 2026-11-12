#!/usr/bin/env python3
"""Large-neighbourhood search on m-fold configurations (float evaluator; evidence only until exact checks).
Repeat: from the incumbent (lowest N8, then N7), remove k random orbits (k = 1..kmax; preferring orbits that lie in
current convex octagons with probability pocc), insert k new orbits (near an existing orbit at a random scale, or at a
random radius/phase), anneal (annealm.Annealer) for EVALS evaluations; accept if N8 does not increase.
N8 = 0 configurations are written to OUT/found_*.json (exact verification by the watcher).
usage: lns.py --m 4 --t 14 --out DIR --tag T --init CFG.json [--hours H] [--kmax 3] [--evals 120000]"""
import sys, os, json, math, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evm import countm, pointsm, enum_k
from ptsio import write_cfg, read_cfg
from annealm import Annealer


def occ_layers(m, lr, th, centre):
    x, y = pointsm(m, lr, th, centre)
    tot, octs = enum_k(x, y, 8, 2000)
    n = m * len(lr)
    s = set()
    for P in octs:
        for p in P:
            if int(p) < n:
                s.add(int(p) // m)
    return sorted(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='lns')
    ap.add_argument('--init', required=True)
    ap.add_argument('--hours', type=float, default=1.0)
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('--kmax', type=int, default=3)
    ap.add_argument('--evals', type=int, default=120000)
    ap.add_argument('--pocc', type=float, default=0.6)
    ap.add_argument('--T0', type=float, default=0.15)
    ap.add_argument('--seed', type=int, default=0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rng = np.random.default_rng(a.seed)
    logf = open(os.path.join(a.out, 'log_%s.txt' % a.tag), 'a')

    def log(*x):
        logf.write(time.strftime('%H:%M:%S ') + ' '.join(str(v) for v in x) + '\n'); logf.flush()
    m_, lr, th, centre = read_cfg(a.init)
    m = a.m; U = 2 * math.pi / m
    o = np.argsort(-lr); lr = lr[o] - lr[o][0]; th = th[o]
    assert len(lr) == a.t
    c, _ = countm(m, lr, th, centre)
    inc = (c[8], c[7], lr.copy(), th.copy())
    log('start', a.init, 'N8', c[8], 'N7', c[7])
    stop = a.stop_at or time.time() + 3600 * a.hours
    it = 0; nfound = 0
    while time.time() < stop:
        it += 1
        lr, th = inc[2].copy(), inc[3].copy()
        t = len(lr)
        k = int(rng.integers(1, a.kmax + 1))
        occ = occ_layers(m, lr, th, centre)
        rem = []
        for _ in range(k):
            cand = [i for i in (occ if occ and rng.random() < a.pocc else range(1, t)) if i not in rem and i != 0]
            if not cand:
                cand = [i for i in range(1, t) if i not in rem]
            rem.append(int(cand[rng.integers(len(cand))]))
        keep = [i for i in range(t) if i not in rem]
        lr2 = list(lr[keep]); th2 = list(th[keep])
        for _ in range(k):
            if rng.random() < 0.6:
                j = int(rng.integers(len(lr2)))
                s = 10 ** rng.uniform(-5, -0.5)
                lr2.append(lr2[j] + rng.normal(0, s)); th2.append(th2[j] + rng.normal(0, s))
            else:
                lr2.append(rng.uniform(min(lr2) - 4, 0)); th2.append(rng.uniform(0, U))
        lr2 = np.array(lr2); th2 = np.array(th2); lr2 -= lr2.max()
        A = Annealer(m, centre, lr2, th2, rng, w7=0.02, out=a.out, tag='%s_i%d' % (a.tag, it), T0=a.T0, Tmin=0.005)
        A.pfocus = 0.3
        while A.nev < a.evals and time.time() < stop:
            A.update_focus()
            for _ in range(2000):
                A.step()
            A.T = max(A.Tmin, A.T * 0.9)
        b = A.best
        n8, n7 = b[3][8], b[3][7]
        acc = (n8, n7) <= (inc[0], inc[1] * 1.05) or n8 < inc[0]
        log('it %d removed %s -> N8 %d N7 %d (incumbent %d) %s' % (it, rem, n8, n7, inc[0], 'ACCEPT' if acc else ''))
        if acc:
            o = np.argsort(-b[1])
            inc = (n8, n7, b[1][o] - b[1][o][0], b[2][o])
            write_cfg(os.path.join(a.out, 'inc_%s.json' % a.tag), m, inc[2], inc[3], centre, b[3])
        if n8 == 0:
            nfound += 1
            write_cfg(os.path.join(a.out, 'found_%s_%d.json' % (a.tag, nfound)), m, b[1], b[2], centre, b[3], note='N8=0 (float)')
            log('N8 = 0 FOUND')
    log('done')


if __name__ == '__main__':
    main()
