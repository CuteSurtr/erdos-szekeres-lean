"""Fast slice engine (LO33, 13 Nov 2026).  Same tree format, same leaf certificates and the same branching
SCORE as pbb_lo.py (phi = min h(Lo) s.t. rows, h(F) <= a), but the LPs are solved with LAZY ROWS: a HiGHS model
holds only the rows that some LP optimum has violated so far; after each solve all rows are checked with one
matrix-vector product and violated ones are added (so the returned optimum is the optimum of the full LP).
The forced-row scan is vectorised.  Leaves: weights come from the dual of a (reduced) standard LP
min sum h; a reduced LP is a relaxation, so its dual is a valid dual for the full row system, and in any case a
leaf is kept only if pbb_strong.margin (exact integers, full row system) is positive.  Whenever the fast path
cannot produce a leaf, the node is handed to pbb_strong's own expand (full LP).
Soundness of a finished tree never depends on this file: the assembled tree is replayed by check_tree."""
import gzip, json, math, os, sys, time
import numpy as np
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
sys.path.insert(0, os.path.join(REPO, 'experiments/omission-final313-2026-10-11/search'))
import pbb_strong as P
N = P.N; SRC = P.SRC
G = {}; STRONG = P.STRONG
PC = int(os.environ.get('LO_PC', '0'))
ITLIM = int(os.environ.get('LO_ITLIM', '0'))
STAT = {'nodes': 0, 'score_lps': 0, 'fallback': 0, 'fast_leaf': 0, 'rounds': 0}

class LazyLP:
    def __init__(self, hs, A, d, sup, obj, allowed, fixed_le=None, seeds=()):
        self.hs, self.A, self.d, self.sup, self.allowed = hs, A, d, sup, allowed
        h = hs.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1); h.setOptionValue('presolve', 'off')
        for k_, v_ in json.loads(os.environ.get('HS_OPTS', '{}')).items(): h.setOptionValue(k_, v_)
        for i in range(N): h.addVariable(lb=0, ub=1, obj=float(obj[i]))
        self.nfixed = 0
        if fixed_le is not None:
            s, rhs = fixed_le
            h.addRow(-hs.kHighsInf, float(rhs), len(s), np.array(s, dtype=np.int32), np.ones(len(s)))
            self.nfixed = 1
        self.h = h; self.glob = []; self.inlp = np.zeros(len(d), bool); self.idx = np.arange(N, dtype=np.int32)
        self.add(seeds)
    def add(self, rs):
        hs = self.hs
        for r in rs:
            r = int(r); s = self.sup[r]
            self.h.addRow(float(self.d[r]), hs.kHighsInf, len(s), np.array(s, dtype=np.int32), np.ones(len(s)))
            self.glob.append(r); self.inlp[r] = True
    def run(self):
        hs, h = self.hs, self.h
        h.run(); st = h.getModelStatus()
        if st != hs.HighsModelStatus.kOptimal and st != hs.HighsModelStatus.kInfeasible:
            h.clearSolver(); h.run(); st = h.getModelStatus()
        return st
    def solve(self, lo, hi, stop_above=None):
        """Optimum of the FULL LP (lazy rows).  Returns (obj, x), (inf, None) or (None, None).
        With stop_above, returns as soon as a reduced LP already exceeds it (valid lower bound)."""
        hs, h = self.hs, self.h
        h.changeColsBounds(N, self.idx, lo, hi)
        while True:
            STAT['rounds'] += 1
            st = self.run()
            if st == hs.HighsModelStatus.kInfeasible: return math.inf, None
            if st != hs.HighsModelStatus.kOptimal: return None, None
            obj = h.getObjectiveValue()
            if stop_above is not None and obj > stop_above: return obj, None
            x = np.array(h.getSolution().col_value)
            slack = self.A @ x - self.d
            viol = np.nonzero((slack < -1e-7) & self.allowed & ~self.inlp)[0]
            if len(viol) == 0: return obj, x
            if len(viol) > 30: viol = viol[np.argsort(slack[viol])[:30]]
            self.add(viol)

