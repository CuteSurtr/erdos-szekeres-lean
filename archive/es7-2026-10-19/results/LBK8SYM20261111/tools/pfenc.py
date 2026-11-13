#!/usr/bin/env python3
"""Phase- and order-fixed CNF for m-fold sets without a convex K-gon (any m >= 2, orbits need not be nested,
optional centre), plus the phase-fixed LP-CEGAR loop on top of it.

Setting.  Orbit i (i = 0..t-1, sorted by DEcreasing radius) is {r_i e^{i(th_i + 2 pi k/m)} : k = 0..m-1}, point id
m*i + k; the centre O (if present) is point id m*t.  The phases th_i are FIXED; the radii are free but their order
r_0 > r_1 > ... > r_{t-1} > 0 is fixed.  With u = 1/r (u_0 < u_1 < ...), every orientation of three non-centre
points is the sign of a linear form a.u (polar formula, ES8SYM Lemma 1); orient(O, p, q) = sign sin(ang q - ang p)
is a constant.

Variables: one per rotation orbit of non-centre triples (canonical sorted triple, as in C7UPPER/gen.py), true iff
orient(canonical triple) > 0; chain variables.

Clauses (all hold for every real configuration with these phases, this radius order and no convex K-gon; written
argument, evidence-level tool):
  (U) sign units: a form with one nonzero coefficient; a two-coefficient form a_i u_i + a_j u_j (i < j) whose zero
      rho = -a_i/a_j <= 1 (then the sign for rho = u_j/u_i > 1 is fixed); a form whose suffix sums
      S_k = sum_{l >= k} a_l (k up to its last nonzero index) all have one sign (u = sum c_k e_k with c_k > 0 and
      e_k the indicator of {l >= k}, so a.u = sum c_k S_k);
  (T) threshold implications between two-coefficient forms of the same layer pair (sorted zeros);
  (C) chains: pivot p = (i, 0); Q = all points of orbits j > i, the other points of orbit i, and O.  Q lies in the
      open half-plane bounded by the tangent at p to the circle |z| = r_i (|q| < r_i, or |q| = r_i and q != p), so
      orientation around p is a strict angular order on Q.  R_l(q, q') = there is a chain of l points of Q ending
      q, q' with orient(p, q_s, q_{s+1}) = + and left turns.  A chain of K - 1 points closes to a convex K-gon with p
      (gen.py docstring, step 4), so it is forbidden.  Completeness: a convex K-gon has a vertex of largest radius;
      rotate it to p = (i, 0): every other vertex is in Q.
So a satisfying assignment exists for every octagon-free configuration with these phases and order (soundness), and
every assignment whose triple signs are realised by radii u gives an octagon-free configuration (completeness of
(C)).  The LP decides realisability of a sign vector for the fixed phases.
"""
import sys, os, json, math, time, itertools
import numpy as np
from scipy.optimize import linprog
from pysat.solvers import Solver
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'py'))
from evm import countm, pointsm, enum_k

TRUE = 1 << 40
PAIRS = False
LAST_BEST = {}
LPN8 = {}
FALSE = -(1 << 40)


