#!/usr/bin/env python
"""Eager decision of D(a, n, m; form) on abstract signotopes by ONE CNF, with an LRAT proof checked by cake_lpr.

F(a,n,m,form[,b]) = base(a,n,m) + witness definitions + one clause for EVERY subset Delta of [m] (size lo..hi):
     "Delta fails" = some b-cap inside Delta, or some convex (n-1)-set inside the complement
                     [strong form: or some convex (n-1)-set inside Delta];   b = a-1 unless given.
F is satisfiable iff some signotope on m points with no a-cap and no convex n-gon defeats every Delta
(soundness argument: README section 2).  UNSAT => D(a,n,m;form) holds for all signotopes, hence all point sets.

usage: eager_cert.py a n m weak|strong [--b B] [--lo L --hi H] [--tl SEC] [--nocert] [--out DIR]
"""
import sys, os, json, time, hashlib, subprocess, itertools, argparse, random, resource
import numpy as np
comb = itertools.combinations
CADICAL = '/usr/bin/cadical'; CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
CADICAL_AS_MAX = 1300 << 20   # address-space limit of the CaDiCaL child (track budget 2 GB since 18:25 KST)
CAKE_OPTS = ['--CML_HEAP_SIZE=900', '--CML_STACK_SIZE=100']   # MB; without them cake_lpr touches about 4 GB
CAKE_INLINE_MAX = 1500e6     # bytes of LRAT above which the cake_lpr check is deferred to a verifier unit

def limit_as():
    resource.setrlimit(resource.RLIMIT_AS, (CADICAL_AS_MAX, CADICAL_AS_MAX))

def sha(fn):
    h = hashlib.sha256()
    with open(fn, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 24), b''): h.update(ch)
    return h.hexdigest()

