"""Witness-complete small-support rows for the (6,6;8) internal catalog (FLAYER20261113).

Question decided by one CNF:  is there a (6,6;8)-signotope on at most n points in which the states of the
list T (indices of etv_common.py, ETV_A=4, ETV_B=4) are all occupied (each by a point whose incoming state
is EXACTLY that state)?

Abstract model (a sound relaxation of real point sets with distinct x in general position):
  o(i,j,k), i<j<k            True = positive orientation (cup triple), False = cap triple
  signotope axioms           on every 4-tuple the sequence (o_ijk, o_ijl, o_ikl, o_jkl) has <= 1 sign change
  pres(p)                    the first m points are present (prefix); absent points carry no constraint
  capE_k(u,v), cupE_k(u,v)   k = 3,4,5: a cap / cup with >= k points ends with the pair (u,v)   (EXACT: iff)
  no 6-cap / 6-cup           ending at a present point
  capF4(u;p,q), cap5(u,v)    one-directional: a 4-cap u,t,p,q exists => capF4;  capF4 and cap (p,q,v) => cap5(u,v)
  no octagon                 not (cap5(u,v) and cup5(u,v)) for present v
  cell(p,a,b)                exists u<p with capE_{a+1}(u,p) and cupE_{b+1}(u,p)                  (EXACT: iff)
  own(p,j)                   point p is the owner of T[j]: p present, corner cells of T[j] true at p,
                             co-corner cells (minimal cells outside the diagram) false at p
  the last present point is an owner.

Soundness of "UNSAT => the states of T are never all occupied" (README section 3):
  if they are all occupied in a real (6,6;8)-set S, let W = owners + for every owner v and every corner (a,b)
  of its state one pair (u,v) attaining it, with an (a+1)-cap and a (b+1)-cup of S ending with (u,v).
  |W| <= nmax(T) = sum over T of (1 + sum over corners of (a+b-1)).  In W every owner keeps its exact state
  (labels do not increase in subsets, corners are still attained), W is a (6,6;8)-set, and its last point is
  an owner (witnesses are left of their owner).  Sorted by x, W gives a satisfying assignment with |W|
  present points (definitional variables at their true values, absent points placed generically far right).
"""
import os, sys, subprocess, itertools, json, time, hashlib
os.environ.setdefault('ETV_A', '4'); os.environ.setdefault('ETV_B', '4')
import etv_common as ec
STATES = ec.STATES

def corners(f):
    return [(a + 1, f[a]) for a in range(4) if f[a] >= 1 and (a == 3 or f[a + 1] < f[a])]

def cocorners(f):
    return [(a + 1, f[a] + 1) for a in range(4) if f[a] < 4 and (a == 0 or f[a - 1] > f[a])]

def nmax(T):
    return sum(1 + sum(a + b - 1 for a, b in corners(STATES[s])) for s in T)

TRUE, FALSE = 'T', 'F'

