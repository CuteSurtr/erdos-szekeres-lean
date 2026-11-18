"""Lazy monolithic engine (memory-light; written after the 9 GB memory rule).
CNF = sub-CNF of the monolithic CNF of mono66.py (all states of W as potential owners, selector guards):
  eager : every pair- and triple-level clause of mono66.generate (state-dependent clauses, threshold monotonicity,
          transitivity, growth with ceilings, C_3/U_3, CE/UE and "not CE or not UE")
  lazy  : the quadruple-level clauses (8 signotope clauses and 4 chain-step clauses per quadruple and chronological
          order, exactly as mono66.generate writes them) are added only for (quadruple, order) pairs that a model
          violated ("activated").
  tail  : fixed states occupied, optional known rows over the selectors (hints), and a totalizer for the number of
          holes, queried by an assumption "at most L holes".
Loop: solve; if SAT, read the occupied owners, their x-order, orientations and chain atoms from the model, activate
every violated (quadruple, order) (numpy), repeat.  UNSAT under "at most L holes" => the sub-CNF, hence mono66's CNF,
has no model with at most L holes => every (6,6,8)-set has at least L+1 holes (given the soundness of mono66's
families, README).  A SAT answer with no violated quadruple is a model of the complete monolithic CNF: a selection
with at most L holes that no monotone coupled row can refute.
The run is discovery; a claim needs CaDiCaL 2.1.3 LRAT + cake_lpr on the written sub-CNF (lazymono_cert.py).
usage: lazymono.py <state.json out> <L start> <L stop> [rows.json|none] [seconds] [W.json]"""
import itertools, json, os, sys, time
import numpy as np
from pysat.solvers import Solver
from pysat.card import ITotalizer
import etv_common as ec, coupled5
from coupled5 import BAD4, MAXK
N = ec.N