def _bound(self, lo, hi, limit):
    """Cheap lower bound for strong branching: ONE run of the reduced LP with a simplex iteration limit
    (dual simplex from a dual-feasible basis, so the interrupted objective is a lower bound up to HiGHS's
    cost perturbation).  Only used to rank branching candidates."""
    hs, h = self.hs, self.h
    h.changeColsBounds(N, self.idx, lo, hi)
    h.setOptionValue('simplex_iteration_limit', int(limit))
    h.run(); st = h.getModelStatus()
    h.setOptionValue('simplex_iteration_limit', 2147483647)
    if st == hs.HighsModelStatus.kInfeasible: return math.inf
    if st == hs.HighsModelStatus.kOptimal or st == hs.HighsModelStatus.kIterationLimit: return h.getObjectiveValue()
    return None
LazyLP.bound = _bound

class FastSlice(P.Solver):
    def __init__(self, rows, budget, nbase):
        super().__init__(rows, budget)             # full production LP (fallback) + masks/demands
        hs = self.hs
        states = json.load(gzip.open(SRC))['states']
        Fset = [i for i in range(N) if states[i][0] >= 5]; Lset = [i for i in range(N) if states[i][0] <= 4]
        capF = [r for r in range(nbase, len(rows)) if sorted(rows[r][0]) == Fset and rows[r][1] > 1]
        capL = [r for r in range(nbase, len(rows)) if sorted(rows[r][0]) == Lset and rows[r][1] > 1]
        assert len(capF) == 1 and len(capL) == 1
        self.a, self.b = rows[capF[0]][1], rows[capL[0]][1]
        assert self.a + self.b == budget, 'slice engine: a + b must equal the budget'
        R = len(rows)
        A = np.zeros((R, N)); d = np.zeros(R)
        for r, (s, dd) in enumerate(rows):
            A[r, list(s)] = 1.0; d[r] = dd
        self.A, self.d = A, d
        sup = [list(s) for s, _ in rows]
        allowed_sc = np.ones(R, bool); allowed_sc[[capF[0], capL[0]]] = False
        objL = np.zeros(N); objL[Lset] = 1.0
        self._mk = lambda: (LazyLP(hs, A, d, sup, objL, allowed_sc, fixed_le=(Fset, self.a)),
                            LazyLP(hs, A, d, sup, np.ones(N), np.ones(R, bool), seeds=[capF[0], capL[0]]))
        self.sc, self.st = self._mk()
        self.pc = [np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)]

    def reset_lazy(self):
        """Forget the lazily collected rows (called at the start of every context, so the LPs stay small)."""
        self.sc, self.st = self._mk()

    def fast_leaf(self, missing, occupied, lo, hi):
        hs, L, budget = self.hs, self.st, self.budget
        h = L.h
        h.changeColsBounds(N, L.idx, lo, hi)
        for _ in range(60):
            st = L.run()
            if st == hs.HighsModelStatus.kInfeasible:
                _, exists, ray = h.getDualRay()
                if not exists: return None
                ray = list(ray)[L.nfixed:]
                for scale in (1000, 1000000, 1000000000):
                    leaf = {'type': 'weighted', 'capacity': 0,
                            'weights': [[L.glob[k], max(0, round(scale * y))] for k, y in enumerate(ray) if y > 0.5 / scale]}
                    if leaf['weights'] and P.margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0:
                        return leaf
                return None
            if st != hs.HighsModelStatus.kOptimal: return None
            obj = h.getObjectiveValue(); sol = h.getSolution()
            if obj > budget + 1e-8:
                dual = list(sol.row_dual)[L.nfixed:]
                for scale in (10, 32, 100, 256, 1000, 10000, 100000):
                    ws = [[L.glob[k], max(0, round(scale * y))] for k, y in enumerate(dual) if y > 0.5 / scale]
                    leaf = {'type': 'weighted', 'capacity': scale, 'weights': [[r, w] for r, w in ws if w]}
                    if P.margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0:
                        return leaf
                return None
            x = np.array(sol.col_value)
            slack = self.A @ x - self.d
            viol = np.nonzero((slack < -1e-7) & ~L.inlp)[0]
            if len(viol) == 0: return None
            if len(viol) > 30: viol = viol[np.argsort(slack[viol])[:30]]
            L.add(viol)
        return None

    def expand(self, missing, occupied):
        budget = self.budget
        STAT['nodes'] += 1
        if missing.bit_count() > budget:
            return 'leaf', {'type': 'over_budget'}
        miss = np.fromiter((float(missing >> i & 1) for i in range(N)), float, N)
        occ = np.fromiter((float(occupied >> i & 1) for i in range(N)), float, N)
        freev = 1.0 - miss - occ
        rem = self.d - self.A @ miss; avail = self.A @ freev
        bad = np.nonzero(rem > avail + 0.5)[0]
        if len(bad):
            leaf = {'type': 'weighted', 'capacity': 0, 'weights': [[int(bad[0]), 1]]}
            assert P.margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0
            return 'leaf', leaf
        forced = np.nonzero((rem > 0.5) & (np.abs(rem - avail) < 0.5))[0]
        if len(forced):
            av = self.masks[int(forced[0])] & (((1 << N) - 1) ^ missing ^ occupied)
            return 'branch', (av & -av).bit_length() - 1
        lo = miss; hi = 1.0 - occ
        obj, x = self.sc.solve(lo, hi)
        STAT['score_lps'] += 1
        if obj is None:
            STAT['fallback'] += 1
            return P.Solver.expand(self, missing, occupied)
        if obj > self.b + 1e-7:
            leaf = self.fast_leaf(missing, occupied, lo, hi)
            if leaf is not None:
                STAT['fast_leaf'] += 1
                return 'leaf', leaf
            STAT['fallback'] += 1
            return P.Solver.expand(self, missing, occupied)
        fr = [i for i in range(N) if freev[i] > 0.5 and 1e-7 < x[i] < 1 - 1e-7]
        if not fr:
            holes = [i for i in range(N) if x[i] > 0.5]
            if len(holes) <= budget and 0 not in holes and all(len(set(holes) & set(s)) >= d for s, d in self.rows):
                return 'witness', holes
            STAT['fallback'] += 1
            return P.Solver.expand(self, missing, occupied)
        K = STRONG.get('k', 0) if (missing | occupied).bit_count() < STRONG.get('depth', 99) else STRONG.get('k_low', 0)
        cand = sorted(fr, key=lambda i: (abs(x[i] - 0.5), i))
        if not K:
            return 'branch', cand[0]
        if PC:
            # pseudo-cost preselection: rank by estimated gain product; unobserved variables use the mean
            pc = self.pc
            m0 = pc[0].sum() / max(pc[1].sum(), 1.0); m1 = pc[2].sum() / max(pc[3].sum(), 1.0)
            def est(i):
                p0 = pc[0][i] / pc[1][i] if pc[1][i] else m0
                p1 = pc[2][i] / pc[3][i] if pc[3][i] else m1
                return max(p0 * x[i], 1e-3) * max(p1 * (1.0 - x[i]), 1e-3)
            ranked = sorted(fr, key=lambda i: (-est(i), i))
            new = [i for i in cand if pc[1][i] + pc[3][i] == 0][:max(1, K // 4)]
            cand = (new + [i for i in ranked if i not in new])
        best = None; capv = self.b + 1
        for c in cand[:K]:
            gains = []
            for bv in (0.0, 1.0):
                l2, h2 = lo.copy(), hi.copy(); l2[c] = bv; h2[c] = bv
                if ITLIM: o2 = self.sc.bound(l2, h2, ITLIM)
                else: o2, _ = self.sc.solve(l2, h2, stop_above=capv)
                STAT['score_lps'] += 1
                if o2 is None: o2 = obj
                gains.append(max(min(o2, capv) - obj, 1e-3))
            if PC:
                pc = self.pc
                pc[0][c] += gains[0] / max(x[c], 1e-6); pc[1][c] += 1
                pc[2][c] += gains[1] / max(1.0 - x[c], 1e-6); pc[3][c] += 1
            key = gains[0] * gains[1]
            if best is None or key > best[0]: best = (key, c)
        return 'branch', best[1]

def init(extra, budget):
    STRONG.update(k=int(os.environ.get('K_TOP', '40')), depth=int(os.environ.get('D_TOP', '12')), k_low=int(os.environ.get('K_LOW', '12')))
    nbase = len(json.load(gzip.open(SRC))['constraints'])
    s = FastSlice(P.load(extra), budget, nbase)
    G['s'] = s; P.G['s'] = s

def run_context(job):
    G['s'].reset_lazy()
    return P.run_context(job)