class Wit:
    def __init__(self, n, T, flags=True, last_owner=True):
        self.n = n; self.T = list(T); self.nv = 0; self.cl = []
        self.names = {}
        n_ = n
        self.o = {}
        for i in range(n_):
            for j in range(i + 1, n_):
                for k in range(j + 1, n_):
                    self.o[i, j, k] = self.new(('o', i, j, k))
        self.pres = [self.new(('pres', p)) for p in range(n_)]
        self.add([self.pres[0]])
        for p in range(n_ - 1):
            self.add([-self.pres[p + 1], self.pres[p]])
        if not flags:
            for p in range(n_): self.add([self.pres[p]])
        self._signotope()
        self._chains()
        self._octagon()
        self._cells_cache = {}
        self._owners(last_owner)

    def new(self, name=None):
        self.nv += 1
        if name is not None: self.names[name] = self.nv
        return self.nv

    def add(self, c):
        self.cl.append(list(c))

    def _signotope(self):
        o = self.o
        for i, j, k, l in itertools.combinations(range(self.n), 4):
            x = [o[i, j, k], o[i, j, l], o[i, k, l], o[j, k, l]]
            for p, q, r in itertools.combinations(range(4), 3):
                self.add([-x[p], x[q], -x[r]]); self.add([x[p], -x[q], x[r]])

    def _chains(self):
        n = self.n; o = self.o
        # E[sgn][k][(u,v)] : literal var; sgn=-1 caps (triples negative), +1 cups
        self.E = {-1: {}, 1: {}}
        for sgn in (-1, 1):
            for k in (3, 4, 5):
                self.E[sgn][k] = {(u, v): self.new(('E', sgn, k, u, v)) for u in range(n) for v in range(u + 1, n)}
            for u in range(n):
                for v in range(u + 1, n):
                    # k = 3
                    e3 = self.E[sgn][3][u, v]
                    lits = [sgn * o[t, u, v] for t in range(u)]   # literal true iff the triple has sign sgn
                    self.add([-e3] + lits)
                    for l in lits: self.add([-l, e3])
                    for k in (4, 5):
                        ek = self.E[sgn][k][u, v]; ys = []
                        for t in range(u):
                            y = self.new(); ys.append(y)
                            tri = sgn * o[t, u, v]; prev = self.E[sgn][k - 1][t, u]
                            self.add([-y, tri]); self.add([-y, prev]); self.add([y, -tri, -prev])
                        self.add([-ek] + ys)
                        for y in ys: self.add([-y, ek])
                    # monotone (redundant, sound)
                    self.add([-self.E[sgn][5][u, v], self.E[sgn][4][u, v]])
                    self.add([-self.E[sgn][4][u, v], self.E[sgn][3][u, v]])
            # no 6-chain ending at a present point
            for t in range(n):
                for u in range(t + 1, n):
                    for v in range(u + 1, n):
                        self.add([-(sgn * o[t, u, v]), -self.E[sgn][5][t, u], -self.pres[v]])

    def _octagon(self):
        n = self.n; o = self.o
        self.F4 = {-1: {}, 1: {}}; self.B5 = {-1: {}, 1: {}}
        for sgn in (-1, 1):
            for u in range(n):
                for p in range(u + 2, n):
                    for q in range(p + 1, n):
                        f = self.F4[sgn][u, p, q] = self.new(('F4', sgn, u, p, q))
                        for t in range(u + 1, p):
                            self.add([-(sgn * o[u, t, p]), -(sgn * o[t, p, q]), f])
            for u in range(n):
                for v in range(u + 4, n):
                    b = self.B5[sgn][u, v] = self.new(('B5', sgn, u, v))
                    for p in range(u + 2, v):
                        for q in range(p + 1, v):
                            self.add([-self.F4[sgn][u, p, q], -(sgn * o[p, q, v]), b])
        for u in range(n):
            for v in range(u + 4, n):
                self.add([-self.B5[-1][u, v], -self.B5[1][u, v], -self.pres[v]])

    def lab(self, sgn, k, u, v):
        """literal / constant for 'a chain of sign sgn with >= k points ends with (u,v)'"""
        if k <= 2: return TRUE
        return self.E[sgn][k][u, v]

    def cell(self, p, a, b):
        """literal or constant: cell (a,b) in I(p)"""
        if p == 0: return FALSE
        if (a, b) == (1, 1): return TRUE
        key = (p, a, b)
        if key in self._cells_cache: return self._cells_cache[key]
        c = self.new(('cell', p, a, b)); ms = []
        for u in range(p):
            x = self.lab(-1, a + 1, u, p); y = self.lab(1, b + 1, u, p)
            if x == TRUE: ms.append(y)
            elif y == TRUE: ms.append(x)
            else:
                m = self.new(); ms.append(m)
                self.add([-m, x]); self.add([-m, y]); self.add([m, -x, -y])
        self.add([-c] + ms)
        for m in ms: self.add([-m, c])
        self._cells_cache[key] = c
        return c

    def _owners(self, last_owner):
        n = self.n
        self.own = {}
        for j, s in enumerate(self.T):
            f = STATES[s]; cs = corners(f); ccs = cocorners(f); vs = []
            for p in range(n):
                # quick constant pruning
                req = [self.cell(p, a, b) for a, b in cs]; forb = [self.cell(p, a, b) for a, b in ccs]
                if FALSE in req or TRUE in forb: continue
                w = self.own[p, j] = self.new(('own', p, j)); vs.append(w)
                self.add([-w, self.pres[p]])
                for l in req:
                    if l != TRUE: self.add([-w, l])
                for l in forb:
                    if l != FALSE: self.add([-w, -l])
            self.add(vs)
            for x, y in itertools.combinations(vs, 2): self.add([-x, -y])
        # one point owns at most one state (automatic for distinct states; kept as redundant clauses)
        for p in range(n):
            ws = [self.own[p, j] for j in range(len(self.T)) if (p, j) in self.own]
            for x, y in itertools.combinations(ws, 2): self.add([-x, -y])
        if last_owner:
            for p in range(n):
                ws = [self.own[p, j] for j in range(len(self.T)) if (p, j) in self.own]
                c = [-self.pres[p]] + ws
                if p + 1 < n: c.append(self.pres[p + 1])
                self.add(c)

    def dimacs(self, extra=()):
        cl = self.cl + [list(c) for c in extra]
        out = ['p cnf %d %d' % (self.nv, len(cl))]
        out += [' '.join(map(str, c)) + ' 0' for c in cl]
        return '\n'.join(out) + '\n'

