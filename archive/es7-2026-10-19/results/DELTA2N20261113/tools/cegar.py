#!/usr/bin/env python
"""CEGAR for the exists-forall Delta-reduction statement on abstract signotopes.

D(a, n, m; weak):   every signotope S on m points with no a-cap and no convex n-gon has a subset Delta with
                    (i) no (a-1)-cap of S inside Delta, (ii) every convex (n-1)-gon of S meets Delta.
D(a, n, m; strong): additionally (iii) no convex (n-1)-gon of S inside Delta.

Loop: SAT-search S (signotope, no a-cap, no n-gon) in which every pooled Delta FAILS; compute a working Delta
for S exactly (explicit enumeration of all (a-1)-caps and all convex (n-1)-sets of S, then a small SAT);
none => S is an abstract counterexample; otherwise add Delta to the pool.  UNSAT of the outer problem =>
D(a, n, m) holds for all signotopes on m points (COMPUTED).

Usage: cegar.py a n m weak|strong [--tl SEC] [--out DIR] [--pick first|short] [--mirror]
"""
import sys, itertools, json, time, os, argparse, random
import numpy as np
from pysat.solvers import Cadical153, Glucose4

comb = itertools.combinations

class Model:
    def __init__(self, a, n, m, strong):
        assert 4 <= a <= n and n >= 5
        self.a, self.n, self.m, self.strong = a, n, m, strong
        self.tri = {t: i + 1 for i, t in enumerate(comb(range(m), 3))}
        self.ntri = len(self.tri)
        self.nv = self.ntri
        self.base = []      # signotope + forbidden a-caps + forbidden n-gons
        self.wit = []       # witness definitions (one-directional)
        tri = self.tri
        # --- signotope axioms: on every 4-tuple the sign sequence (ijk, ijl, ikl, jkl) changes sign at most once
        for i, j, k, l in comb(range(m), 4):
            s = [tri[i, j, k], tri[i, j, l], tri[i, k, l], tri[j, k, l]]
            for p, q, r in comb(range(4), 3):
                self.base.append([-s[p], s[q], -s[r]]); self.base.append([s[p], -s[q], s[r]])
        # --- no a-cap (variable true = cup): some consecutive triple is a cup
        for K in comb(range(m), a):
            self.base.append([tri[K[i], K[i + 1], K[i + 2]] for i in range(a - 2)])
        # --- no convex n-gon: for every n-subset and every split of its interior points into a cap part A
        #     (|A| <= a-3, so that the cap has at most a-1 points) and a cup part B: not (cap and cup)
        for G in comb(range(m), n):
            inner = G[1:-1]
            for r in range(0, a - 2):
                for A in comb(inner, r):
                    B = [g for g in inner if g not in A]
                    c = (G[0],) + A + (G[-1],); d = [G[0]] + B + [G[-1]]
                    self.base.append([tri[c[i], c[i + 1], c[i + 2]] for i in range(len(c) - 2)] +
                                     [-tri[d[i], d[i + 1], d[i + 2]] for i in range(len(d) - 2)])
        # --- witnesses
        # Y[K], K an (a-1)-subset: Y -> K is a cap (all consecutive triples caps)
        self.Y = {}
        if a - 1 == 3:
            for K in comb(range(m), 3): self.Y[K] = -tri[K]
        else:
            for K in comb(range(m), a - 1):
                self.nv += 1; self.Y[K] = self.nv
                for i in range(a - 3): self.wit.append([-self.nv, -tri[K[i], K[i + 1], K[i + 2]]])
        # Q4[Q], Q a 4-subset: Q4 -> Q in convex position  (sign(abc)=sign(abd) and sign(acd)=sign(bcd))
        self.Q4 = {}
        for Q in comb(range(m), 4):
            self.nv += 1; v = self.nv; self.Q4[Q] = v
            x, y, z, w = Q
            t1, t2, t3, t4 = tri[x, y, z], tri[x, y, w], tri[x, z, w], tri[y, z, w]
            self.wit += [[-v, -t1, t2], [-v, t1, -t2], [-v, -t3, t4], [-v, t3, -t4]]
        # Z[G], G an (n-1)-subset: Z -> every 4-subset of G is in convex position (<=> G convex in a signotope)
        self.Z = {}
        if n - 1 == 4: self.Z = self.Q4
        else:
            for G in comb(range(m), n - 1):
                self.nv += 1; v = self.nv; self.Z[G] = v
                for Q in comb(G, 4): self.wit.append([-v, self.Q4[Q]])
        # --- numpy tables for exact evaluation of a signotope
        Qs = list(comb(range(m), 4)); qid = {Q: i for i, Q in enumerate(Qs)}
        self.q_t = np.array([[tri[x, y, z] - 1, tri[x, y, w] - 1, tri[x, z, w] - 1, tri[y, z, w] - 1] for x, y, z, w in Qs], dtype=np.int64).reshape(-1, 4)
        self.Gs = list(comb(range(m), n - 1))
        self.G_sub = np.array([[qid[Q] for Q in comb(G, 4)] for G in self.Gs], dtype=np.int64).reshape(len(self.Gs), -1)
        self.Ks = list(comb(range(m), a - 1))
        self.K_tr = np.array([[tri[K[i], K[i + 1], K[i + 2]] - 1 for i in range(a - 3)] for K in self.Ks], dtype=np.int64).reshape(len(self.Ks), -1)

    def pool_clause(self, D):
        D = sorted(D); Ds = set(D); C = [i for i in range(self.m) if i not in Ds]
        cl = [self.Y[K] for K in comb(D, self.a - 1)] + [self.Z[G] for G in comb(C, self.n - 1)]
        if self.strong: cl += [self.Z[G] for G in comb(D, self.n - 1)]
        return cl

    def clause_len(self, d):
        from math import comb as C
        return C(d, self.a - 1) + C(self.m - d, self.n - 1) + (C(d, self.n - 1) if self.strong else 0)

    def analyse(self, o):
        """o: bool array over triples (True = cup).  Returns (list of (a-1)-caps, list of convex (n-1)-sets)."""
        conv4 = (o[self.q_t[:, 0]] == o[self.q_t[:, 1]]) & (o[self.q_t[:, 2]] == o[self.q_t[:, 3]])
        gm = conv4[self.G_sub].all(axis=1)
        km = (~o[self.K_tr]).all(axis=1)
        return [self.Ks[i] for i in np.nonzero(km)[0]], [self.Gs[i] for i in np.nonzero(gm)[0]]

