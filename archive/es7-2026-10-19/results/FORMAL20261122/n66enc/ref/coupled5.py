"""Coupled owner model for an ETV support S (discovery tooling, adapted from RES33N coupled.py).

Owners v_0..v_{n-1} of the distinct states S[0..n-1] in one actual configuration of the (A,B) class
(every cap <= A+1 points, every cup <= B+1 points, no convex octagon).  Atoms:
  before(i,j)      v_i left of v_j
  cap_ge(i,j,k)    d(earlier,later)_1 >= k     (k = 2..A; k<=1 true, k>A false)
  cup_ge(i,j,k)    d(earlier,later)_2 >= k     (k = 2..B)
  orientation(ijk) det(p_i,p_j,p_k) > 0 in sorted index order
  convex_four      the four owners are in convex position
Clause families (tags; None = state independent, cached per n):
  None : threshold monotonicity, order transitivity, cap/cup growth (strict, with the A/B ceilings),
         signotope packets (4 owners in chronological order: at most one sign change),
         convex_four definition, complete no-octagon (every 8 owners: some 4-subset not convex)
  'empty'   (u,v): refined domain D'(s_u -> s_v) empty  =>  not before(u,v)
  'domain'  (u,v,a,b): (a,b) not in D'(s_u -> s_v)       =>  before(u,v) -> label(u,v) != (a,b)
  'positive'(i,j,k): TT[s_i,s_j,s_k] (six-order bounding-box test) => orientation positive in that order
D'(s->t) = {(a,b) in I(t)\\I(s) : a <= capH(s)+1, b <= cupH(s)+1}  (state separation + rank attainment)
UNSAT of this CNF means: no configuration of the class occupies all states of S.
"""
import itertools, subprocess, os, hashlib
import etv_common as ec
from etv_common import STATES, N, A, B
HERE = os.path.dirname(os.path.abspath(__file__))
TT = ec.TT
DIFF = ec.DREF
MAXK = {'cap': A, 'cup': B}

def neg(l):
    return (not l) if isinstance(l, bool) else -l

BAD4 = [bits for bits in itertools.product([False, True], repeat=4)
        if sum(x != y for x, y in zip(bits, bits[1:])) > 1]

