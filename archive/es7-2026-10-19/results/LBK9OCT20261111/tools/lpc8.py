#!/usr/bin/env python3
"""Phase-fixed LP-CEGAR for t nested regular octagons without a convex 9-gon (m = 8, K = 9); adapted from
<six10-work-dir>/search/cegar/lpcegar.py (m = 6, K = 8).

For FIXED phases theta_i (layer i in radial order, theta_0 = 0, theta_i in (0, 45 deg)), every orientation
  2 area(p, q, s) / (r_p r_q r_s) = u_p sin(th_s - th_q) + u_q sin(th_p - th_s) + u_s sin(th_q - th_p),   u = 1/r,
is linear in u = (1/r_0, ..., 1/r_{t-1}), with 0 < u_0 < u_1 < ... (nesting).  Per phase vector:
  * an orbit variable whose form has the same strict sign on all generators of the cone 0 < u_a < u_b < u_c of its
    layers is FORCED (sound for every radius vector: the form is positive on the open cone);
  * a phase-specialised CNF is built: forced units, Y units, gen.py's chain family simplified with the forced values
    (C7UPPER/gen.py fam_chain), gen.py's angle clauses and the chord clauses (both must agree with the forced values;
    checked), 2-layer threshold implications (as lpcegar.py);
  * loop: SAT model -> LP over the free orbit variables (max normalized margin, cone constraints) ->
    feasible: candidate (float convex-9-gon count, then exact verification elsewhere);
    infeasible: Farkas support from the LP duals -> blocking clause.
UNSAT for a phase vector is EVIDENCE ONLY (float LP cuts).  A candidate is only a candidate until verified exactly.

usage: lpc8.py --t 16 --phases FILE.json [...] --out DIR [--tmax SEC] [--tag TAG]
  phases JSON: {"th": [...], "lr": [...]} in radians (lr optional, used as SAT phase hint; layers sorted by -lr)
"""
import sys, os, json, math, time, argparse
import numpy as np
from scipy.optimize import linprog
from pysat.solvers import Solver
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen
import ev9

M = 8
K = 9


class Base:
    def __init__(self, t, chord_file=None):
        self.t = t
        E = gen.Enc(M, K, t)
        self.E = E
        self.base_nv = E.nv
        nt = E.ntriplevars
        self.nt = nt
        self.pts = np.zeros((nt + 1, 3), dtype=int)
        for C, v in E.tvar.items():
            self.pts[v] = C
        self.lay = self.pts // M
        self.kk = self.pts % M
        # gen.py angle clauses (with Y literals) for the consistency check
        E.cls = []; E.ncls = 0; E.body = None; E.forced = {}
        E.fam_order(); self.order_cls = list(E.cls)
        E.cls = []; E.ncls = 0
        E.fam_angle(); self.angle_cls = list(E.cls)
        E.cls = []; E.ncls = 0
        E.fam_nest(); self.nest_cls = list(E.cls)
        E.cls = []; E.ncls = 0; E.forced = {}
        self.chord_cls = []
        if chord_file:
            for line in open(chord_file):
                if line.strip():
                    self.chord_cls.append([int(x) for x in line.split()[:-1]])

    def forms(self, th):
        ang = th[self.lay] + 2 * math.pi * self.kk / M          # (nt+1, 3)
        A = np.zeros((self.nt + 1, self.t))
        c0 = np.sin(ang[:, 2] - ang[:, 1]); c1 = np.sin(ang[:, 0] - ang[:, 2]); c2 = np.sin(ang[:, 1] - ang[:, 0])
        rows = np.arange(self.nt + 1)
        np.add.at(A, (rows, self.lay[:, 0]), c0)
        np.add.at(A, (rows, self.lay[:, 1]), c1)
        np.add.at(A, (rows, self.lay[:, 2]), c2)
        A[0] = 0
        return A

    def forced_signs(self, A, rtol=1e-9):
        """+1/-1 if the form has that strict sign on every generator of the cone of its layers, else 0"""
        t = self.t
        # suffix sums over layers in increasing order: generator g_r = sum_{q >= r} e_q, restricted to nonzero layers
        S = np.cumsum(A[:, ::-1], axis=1)[:, ::-1]        # S[:, l] = sum_{q >= l} A[:, q]
        nrm = np.linalg.norm(A, axis=1) + 1e-300
        tol = rtol * nrm
        res = np.zeros(self.nt + 1, dtype=int)
        for v in range(1, self.nt + 1):
            Ls = sorted(set(self.lay[v]))
            vals = [S[v, l] for l in Ls]
            # the generators are e_{Ls[-1]}, e_{Ls[-2]}+e_{Ls[-1]}, ...; suffix sums over ALL layers >= l equal the sum
            # over involved layers >= l because A is zero elsewhere
            if all(x > tol[v] for x in vals):
                res[v] = 1
            elif all(x < -tol[v] for x in vals):
                res[v] = -1
        return res