def solve_cnf(text, timeout=None, lrat=None, cnf_path=None):
    """Run CaDiCaL 2.1.3. Returns (status, model or None). status in SAT/UNSAT/UNKNOWN."""
    import tempfile
    if cnf_path is None:
        fd, cnf_path = tempfile.mkstemp(suffix='.cnf', dir=os.environ.get('FL_TMP', '.')); os.close(fd); tmp = True
    else: tmp = False
    open(cnf_path, 'w').write(text)
    cmd = ['/usr/bin/cadical', '-q']
    if timeout: cmd += ['-t', str(int(timeout))]
    if lrat: cmd += ['--lrat', '--no-binary', cnf_path, lrat]
    else: cmd += [cnf_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if tmp: os.remove(cnf_path)
    st = 'UNKNOWN'; model = None
    if r.returncode == 10:
        st = 'SAT'; model = set()
        for line in r.stdout.splitlines():
            if line.startswith('v '):
                for tok in line.split()[1:]:
                    x = int(tok)
                    if x > 0: model.add(x)
    elif r.returncode == 20: st = 'UNSAT'
    return st, model

# ---------- independent decoding / checking of models (pure Python DP on the signotope) ----------
def decode(w, model):
    n = w.n
    m = max(p for p in range(n) if w.pres[p] in model) + 1
    sg = {}
    for (i, j, k), v in w.o.items():
        sg[i, j, k] = 1 if v in model else -1
    return m, sg

def check_signotope(n, sg):
    for i, j, k, l in itertools.combinations(range(n), 4):
        x = [sg[i, j, k], sg[i, j, l], sg[i, k, l], sg[j, k, l]]
        if sum(1 for a in range(3) if x[a] != x[a + 1]) > 1: return False
    return True

def analyze_sig(m, sg):
    """exact DP on the first m points: returns (maxcap, maxcup, octagon?, list of state tuples)."""
    Em = {}; Ep = {}
    for v in range(m):
        for u in range(v):
            em = ep = 2
            for t in range(u):
                if sg[t, u, v] < 0: em = max(em, Em[t, u] + 1)
                else: ep = max(ep, Ep[t, u] + 1)
            Em[u, v] = em; Ep[u, v] = ep
    maxcap = max([1] + list(Em.values())); maxcup = max([1] + list(Ep.values()))
    states = []
    for v in range(m):
        f = [0] * 4
        for u in range(v):
            a = Em[u, v] - 1; b = Ep[u, v] - 1
            for c in range(min(a, 4)):
                f[c] = max(f[c], min(b, 4))
        states.append(tuple(f))
    # largest polygon: for each start s, longest cap / cup from s to t
    octa = False; best = 0
    for s in range(m):
        Dc = {}; Du = {}
        for j in range(s + 1, m): Dc[s, j] = 2; Du[s, j] = 2
        for j in range(s + 1, m):
            for i in range(s + 1, j):
                bc = bu = 0
                for h in range(s, i):
                    if (h, i) not in Dc: continue
                    if sg[h, i, j] < 0:
                        if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                    else:
                        if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                Dc[i, j] = bc; Du[i, j] = bu
        for t in range(s + 1, m):
            c = max(Dc[i, t] for i in range(s, t)); u_ = max(Du[i, t] for i in range(s, t))
            best = max(best, c + u_ - 2)
    return maxcap, maxcup, best, states

def check_model(w, model):
    m, sg = decode(w, model)
    if not check_signotope(w.n, sg): return False, 'signotope axioms violated'
    mc, mu, gon, st = analyze_sig(m, sg)
    if mc > 5 or mu > 5 or gon > 7: return False, 'not (6,6;8): %s' % ((mc, mu, gon),)
    occ = set(st)
    for s in w.T:
        if STATES[s] not in occ: return False, 'state %s not occupied' % (STATES[s],)
    return True, (m, mc, mu, gon, [ec.SINDEX[s] for s in st])

def decide(T, n=None, timeout=None, flags=True):
    """Returns (status, info).  UNSAT at n = nmax(T) means: the states of T are never all occupied."""
    if n is None: n = nmax(T)
    w = Wit(n, T, flags=flags)
    st, model = solve_cnf(w.dimacs(), timeout)
    info = {'n': n, 'vars': w.nv, 'clauses': len(w.cl)}
    if st == 'SAT':
        ok, det = check_model(w, model)
        info['model_ok'] = ok; info['detail'] = det
        m, sg = decode(w, model)
        info['m'] = m
        info['sig'] = ''.join('+' if sg[t] > 0 else '-' for t in itertools.combinations(range(m), 3))
    return st, info

if __name__ == '__main__':
    T = [int(x) for x in sys.argv[1].split(',')]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else None
    t0 = time.time()
    st, info = decide(T, n, timeout=float(sys.argv[3]) if len(sys.argv) > 3 else None)
    info.pop('sig', None)
    print([''.join(map(str, STATES[s])) for s in T], st, info, '%.1fs' % (time.time() - t0))
