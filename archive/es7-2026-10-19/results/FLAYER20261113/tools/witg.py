"""General witness-complete catalog model (FLAYER20261113).

Class FL(a,b): no a-cap, no b-cup, no ((a-1)-cap,(b-1)-cup)-gon on common endpoints (first layer).
States: Young diagrams in the (a-2) x (b-2) box, column heights f_1 >= ... >= f_{a-2}, f_x <= b-2
(column x = cap coordinate x; cell (x,y) in I(p) iff some u<p has an (x+1)-cap and a (y+1)-cup ending with (u,p)).

Abstract model as in wit.py (signotope + exact chain definitions + present-prefix flags), with
  st(p,s)  <=> p present and I(p) = s          occ(s) <=> some present point has state s.
A model with n points and the units/assumptions occ(s), s in T, is exactly: an FL(a,b)-signotope on at most
n points in which all states of T are occupied.  (No 'last present point is an owner' clause here: this
module is used for SAT answers, enumeration and small exact tables; wit.py is the (6,6;8) row certifier.)
"""
import os, sys, itertools, json, time
from pysat.solvers import Cadical153

def states_of(a, b):
    A, B = a - 2, b - 2
    out = [f for f in itertools.product(range(B + 1), repeat=A) if all(f[i] >= f[i + 1] for i in range(A - 1))]
    out.sort(key=lambda f: (sum(f), f))
    return out

def corners(f):
    A = len(f)
    return [(x + 1, f[x]) for x in range(A) if f[x] >= 1 and (x == A - 1 or f[x + 1] < f[x])]

def cocorners(f, B):
    return [(x + 1, f[x] + 1) for x in range(len(f)) if f[x] < B and (x == 0 or f[x - 1] > f[x])]

class WitG:
    def __init__(self, a, b, n, flags=True, gon=True):
        self.a, self.b, self.n = a, b, n; self.nv = 0; self.cl = []
        self.S = states_of(a, b); self.SI = {s: i for i, s in enumerate(self.S)}
        A, B = a - 2, b - 2
        o = self.o = {t: self.new() for t in itertools.combinations(range(n), 3)}
        self.pres = [self.new() for _ in range(n)]
        self.cl.append([self.pres[0]])
        for p in range(n - 1): self.cl.append([-self.pres[p + 1], self.pres[p]])
        if not flags:
            for p in range(n): self.cl.append([self.pres[p]])
        for i, j, k, l in itertools.combinations(range(n), 4):
            x = [o[i, j, k], o[i, j, l], o[i, k, l], o[j, k, l]]
            for p, q, r in itertools.combinations(range(4), 3):
                self.cl.append([-x[p], x[q], -x[r]]); self.cl.append([x[p], -x[q], x[r]])
        self.E = {}
        for sgn, L in ((-1, a), (1, b)):
            E = self.E[sgn] = {}
            for k in range(3, L):
                for u in range(n):
                    for v in range(u + 1, n):
                        e = E[k, u, v] = self.new(); ys = []
                        for t in range(u):
                            tri = sgn * o[t, u, v]
                            if k == 3: ys.append(tri)
                            else:
                                y = self.new(); ys.append(y); prev = E[k - 1, t, u]
                                self.cl += [[-y, tri], [-y, prev], [y, -tri, -prev]]
                        self.cl.append([-e] + ys)
                        for y in ys: self.cl.append([-y, e])
                        if k > 3: self.cl.append([-e, E[k - 1, u, v]])
            for t, u, v in itertools.combinations(range(n), 3):
                if L == 3: self.cl.append([-(sgn * o[t, u, v]), -self.pres[v]])
                else: self.cl.append([-(sgn * o[t, u, v]), -E[L - 1, t, u], -self.pres[v]])
        if gon:
            Bv = {}
            for sgn, L in ((-1, a - 1), (1, b - 1)):
                F = {}
                for u in range(n):
                    for p in range(u + 1, n):
                        for q in range(p + 1, n):
                            for k in range(3, L + 1):
                                if k == 3: F[3, u, p, q] = sgn * o[u, p, q]
                                else:
                                    if p - u < k - 2: continue
                                    f = F[k, u, p, q] = self.new()
                                    for t in range(u + 1, p):
                                        if (k - 1, u, t, p) in F:
                                            self.cl.append([-F[k - 1, u, t, p], -(sgn * o[t, p, q]), f])
                for u in range(n):
                    for v in range(u + 1, n):
                        ws = [F[L, u, p, v] for p in range(u + 1, v) if (L, u, p, v) in F]
                        if not ws: continue
                        bb = Bv[sgn, u, v] = self.new()
                        for w in ws: self.cl.append([-w, bb])
            for u in range(n):
                for v in range(u + 1, n):
                    if (-1, u, v) in Bv and (1, u, v) in Bv:
                        self.cl.append([-Bv[-1, u, v], -Bv[1, u, v], -self.pres[v]])
        # cells: constants 'T'/'F' or literals
        self.cellv = {}
        def lab(sgn, k, u, v):
            return 'T' if k <= 2 else self.E[sgn][k, u, v]
        for p in range(n):
            for x in range(1, A + 1):
                for y in range(1, B + 1):
                    if p == 0: self.cellv[p, x, y] = 'F'; continue
                    if (x, y) == (1, 1): self.cellv[p, x, y] = 'T'; continue
                    c = self.new(); ms = []
                    for u in range(p):
                        X = lab(-1, x + 1, u, p); Y = lab(1, y + 1, u, p)
                        if X == 'T': ms.append(Y)
                        elif Y == 'T': ms.append(X)
                        else:
                            m = self.new(); ms.append(m)
                            self.cl += [[-m, X], [-m, Y], [m, -X, -Y]]
                    self.cl.append([-c] + ms)
                    for m in ms: self.cl.append([-m, c])
                    self.cellv[p, x, y] = c
        # state indicators
        self.st = {}; self.occ = []
        for si, f in enumerate(self.S):
            cs = corners(f); ccs = cocorners(f, B); vs = []
            for p in range(n):
                req = [self.cellv[p, x, y] for x, y in cs]; forb = [self.cellv[p, x, y] for x, y in ccs]
                if 'F' in req or 'T' in forb: continue
                lits = [self.pres[p]] + [l for l in req if l != 'T'] + [-l for l in forb if l != 'F']
                w = self.st[p, si] = self.new(); vs.append(w)
                for l in lits: self.cl.append([-w, l])
                self.cl.append([w] + [-l for l in lits])
            oc = self.new(); self.occ.append(oc)
            self.cl.append([-oc] + vs)
            for w in vs: self.cl.append([-w, oc])
    def new(self):
        self.nv += 1; return self.nv
    def solver(self):
        return Cadical153(bootstrap_with=self.cl)
    def decode_states(self, model):
        """independent DP on the signotope given by the model; returns (m, list of state indices of present points)"""
        ms = set(x for x in model if x > 0); n = self.n; a, b = self.a, self.b
        m = max(p for p in range(n) if self.pres[p] in ms) + 1
        sg = {t: (1 if v in ms else -1) for t, v in self.o.items()}
        for i, j, k, l in itertools.combinations(range(m), 4):
            x = [sg[i, j, k], sg[i, j, l], sg[i, k, l], sg[j, k, l]]
            assert sum(1 for q in range(3) if x[q] != x[q + 1]) <= 1
        Em = {}; Ep = {}
        for v in range(m):
            for u in range(v):
                em = ep = 2
                for t in range(u):
                    if sg[t, u, v] < 0: em = max(em, Em[t, u] + 1)
                    else: ep = max(ep, Ep[t, u] + 1)
                Em[u, v] = em; Ep[u, v] = ep
        assert max([1] + list(Em.values())) < a and max([1] + list(Ep.values())) < b
        for s in range(m):
            Dc = {}; Du = {}
            for j in range(s + 1, m): Dc[s, j] = 2; Du[s, j] = 2
            for j in range(s + 1, m):
                for i in range(s + 1, j):
                    bc = bu = 0
                    for h in range(s, i):
                        if sg[h, i, j] < 0:
                            if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                        else:
                            if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                    Dc[i, j] = bc; Du[i, j] = bu
            for t in range(s + 1, m):
                assert not (max(Dc[i, t] for i in range(s, t)) >= a - 1 and max(Du[i, t] for i in range(s, t)) >= b - 1)
        out = []
        for v in range(m):
            f = [0] * (a - 2)
            for u in range(v):
                x = Em[u, v] - 1; y = Ep[u, v] - 1
                for c in range(x): f[c] = max(f[c], y)
            out.append(self.SI[tuple(f)])
        sig = ''.join('+' if sg[t] > 0 else '-' for t in itertools.combinations(range(m), 3))
        return m, out, sig