class Enc:
    """Deterministic builder.  Variable v(t) = 1 + rank of triple t (lexicographic); true = cup (positive orientation)."""
    def __init__(self, a, n, m, strong, b=None, base_only=False):
        assert 4 <= a <= n and n >= 5
        b = a - 1 if b is None else b
        assert b >= 3
        self.a, self.n, self.m, self.strong, self.b = a, n, m, strong, b
        tri = self.tri = {t: i + 1 for i, t in enumerate(comb(range(m), 3))}
        self.ntri = self.nv = len(tri)
        base = self.base = []; wit = self.wit = []
        for i, j, k, l in comb(range(m), 4):                 # signotope axioms
            s = [tri[i, j, k], tri[i, j, l], tri[i, k, l], tri[j, k, l]]
            for p, q, r in comb(range(4), 3):
                base.append([-s[p], s[q], -s[r]]); base.append([s[p], -s[q], s[r]])
        for K in comb(range(m), a):                           # no a-cap
            base.append([tri[K[i], K[i + 1], K[i + 2]] for i in range(a - 2)])
        for G in comb(range(m), n):                           # no convex n-gon
            inner = G[1:-1]
            for r in range(0, a - 2):
                for A in comb(inner, r):
                    B = [g for g in inner if g not in A]
                    c = (G[0],) + A + (G[-1],); d = [G[0]] + B + [G[-1]]
                    base.append([tri[c[i], c[i + 1], c[i + 2]] for i in range(len(c) - 2)] +
                                [-tri[d[i], d[i + 1], d[i + 2]] for i in range(len(d) - 2)])
        if base_only: return
        self.Y = {}                                           # Y[K] -> K is a b-cap
        if b == 3:
            for K in comb(range(m), 3): self.Y[K] = -tri[K]
        else:
            for K in comb(range(m), b):
                self.nv += 1; self.Y[K] = self.nv
                for i in range(b - 2): wit.append([-self.nv, -tri[K[i], K[i + 1], K[i + 2]]])
        self.Q4 = {}                                          # Q4[Q] -> Q in convex position
        for Q in comb(range(m), 4):
            self.nv += 1; v = self.nv; self.Q4[Q] = v
            x, y, z, w = Q
            t1, t2, t3, t4 = tri[x, y, z], tri[x, y, w], tri[x, z, w], tri[y, z, w]
            wit += [[-v, -t1, t2], [-v, t1, -t2], [-v, -t3, t4], [-v, t3, -t4]]
        if n - 1 == 4: self.Z = self.Q4                       # Z[G] -> G in convex position
        else:
            self.Z = {}
            for G in comb(range(m), n - 1):
                self.nv += 1; v = self.nv; self.Z[G] = v
                for Q in comb(G, 4): wit.append([-v, self.Q4[Q]])

    def restrict(self, mode):
        """Restricted statement: a working Delta exists INSIDE an S-defined allowed set.  NA[p] -> p is not allowed
        (one direction).  Every pool clause gets the extra literals NA[p], p in Delta.
        mode 'QQ'  : allowed = points that start no b-cap or end no b-cap (Q u Q');
        mode 'ends': allowed = left or right ends of convex (n-1)-gons (E_L u E_R)."""
        m, b, n = self.m, self.b, self.n; self.NA = {}; self.mode = mode
        if mode == 'Q':                               # negative control: allowed = points that start no b-cap
            for p in range(m):
                self.nv += 1; v = self.nv; self.NA[p] = v
                self.wit.append([-v] + [self.Y[K] for K in comb(range(p, m), b) if K[0] == p])
        elif mode == 'QQ':
            for p in range(m):
                self.nv += 1; v = self.nv; self.NA[p] = v
                self.wit.append([-v] + [self.Y[K] for K in comb(range(p, m), b) if K[0] == p])       # p starts a b-cap
                self.wit.append([-v] + [self.Y[K] for K in comb(range(0, p + 1), b) if K[-1] == p])  # p ends a b-cap
        elif mode == 'ends':
            CV = {}                                   # CV[Q] <- Q convex   (over-approximation: false only if not convex)
            for Q in comb(range(m), 4):
                self.nv += 1; v = self.nv; CV[Q] = v
                x, y, z, w = Q; tri = self.tri
                t1, t2, t3, t4 = tri[x, y, z], tri[x, y, w], tri[x, z, w], tri[y, z, w]
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        self.wit.append([v, -s1 * t1, -s1 * t2, -s2 * t3, -s2 * t4])
            ZZ = {}                                   # ZZ[G] <- G convex
            for G in comb(range(m), n - 1):
                if n - 1 == 4: ZZ[G] = CV[G]; continue
                self.nv += 1; v = self.nv; ZZ[G] = v
                self.wit.append([v] + [-CV[Q] for Q in comb(G, 4)])
            for p in range(m):
                self.nv += 1; v = self.nv; self.NA[p] = v
                for G in comb(range(m), n - 1):
                    if G[0] == p or G[-1] == p: self.wit.append([-v, -ZZ[G]])
        elif mode in ('cupint', 'capint', 'cupint+ends', 'capint+ends', 'int'):
            # allowed = interior vertices of the cup parts (cupint) / cap parts (capint) of convex (n-1)-gons,
            # optionally together with the ends of gons; 'int' = all non-end vertices of gons.
            tri = self.tri
            CV = {}
            for Q in comb(range(m), 4):
                self.nv += 1; v = self.nv; CV[Q] = v
                x, y, z, w = Q
                t1, t2, t3, t4 = tri[x, y, z], tri[x, y, w], tri[x, z, w], tri[y, z, w]
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        self.wit.append([v, -s1 * t1, -s1 * t2, -s2 * t3, -s2 * t4])
            ZZ = {}
            for G in comb(range(m), n - 1):
                if n - 1 == 4: ZZ[G] = CV[G]; continue
                self.nv += 1; v = self.nv; ZZ[G] = v
                self.wit.append([v] + [-CV[Q] for Q in comb(G, 4)])
            for p in range(m):
                self.nv += 1; v = self.nv; self.NA[p] = v
                for G in comb(range(m), n - 1):
                    if p not in G: continue
                    if G[0] == p or G[-1] == p:
                        if mode.endswith('+ends'): self.wit.append([-v, -ZZ[G]])
                        continue
                    t = tri[G[0], p, G[-1]]                 # true: p below the chord (cup part); false: cap part
                    if mode in ('cupint', 'cupint+ends'): self.wit.append([-v, -ZZ[G], -t])
                    elif mode in ('capint', 'capint+ends'): self.wit.append([-v, -ZZ[G], t])
                    else: self.wit.append([-v, -ZZ[G]])
        elif mode == 'rank':
            # allowed = Delta_R u Delta_L of ETVTHY20261113 section 3.2 (rank-defined):
            #   Delta_R = {p : for some j in 2..a-1, a j-cap ends at p and an (n+1-j)-cup ends at p},
            #   Delta_L = {p : for some j, a j-cap starts at p and an (n+1-j)-cup starts at p}.
            # CE[p,j] <- a j-cap ends at p ; UE[p,k] <- a k-cup ends at p ; CS, US: the same for 'starts'.
            tri = self.tri; a = self.a
            def chain_ind(p, size, cap, end):
                self.nv += 1; v = self.nv
                if size == 2:
                    exists = (p > 0) if end else (p < m - 1)
                    if exists: self.wit.append([v])
                    return v
                rng = range(0, p) if end else range(p + 1, m)
                for rest in comb(rng, size - 1):
                    K = rest + (p,) if end else (p,) + rest
                    ts = [tri[K[i], K[i + 1], K[i + 2]] for i in range(size - 2)]
                    self.wit.append([v] + ([t for t in ts] if cap else [-t for t in ts]))   # chain present -> v
                return v
            for p in range(m):
                self.nv += 1; na = self.nv; self.NA[p] = na
                for j in range(2, a):
                    k = n + 1 - j
                    ce = chain_ind(p, j, True, True); ue = chain_ind(p, k, False, True)
                    cs = chain_ind(p, j, True, False); us = chain_ind(p, k, False, False)
                    self.wit.append([-na, -ce, -ue]); self.wit.append([-na, -cs, -us])
        else: raise ValueError(mode)

    def must_contain(self, mode):
        """Restricted statement: a working Delta exists that CONTAINS an S-defined set F(S).  MU[p] -> p in F(S)
        (one direction); every pool clause gets the extra literals MU[p], p not in Delta.
        mode 'cupR'  : F = right ends of (n-1)-cups;      mode 'cupRL': F = left and right ends of (n-1)-cups;
        mode 'gonRQ' : F = right ends of convex (n-1)-gons that start no b-cap;   mode 'Qall': F = points starting no b-cap."""
        m, b, n = self.m, self.b, self.n; tri = self.tri; self.MU = {}; self.must = mode
        XS = {}
        def starts_ind(p):                            # XS[p] <- p starts a b-cap
            if p not in XS:
                self.nv += 1; XS[p] = self.nv
                for K in comb(range(p, m), b):
                    if K[0] == p: self.wit.append([XS[p]] + [tri[K[i], K[i + 1], K[i + 2]] for i in range(b - 2)])
            return XS[p]
        CW = {}
        if mode in ('cupR', 'cupLR', 'cupRL'):
            for C in comb(range(m), n - 1):           # CW[C] -> C is an (n-1)-cup
                self.nv += 1; CW[C] = self.nv
                for i in range(n - 3): self.wit.append([-self.nv, tri[C[i], C[i + 1], C[i + 2]]])
        for p in range(m):
            self.nv += 1; v = self.nv; self.MU[p] = v
            if mode == 'cupR': self.wit.append([-v] + [CW[C] for C in CW if C[-1] == p])
            elif mode == 'cupRL': self.wit.append([-v] + [CW[C] for C in CW if C[-1] == p or C[0] == p])
            elif mode == 'gonRQ':
                self.wit.append([-v] + [self.Z[G] for G in comb(range(m), n - 1) if G[-1] == p])
                self.wit.append([-v, -starts_ind(p)])
            elif mode == 'Qall': self.wit.append([-v, -starts_ind(p)])
            else: raise ValueError(mode)

    def reduce_minimal(self):
        """Clauses valid for a MINIMUM counterexample (README Lemma 4): every point lies on a convex (n-1)-gon, and in the
        weak form on a b-cap.  F + these clauses UNSAT, together with the statement for m-1 points, gives it for m points."""
        self.red = []
        for p in range(self.m):
            self.red.append([self.Z[G] for G in comb(range(self.m), self.n - 1) if p in G])
            if not self.strong: self.red.append([self.Y[K] for K in comb(range(self.m), self.b) if p in K])
        self.wit += self.red

    def pool_clause(self, D):
        Ds = set(D); C = [i for i in range(self.m) if i not in Ds]
        cl = [self.Y[K] for K in comb(D, self.b)] + [self.Z[G] for G in comb(C, self.n - 1)]
        if self.strong: cl += [self.Z[G] for G in comb(D, self.n - 1)]
        if getattr(self, 'NA', None): cl += [self.NA[p] for p in D]
        if getattr(self, 'MU', None): cl += [self.MU[p] for p in C]
        return cl

    def pool(self, lo, hi):
        for d in range(lo, hi + 1):
            for D in comb(range(self.m), d): yield D

    def write(self, fn, lo, hi):
        from math import comb as C
        npool = sum(C(self.m, d) for d in range(lo, hi + 1))
        with open(fn, 'w') as f:
            f.write('p cnf %d %d\n' % (self.nv, len(self.base) + len(self.wit) + npool))
            for c in self.base: f.write(' '.join(map(str, c)) + ' 0\n')
            for c in self.wit: f.write(' '.join(map(str, c)) + ' 0\n')
            for D in self.pool(lo, hi): f.write(' '.join(map(str, self.pool_clause(D))) + ' 0\n')
        return len(self.base) + len(self.wit) + npool

