"""Coupled owner model for a residual support S (discovery only).

Same clause families as experiments/omission-residual32-rank-search-2026-10-10/cnf_export.py
(threshold_monotone, source_cup, empty_direction, domain, order_transitive, growth, fixed_sign,
packet, convex_four), except that no_octagon is complete: every 8-subset of owners gets the clause
"some 4-subset is not convex".  UNSAT of this CNF means: no residual configuration occupies all of S.
"""
import itertools, subprocess, os, tempfile, hashlib, json
from common import STATES, CELLS, N
import numpy as np

# ---- triple table TT (same formulas as model.py / template_search_lib.py)
nonempty = np.zeros((N, N), bool)
mn = np.zeros((2, N, N), np.int16)
mx = np.zeros((2, N, N), np.int16)
for a in range(N):
    for b in range(N):
        d = CELLS[b] - CELLS[a]
        if d:
            nonempty[a, b] = True
            mn[0, a, b] = min(z[0] for z in d); mx[0, a, b] = max(z[0] for z in d)
            mn[1, a, b] = min(z[1] for z in d); mx[1, a, b] = max(z[1] for z in d)
idx = np.arange(N, dtype=np.int16)
A_, B_, C_ = np.meshgrid(idx, idx, idx, indexing='ij')
TT = (A_ != B_) & (B_ != C_) & (A_ != C_)
grids = (A_, B_, C_)
for perm in itertools.permutations(range(3)):
    odd = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3)) % 2
    coord = 1 if odd else 0
    p, q, r = (grids[perm[k]] for k in range(3))
    present = nonempty[p, q] & nonempty[q, r] & nonempty[p, r]
    forced = mx[coord][q, r] <= mn[coord][p, q]
    TT &= (~present) | forced
del A_, B_, C_, grids
DIFF = [[CELLS[b] - CELLS[a] - {(1, 6)} for b in range(N)] for a in range(N)]

def neg(l):
    return (not l) if isinstance(l, bool) else -l


BAD4 = [bits for bits in itertools.product([False, True], repeat=4)
        if sum(x != y for x, y in zip(bits, bits[1:])) > 1]


class CNF:
    def __init__(self, S, octagon='full', static=True):
        self.S = list(S); n = self.n = len(S)
        self.ids = {}; self.nv = 0; self.clauses = []; self.tags = []
        cells = CELLS
        for i, j in itertools.combinations(range(n), 2):
            self.before(i, j)
            for k in range(2, 5): self.ge('cap', i, j, k)
            for k in range(2, 7): self.ge('cup', i, j, k)
        for q in itertools.combinations(range(n), 3): self.orient(q)
        for q in itertools.combinations(range(n), 4): self.convex(q)
        diffs = {(i, j): DIFF[S[i]][S[j]] for i, j in itertools.permutations(range(n), 2)}
        for i, j in itertools.combinations(range(n), 2):
            for typ, maximum in [('cap', 4), ('cup', 6)]:
                if not static: break
                for k in range(2, maximum): self.add([neg(self.ge(typ, i, j, k + 1)), self.ge(typ, i, j, k)])
            for u, v in [(i, j), (j, i)]:
                self.add([-self.before(u, v), neg(self.ge('cup', u, v, STATES[S[u]][0] + 2))], ('source', u, v))
                if not diffs[u, v]:
                    self.add([-self.before(u, v)], ('empty', u, v))
                    continue
                for a in range(1, 5):
                    for b in range(1, 7):
                        if (a, b) in diffs[u, v]: continue
                        self.add([-self.before(u, v), neg(self.ge('cap', i, j, a)), self.ge('cap', i, j, a + 1),
                                  neg(self.ge('cup', i, j, b)), self.ge('cup', i, j, b + 1)], ('domain', u, v, a, b))
        for a, b, c in (itertools.permutations(range(n), 3) if static else ()):
            self.add([-self.before(a, b), -self.before(b, c), self.before(a, c)])
            for typ, maximum, color in [('cap', 4, False), ('cup', 6, True)]:
                o = self.orient((a, b, c))
                gate = [-self.before(a, b), -self.before(b, c), -o if color else o]
                for k in range(1, maximum + 1):
                    self.add(gate + [neg(self.ge(typ, a, b, k)), self.ge(typ, b, c, k + 1)])
        for q in itertools.combinations(range(n), 3):
            a, b, c = [S[i] for i in q]
            if TT[a, b, c]: self.add([self.orient(q)], ('positive', q[0], q[1], q[2]))
            elif TT[a, c, b]: self.add([-self.orient(q)], ('positive', q[0], q[2], q[1]))
        for quad in (itertools.combinations(range(n), 4) if static else ()):
            for q in itertools.permutations(quad):
                order = [-self.before(a, b) for a, b in zip(q, q[1:])]
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
        if octagon == 'full' and static:
            for eight in itertools.combinations(range(n), 8):
                self.add([-self.convex(q) for q in itertools.combinations(eight, 4)])

    def var(self, key):
        v = self.ids.get(key)
        if v is None:
            self.nv += 1; v = self.ids[key] = self.nv
        return v

    def before(self, i, j):
        return self.var(('before', min(i, j), max(i, j))) * (1 if i < j else -1)

    def ge(self, typ, i, j, k):
        maximum = 4 if typ == 'cap' else 6
        if k <= 1: return True
        if k > maximum: return False
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


def solve(S, seconds=60, workdir='/home/jay/research/data/res33-20261113/cnf', keep=False, lrat=False):
    os.makedirs(workdir, exist_ok=True)
    cnf = CNF(S)
    h = hashlib.sha256(bytes(S)).hexdigest()[:12]
    path = os.path.join(workdir, f'S{len(S)}_{h}.cnf')
    with open(path, 'w') as f: f.write(cnf.dimacs())
    cmd = ['cadical', '-q', '-n', '-t', str(int(seconds)), path]
    if lrat:
        cmd = ['cadical', '-q', '-n', '--lrat', '-t', str(int(seconds)), path, path[:-4] + '.lrat']
    r = subprocess.run(cmd, capture_output=True, text=True)
    status = {10: 'sat', 20: 'unsat'}.get(r.returncode, 'unknown')
    if not keep and status != 'unsat':
        os.remove(path)
    return status, path, cnf.nv, len(cnf.clauses)


_STATIC = {}
def _static(n):
    """Untagged (state-independent) clauses for support size n, as DIMACS text, cached on disk."""
    if n in _STATIC: return _STATIC[n]
    p = f'/home/jay/research/data/res33-20261113/static/static_{n}.txt'
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

def fast_dimacs(S):
    nv, nc, body = _static(len(S))
    dyn = CNF(S, static=False)
    assert dyn.nv == nv
    return f'p cnf {nv} {nc + len(dyn.clauses)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c in dyn.clauses)

def fast_solve(S, seconds=30, workdir='/home/jay/research/data/res33-20261113/fcnf'):
    os.makedirs(workdir, exist_ok=True)
    path = os.path.join(workdir, f'{os.getpid()}.cnf')
    with open(path, 'w') as f: f.write(fast_dimacs(S))
    r = subprocess.run(['cadical', '-q', '-n', '-t', str(int(seconds)), path], capture_output=True)
    return {10: 'sat', 20: 'unsat'}.get(r.returncode, 'unknown')