class CNF:
    def __init__(self, S, static=True, octagon=True):
        self.S = list(S); n = self.n = len(S)
        self.ids = {}; self.nv = 0; self.clauses = []; self.tags = []
        for i, j in itertools.combinations(range(n), 2):
            self.before(i, j)
            for k in range(2, A + 1): self.ge('cap', i, j, k)
            for k in range(2, B + 1): self.ge('cup', i, j, k)
        for q in itertools.combinations(range(n), 3): self.orient(q)
        for q in itertools.combinations(range(n), 4): self.convex(q)
        if static:
            for i, j in itertools.combinations(range(n), 2):
                for typ in ('cap', 'cup'):
                    for k in range(2, MAXK[typ]): self.add([neg(self.ge(typ, i, j, k + 1)), self.ge(typ, i, j, k)])
            for a, b, c in itertools.permutations(range(n), 3):
                self.add([-self.before(a, b), -self.before(b, c), self.before(a, c)])
                o = self.orient((a, b, c))
                for typ, color in (('cap', False), ('cup', True)):
                    gate = [-self.before(a, b), -self.before(b, c), -o if color else o]
                    for k in range(1, MAXK[typ] + 1):
                        self.add(gate + [neg(self.ge(typ, a, b, k)), self.ge(typ, b, c, k + 1)])
            for quad in itertools.combinations(range(n), 4):
                for q in itertools.permutations(quad):
                    order = [-self.before(x, y) for x, y in zip(q, q[1:])]
                    triples = list(itertools.combinations(q, 3))
                    for bits in BAD4:
                        self.add(order + [-self.orient(t) if bit else self.orient(t) for t, bit in zip(triples, bits)])
                a, b, c, d = quad
                triples = [(a, b, c), (a, b, d), (a, c, d), (b, c, d)]
                for bits in itertools.product([False, True], repeat=4):
                    x, y, z, w = bits
                    convex = sum([not w, z, not y, x]) == 2
                    self.add([-self.orient(t) if bit else self.orient(t) for t, bit in zip(triples, bits)] +
                             [self.convex(quad) if convex else -self.convex(quad)])
            if octagon:
                for eight in itertools.combinations(range(n), 8):
                    self.add([-self.convex(q) for q in itertools.combinations(eight, 4)])
        # state-dependent clauses
        for i, j in itertools.combinations(range(n), 2):
            for u, v in ((i, j), (j, i)):
                D = DIFF[S[u]][S[v]]
                if not D:
                    self.add([-self.before(u, v)], ('empty', u, v)); continue
                for a in range(1, A + 1):
                    for b in range(1, B + 1):
                        if (a, b) in D: continue
                        self.add([-self.before(u, v), neg(self.ge('cap', i, j, a)), self.ge('cap', i, j, a + 1),
                                  neg(self.ge('cup', i, j, b)), self.ge('cup', i, j, b + 1)], ('domain', u, v, a, b))
        for q in itertools.combinations(range(n), 3):
            a, b, c = [S[i] for i in q]
            if TT[a, b, c]: self.add([self.orient(q)], ('positive', q[0], q[1], q[2]))
            elif TT[a, c, b]: self.add([-self.orient(q)], ('positive', q[0], q[2], q[1]))

    def var(self, key):
        v = self.ids.get(key)
        if v is None:
            self.nv += 1; v = self.ids[key] = self.nv
        return v
    def before(self, i, j):
        return self.var(('before', min(i, j), max(i, j))) * (1 if i < j else -1)
    def ge(self, typ, i, j, k):
        if k <= 1: return True
        if k > MAXK[typ]: return False
        return self.var((typ + '_ge', min(i, j), max(i, j), k))
    def orient(self, q):
        parity = sum(q[i] > q[j] for i in range(3) for j in range(i + 1, 3)) % 2
        return self.var(('orientation',) + tuple(sorted(q))) * (1 if not parity else -1)
    def convex(self, q):
        return self.var(('convex_four',) + tuple(sorted(q)))
    def add(self, lits, tag=None):
        out = set()
        for l in lits:
            if l is True: return
            if l is False: continue
            assert type(l) is int and l != 0, lits
            out.add(l)
        if any(-l in out for l in out): return
        self.clauses.append(sorted(out, key=abs)); self.tags.append(tag)
    def dimacs(self):
        return f'p cnf {self.nv} {len(self.clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in self.clauses)

_STATIC = {}
def _static(n):
    if n in _STATIC: return _STATIC[n]
    p = os.path.join(HERE, 'static', f'static_A{A}_B{B}_{n}.txt')
    if os.path.exists(p):
        with open(p) as f:
            nv, nc = map(int, f.readline().split()); body = f.read()
    else:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        cnf = CNF(list(range(n)))
        cls = [c for c, t in zip(cnf.clauses, cnf.tags) if t is None]
        nv, nc = cnf.nv, len(cls)
        body = ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)
        tmp = p + f'.{os.getpid()}'
        with open(tmp, 'w') as f: f.write(f'{nv} {nc}\n' + body)
        os.replace(tmp, p)
    _STATIC[n] = (nv, nc, body)
    return _STATIC[n]

def fast_dimacs(S, keep=None):
    nv, nc, body = _static(len(S))
    dyn = CNF(S, static=False)
    assert dyn.nv == nv
    cls = [c for c, t in zip(dyn.clauses, dyn.tags) if keep is None or t in keep]
    return f'p cnf {nv} {nc + len(cls)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)

def fast_solve(S, seconds=30, keep=None, workdir=os.path.join(HERE, 'fcnf')):
    os.makedirs(workdir, exist_ok=True)
    path = os.path.join(workdir, f'{os.getpid()}.cnf')
    with open(path, 'w') as f: f.write(fast_dimacs(S, keep))
    r = subprocess.run(['cadical', '-q', '-n', '-t', str(int(seconds)), path], capture_output=True)
    return {10: 'sat', 20: 'unsat'}.get(r.returncode, 'unknown')