def threshold_clauses(base, A, forced):
    t = base.t
    cls = []
    bypair = {}
    for v in range(1, base.nt + 1):
        if forced[v]:
            continue
        nz = [i for i in range(t) if abs(A[v, i]) > 1e-15]
        if len(nz) == 2:
            i, j = nz
            a, b = A[v, i], A[v, j]
            c = -a / b
            lit_gt = v if b > 0 else -v         # sign for rho = u_j/u_i > c
            if c > 1.0:
                bypair.setdefault((i, j), []).append((c, lit_gt))
    for key, L in bypair.items():
        L.sort()
        for (c1, l1), (c2, l2) in zip(L, L[1:]):
            cls.append([-l2, l1])
    return cls


def lp_check(A, signs, vars_, t):
    rows = A[vars_] * signs[:, None]
    nrm = np.linalg.norm(rows, axis=1)
    rows = rows / nrm[:, None]
    nvar = t + 1
    c = np.zeros(nvar); c[-1] = -1.0
    A1 = np.hstack([-rows, np.ones((len(rows), 1))])
    # cone: u_i (1 + 1e-7) - u_{i+1} <= 0
    A2 = np.zeros((t - 1, nvar))
    for i in range(t - 1):
        A2[i, i] = 1.0 + 1e-7; A2[i, i + 1] = -1.0
    A_ub = np.vstack([A1, A2]); b_ub = np.zeros(len(A_ub))
    A_eq = np.zeros((1, nvar)); A_eq[0, 0] = 1.0
    bounds = [(0, 1e9)] * t + [(None, 1.0)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=np.array([1.0]), bounds=bounds, method='highs')
    if res.status != 0:
        return None, None, None
    return -res.fun, res.x[:t], res.ineqlin.marginals[:len(rows)]


def build_phase_cnf(base, th, log, S):
    """adds the phase-specialised CNF to solver S (streamed); returns A, forced signs, conflicts, sizes"""
    E = base.E
    t = base.t
    A = base.forms(th)
    fs = base.forced_signs(A)
    forced = {}
    for v in range(1, base.nt + 1):
        if fs[v]:
            forced[v] = v if fs[v] > 0 else -v
    ylit = {}
    for (i, j), y in E.Y.items():
        ylit[y] = y if th[i] < th[j] else -y
    val = {}
    for v, l in forced.items():
        val[v] = (l > 0)
    for y, l in ylit.items():
        val[y] = (l > 0)
    for l in forced.values():
        S.add_clause([l])
    for l in ylit.values():
        S.add_clause([l])
    # consistency: every gen.py order/angle/nest clause and chord clause must not be falsified by the fixed values
    bad = 0
    nkeep = 0
    for fam, cl_list in (('order', base.order_cls), ('angle', base.angle_cls), ('nest', base.nest_cls),
                         ('chord', base.chord_cls)):
        for cl in cl_list:
            sat = False; rest = []
            for l in cl:
                a = abs(l)
                if a in val:
                    if val[a] == (l > 0):
                        sat = True; break
                else:
                    rest.append(l)
            if sat:
                continue
            if not rest:
                bad += 1
                if bad <= 5:
                    log('  CONFLICT %s clause %s with fixed phase values' % (fam, cl))
            else:
                S.add_clause(rest); nkeep += 1
    thr = [] if os.environ.get('LPC8_NO_THR') else threshold_clauses(base, A, fs)
    for cl in thr:
        S.add_clause(cl)
    # chain family simplified with the forced values, streamed into S
    E.cls = []; E.ncls = 0; E.nv = base.base_nv; E.body = None
    E.forced = dict(forced)
    cnt = [0]
    def add(cl):
        S.add_clause(cl); cnt[0] += 1
    E.add = add
    E.fam_chain()
    del E.add
    return A, fs, E.nv, bad, (len(forced), nkeep, len(thr), cnt[0])