class PF:
    def __init__(self, m, t, centre, th, K=8):
        self.m, self.t, self.centre, self.K = m, t, int(centre), K
        self.th = np.array(th, float)
        self.n = m * t
        self.N = self.n + self.centre
        n = self.n
        self.ang = np.array([self.th[x // m] + 2 * math.pi * (x % m) / m for x in range(n)] + ([0.0] if self.centre else []))
        # orbit variables of non-centre triples
        self.tvar = {}
        self.canon = {}
        nv = 0
        for T in itertools.combinations(range(n), 3):
            best = None
            for s in range(m):
                rt = [self.rot(x, s) for x in T]
                srt, par = self.sortpar(rt)
                if best is None or srt < best[0]:
                    best = (srt, par)
            C = best[0]
            if C not in self.tvar:
                nv += 1
                self.tvar[C] = nv
            self.canon[T] = (C, best[1])
        self.ntv = nv
        self.nv = nv
        self.Cof = [None] * (nv + 1)
        for C, v in self.tvar.items():
            self.Cof[v] = C
        self.forms()

    def rot(self, x, s):
        i, k = divmod(x, self.m)
        return i * self.m + (k + s) % self.m

    @staticmethod
    def sortpar(lst):
        a = list(lst); par = 1
        for i in range(len(a)):
            for j in range(len(a) - 1 - i):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]; par = -par
        return tuple(a), par

    def forms(self):
        m, t = self.m, self.t
        A = np.zeros((self.ntv + 1, t))
        for v in range(1, self.ntv + 1):
            C = self.Cof[v]
            ang = [self.ang[x] for x in C]; lay = [x // m for x in C]
            A[v, lay[0]] += math.sin(ang[2] - ang[1])
            A[v, lay[1]] += math.sin(ang[0] - ang[2])
            A[v, lay[2]] += math.sin(ang[1] - ang[0])
        self.A = A

    def units(self):
        """sign units and threshold implications, as literal lists"""
        t = self.t
        units = {}
        imps = []
        bypair = {}
        for v in range(1, self.ntv + 1):
            a = self.A[v]
            nz = [i for i in range(t) if abs(a[i]) > 1e-13]
            if len(nz) == 0:
                raise ValueError('degenerate form %d' % v)
            if len(nz) == 1:
                units[v] = v if a[nz[0]] > 0 else -v; continue
            if len(nz) == 2:
                i, j = nz
                c = -a[i] / a[j]
                lit_gt = v if a[j] > 0 else -v
                if c <= 1.0:
                    units[v] = lit_gt
                else:
                    bypair.setdefault((i, j), []).append((c, lit_gt))
                continue
            suf = np.cumsum(a[::-1])[::-1][:nz[-1] + 1]
            if np.all(suf > 1e-12):
                units[v] = v
            elif np.all(suf < -1e-12):
                units[v] = -v
        for key, L in bypair.items():
            L.sort()
            for (c1, l1), (c2, l2) in zip(L, L[1:]):
                imps.append([-l2, l1])
        return units, imps

    def lit(self, a, b, c, units):
        """literal (or TRUE/FALSE constant) for orient(a, b, c) > 0"""
        n = self.n
        if self.centre and n in (a, b, c):
            # rotate so that O is first: orient(O, p, q) = sign sin(ang q - ang p)
            if a == n:
                p, q = b, c
            elif b == n:
                p, q = c, a
            else:
                p, q = a, b
            s = math.sin(self.ang[q] - self.ang[p])
            if abs(s) < 1e-13:
                raise ValueError('centre collinear')
            return TRUE if s > 0 else FALSE
        T, s1 = self.sortpar((a, b, c))
        C, s2 = self.canon[T]
        v = self.tvar[C]
        l = v if s1 * s2 > 0 else -v
        u = units.get(v)
        if u is not None:
            return TRUE if u == l else FALSE
        return l

    def chain_clauses(self, units, fixed=None):
        """(C) for every pivot orbit; 'fixed' = dict var -> literal of additional fixed signs (trust region)."""
        if fixed:
            U = dict(units); U.update(fixed)
        else:
            U = units
        m, K = self.m, self.K
        Lc = K - 1
        cls = []
        nv = self.nv
        N = self.N
        # literal table
        for i in range(self.t):
            p = i * m
            Q = [x for x in range(i * m, N) if x != p]
            R = {}

            def rv(key):
                nonlocal nv
                if key not in R:
                    nv += 1
                    R[key] = nv
                return R[key]
            succ = {}
            pairs = []
            for q in Q:
                for q2 in Q:
                    if q == q2:
                        continue
                    l = self.lit(p, q, q2, U)
                    if l == FALSE:
                        continue
                    pairs.append((q, q2, l))
                    succ.setdefault(q, []).append((q2, l))
            turn = {}
            for q, q2, l in pairs:
                cl = [rv((2, q, q2))] + ([] if l == TRUE else [-l])
                cls.append(cl)
            for lv in range(2, Lc):
                for q, q2, _ in pairs:
                    key = (lv, q, q2)
                    if key not in R:
                        continue
                    for q3, l2 in succ.get(q2, []):
                        if q3 == q:
                            continue
                        tk = (q, q2, q3)
                        lt = turn.get(tk)
                        if lt is None:
                            lt = self.lit(q, q2, q3, U); turn[tk] = lt
                        if lt == FALSE:
                            continue
                        cl = [-R[key]]
                        if l2 != TRUE:
                            cl.append(-l2)
                        if lt != TRUE:
                            cl.append(-lt)
                        if lv + 1 < Lc:
                            cl.append(rv((lv + 1, q2, q3)))
                        cls.append(cl)
        self.nv = nv
        return cls


def pair_cuts(P, units, tol=1e-9, B=40):
    """All sign combinations of two non-unit forms that no ordered radii realise (exact criterion up to tolerance,
    conservative: a cut is added only when infeasibility holds with margin tol).  With c_k = u_k - u_{k-1} >= 0
    (u_{-1} = 0), a.u = sum_k c_k S^a_k (suffix sums).  By Ville's theorem, {x.c > 0, y.c > 0, c >= 0} has no
    solution iff lambda x + mu y <= 0 componentwise for some lambda, mu >= 0 not both 0; the cases lambda = 0 or
    mu = 0 are the sign units, so it remains to test x + alpha y <= 0 for some alpha > 0, an interval condition.
    Returns binary clauses [-l_a, -l_b]."""
    t = P.t
    free = np.array([v for v in range(1, P.ntv + 1) if v not in units])
    if len(free) == 0:
        return []
    S = np.cumsum(P.A[free][:, ::-1], axis=1)[:, ::-1]       # suffix sums, shape (F, t)
    S = S / np.abs(S).max(axis=1, keepdims=True)
    F = len(free)
    out = []
    for sa in (1, -1):
        for sb in (1, -1):
            Y = sb * S[None, :, :]
            for i0 in range(0, F, B):
                X = sa * S[i0:i0 + B, None, :]
                with np.errstate(divide='ignore', invalid='ignore'):
                    R = -X / Y
                pos = Y > tol; neg = Y < -tol; zer = ~(pos | neg)
                U = np.where(pos, R, np.inf).min(axis=2)
                L = np.maximum(np.where(neg, R, -np.inf).max(axis=2), 0.0)
                zok = np.all(~zer | (X <= -tol) | ((np.abs(X) <= tol) & (np.abs(Y) <= tol)), axis=2)
                bad = zok & (L + tol < U) & (U > tol)
                ii, jj = np.nonzero(bad)
                for i, j in zip(ii, jj):
                    a = int(free[i0 + i]); b = int(free[j])
                    if a < b or (a == b and sa != sb):
                        out.append([-sa * a, -sb * b])
    return out


def chain_phases(cls, ntv, nv, sg):
    """least fixpoint of the chain variables for the triple signs sg (sg[v-1] = +-1), as decision phases.  Chain
    clauses are Horn: (body) -> head with the head the unique positive chain literal; they are generated level by
    level, so one pass in order computes the least fixpoint."""
    val = np.zeros(nv + 1, dtype=np.int8)
    val[1:ntv + 1] = (np.asarray(sg) > 0)
    for c in cls:
        head = 0
        ok = True
        for x in c:
            if x > ntv:
                head = x
            else:
                y = -x
                if y > 0:
                    if not val[y]:
                        ok = False; break
                else:
                    if val[-y]:
                        ok = False; break
        if ok and head:
            val[head] = 1
    return [v if val[v] else -v for v in range(ntv + 1, nv + 1)]


def l1_point(A, signs, t, eps=1e-4):
    """radii (u, ordered, u_0 = 1) minimising the total hinge violation sum max(0, eps - s_v a_v.u/|a_v|)"""
    from scipy.sparse import csr_matrix, hstack, vstack, identity
    rows = A[1:] * signs[:, None]
    rows = rows / np.linalg.norm(rows, axis=1)[:, None]
    N = len(rows)
    A1 = hstack([csr_matrix(-rows), -identity(N, format='csr')])
    ordr = np.zeros((t - 1, t))
    for i in range(t - 1):
        ordr[i, i] = 1; ordr[i, i + 1] = -1
    A2 = hstack([csr_matrix(ordr), csr_matrix((t - 1, N))])
    A_ub = vstack([A1, A2]).tocsr()
    b_ub = np.concatenate([-eps * np.ones(N), np.zeros(t - 1)])
    A_eq = hstack([csr_matrix(np.eye(1, t)), csr_matrix((1, N))])
    res = linprog(np.concatenate([np.zeros(t), np.ones(N)]), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * (t + N), method='highs')
    if res.status != 0:
        return None, None
    u = res.x[:t]
    return u, int((rows @ u <= 0).sum())


def lp_check(A, signs, t, vars_):
    rows = A[vars_] * signs[:, None]
    nrm = np.linalg.norm(rows, axis=1)
    rows = rows / nrm[:, None]
    nv = t + 1
    c = np.zeros(nv); c[-1] = -1.0
    # radius order: u_{i+1} - u_i >= 0 (strictness via the margin of the sign rows; order rows unscaled)
    ordr = np.zeros((t - 1, nv))
    for i in range(t - 1):
        ordr[i, i] = 1.0; ordr[i, i + 1] = -1.0
    A_ub = np.vstack([np.hstack([-rows, np.ones((len(rows), 1))]), ordr])
    b_ub = np.zeros(len(rows) + t - 1)
    A_eq = np.zeros((1, nv)); A_eq[0, 0] = 1.0
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=np.array([1.0]),
                  bounds=[(0, None)] * t + [(None, 1.0)], method='highs')
    if res.status != 0:
        return None, None, None
    return -res.fun, res.x[:t], res.ineqlin.marginals[:len(rows)]


def run(m, t, centre, th, lr_hint, tmax, log, out, tag, K_free=None, extra_free=(), conf=None):
    """phase-fixed CEGAR; K_free = None: all signs free; else trust region (fix the hint's signs except the K_free
    smallest normalised |forms| and extra_free vars)."""
    t0 = time.time()
    P = PF(m, t, centre, th)
    units, imps = P.units()
    u_h = np.exp(-np.array(lr_hint))
    val = P.A[1:] @ u_h / np.linalg.norm(P.A[1:], axis=1)
    sg = np.where(val > 0, 1, -1)
    bad = sum(1 for v, l in units.items() if l != v * sg[v - 1])
    fixed = {}
    if K_free is not None:
        order = np.argsort(np.abs(val))
        free = set(int(x) + 1 for x in order[:K_free]) | set(extra_free)
        for v in range(1, P.ntv + 1):
            if v not in free and v not in units:
                fixed[v] = int(v * sg[v - 1])
    cls = P.chain_clauses(units, fixed)
    pcs = pair_cuts(P, units) if PAIRS else []
    S = Solver(name='cadical195')
    for c in pcs:
        S.add_clause(c)
    for v, l in units.items():
        S.add_clause([l])
    for v, l in fixed.items():
        S.add_clause([l])
    for c in imps:
        S.add_clause(c)
    for c in cls:
        if not c:
            log('  %s: empty chain clause (forced convex K-gon) after %.1f s' % (tag, time.time() - t0))
            S.delete(); return 'UNSAT0', 0, -9, None
        S.add_clause(c)
    log('  %s: units %d (conflicts with hint %d) fixed %d imps %d pair cuts %d chain clauses %d vars %d, built in %.1f s' % (
        tag, len(units), bad, len(fixed), len(imps), len(pcs), len(cls), P.nv, time.time() - t0))
    chainph = chain_phases(cls, P.ntv, P.nv, sg)   # chain variables: least fixpoint of the hint's signs
    S.set_phases([int(v * sg[v - 1]) for v in range(1, P.ntv + 1)] + chainph)
    allv = np.arange(1, P.ntv + 1)
    it = 0; best = -9; t1 = time.time()
    try:
        while time.time() - t1 < tmax:
            it += 1
            if conf:
                S.conf_budget(conf); ok = S.solve_limited()
                if ok is None:
                    return 'BUDGET', it, best, None
            else:
                ok = S.solve()
            if not ok:
                return 'UNSAT', it, best, None
            mdl = S.get_model()
            s = np.array([1.0 if mdl[v - 1] > 0 else -1.0 for v in allv])
            delta, uu, du = lp_check(P.A, s, t, allv)
            if delta is None:
                return 'LPFAIL', it, best, None
            if delta > 1e-10:
                lr = -np.log(uu / uu[0])
                c, _ = countm(m, lr, th, centre)
                fn = os.path.join(out, 'cand_%s_%d.json' % (tag, it))
                json.dump(dict(m=m, centre=int(centre), lr=lr.tolist(), th=list(map(float, th)), delta=delta,
                               counts={str(k): int(c[k]) for k in range(3, 9)}, note='pfenc LP-CEGAR candidate'),
                          open(fn, 'w'), indent=1)
                log('  CAND delta %.3e float N8 %d N7 %d -> %s' % (delta, c[8], c[7], fn))
                return 'CAND', it, delta, fn
            # the LP point is a real configuration (its own signs may differ from the model): test it directly
            lrp = -np.log(np.maximum(uu, 1e-300) / uu[0])
            if np.all(np.isfinite(lrp)) and np.all(np.diff(lrp) <= 1e-12) and uu.min() > 0:
                cpt, _ = countm(m, lrp, th, centre)
                LPN8['min'] = min(LPN8.get('min', 1 << 62), cpt[8])
                if cpt[8] == 0:
                    fn = os.path.join(out, 'cand_%s_%d_lppoint.json' % (tag, it))
                    json.dump(dict(m=m, centre=int(centre), lr=lrp.tolist(), th=list(map(float, th)), delta=float(delta),
                                   counts={str(k): int(cpt[k]) for k in range(3, 9)},
                                   note='pfenc LP point (margin %.3e) with float N8 = 0' % delta), open(fn, 'w'), indent=1)
                    log('  CAND (LP point) delta %.3e float N8 0 N7 %d -> %s' % (delta, cpt[7], fn))
                    return 'CAND', it, delta, fn
            if delta > best and delta > -0.05:
                ul, nviol = l1_point(P.A, s, t)
                if ul is not None and ul.min() > 0:
                    lrl = -np.log(ul / ul[0])
                    cl1, _ = countm(m, lrl, th, centre)
                    LPN8['l1'] = min(LPN8.get('l1', 1 << 62), cl1[8])
                    log('  %s: it %d new best delta %.3e; L1 point: %d violated rows, float N8 %d' % (tag, it, delta, nviol, cl1[8]))
                    if cl1[8] == 0:
                        fn = os.path.join(out, 'cand_%s_%d_l1point.json' % (tag, it))
                        json.dump(dict(m=m, centre=int(centre), lr=lrl.tolist(), th=list(map(float, th)), delta=float(delta),
                                       counts={str(k): int(cl1[k]) for k in range(3, 9)},
                                       note='pfenc L1 point with float N8 = 0'), open(fn, 'w'), indent=1)
                        log('  CAND (L1 point) -> %s' % fn)
                        return 'CAND', it, delta, fn
            if delta > best:
                LAST_BEST['lr'] = lrp.tolist()
                LAST_BEST['delta'] = float(delta)
                LAST_BEST['signs'] = s.astype(int).tolist()
                LAST_BEST['dirty'] = True
            best = max(best, delta)
            if it % 100 == 0 and LAST_BEST.get('dirty'):
                LAST_BEST['dirty'] = False
                json.dump(dict(m=m, centre=int(centre), th=list(map(float, th)), lr=LAST_BEST['lr'], delta=LAST_BEST['delta'],
                               signs=LAST_BEST['signs'], note='best SAT model so far (orbit-variable signs) and its LP point'),
                          open(os.path.join(out, 'bestmodel_%s.json' % tag), 'w'))
            if it % 500 == 0:
                log('  %s: it %d delta %.3e best %.3e min N8 at LP points %s %.0f s' % (tag, it, delta, best, LPN8.get('min'), time.time() - t1))
            sup = [k for k in range(len(allv)) if abs(du[k]) > 1e-9]
            if not sup:
                return 'NODUAL', it, best, None
            S.add_clause([int(-s[k] * allv[k]) for k in sup])
            su = P.A[1:] @ np.maximum(uu, 0)
            sgu = np.where(su > 0, 1, -1)
            S.set_phases([int(v * sgu[v - 1]) for v in allv] + chain_phases(cls, P.ntv, P.nv, sgu))
        return 'TIMEOUT', it, best, None
    finally:
        S.delete()


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='pf')
    ap.add_argument('--tmax', type=float, default=60)
    ap.add_argument('--K', default='all', help='comma list of trust-region sizes, or all')
    ap.add_argument('--sigma', type=float, default=0.0)
    ap.add_argument('--npert', type=int, default=0)
    ap.add_argument('--keep0', type=int, default=1)
    ap.add_argument('--players', default='')
    ap.add_argument('--scan', default='')
    ap.add_argument('--centre', type=int, default=-1)
    ap.add_argument('--pairs', type=int, default=0, help='1: add all infeasible two-form sign combinations (pair cuts)')
    ap.add_argument('--recenter', type=int, default=0, help='rounds: re-run the trust region around the best LP point (radii) of the previous round')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('cfgs', nargs='+')
    a = ap.parse_args()
    global PAIRS
    PAIRS = bool(a.pairs)
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'log_%s.txt' % a.tag), 'a')
    tsv = open(os.path.join(a.out, 'res_%s.tsv' % a.tag), 'a')

    def log(s):
        logf.write(time.strftime('%H:%M:%S ') + s + '\n'); logf.flush()
    rng = np.random.default_rng(a.seed)
    U = 2 * math.pi / a.m
    Ks = [None] if a.K == 'all' else [int(k) for k in a.K.split(',')]
    for pf in a.cfgs:
        d = json.load(open(pf))
        lr = np.array(d['lr'], float); th = np.array(d['th'], float)
        centre = int(d.get('centre', 0)) if a.centre < 0 else a.centre
        o = np.argsort(-lr); lr = lr[o] - lr[o][0]; th = th[o]
        t = len(lr)
        base = os.path.basename(pf).replace('.json', '')
        jobs = []
        for spec in (a.scan.split(';') if a.scan else []):
            li, lo, hi, st = spec.split(':'); li = int(li)
            for ph in np.arange(float(lo), float(hi), float(st)):
                th2 = th.copy(); th2[li] = th[0] + math.radians(ph)
                jobs.append((base + '_L%d_%.4f' % (li, ph), th2))
        if a.keep0:
            jobs.append((base + '_p0', th.copy()))
        for k in range(a.npert):
            mask = np.ones(t)
            if a.players:
                mask = np.zeros(t); mask[[int(x) for x in a.players.split(',')]] = 1
            sig = a.sigma if a.sigma > 0 else 10 ** rng.uniform(-2, 0.5)
            jobs.append((base + '_s%.3g_%d' % (sig, k + 1), th + np.radians(rng.normal(0, sig, t)) * mask))
        for tag, th2 in jobs:
            if a.stop_at and time.time() > a.stop_at:
                break
            th2 = (th2 - th2[0]) % U
            c, _ = countm(a.m, lr, th2, centre)
            for K in Ks:
                extra = ()
                if K is not None:
                    # free also every orbit variable of a triple inside a convex octagon of the hint configuration
                    xx, yy = pointsm(a.m, lr, th2, centre)
                    tot, octs = enum_k(xx, yy, 8, 5000)
                    Pfull = PF(a.m, t, centre, th2)
                    ev = set()
                    nn = a.m * t
                    for Q in octs:
                        Q = [int(q) for q in Q if int(q) < nn]
                        for i1, i2, i3 in itertools.combinations(Q, 3):
                            T_, s1 = Pfull.sortpar((i1, i2, i3)); C_, s2 = Pfull.canon[T_]
                            ev.add(Pfull.tvar[C_])
                    extra = tuple(ev)
                    del Pfull
                t0 = time.time()
                hint = lr
                for rc in range(a.recenter + 1):
                    LAST_BEST.clear()
                    try:
                        r = run(a.m, t, centre, th2, hint, a.tmax, log, a.out, '%s_K%s_rc%d' % (tag, K, rc), K_free=K, extra_free=extra)
                    except ValueError as e:
                        r = ('DEGEN', 0, 0, str(e))
                    if r[0] != 'TIMEOUT' or 'lr' not in LAST_BEST or rc == a.recenter:
                        break
                    # re-centre: hint radii = best LP point (its signs differ from an octagon-free model in few places)
                    hint = np.array(LAST_BEST['lr'])
                    if not np.all(np.isfinite(hint)) or np.any(np.diff(hint) > 1e-12):
                        break
                    cc, _ = countm(a.m, hint, th2, centre)
                    log('  recenter %d: best delta %.3e, LP point float N8 %d N7 %d' % (rc + 1, LAST_BEST['delta'], cc[8], cc[7]))
                    if K is not None:
                        xx, yy = pointsm(a.m, hint, th2, centre)
                        tot, octs = enum_k(xx, yy, 8, 5000)
                        Pfull = PF(a.m, t, centre, th2)
                        ev = set()
                        for Q in octs:
                            Q = [int(q) for q in Q if int(q) < a.m * t]
                            for i1, i2, i3 in itertools.combinations(Q, 3):
                                T_, s1 = Pfull.sortpar((i1, i2, i3)); C_, s2 = Pfull.canon[T_]
                                ev.add(Pfull.tvar[C_])
                        extra = tuple(ev)
                        del Pfull
                log('RESULT %s K %s N8(hint) %d -> %s it %d best %.3e (%.1f s)' % (tag, K, c[8], r[0], r[1], r[2], time.time() - t0))
                tsv.write('%s\t%s\t%d\t%s\t%d\t%.3e\t%.1f\t%s\n' % (tag, K, c[8], r[0], r[1], r[2], time.time() - t0, r[3] or ''))
                tsv.flush()
                if r[0] in ('TIMEOUT', 'BUDGET'):
                    json.dump(dict(m=a.m, centre=centre, lr=list(map(float, lr)), th=list(map(float, th2)),
                                   note='live phase vector (pfenc %s, best delta %.3e)' % (r[0], r[2])),
                              open(os.path.join(a.out, 'live_%s.json' % tag), 'w'), indent=1)
                if r[0] == 'CAND':
                    break
    log('done')


if __name__ == '__main__':
    main()
