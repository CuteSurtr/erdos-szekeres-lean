#!/usr/bin/env python3
"""Trust-region phase-fixed LP-CEGAR (m-fold, nested layers, no centre).  EVIDENCE ONLY for negative answers; a
positive answer is a candidate for the exact pipeline.

Given a real configuration R (lr, th) with a few convex octagons, keep its phases fixed and look for radii that
remove the octagons while changing few orientation signs:
  * forms a_v (orbit variable v of gen.py Enc(m, 8, t)) are linear in u = 1/r for the fixed phases;
  * free set F = orbit variables of all triples inside R's convex octagons, plus the K variables with the smallest
    normalised |a_v . u_R|;  every other orbit variable is fixed to R's sign (root unit);
  * CEGAR: SAT model of the simplified CNF (gen.py CNF + phase-order units + threshold units + fixed signs) -> LP for u
    (max-min normalised margin) -> Farkas clause or candidate.
K grows over the list given; for each K the loop runs at most TMAX seconds.

usage: trlp.py --m 4 --t 14 --cnf FILE --out DIR --tag T [--K 300,1000,3000] [--tmax 60] [--sigma DEG --npert N] CFG.json ...
"""
import sys, os, json, math, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'py'))
import gen
import lpcegar2 as L
from evm import countm, pointsm, enum_k


def octagon_vars(E, th, lr, maxout=20000):
    x, y = pointsm(E.m, lr, th, 0)
    tot, octs = enum_k(x, y, 8, maxout)
    vs = set()
    for P in octs:
        P = list(map(int, P))
        for a in range(8):
            for b in range(a + 1, 8):
                for c in range(b + 1, 8):
                    vs.add(abs(E.o(P[a], P[b], P[c])))
    return tot, vs


def cegar(E, A, th, lr_hint, units, rest, cnf_files, tmax, log, out, tag):
    t = E.t
    S = L.build_solver(cnf_files, units, rest)
    u = np.exp(-np.array(lr_hint))
    sg = np.sign(A[1:] @ u)
    S.set_phases([int(v if sg[v - 1] > 0 else -v) for v in range(1, E.ntriplevars + 1)])
    allv = np.arange(1, E.ntriplevars + 1)
    t0 = time.time(); it = 0; best = -9
    try:
        while time.time() - t0 < tmax:
            it += 1
            if not S.solve():
                return 'UNSAT', it, best, None
            mdl = S.get_model()
            s = np.array([1.0 if mdl[v - 1] > 0 else -1.0 for v in allv])
            delta, uu, du = L.lp_check(A, s, t, allv)
            if delta is None:
                return 'LPFAIL', it, best, None
            if delta > 1e-10:
                lr = -np.log(uu / uu[0])
                c, _ = countm(E.m, lr, th, 0)
                fn = os.path.join(out, 'cand_%s_%d.json' % (tag, it))
                json.dump(dict(m=E.m, centre=0, lr=lr.tolist(), th=list(map(float, th)), delta=delta,
                               counts={str(k): int(c[k]) for k in range(3, 9)}, note='trust-region LP-CEGAR candidate'),
                          open(fn, 'w'), indent=1)
                log('  CAND delta %.3e float N8 %d N7 %d -> %s' % (delta, c[8], c[7], fn))
                return 'CAND', it, delta, fn
            best = max(best, delta)
            sup = [k for k in range(len(allv)) if abs(du[k]) > 1e-9]
            if not sup:
                return 'NODUAL', it, best, None
            S.add_clause([int(-s[k] * allv[k]) for k in sup])
            su = A[1:] @ np.maximum(uu, 0)
            S.set_phases([int(v if su[v - 1] > 0 else -v) for v in allv])
        return 'TIMEOUT', it, best, None
    finally:
        S.delete()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--cnf', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='tr')
    ap.add_argument('--K', default='200,600,1500,3000')
    ap.add_argument('--tmax', type=float, default=60)
    ap.add_argument('--sigma', type=float, default=0.0)
    ap.add_argument('--npert', type=int, default=0)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('cfgs', nargs='+')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'log_%s.txt' % a.tag), 'a')
    tsv = open(os.path.join(a.out, 'res_%s.tsv' % a.tag), 'a')

    def log(s):
        logf.write(time.strftime('%H:%M:%S ') + s + '\n'); logf.flush()
    E = gen.Enc(a.m, 8, a.t)
    U = 2 * math.pi / a.m
    rng = np.random.default_rng(a.seed)
    Ks = [int(k) for k in a.K.split(',')]
    for pf in a.cfgs:
        d = json.load(open(pf))
        lr0 = np.array(d['lr'], float); th0 = np.array(d['th'], float)
        o = np.argsort(-lr0); lr0 = lr0[o] - lr0[o][0]; th0 = th0[o]
        variants = [('p0', th0.copy())] + [('s%g_%d' % (a.sigma, k + 1), th0 + np.radians(rng.normal(0, a.sigma, a.t)))
                                           for k in range(a.npert)]
        for vn, th in variants:
            if a.stop_at and time.time() > a.stop_at:
                break
            th = (th - th[0]) % U
            tag = os.path.basename(pf).replace('.json', '') + '_' + vn
            c, _ = countm(a.m, lr0, th, 0)
            A = L.triple_forms(E, th)
            cls, nunit, nimp = L.threshold_clauses(E, A, 10 ** 8)
            punits = set(L.phase_assumptions(E, th))
            rest = []
            for cl in cls:
                cc = [x for x in cl if x != -10 ** 8]
                if len(cc) == 1:
                    punits.add(cc[0])
                else:
                    rest.append(cc)
            u = np.exp(-lr0)
            val = A[1:] @ u / np.linalg.norm(A[1:], axis=1)
            sgn = np.where(val > 0, 1, -1)
            nocts, ovars = octagon_vars(E, th, lr0)
            # consistency: R's own signs must satisfy the phase/threshold units
            Rlits = {int((v + 1) * sgn[v]) for v in range(E.ntriplevars)}
            bad = [x for x in punits if abs(x) <= E.ntriplevars and x not in Rlits]
            log('%s: N8 %d N7 %d, octagon vars %d, unit conflicts with R %d' % (tag, c[8], c[7], len(ovars), len(bad)))
            order = np.argsort(np.abs(val))
            for K in Ks:
                if a.stop_at and time.time() > a.stop_at:
                    break
                free = set(ovars) | set(int(v) + 1 for v in order[:K])
                units = set(punits)
                for v in range(1, E.ntriplevars + 1):
                    if v not in free:
                        lit = int(v * sgn[v - 1])
                        if -lit in units:
                            continue
                        units.add(lit)
                t0 = time.time()
                r = cegar(E, A, th, lr0, units, rest, [a.cnf], a.tmax, log, a.out, '%s_K%d' % (tag, K))
                log('  K %d free %d -> %s it %d best delta %.3e (%.1f s)' % (K, len(free), r[0], r[1], r[2], time.time() - t0))
                tsv.write('%s\t%d\t%d\t%s\t%d\t%.3e\t%.1f\t%s\n' % (tag, c[8], K, r[0], r[1], r[2], time.time() - t0, r[3] or ''))
                tsv.flush()
                if r[0] == 'CAND':
                    break
    log('done')


if __name__ == '__main__':
    main()
