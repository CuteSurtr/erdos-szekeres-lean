#!/usr/bin/env python3
"""Phase-fixed LP-CEGAR (root-unit variant: a fresh solver per phase vector, the phase order and the
phase-specific threshold units added at root level) for t nested regular m-gons (no centre) without a convex octagon; generic m.
Adapted from <six10-work-dir>/search/cegar/lpcegar.py (m = 6 there).

For FIXED phases theta_i (layer i in radial order, theta_0 = 0, theta_i in (0, 2pi/m)), every orientation
  2 area(p, q, s) / (r_p r_q r_s) = u_p sin(a_s - a_q) + u_q sin(a_p - a_s) + u_s sin(a_q - a_p),   u = 1/r,
is LINEAR in u = (1/r_0, ..., 1/r_{t-1}) (ES8SYM Lemma 1).  So a sign vector of the orbit variables of gen.py's
Enc(m, 8, t) is realizable with these phases iff an LP in u is feasible.  Loop:
  SAT model of CNF(gen.py m 8 t) + phase-order units (Y, and H for odd m) + phase-specific 2-layer threshold chains
  + LP cuts  ->  LP (maximise the normalised margin)  ->  margin > 0: radii (float check, exact verification later);
  margin <= 0: Farkas support from the LP duals -> clause "not all these signs" (guarded by an activation literal).
UNSAT for a phase vector: no radii for these phases (numerical cuts: EVIDENCE ONLY).  A positive answer is only a
candidate until it passes the exact pipeline.

usage: lpcegarm.py --m 4 --t 14 --cnf FILE --out DIR --tag T --tmax SEC [--sigma DEG --npert N --seed S] CFG.json ...
   CFG.json: {"lr": [...], "th": [...]} (annealm.py output works); with --npert N > 0 each config also yields N
   random perturbations of its phases (normal, sigma degrees), in addition to the unperturbed phases (if --keep0).
"""
import sys, os, json, math, time, argparse
import numpy as np
from scipy.optimize import linprog
from pysat.solvers import Solver
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'py'))
import gen
from evm import countm

POLARITY = True
SUFFIX3 = True
REPHASE = True


def triple_forms(E, th):
    M = E.m
    t = E.t
    A = np.zeros((E.ntriplevars + 1, t))
    for C, v in E.tvar.items():
        ang = []
        lay = []
        for x in C:
            i, k = divmod(x, M)
            ang.append(th[i] + 2 * math.pi * k / M)
            lay.append(i)
        p, q, s = 0, 1, 2
        A[v, lay[p]] += math.sin(ang[s] - ang[q])
        A[v, lay[q]] += math.sin(ang[p] - ang[s])
        A[v, lay[s]] += math.sin(ang[q] - ang[p])
    return A


def threshold_clauses(E, A, act):
    t = E.t
    cls = []
    nunit = 0
    bypair = {}
    for v in range(1, E.ntriplevars + 1):
        nz = [i for i in range(t) if abs(A[v, i]) > 1e-13]
        if len(nz) == 1:
            lit = v if A[v, nz[0]] > 0 else -v
            cls.append([-act, lit]); nunit += 1
        elif len(nz) == 2:
            i, j = nz
            a, b = A[v, i], A[v, j]
            c = -a / b
            lit_gt = v if b > 0 else -v
            if c <= 1.0:
                cls.append([-act, lit_gt]); nunit += 1
            else:
                bypair.setdefault((i, j), []).append((c, lit_gt))
    # forms with 3 nonzero coefficients: with u_0 < u_1 < ... < u_{t-1} (radii decrease with the layer index),
    # u = sum_k c_k e_k (e_k = indicator of {i >= k}, c_k > 0), so a.u has the sign of the suffix sums of a when
    # they all share one sign (sound for every configuration of nested layers with these phases).
    n3 = 0
    if SUFFIX3:
        for v in range(1, E.ntriplevars + 1):
            nz = [i for i in range(t) if abs(A[v, i]) > 1e-13]
            if len(nz) != 3:
                continue
            suf = np.cumsum(A[v, ::-1])[::-1][:nz[-1] + 1]   # S_k for k > last nonzero index are exactly 0
            if np.all(suf > 1e-12):
                cls.append([-act, v]); nunit += 1; n3 += 1
            elif np.all(suf < -1e-12):
                cls.append([-act, -v]); nunit += 1; n3 += 1
    nimp = 0
    for key, L in bypair.items():
        L.sort()
        for (c1, l1), (c2, l2) in zip(L, L[1:]):
            cls.append([-act, -l2, l1]); nimp += 1
    return cls, nunit, nimp