def radii_anneal(th, lr0, secs, log, seed=1):
    """evidence only: minimise the float convex-9-gon count over the radii with the phases fixed (radial order kept)"""
    rng = np.random.default_rng(seed)
    lr = np.array(lr0, float).copy(); lr -= lr[0]
    c, md = ev9.count_cfg(lr, th, 9)
    best = (c, lr.copy())
    t0 = time.time(); T = 0.3; n = 0
    while time.time() - t0 < secs and best[0] > 0:
        n += 1
        i = int(rng.integers(1, len(lr)))
        old = lr[i]
        lr[i] += 10 ** rng.uniform(-4, -0.5) * rng.normal()
        lo = lr[i + 1] if i + 1 < len(lr) else -1e9
        if not (lo < lr[i] < lr[i - 1]):
            lr[i] = old; continue
        c2, _ = ev9.count_cfg(lr, th, 9)
        if c2 <= c or rng.random() < math.exp(-(math.log1p(c2) - math.log1p(c)) / T):
            c = c2
            if c < best[0]:
                best = (c, lr.copy())
        else:
            lr[i] = old
        T = max(0.02, 0.3 * (1 - (time.time() - t0) / secs))
    log('  radii anneal: %d moves, best float N9 %d' % (n, best[0]))
    return best[1], best[0]


def run_phase(base, th, tmax, log, out, tag, hint_lr=None, solver='cadical195', guide=False, relax_frac=1.0,
              anneal_secs=0):
    t = base.t
    t0 = time.time()
    S = Solver(name=solver)
    A, fs, nv, bad, sizes = build_phase_cnf(base, th, log, S)
    free = np.array([v for v in range(1, base.nt + 1) if fs[v] == 0])
    log('phase %s: th(deg)=%s' % (tag, [round(math.degrees(x), 4) for x in th]))
    log('  forced %d, free %d, kept rule clauses %d, threshold %d, chain %d, conflicts %d, build %.1f s' % (
        sizes[0], len(free), sizes[1], sizes[2], sizes[3], bad, time.time() - t0))
    if bad:
        S.delete()
        return 'CONFLICT', 0, 0
    assum = set()
    if hint_lr is not None:
        u = np.exp(-np.array(hint_lr))
        sg = np.sign(A @ u)
        S.set_phases([int(v if sg[v] > 0 else -v) for v in free])
        nrm_h = np.linalg.norm(A, axis=1) + 1e-300
        marg = {}
        for v in free:
            marg[int(v)] = abs(float(A[v] @ u)) / nrm_h[v] / float(np.max(u))
        if guide:
            assum = set(int(v if sg[v] > 0 else -v) for v in free)
            log('  guided: %d hint assumptions' % len(assum))
    it = 0; ncut = 0; nrelax = 0
    best = -1
    t1 = time.time()
    if not S.solve():          # phase filter: the phase-specialised CNF itself
        log('  PHASE-UNSAT (first solve, no cuts, no assumptions) %.1f s' % (time.time() - t1))
        S.delete()
        return 'UNSAT', 0, 0
    log('  phase-SAT (first solve) %.1f s' % (time.time() - t1))
    if anneal_secs > 0 and hint_lr is not None:
        hint_lr, n9 = radii_anneal(th, hint_lr, anneal_secs, log)
        u = np.exp(-np.array(hint_lr))
        sg = np.sign(A @ u)
        S.set_phases([int(v if sg[v] > 0 else -v) for v in free])
        nrm_h = np.linalg.norm(A, axis=1) + 1e-300
        marg = {int(v): abs(float(A[v] @ u)) / nrm_h[v] / float(np.max(u)) for v in free}
        if guide:
            assum = set(int(v if sg[v] > 0 else -v) for v in free)
            log('  guided (after radii anneal): %d hint assumptions' % len(assum))
        if n9 == 0:
            fn = os.path.join(out, 'cand_%s_anneal.json' % tag)
            json.dump(dict(lr=list(map(float, hint_lr)), th=list(map(float, th)), N9=0, note='radii anneal (float)'),
                      open(fn, 'w'), indent=1)
            log('  float N9 = 0 after radii anneal: %s' % fn)
    while time.time() - t1 < tmax:
        it += 1
        ok = S.solve(assumptions=sorted(assum, key=abs)) if assum else S.solve()
        if not ok and assum:
            core = S.get_core() or []
            nrelax += 1
            if not core:
                assum = set()
            elif relax_frac >= 1.0:
                assum -= set(core)
            else:
                cs = sorted(core, key=lambda l: marg.get(abs(l), 0.0))
                assum -= set(cs[:max(1, int(len(cs) * relax_frac))])
            if nrelax % 20 == 1:
                log('  relax %d: core %d, %d assumptions left' % (nrelax, len(core), len(assum)))
            continue
        if not ok:
            log('  UNSAT after %d iterations, %d cuts, %.1f s (no radii for these phases; float cuts: evidence)' % (
                it, ncut, time.time() - t1))
            S.delete()
            return 'UNSAT', it, ncut
        mdl = S.get_model()
        sg = np.array([1.0 if mdl[v - 1] > 0 else -1.0 for v in free])
        delta, u, duals = lp_check(A, sg, free, t)
        if delta is None:
            log('  LP failure'); S.delete(); return 'LPFAIL', it, ncut
        if delta > 1e-10:
            lr = -np.log(u / u[0])
            c9, md = ev9.count_cfg(lr, th, 9)
            log('  [it %d relax %d] REALIZABLE sign vector: delta=%.3e float N9=%d mindet=%.2e lr=%s' % (
                it, nrelax, delta, c9, md, np.round(lr, 6).tolist()))
            fn = os.path.join(out, 'cand_%s_%d.json' % (tag, it))
            json.dump(dict(lr=lr.tolist(), th=list(map(float, th)), delta=float(delta), N9=int(c9), mindet=md,
                           note='LP-CEGAR candidate (float)'), open(fn, 'w'), indent=1)
            S.delete()
            return 'CAND', it, ncut
        best = max(best, delta)
        sup = [k for k in range(len(free)) if abs(duals[k]) > 1e-9]
        if not sup:
            log('  empty dual support, delta=%g' % delta); S.delete(); return 'NODUAL', it, ncut
        S.add_clause([int(-sg[k] * free[k]) for k in sup])
        su = A[free] @ np.maximum(u, 0)
        S.set_phases([int(v if s > 0 else -v) for v, s in zip(free, su)])
        ncut += 1
        if it % 100 == 0 or ncut == 1:
            log('  it %d relax %d assum %d cuts %d last support %d delta %.3e  %.1f s' % (it, nrelax, len(assum), ncut, len(sup), delta, time.time() - t1))
    log('  TIMEOUT after %d iterations, %d cuts, %.1f s' % (it, ncut, time.time() - t1))
    S.delete()
    return 'TIMEOUT', it, ncut