def enumerate_maximal(a, b, n, log=None, limit=100000):
    """All inclusion-maximal realizable occupancy sets of the abstract FL(a,b) model on at most n points."""
    w = WitG(a, b, n); so = w.solver(); NS = len(w.S); res = []; t0 = time.time()
    while len(res) < limit:
        if not so.solve(): break
        mod = so.get_model(); m, st, sig = w.decode_states(mod); M = set(st); pos = set(x for x in mod if x > 0)
        assert all((w.occ[s] in pos) == (s in M) for s in range(NS)), 'occ variables disagree with the independent DP'
        while True:   # grow to a maximal set
            act = w.new()
            so.add_clause([-act] + [w.occ[s] for s in range(NS) if s not in M])
            if so.solve(assumptions=[act] + [w.occ[s] for s in M]):
                mod = so.get_model(); m, st, sig = w.decode_states(mod); M2 = set(st); assert M < M2; M = M2
                pos = set(x for x in mod if x > 0)
                assert all((w.occ[s] in pos) == (s in M) for s in range(NS)), 'occ variables disagree with the independent DP'
                so.add_clause([-act])
            else:
                so.add_clause([-act]); break
        res.append((sorted(M), m, sig))
        so.add_clause([w.occ[s] for s in range(NS) if s not in M])
        if log and len(res) % 20 == 0: print(len(res), 'maximal sets', '%.0fs' % (time.time() - t0), file=log, flush=True)
    return w, res

if __name__ == '__main__':
    a, b, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    w, res = enumerate_maximal(a, b, n, log=sys.stdout)
    print('states', len(w.S), 'maximal realizable sets', len(res), 'sizes', sorted({len(M) for M, m, s in res}))
    json.dump({'a': a, 'b': b, 'n': n, 'states': w.S, 'maximal': [[M, m, sig] for M, m, sig in res]}, open(f'maximal_{a}_{b}_{n}.json', 'w'))
