#!/usr/bin/env python3
"""Alternating projections (m-fold, nested layers, no centre) from given start configurations.
Adapted from <six10-work-dir>/realize/p2/mfold/tools/mf_altproj.py; differences: starts are given configurations
(annealing optima), and the SAT step uses a fresh CaDiCaL per round with R's full phase order (Y, H) as ROOT units
(the CNF is simplified by them), R's orientation signs as decision phases.

Round: R --SAT (phase order of R fixed, phases = R's signs)--> octagon-free model M of gen.py's Enc(m, 8, t)
          --scale-free fit from R (mf.Fit)--> R'.
The best round is annealed on N8 (float evaluator); N8 = 0 configurations are written for exact verification.
Evidence only until the exact pipeline accepts a rounding.

usage: altproj2.py --m 4 --t 14 --cnf FILE --out DIR --tag T [--rounds 8] [--conf 2000000] [--stop-at EPOCH] CFG.json ...
"""
import sys, os, json, time, math, argparse
import numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mf as MFM
from pysat.solvers import Solver
from ptsio import write_cfg
from evm import enum_k
import itertools


def build(cnf, units):
    S = Solver(name='cadical195')
    us = set(units)
    with open(cnf) as f:
        for line in f:
            if line[0] in 'pc' or not line.strip():
                continue
            c = [int(x) for x in line.split()[:-1]]
            if any(x in us for x in c):
                continue
            S.add_clause([x for x in c if -x not in us])
    for u in us:
        S.add_clause([u])
    return S


def cfg_z(fn):
    d = json.load(open(fn))
    lr = np.array(d['lr'], float); th = np.array(d['th'], float)
    return np.exp(lr + 1j * th)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--cnf', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='ap')
    ap.add_argument('--rounds', type=int, default=8)
    ap.add_argument('--conf', type=int, default=2000000)
    ap.add_argument('--anneal', type=int, default=30000)
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--repeat', type=int, default=1, help='passes over the start list (chain: improved results are re-used)')
    ap.add_argument('--trust', default='', help='comma list of trust-region sizes K: fix R signs except the K least robust records and the triples of R octagons')
    ap.add_argument('cfgs', nargs='+')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'log_%s.txt' % a.tag), 'a')

    def LOG(*x):
        s = time.strftime('%H:%M:%S ') + ' '.join(str(v) for v in x)
        logf.write(s + '\n'); logf.flush()
    F = MFM.MF(a.m, a.t)
    yinv = {v: ij for ij, v in F.E.Y.items()}; hinv = {v: i for i, v in F.E.H.items()}
    stop = a.stop_at or time.time() + 10 ** 7
    starts = [(fn, F.normalise(cfg_z(fn))) for fn in a.cfgs]
    nst = 0
    for rep in range(a.repeat):
        newstarts = []
        for fn, z in starts:
            if time.time() > stop - 30:
                break
            nst += 1
            R = F.normalise(z)
            n8R, n7R = F.octs(R)
            LOG('start', nst, os.path.basename(fn), 'N8', n8R, 'N7', n7R)
            hist = []; seen = set()
            for rnd in range(a.rounds):
                if time.time() > stop - 30:
                    break
                L, sR = F.lits(R)
                units = [l for l in L if abs(l) in yinv or abs(l) in hinv]
                t1 = time.time()
                if a.trust:
                    rob = np.abs(MFM.Fit(F, sR).values(MFM.Fit(F, sR).x_of(R)))
                    order = np.argsort(rob)
                    P = F.points(R)
                    tot, octs = enum_k(P.real.copy(), P.imag.copy(), 8, 5000)
                    ov = set()
                    for Q in octs:
                        Q = list(map(int, Q))
                        for i1, i2, i3 in itertools.combinations(Q, 3):
                            ov.add(abs(F.E.o(i1, i2, i3)))
                    for K in [int(k) for k in a.trust.split(',')]:
                        free = ov | set(int(v) + 1 for v in order[:K])
                        fixu = units + [L[v] for v in range(F.NT) if (v + 1) not in free]
                        S = build(a.cnf, fixu)
                        S.set_phases(L)
                        S.conf_budget(a.conf)
                        r_ = S.solve_limited()
                        if r_ is True:
                            break
                        S.delete()
                    LOG('  rnd', rnd, 'trust K', K, 'free', len(free), 'octagon vars', len(ov), 'result', r_)
                else:
                    S = build(a.cnf, units)
                    S.set_phases(L)
                    S.conf_budget(a.conf)
                    r_ = S.solve_limited()
                tsat = time.time() - t1
                if r_ is not True:
                    LOG('  rnd', rnd, 'solver', r_, 'tsat %.0f' % tsat); S.delete(); break
                mod = S.get_model(); S.delete()
                pos = set(l for l in mod[:F.NT] if l > 0)
                want = np.array([1 if (v + 1) in pos else -1 for v in range(F.NT)])
                d = int((want != sR).sum()); h = hash(want.tobytes())
                t1 = time.time(); fit = MFM.Fit(F, want); R2, w = fit.fit(R); tfit = time.time() - t1
                R2 = F.normalise(R2); w = F.nwrong(R2, want)
                o8, o7 = F.octs(R2)
                LOG('  rnd', rnd, 'd(M,R)=', d, 'wrong(M,fit)=', w, 'N8(fit)=', o8, 'N7', o7, 'tsat %.1f tfit %.1f' % (tsat, tfit))
                hist.append((o8, w, R2))
                if o8 == 0:
                    break
                if h in seen:
                    break
                seen.add(h); R = R2
            if not hist:
                continue
            hb = min(hist, key=lambda x: (x[0], x[1]))
            if hb[0] == 0:
                n8, n7, z2 = 0, F.octs(hb[2])[1], hb[2]
            else:
                n8, n7, z2 = MFM.anneal(F, hb[2], iters=a.anneal, seed=nst + 1000 * a.seed, deadline=stop)
            LOG('start', nst, 'anneal from N8', hb[0], '->', n8, 'N7', n7)
            z2 = F.normalise(z2)
            outfn = os.path.join(a.out, '%s_res%d_N8_%d.json' % (a.tag, nst, n8))
            write_cfg(outfn, a.m, np.log(np.abs(z2)), np.angle(z2), 0, None, note='altproj2 from %s' % fn)
            if n8 == 0:
                LOG('N8 = 0 CONFIGURATION (float)', outfn)
            if n8 < n8R:
                newstarts.append((outfn, z2))
        if newstarts:
            starts = newstarts
    LOG('DONE')


if __name__ == '__main__':
    main()