class LazyMono:
    def __init__(self, W=None, emit=None):
        self.W = W = list(range(N)) if W is None else list(W); n = self.n = len(W)
        cnf = self.cnf = coupled5.CNF(W, static=False)
        top = cnf.nv
        self.sel = sel = [top + 1 + i for i in range(n)]; top += n
        self.nsel = nsel = [-x for x in sel]
        self.can = can = [[bool(ec.DREF[W[u]][W[v]]) for v in range(n)] for u in range(n)]
        self.eager = eager = []
        add = eager.append if emit is None else emit
        for c, t in zip(cnf.clauses, cnf.tags):
            add(list(c) + [nsel[o] for o in (t[1:4] if t[0] == 'positive' else t[1:3])])
        self.bef = bef = np.zeros((n, n), np.int64)
        for i in range(n):
            for j in range(n):
                if i != j: bef[i, j] = cnf.before(i, j)
        ge = cnf.ge
        self.ori = ori = np.zeros((n, n, n), np.int64)
        for a, b, c in itertools.permutations(range(n), 3): ori[a, b, c] = cnf.orient((a, b, c))
        for i, j in itertools.combinations(range(n), 2):
            for typ in ('cap', 'cup'):
                for k in range(2, MAXK[typ]): add([-ge(typ, i, j, k + 1), ge(typ, i, j, k), nsel[i], nsel[j]])
        self.C = C = np.zeros((6, n, n, n), np.int64); self.U = U = np.zeros((6, n, n, n), np.int64)
        for a, b, c in itertools.permutations(range(n), 3):
            if not (can[a][b] and can[b][c]): continue
            g3 = [nsel[a], nsel[b], nsel[c]]
            ab, bc = int(bef[a, b]), int(bef[b, c])
            add([-ab, -bc, int(bef[a, c])] + g3)
            if not can[a][c]: continue
            o = int(ori[a, b, c])
            for typ, color in (('cap', False), ('cup', True)):
                gate = [-ab, -bc, -o if color else o]
                for k in range(1, MAXK[typ] + 1):
                    x = ge(typ, a, b, k); y = ge(typ, b, c, k + 1)
                    if x is False or y is True: continue
                    add(gate + ([] if x is True else [-x]) + ([] if y is False else [y]) + g3)
            for k in (3, 4, 5):
                top += 1; C[k, a, b, c] = top; top += 1; U[k, a, b, c] = top
            add([-ab, -bc, o, int(C[3, a, b, c])] + g3)
            add([-ab, -bc, -o, int(U[3, a, b, c])] + g3)
        CE = {}; UE = {}
        for p, u, q in itertools.permutations(range(n), 3):
            v = int(C[5, p, u, q])
            if v:
                if (p, q) not in CE:
                    top += 1; CE[(p, q)] = top; top += 1; UE[(p, q)] = top
                    add([-CE[(p, q)], -UE[(p, q)], nsel[p], nsel[q]])
                add([-v, CE[(p, q)], nsel[p], nsel[u], nsel[q]]); add([-int(U[5, p, u, q]), UE[(p, q)], nsel[p], nsel[u], nsel[q]])
        self.top = top; self.activated = set()

    def quad_clauses(self, a, b, c, d):
        """The 12 clauses of mono66.generate for the chronological order a<b<c<d (guards: the four selectors)."""
        bef, ori, C, U, nsel = self.bef, self.ori, self.C, self.U, self.nsel
        g = [nsel[a], nsel[b], nsel[c], nsel[d]]
        order = [-int(bef[a, b]), -int(bef[b, c]), -int(bef[c, d])]
        tr = (int(ori[a, b, c]), int(ori[a, b, d]), int(ori[a, c, d]), int(ori[b, c, d]))
        out = [order + [-t if bit else t for t, bit in zip(tr, bits)] + g for bits in BAD4]
        o = tr[3]
        for k in (3, 4):
            out.append([-int(C[k, a, b, c]), -int(bef[c, d]), o, int(C[k + 1, a, c, d])] + g)
            out.append([-int(U[k, a, b, c]), -int(bef[c, d]), -o, int(U[k + 1, a, c, d])] + g)
        return out

    def violated(self, model):
        """(a,b,c,d) chronological quadruples of occupied owners whose clauses the model violates."""
        val = np.zeros(self.top + 2, bool); m = np.array(model[:self.top], np.int64); val[1:len(m) + 1] = m > 0
        lv = lambda L: np.where(L > 0, val[np.abs(L)], ~val[np.abs(L)])
        occ = np.array([i for i in range(self.n) if val[self.sel[i]]])
        B = lv(self.bef[np.ix_(occ, occ)]); np.fill_diagonal(B, False)
        rank = B.sum(axis=0)                                  # number of occupied owners before each owner
        order = occ[np.argsort(rank, kind='stable')]
        k = len(order)
        Q = np.array(list(itertools.combinations(range(k), 4)), np.int64)
        a, b, c, d = order[Q[:, 0]], order[Q[:, 1]], order[Q[:, 2]], order[Q[:, 3]]
        s0, s1, s2, s3 = lv(self.ori[a, b, c]), lv(self.ori[a, b, d]), lv(self.ori[a, c, d]), lv(self.ori[b, c, d])
        bad = ((s0 != s1).astype(np.int8) + (s1 != s2) + (s2 != s3)) >= 2
        for kk in (3, 4):
            bad |= val[self.C[kk, a, b, c]] & (self.C[kk, a, b, c] > 0) & ~s3 & ~val[self.C[kk + 1, a, c, d]]
            bad |= val[self.U[kk, a, b, c]] & (self.U[kk, a, b, c] > 0) & s3 & ~val[self.U[kk + 1, a, c, d]]
        idx = np.nonzero(bad)[0]
        return [(int(a[i]), int(b[i]), int(c[i]), int(d[i])) for i in idx], [self.W[i] for i in range(self.n) if not val[self.sel[i]]], order

