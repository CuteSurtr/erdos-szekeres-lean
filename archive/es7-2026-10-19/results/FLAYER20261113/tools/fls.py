"""General first-layer signotope instances (abstract model; sound relaxation of real point sets).
Class FL(a,b): n points, no a-cap, no b-cup, no ((a-1)-cap,(b-1)-cup)-gon on common endpoints.
Extra: at least K points in E (ends of (b-1)-cups), or in A (ends of (a-1)-caps), or in E u A, or E n A.
usage: fls.py a b n what K [timeout]     what in {none,E,A,EuA,EnA}
"""
import sys, itertools, os, time
os.environ.setdefault('FL_TMP', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp'))
from pysat.card import CardEnc, EncType

class FL:
    def __init__(self, a, b, n, gon=True):
        self.a, self.b, self.n = a, b, n; self.nv = 0; self.cl = []
        self.o = {t: self.new() for t in itertools.combinations(range(n), 3)}
        for i, j, k, l in itertools.combinations(range(n), 4):
            x = [self.o[i, j, k], self.o[i, j, l], self.o[i, k, l], self.o[j, k, l]]
            for p, q, r in itertools.combinations(range(4), 3):
                self.cl.append([-x[p], x[q], -x[r]]); self.cl.append([x[p], -x[q], x[r]])
        self.E = {}
        self.end = {}
        for sgn, L in ((-1, a), (1, b)):       # chains of sign sgn must have < L points
            E = self.E[sgn] = {}
            for k in range(3, L):
                for u in range(n):
                    for v in range(u + 1, n):
                        e = E[k, u, v] = self.new(); ys = []
                        for t in range(u):
                            tri = sgn * self.o[t, u, v]
                            if k == 3: ys.append(tri)
                            else:
                                y = self.new(); ys.append(y); prev = E[k - 1, t, u]
                                self.cl += [[-y, tri], [-y, prev], [y, -tri, -prev]]
                        self.cl.append([-e] + ys)
                        for y in ys: self.cl.append([-y, e])
                        if k > 3: self.cl.append([-e, E[k - 1, u, v]])
            for t, u, v in itertools.combinations(range(n), 3):   # no L-chain
                if L == 3: self.cl.append([-(sgn * self.o[t, u, v])])
                else: self.cl.append([-(sgn * self.o[t, u, v]), -E[L - 1, t, u]])
            # end indicators: v ends a chain of L-1 points
            for v in range(n):
                w = self.end[sgn, v] = self.new()
                if L - 1 <= 1: self.cl.append([w]); continue
                if L - 1 == 2:
                    self.cl.append([w] if v >= 1 else [-w]); continue
                ys = [E[L - 1, u, v] for u in range(v)]
                self.cl.append([-w] + ys)
                for y in ys: self.cl.append([-y, w])
        if gon:
            B = {}
            for sgn, L in ((-1, a - 1), (1, b - 1)):   # chain of exactly L points from u to v (one-directional)
                F = {}
                for u in range(n):
                    for p in range(u + 1, n):
                        for q in range(p + 1, n):
                            for k in range(3, L + 1):
                                if k == 3: F[3, u, p, q] = sgn * self.o[u, p, q]
                                else:
                                    if p - u < k - 2: continue
                                    f = F[k, u, p, q] = self.new()
                                    for t in range(u + 1, p):
                                        if (k - 1, u, t, p) in F:
                                            self.cl.append([-F[k - 1, u, t, p], -(sgn * self.o[t, p, q]), f])
                for u in range(n):
                    for v in range(u + 1, n):
                        if L == 2: B[sgn, u, v] = None; continue
                        ws = [F[L, u, p, v] for p in range(u + 1, v) if (L, u, p, v) in F]
                        if not ws: continue
                        bb = B[sgn, u, v] = self.new()
                        for w in ws: self.cl.append([-w, bb])
            for u in range(n):
                for v in range(u + 1, n):
                    if (-1, u, v) in B and (1, u, v) in B:
                        c = [-x for x in (B[-1, u, v], B[1, u, v]) if x is not None]
                        self.cl.append(c)
    def new(self):
        self.nv += 1; return self.nv
    def atleast(self, lits, K):
        if K <= 0: return
        if K > len(lits): self.cl.append([]); return
        enc = CardEnc.atleast(lits=lits, bound=K, top_id=self.nv, encoding=EncType.seqcounter)
        self.nv = max(self.nv, enc.nv); self.cl += enc.clauses
    def require(self, what, K):
        n = self.n
        if what == 'E': self.atleast([self.end[1, v] for v in range(n)], K)
        elif what == 'A': self.atleast([self.end[-1, v] for v in range(n)], K)
        elif what in ('EuA', 'EnA'):
            zs = []
            for v in range(n):
                z = self.new(); zs.append(z); e, a_ = self.end[1, v], self.end[-1, v]
                if what == 'EuA': self.cl += [[-z, e, a_], [-e, z], [-a_, z]]
                else: self.cl += [[-z, e], [-z, a_], [z, -e, -a_]]
            self.atleast(zs, K)
    def dimacs(self):
        return 'p cnf %d %d\n' % (self.nv, len(self.cl)) + ''.join(' '.join(map(str, c)) + ' 0\n' for c in self.cl)

def check_model(a, b, n, o, model):
    """independent DP on the signotope: returns (maxcap, maxcup, has first-layer gon, |E|, |A|, |EuA|, |EnA|)"""
    sg = {t: (1 if v in model else -1) for t, v in o.items()}
    for i, j, k, l in itertools.combinations(range(n), 4):
        x = [sg[i, j, k], sg[i, j, l], sg[i, k, l], sg[j, k, l]]
        assert sum(1 for q in range(3) if x[q] != x[q + 1]) <= 1
    Em = {}; Ep = {}
    for v in range(n):
        for u in range(v):
            em = ep = 2
            for t in range(u):
                if sg[t, u, v] < 0: em = max(em, Em[t, u] + 1)
                else: ep = max(ep, Ep[t, u] + 1)
            Em[u, v] = em; Ep[u, v] = ep
    mc = max([1] + list(Em.values())); mu = max([1] + list(Ep.values()))
    cend = [max([1] + [Em[u, v] for u in range(v)]) for v in range(n)]
    uend = [max([1] + [Ep[u, v] for u in range(v)]) for v in range(n)]
    gon = False
    for s in range(n):
        Dc = {}; Du = {}
        for j in range(s + 1, n): Dc[s, j] = 2; Du[s, j] = 2
        for j in range(s + 1, n):
            for i in range(s + 1, j):
                bc = bu = 0
                for h in range(s, i):
                    if sg[h, i, j] < 0:
                        if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                    else:
                        if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                Dc[i, j] = bc; Du[i, j] = bu
        for t in range(s + 1, n):
            if max(Dc[i, t] for i in range(s, t)) >= a - 1 and max(Du[i, t] for i in range(s, t)) >= b - 1: gon = True
    Eset = {v for v in range(n) if uend[v] >= b - 1}; Aset = {v for v in range(n) if cend[v] >= a - 1}
    return mc, mu, gon, len(Eset), len(Aset), len(Eset | Aset), len(Eset & Aset)

def run(a, b, n, what='none', K=0, timeout=None, lrat=None, keep=None):
    import wit
    w = FL(a, b, n)
    if what != 'none': w.require(what, K)
    st, model = wit.solve_cnf(w.dimacs(), timeout, lrat=lrat, cnf_path=keep)
    info = None
    if st == 'SAT':
        info = check_model(a, b, n, w.o, model)
        mc, mu, gon, e, a_, eu, en = info
        assert mc < a and mu < b and not gon, info
        if what != 'none': assert {'E': e, 'A': a_, 'EuA': eu, 'EnA': en}[what] >= K, info
    return st, info, (w.nv, len(w.cl))

if __name__ == '__main__':
    a, b, n, what, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
    to = float(sys.argv[6]) if len(sys.argv) > 6 else None
    t0 = time.time(); st, info, size = run(a, b, n, what, K, to)
    print(f'FL({a},{b}) n={n} {what}>={K}: {st} {info} vars/clauses {size} {time.time()-t0:.1f}s', flush=True)
