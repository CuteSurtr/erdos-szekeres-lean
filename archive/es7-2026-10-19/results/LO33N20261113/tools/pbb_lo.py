"""Slice variant of pbb_strong (LO33, 13 Nov 2026): same exact search and the SAME leaf certificates
(weighted leaves with a positive exact integer margin against the row system base + extra), but a different
BRANCHING SCORE.  For a slice the extra rows contain  h(F) >= a  and  h(Lo) >= b  with a + b = budget, so the
standard LP (min sum h) is stuck at exactly `budget` on every live node and pbb_strong's strong-branching gains
are all zero.  Here the branching variable is chosen with the score LP
        phi = min h(Lo)  subject to all coupled/Lean rows, node bounds, h(F) <= a,
whose value rises towards b + (something) as the node gets closer to infeasibility:
   node dead  <=>  score LP infeasible or phi > b  <=>  standard LP infeasible or > budget
(covering rows are monotone, so a point with h(F) <= a, h(Lo) <= b can be raised to equality unless a row
is already unsatisfiable, which the forced-row scan catches).
The branching rule has NO bearing on soundness: every leaf is still produced by pbb_strong's own code from the
standard LP dual and kept only if its exact integer margin is positive, and the assembled tree is replayed by
scripts/omission_tree.check_tree.  If a leaf cannot be extracted (numerics) the node is simply branched."""
import gzip, json, math, os, sys, time
from pathlib import Path
import numpy as np
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
sys.path.insert(0, os.path.join(REPO, 'experiments/omission-final313-2026-10-11/search'))
import pbb_strong as P
N = P.N; SRC = P.SRC
G = {}; STRONG = P.STRONG

class SliceSolver(P.Solver):
    def __init__(self, rows, budget, nbase):
        super().__init__(rows, budget)
        import highspy
        hs = highspy
        states = json.load(gzip.open(SRC))['states']
        Fset = [i for i in range(N) if states[i][0] >= 5]; Lset = [i for i in range(N) if states[i][0] <= 4]
        capF = [r for r in range(nbase, len(rows)) if sorted(rows[r][0]) == Fset and rows[r][1] > 1]
        capL = [r for r in range(nbase, len(rows)) if sorted(rows[r][0]) == Lset and rows[r][1] > 1]
        assert len(capF) == 1 and len(capL) == 1
        self.a, self.b = rows[capF[0]][1], rows[capL[0]][1]
        assert self.a + self.b == budget, 'pbb_lo is for slices only'
        skip = {capF[0], capL[0]}
        g = hs.Highs(); g.setOptionValue('output_flag', False); g.setOptionValue('threads', 1); g.setOptionValue('presolve', 'off')
        L = set(Lset)
        v = [g.addVariable(lb=0, ub=1, obj=(1.0 if i in L else 0.0)) for i in range(N)]
        g.addConstr(g.qsum(v[i] for i in Fset) <= self.a)
        for r, (s, d) in enumerate(rows):
            if r not in skip: g.addConstr(g.qsum(v[i] for i in s) >= d)
        self.g = g; self.score_lps = 0

    def score(self, lo, hi):
        hs, g = self.hs, self.g
        self.score_lps += 1
        g.changeColsBounds(N, self.idx, lo, hi); g.run(); st = g.getModelStatus()
        if st != hs.HighsModelStatus.kOptimal and st != hs.HighsModelStatus.kInfeasible:
            g.clearSolver(); g.run(); st = g.getModelStatus()
        if st == hs.HighsModelStatus.kOptimal:
            return g.getObjectiveValue(), np.array(g.getSolution().col_value)
        if st == hs.HighsModelStatus.kInfeasible:
            return math.inf, None
        return None, None            # unknown status: caller falls back to the standard rule

    def expand(self, missing, occupied):
        budget = self.budget
        if missing.bit_count() > budget:
            return 'leaf', {'type': 'over_budget'}
        free = ((1 << N) - 1) ^ missing ^ occupied
        force = None
        for r, mask in enumerate(self.masks):
            rem = self.demands[r] - (mask & missing).bit_count()
            avail = mask & free
            if rem > avail.bit_count():
                leaf = {'type': 'weighted', 'capacity': 0, 'weights': [[r, 1]]}
                assert P.margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0
                return 'leaf', leaf
            if rem and rem == avail.bit_count() and force is None:
                force = (avail & -avail).bit_length() - 1
        if force is not None:
            return 'branch', force
        lo = np.fromiter((float(missing >> i & 1) for i in range(N)), float, N)
        hi = np.fromiter((float(not (occupied >> i & 1)) for i in range(N)), float, N)
        obj, x = self.score(lo, hi)
        if obj is None or obj > self.b + 1e-7:
            # dead by the score LP (or unknown): let pbb_strong's own code produce the certified leaf or a branch
            return P.Solver.expand(self, missing, occupied)
        fr = [i for i in range(N) if free >> i & 1 and 1e-7 < x[i] < 1 - 1e-7]
        if not fr:
            holes = [i for i in range(N) if x[i] > 0.5]
            if len(holes) <= budget and 0 not in holes and all(len(set(holes) & set(s)) >= d for s, d in self.rows):
                return 'witness', holes
            return P.Solver.expand(self, missing, occupied)
        K = STRONG.get('k', 0) if (missing | occupied).bit_count() < STRONG.get('depth', 99) else STRONG.get('k_low', 0)
        cand = sorted(fr, key=lambda i: (abs(x[i] - 0.5), i))
        if not K:
            return 'branch', cand[0]
        best = None
        for c in cand[:K]:
            gains = []
            for bv in (0, 1):
                l2, h2 = lo.copy(), hi.copy(); l2[c] = bv; h2[c] = bv
                o2, _ = self.score(l2, h2)
                if o2 is None: o2 = obj
                gains.append(max(min(o2, self.b + 1) - obj, 1e-3))
            key = gains[0] * gains[1]
            if best is None or key > best[0]: best = (key, c)
        return 'branch', best[1]

def init(extra, budget):
    STRONG.update(k=int(os.environ.get('K_TOP', '40')), depth=int(os.environ.get('D_TOP', '12')), k_low=int(os.environ.get('K_LOW', '12')))
    nbase = len(json.load(gzip.open(SRC))['constraints'])
    s = SliceSolver(P.load(extra), budget, nbase)
    G['s'] = s; P.G['s'] = s          # pbb_strong.run_context reads P.G['s']

run_context = P.run_context