if __name__ == '__main__':
    out = sys.argv[1]; L = int(sys.argv[2]); Lstop = int(sys.argv[3])
    rowsfile = sys.argv[4] if len(sys.argv) > 4 else 'none'
    secs = float(sys.argv[5]) if len(sys.argv) > 5 else 3000
    W = sorted(json.load(open(sys.argv[6]))) if len(sys.argv) > 6 else list(range(N))
    CAPQ = int(os.environ.get('CAPQ', '30000')); MAXQ = int(os.environ.get('MAXQ', '900000'))
    t0 = time.time()
    s = Solver(name='cadical195'); ncl = [0]
    def emit(c): s.add_clause(c); ncl[0] += 1
    E = LazyMono(W, emit=emit); idx = {st: i for i, st in enumerate(W)}
    for st in ec.FIXED_OCC:
        if st in idx: emit([E.sel[idx[st]]])
    CUBE = [(int(x.split(':')[0]), int(x.split(':')[1])) for x in os.environ.get('CUBE', '').split(',') if x]
    for st_, bit in CUBE: emit([E.sel[idx[st_]] if bit else E.nsel[idx[st_]]])       # cube: state occupied (1) / hole (0)
    nrows = 0
    if rowsfile != 'none':
        for supp, dd in json.load(open(rowsfile)):
            if dd == 1 and all(x in idx for x in supp): emit([E.nsel[idx[x]] for x in supp]); nrows += 1
    tot = ITotalizer(lits=[E.nsel[i] for i in range(E.n) if W[i] not in ec.FIXED_OCC], ubound=Lstop + 2, top_id=E.top)
    for c in tot.cnf.clauses: emit(c)
    print(json.dumps({'event': 'built', 'n': E.n, 'eager_clauses': ncl[0], 'rows': nrows, 'secs': round(time.time() - t0, 1)}), flush=True)
    it = 0; rng = np.random.default_rng(1); tl = time.time(); itl = 0
    def save(status):
        json.dump({'W': W, 'L': L, 'status': status, 'rows_file': rowsfile, 'cube': CUBE, 'activated': sorted(E.activated), 'iterations': it,
                   'seconds': round(time.time() - t0, 1)}, open(out + '.tmp', 'w')); os.replace(out + '.tmp', out)
    while time.time() - t0 < secs and L <= Lstop:
        it += 1; itl += 1
        r = s.solve(assumptions=[-tot.rhs[L]])
        if not r:
            print(json.dumps({'event': 'UNSAT', 'budget': L, 'holes_at_least': L + 1, 'iterations_this_level': itl, 'iterations': it,
                              'activated': len(E.activated), 'clauses': ncl[0], 'level_secs': round(time.time() - tl, 1), 'secs': round(time.time() - t0, 1)}), flush=True)
            save(f'UNSAT at budget {L}')
            os.replace(out, out.replace('.json', f'_L{L}.json'))
            L += 1; tl = time.time(); itl = 0; continue
        viol, holes, order = E.violated(s.get_model())
        new = [q for q in viol if q not in E.activated]
        if not new:
            print(json.dumps({'event': 'SAT_MODEL', 'budget': L, 'holes': holes, 'n_holes': len(holes), 'hole_states': [''.join(map(str, ec.STATES[h])) for h in holes],
                              'x_order': [W[int(i)] for i in order], 'iterations': it, 'activated': len(E.activated), 'secs': round(time.time() - t0, 1)}), flush=True)
            save(f'SAT at budget {L}'); break
        if len(new) > CAPQ:
            sel_idx = rng.choice(len(new), CAPQ, replace=False); new = [new[i] for i in sel_idx]
        for q in new:
            E.activated.add(q)
            for c in E.quad_clauses(*q): emit(c)
        if it % 10 == 0 or it <= 5:
            print(json.dumps({'event': 'iter', 'it': it, 'budget': L, 'violated': len(viol), 'added': len(new), 'activated': len(E.activated), 'clauses': ncl[0],
                              'holes': len(holes), 'secs': round(time.time() - t0, 1)}), flush=True)
        if len(E.activated) > MAXQ:
            print(json.dumps({'event': 'STOP_MAXQ', 'activated': len(E.activated)}), flush=True); save('stopped: MAXQ'); break
    else:
        save('time limit' if L <= Lstop else 'done')
    print(json.dumps({'event': 'end', 'budget': L, 'iterations': it, 'activated': len(E.activated), 'clauses': ncl[0], 'secs': round(time.time() - t0, 1)}), flush=True)