def works(D, caps, gons, strong):
    Ds = set(D)
    if any(Ds.issuperset(K) for K in caps): return False
    if any(Ds.isdisjoint(G) for G in gons): return False
    if strong and any(Ds.issuperset(G) for G in gons): return False
    return True

def find_delta(M, caps, gons, rnd, pick):
    """A working Delta for the signotope with the given caps/gons, or None (exact: small SAT)."""
    m = M.m
    with Glucose4() as s:
        for K in caps: s.add_clause([-(i + 1) for i in K])
        for G in gons:
            s.add_clause([i + 1 for i in G])
            if M.strong: s.add_clause([-(i + 1) for i in G])
        if not s.solve(): return None
        D = [i for i in range(m) if s.get_model()[i] > 0]
    assert works(D, caps, gons, M.strong)
    if pick == 'first': return D
    # candidates: greedy-minimal and greedy-maximal variants; choose the shortest pool clause
    best = D; bl = M.clause_len(len(D))
    for rep in range(6):
        E = list(D); order = list(range(m)); rnd.shuffle(order)
        if rep % 2 == 0:   # shrink
            for i in order:
                if i in E:
                    F = [j for j in E if j != i]
                    if works(F, caps, gons, M.strong): E = F
        else:              # grow
            for i in order:
                if i not in E:
                    F = sorted(E + [i])
                    if works(F, caps, gons, M.strong): E = F
        l = M.clause_len(len(E))
        if l < bl: best, bl = sorted(E), l
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('a', type=int); ap.add_argument('n', type=int); ap.add_argument('m', type=int)
    ap.add_argument('form', choices=['weak', 'strong'])
    ap.add_argument('--tl', type=float, default=3000); ap.add_argument('--out', default='runs')
    ap.add_argument('--pick', default='short'); ap.add_argument('--mirror', action='store_true')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--phase', action='store_true', help='prefer witness variables true')
    ap.add_argument('--maximize', action='store_true', help='make S maximal in (caps, gons) before answering')
    A = ap.parse_args()
    a, n, m, strong = A.a, A.n, A.m, A.form == 'strong'
    tag = 'a%d_n%d_m%d_%s' % (a, n, m, A.form)
    os.makedirs(A.out, exist_ok=True)
    fpool = os.path.join(A.out, tag + '.pool.json'); fres = os.path.join(A.out, tag + '.result.json')
    t0 = time.time(); rnd = random.Random(A.seed)
    M = Model(a, n, m, strong)
    sol = Cadical153(bootstrap_with=M.base + M.wit)
    tb = time.time() - t0
    allw = sorted(set(M.Y.values()) | set(M.Z.values()))
    if A.phase: sol.set_phases(allw)
    nmax = 0
    pool = []; hard = []
    if os.path.exists(fpool):
        st = json.load(open(fpool)); pool = [tuple(D) for D in st['pool']]
        for D in pool: sol.add_clause(M.pool_clause(D))
    status = 'TIMEOUT'; cex = None; it = 0; last = time.time()
    while time.time() - t0 < A.tl:
        if not sol.solve(): status = 'UNSAT'; break
        it += 1
        mod = sol.get_model()
        o = np.array([mod[i] > 0 for i in range(M.ntri)])
        caps, gons = M.analyse(o)
        if A.maximize:
            while True:
                cur = set(M.Y[K] for K in caps) | set(M.Z[G] for G in gons)
                M.nv += 1; act = M.nv
                sol.add_clause([-act] + [w for w in allw if w not in cur])
                ok = sol.solve(assumptions=sorted(cur, key=abs) + [act])
                if ok:
                    mod = sol.get_model(); o = np.array([mod[i] > 0 for i in range(M.ntri)])
                sol.add_clause([-act])
                if not ok: break
                nmax += 1
                caps2, gons2 = M.analyse(o)
                assert set(caps) <= set(caps2) and set(gons) <= set(gons2) and len(caps2) + len(gons2) > len(caps) + len(gons)
                caps, gons = caps2, gons2
        D = find_delta(M, caps, gons, rnd, A.pick)
        if D is None:
            status = 'COUNTEREXAMPLE'; cex = ''.join('+' if x else '-' for x in o); break
        new = [tuple(D)]
        if A.mirror:
            Dm = tuple(sorted(m - 1 - i for i in D))
            if Dm != new[0]: new.append(Dm)
        for D in new:
            assert D not in pool, 'pooled Delta works for S: encoding error'
            pool.append(D); sol.add_clause(M.pool_clause(D))
        if time.time() - last > 60:
            json.dump({'a': a, 'n': n, 'm': m, 'form': A.form, 'pool': pool}, open(fpool + '.tmp', 'w')); os.replace(fpool + '.tmp', fpool)
            print('  ..', tag, 'pool', len(pool), 'iter', it, '%.0fs' % (time.time() - t0), flush=True); last = time.time()
    json.dump({'a': a, 'n': n, 'm': m, 'form': A.form, 'pool': pool}, open(fpool + '.tmp', 'w')); os.replace(fpool + '.tmp', fpool)
    res = {'a': a, 'n': n, 'm': m, 'form': A.form, 'status': status, 'pool_size': len(pool), 'iterations': it,
           'vars': M.nv, 'base_clauses': len(M.base), 'wit_clauses': len(M.wit), 'build_s': round(tb, 1),
           'seconds': round(time.time() - t0, 1), 'pick': A.pick, 'mirror': A.mirror, 'phase': A.phase, 'maximize': A.maximize, 'max_rounds': nmax, 'cex': cex}
    json.dump(res, open(fres, 'w'))
    print(json.dumps(res), flush=True)

if __name__ == '__main__':
    main()