def exact_sets(E, o):
    """All b-caps and all convex (n-1)-sets of the signotope o (dict triple -> bool, True = cup); plain Python."""
    m = E.m
    def conv4(Q):
        x, y, z, w = Q
        return o[x, y, z] == o[x, y, w] and o[x, z, w] == o[y, z, w]
    c4 = {Q: conv4(Q) for Q in comb(range(m), 4)}
    caps = [K for K in comb(range(m), E.b) if all(not o[K[i], K[i + 1], K[i + 2]] for i in range(E.b - 2))]
    gons = [G for G in comb(range(m), E.n - 1) if all(c4[Q] for Q in comb(G, 4))]
    return caps, gons

def exact_delta(E, caps, gons):
    """Some working Delta (list) or None, by an independent small SAT (pysat Glucose4)."""
    from pysat.solvers import Glucose4
    with Glucose4() as s:
        for K in caps: s.add_clause([-(i + 1) for i in K])
        for G in gons:
            s.add_clause([i + 1 for i in G])
            if E.strong: s.add_clause([-(i + 1) for i in G])
        if not s.solve(): return None
        return [i for i in range(E.m) if s.get_model()[i] > 0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('a', type=int); ap.add_argument('n', type=int); ap.add_argument('m', type=int)
    ap.add_argument('form', choices=['weak', 'strong', 'base'])
    ap.add_argument('--b', type=int, default=None); ap.add_argument('--lo', type=int, default=0); ap.add_argument('--hi', type=int, default=None)
    ap.add_argument('--tl', type=int, default=3600); ap.add_argument('--nocert', action='store_true')
    ap.add_argument('--out', default='eager'); ap.add_argument('--keep', action='store_true')
    ap.add_argument('--allow', default=None, choices=['QQ', 'ends', 'Q', 'rank', 'cupint', 'capint', 'cupint+ends', 'capint+ends', 'int'])
    ap.add_argument('--must', default=None, choices=['cupR', 'cupRL', 'gonRQ', 'Qall'])
    ap.add_argument('--reduced', action='store_true', help='add the minimum-counterexample clauses (needs the statement for m-1)')
    A = ap.parse_args()
    a, n, m = A.a, A.n, A.m; hi = m if A.hi is None else A.hi
    tag = 'a%d_n%d_m%d_%s' % (a, n, m, A.form) + ('' if A.b is None else '_b%d' % A.b) + ('' if (A.lo == 0 and hi == m) else '_s%d-%d' % (A.lo, hi)) + ('' if not A.allow else '_' + A.allow) + ('_red' if A.reduced else '') + ('' if not A.must else '_must' + A.must)
    os.makedirs(A.out, exist_ok=True)
    cnf = os.path.join(A.out, tag + '.cnf'); lrat = os.path.join(A.out, tag + '.lrat'); log = os.path.join(A.out, tag + '.cadical.out')
    t0 = time.time()
    E = Enc(a, n, m, A.form == 'strong', A.b, base_only=(A.form == 'base'))
    if A.allow: E.restrict(A.allow)
    if A.reduced: E.reduce_minimal()
    if A.must: E.must_contain(A.must)
    if A.form == 'base':
        with open(cnf, 'w') as f:
            f.write('p cnf %d %d\n' % (E.nv, len(E.base)))
            for c in E.base: f.write(' '.join(map(str, c)) + ' 0\n')
        ncl = len(E.base)
    else:
        ncl = E.write(cnf, A.lo, hi)
    info = {'a': a, 'n': n, 'm': m, 'form': A.form, 'b': E.b, 'lo': A.lo, 'hi': hi, 'allow': A.allow, 'must': A.must, 'reduced': A.reduced, 'vars': E.nv, 'clauses': ncl,
            'cnf_bytes': os.path.getsize(cnf), 'cnf_sha256': sha(cnf), 'build_s': round(time.time() - t0, 1)}
    t = time.time(); keep_lrat = False
    cmd = [CADICAL, '-q', '-t', str(A.tl)] + ([] if A.nocert else ['--lrat=true', '--binary=false']) + [cnf] + ([] if A.nocert else [lrat])
    with open(log, 'w') as f: r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, preexec_fn=limit_as)
    info['cadical_exit'] = r.returncode; info['cadical_s'] = round(time.time() - t, 1)
    if r.returncode == 20:
        info['status'] = 'UNSAT'
        if not A.nocert:
            info['lrat_bytes'] = os.path.getsize(lrat); info['lrat_sha256'] = sha(lrat)
            if info['lrat_bytes'] > CAKE_INLINE_MAX:
                # memory policy (13 Nov 18:25 KST): cake_lpr on a large proof does not fit the track budget;
                # keep the proof and check it later in a nov13c-vfy-* unit (cake_deferred.sh)
                info['cake_lpr'] = 'DEFERRED'; keep_lrat = True
            else:
                t = time.time()
                c = subprocess.run([CAKE] + CAKE_OPTS + [cnf, lrat], capture_output=True, text=True)
                info['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else ('FAILED: ' + (c.stdout + c.stderr)[-300:])
                info['cake_s'] = round(time.time() - t, 1)
    elif r.returncode == 10:
        info['status'] = 'SAT'
        lits = []
        for line in open(log):
            if line.startswith('v '): lits += [int(x) for x in line.split()[1:]]
        val = {abs(l): l > 0 for l in lits}
        o = {t: val[v] for t, v in E.tri.items()}
        info['model'] = ''.join('+' if o[t] else '-' for t in comb(range(m), 3))
        if A.form != 'base':
            caps, gons = exact_sets(E, o); D = exact_delta(E, caps, gons)
            info['exact_delta'] = D; info['n_caps'] = len(caps); info['n_gons'] = len(gons)
            if A.must:
                starts = {K[0] for K in caps}
                def is_cup(G): return all(o[G[i], G[i + 1], G[i + 2]] for i in range(len(G) - 2))
                if A.must == 'cupR': F = {G[-1] for G in gons if is_cup(G)}
                elif A.must == 'cupRL': F = {G[-1] for G in gons if is_cup(G)} | {G[0] for G in gons if is_cup(G)}
                elif A.must == 'gonRQ': F = {G[-1] for G in gons} - starts
                else: F = set(range(m)) - starts
                info['must_set'] = sorted(F)
                from pysat.solvers import Glucose4
                with Glucose4() as s2:
                    for K in caps: s2.add_clause([-(i + 1) for i in K])
                    for G in gons:
                        s2.add_clause([i + 1 for i in G])
                        if E.strong: s2.add_clause([-(i + 1) for i in G])
                    for p in F: s2.add_clause([p + 1])
                    ok = s2.solve()
                info['verdict'] = ('model has NO working Delta containing the must-set (a working Delta exists: %s)' % (D is not None)) if not ok else 'ENCODING ERROR: such a Delta exists'
            elif A.allow:
                if A.allow == 'QQ':
                    allowed = [p for p in range(m) if not (any(K[0] == p for K in caps) and any(K[-1] == p for K in caps))]
                elif A.allow == 'Q':
                    allowed = [p for p in range(m) if not any(K[0] == p for K in caps)]
                elif A.allow in ('cupint', 'capint', 'cupint+ends', 'capint+ends', 'int'):
                    al = set()
                    for G in gons:
                        u, v = G[0], G[-1]
                        if A.allow.endswith('+ends'): al |= {u, v}
                        for x in G[1:-1]:
                            below = o[u, x, v]
                            if A.allow == 'int' or (below and A.allow.startswith('cupint')) or ((not below) and A.allow.startswith('capint')): al.add(x)
                    allowed = sorted(al)
                elif A.allow == 'rank':
                    def has(p, size, cap, end):
                        if size == 2: return (p > 0) if end else (p < m - 1)
                        rng = range(0, p) if end else range(p + 1, m)
                        for rest in comb(rng, size - 1):
                            K = rest + (p,) if end else (p,) + rest
                            if all(o[K[i], K[i + 1], K[i + 2]] != cap for i in range(size - 2)): return True
                        return False
                    allowed = [p for p in range(m) if any((has(p, j, True, True) and has(p, n + 1 - j, False, True)) or
                                                          (has(p, j, True, False) and has(p, n + 1 - j, False, False)) for j in range(2, a))]
                else:
                    allowed = sorted({G[0] for G in gons} | {G[-1] for G in gons})
                info['allowed'] = allowed
                from pysat.solvers import Glucose4
                with Glucose4() as s2:
                    for K in caps: s2.add_clause([-(i + 1) for i in K])
                    for G in gons:
                        s2.add_clause([i + 1 for i in G])
                        if E.strong: s2.add_clause([-(i + 1) for i in G])
                    for p in range(m):
                        if p not in allowed: s2.add_clause([-(p + 1)])
                    ok = s2.solve()
                info['verdict'] = ('model has NO working Delta inside the allowed set (a working Delta exists: %s)' % (D is not None)) if not ok else 'ENCODING ERROR: restricted Delta exists'
            else:
                info['verdict'] = 'ABSTRACT COUNTEREXAMPLE' if D is None else 'model has a working Delta outside the pool sizes'
    else:
        info['status'] = 'UNKNOWN'
    if os.path.exists(lrat) and not keep_lrat: os.remove(lrat)
    if not A.keep and not keep_lrat and os.path.getsize(cnf) > 30e6: os.remove(cnf)
    info['total_s'] = round(time.time() - t0, 1)
    print(json.dumps(info), flush=True)
    with open(os.path.join(A.out, 'results.jsonl'), 'a') as f: f.write(json.dumps(info) + '\n')

if __name__ == '__main__':
    main()