def load_phase(pf, t):
    d = json.load(open(pf))
    th = np.array(d['th'], float)
    lr = np.array(d['lr'], float) if 'lr' in d else None
    if lr is not None:
        o = np.argsort(-lr); th = th[o]; lr = lr[o]
    th = (th - th[0]) % (math.pi / 4)
    assert len(th) == t
    return th, lr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=int, default=16)
    ap.add_argument('--phases', nargs='+', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tmax', type=float, default=600)
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('--tag', default='lp')
    ap.add_argument('--guide', action='store_true')
    ap.add_argument('--relax-frac', type=float, default=1.0)
    ap.add_argument('--anneal', type=float, default=0)
    ap.add_argument('--chord', default=os.path.join(HERE, '..', 'cnf', 'chord_m8t16.clauses'))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'log_%s.txt' % a.tag), 'a')

    def log(s):
        logf.write(time.strftime('%H:%M:%S ') + s + '\n'); logf.flush()
    base = Base(a.t, a.chord)
    log('base built: t=%d, %d triple vars' % (a.t, base.nt))
    for pf in a.phases:
        if a.stop_at and time.time() > a.stop_at:
            break
        th, lr = load_phase(pf, a.t)
        tag = os.path.basename(pf).replace('.json', '')
        r = run_phase(base, th, a.tmax, log, a.out, tag, hint_lr=lr, guide=a.guide, relax_frac=a.relax_frac, anneal_secs=a.anneal)
        log('RESULT %s %s' % (pf, r))
    log('done')


if __name__ == '__main__':
    main()