def lp_check(A, signs, t, vars_):
    rows = A[vars_] * signs[:, None]
    nrm = np.linalg.norm(rows, axis=1)
    rows = rows / nrm[:, None]
    nv = t + 1
    c = np.zeros(nv); c[-1] = -1.0
    A_ub = np.hstack([-rows, np.ones((len(rows), 1))])
    b_ub = np.zeros(len(rows))
    A_eq = np.zeros((1, nv)); A_eq[0, 0] = 1.0
    b_eq = np.array([1.0])
    bounds = [(0, None)] * t + [(None, 1.0)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    if res.status != 0:
        return None, None, None
    return -res.fun, res.x[:t], res.ineqlin.marginals


def phase_assumptions(E, th):
    m = E.m
    if m % 2:
        psi = th % (math.pi / m)
    else:
        psi = th
    assum = []
    for (i, j), y in E.Y.items():
        assum.append(y if psi[i] < psi[j] else -y)
    for i, h in E.H.items():
        assum.append(h if th[i] < math.pi / m else -h)
    return assum


def build_solver(cnf_files, units, extra_cls):
    """fresh CaDiCaL with the CNF simplified by the given root units (clauses satisfied by a unit are dropped,
    falsified literals removed; every unit is also added as a clause, so the formula is equivalent)."""
    S = Solver(name='cadical195')
    us = set(units)
    for fn in cnf_files:
        with open(fn) as f:
            for line in f:
                if line[0] in 'pc' or not line.strip():
                    continue
                c = [int(x) for x in line.split()[:-1]]
                if any(x in us for x in c):
                    continue
                S.add_clause([x for x in c if -x not in us])
    for u in us:
        S.add_clause([u])
    for c in extra_cls:
        S.add_clause(c)
    return S


def run_phase(S, E, th, act, tmax, log, out, tag, hint_lr=None, max_iter=10 ** 7, cnf_files=None):
    t = E.t
    A = triple_forms(E, th)
    cls, nunit, nimp = threshold_clauses(E, A, act)
    if cnf_files is not None:
        units = set(phase_assumptions(E, th))
        rest = []
        for cl in cls:
            c = [x for x in cl if x != -act]
            if len(c) == 1:
                units.add(c[0])
            else:
                rest.append(c)
        tl = time.time()
        S = build_solver(cnf_files, units, rest)
        log('  fresh solver with %d root units, %.1f s' % (len(units), time.time() - tl))
        assum = []
    else:
        for cl in cls:
            S.add_clause(cl)
        assum = [act] + phase_assumptions(E, th)
    log('phase %s: th(deg)=%s units %d impl %d' % (tag, [round(math.degrees(v), 4) for v in th], nunit, nimp))
    if hint_lr is not None and POLARITY:
        u = np.exp(-np.array(hint_lr))
        sg = np.sign(A[1:] @ u)
        S.set_phases([int(v if sg[v - 1] > 0 else -v) for v in range(1, E.ntriplevars + 1)])
    t0 = time.time()
    it = 0
    allv = np.arange(1, E.ntriplevars + 1)
    ncut = 0
    best_delta = -1
    while time.time() - t0 < tmax and it < max_iter:
        it += 1
        ok = S.solve(assumptions=assum)
        if not ok:
            log('  UNSAT after %d iterations, %d cuts, %.1f s' % (it, ncut, time.time() - t0))
            if cnf_files is not None:
                S.delete()
            return 'UNSAT', it, ncut, None
        mdl = S.get_model()
        sg = np.array([1.0 if mdl[v - 1] > 0 else -1.0 for v in allv])
        delta, u, duals = lp_check(A, sg, t, allv)
        if delta is None:
            log('  LP failure'); return 'LPFAIL', it, ncut, None
        if delta > 1e-10:
            lr = -np.log(u / u[0])
            c, _ = countm(E.m, lr, th, 0)
            log('  REALIZABLE sign vector: delta=%.3e  float N8=%d N7=%d  lr=%s' % (delta, c[8], c[7], np.round(lr, 6).tolist()))
            fn = os.path.join(out, 'cand_%s_%d.json' % (tag, it))
            json.dump(dict(m=E.m, centre=0, lr=lr.tolist(), th=list(map(float, th)), delta=delta,
                           counts={str(k): int(c[k]) for k in range(3, 9)}, note='LP-CEGAR candidate'),
                      open(fn, 'w'), indent=1)
            if cnf_files is not None:
                S.delete()
            return 'CAND', it, ncut, fn
        best_delta = max(best_delta, delta)
        sup = [k for k in range(len(allv)) if abs(duals[k]) > 1e-9]
        if not sup:
            log('  empty dual support, delta=%g' % delta); return 'NODUAL', it, ncut, None
        clause = ([-act] if assum else []) + [int(-sg[k] * allv[k]) for k in sup]
        S.add_clause(clause)
        if REPHASE:
            su = A[1:] @ np.maximum(u, 0)
            S.set_phases([int(v if su[v - 1] > 0 else -v) for v in range(1, E.ntriplevars + 1)])
        ncut += 1
        if it % 200 == 0:
            log('  it %d cuts %d last support %d delta %.3e  %.1f s' % (it, ncut, len(sup), delta, time.time() - t0))
    log('  TIMEOUT after %d iterations, %d cuts, %.1f s best delta %.3e' % (it, ncut, time.time() - t0, best_delta))
    if cnf_files is not None:
        S.delete()
    return 'TIMEOUT', it, ncut, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--cnf', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='lp')
    ap.add_argument('--tmax', type=float, default=120)
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('--sigma', type=float, default=0.0)
    ap.add_argument('--npert', type=int, default=0)
    ap.add_argument('--keep0', type=int, default=1)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--scan', default='', help='LAYER:LO:HI:STEP (degrees, relative to layer 0): scan this layer phase')
    ap.add_argument('--players', default='', help='comma list of layers (radial order) to perturb; default all')
    ap.add_argument('--extra', nargs='*', default=[], help='extra clause files (sound cuts)')
    ap.add_argument('cfgs', nargs='+')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'log_%s.txt' % a.tag), 'a')
    tsv = open(os.path.join(a.out, 'res_%s.tsv' % a.tag), 'a')
    rng = np.random.default_rng(a.seed)
    U = 2 * math.pi / a.m

    def log(s):
        logf.write(time.strftime('%H:%M:%S ') + s + '\n'); logf.flush()
    E = gen.Enc(a.m, 8, a.t)
    log('Enc built: m=%d t=%d %d triple vars, %d Y, %d H' % (a.m, a.t, E.ntriplevars, len(E.Y), len(E.H)))
    S = None
    act = 10 ** 8
    jobs = []
    for pf in a.cfgs:
        d = json.load(open(pf))
        th = np.array(d['th'], float)
        lr = np.array(d['lr'], float)
        o = np.argsort(-lr); th = th[o]; lr = lr[o]
        assert len(th) == a.t, (pf, len(th))
        base = os.path.basename(pf).replace('.json', '')
        for spec in (a.scan.split(';') if a.scan else []):
            li, lo, hi, st = spec.split(':'); li = int(li)
            for ph in np.arange(float(lo), float(hi), float(st)):
                th2 = th.copy(); th2[li] = th[0] + math.radians(ph)
                jobs.append((base + '_L%d_%.4f' % (li, ph), th2, lr.copy()))
        if a.keep0:
            jobs.append((base + '_p0', th.copy(), lr.copy()))
        for k in range(a.npert):
            mask = np.ones(len(th))
            if a.players:
                mask = np.zeros(len(th)); mask[[int(x) for x in a.players.split(',')]] = 1
            sig = a.sigma if a.sigma > 0 else 10 ** rng.uniform(-2, 0.5)
            th2 = th + np.radians(rng.normal(0, sig, len(th))) * mask
            jobs.append((base + '_s%g_%d' % (a.sigma, k + 1), th2, lr.copy()))
    log('%d phase vectors' % len(jobs))
    for tag, th, lr in jobs:
        if a.stop_at and time.time() > a.stop_at:
            break
        th = (th - th[0]) % U
        act += 1
        t0 = time.time()
        r = run_phase(S, E, th, act, a.tmax, log, a.out, tag, hint_lr=lr, cnf_files=[a.cnf] + a.extra)
        tsv.write('%s\t%s\t%d\t%d\t%.1f\t%s\n' % (tag, r[0], r[1], r[2], time.time() - t0, r[3] or ''))
        tsv.flush()
        log('RESULT %s %s' % (tag, r[:3]))
    log('done')


if __name__ == '__main__':
    main()
