"""Independent CNF encoder for the C15 block-capacity question (written from scratch).

n owners 0..n-1 (x-order) occupy n distinct states of the support S of residual row K (source-2650).
Listed conditions (as in C15):
  signotope axioms on o(i,j,k) (true = positive = cup);
  injective owner -> S map;
  labels L(p,q,c), c in [1..4]x[1..6] minus (1,6), with c in I(state q) minus I(state p);
  growth (order encoding Age/Bge): cap => a(p,q) < a(q,r); cup => b(p,q) < b(q,r);
  no 6-cap, no 8-cup, no cap+cup with common endpoints and >= 8 vertices (chains with explicit start).
Optional extra necessary conditions (derived from the Lean rank definitions, see check_extra.py):
  --fcw : a(p,q) = a <= 3  =>  f_{a+1}(state q) <= 5
  --bcw : b(p,q) = b >= 2  =>  f_1(state p) >= b-1
Usage: enc_c15.py K n out.cnf [--fcw] [--bcw]   (writes out.cnf and out.cnf.map.json)
"""
import sys, json, gzip, itertools

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
SRC = (ROOT + '/experiments/'
       'omission-residual32-rank-global-2026-10-10/source-2650.json.gz')
K, n, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
FCW, BCW = '--fcw' in sys.argv, '--bcw' in sys.argv
src = json.load(gzip.open(SRC))
supp = src['constraints'][K]['support']
S = [tuple(src['states'][i][:4]) for i in supp]
CELLS = [(a, b) for a in range(1, 5) for b in range(1, 7) if (a, b) != (1, 6)]
inI = lambda f, a, b: b <= f[a - 1]

nv = 0
def var():
    global nv
    nv += 1
    return nv
clauses = []
add = clauses.append
pairs = list(itertools.combinations(range(n), 2))
o = {t: var() for t in itertools.combinations(range(n), 3)}
x = {(p, s): var() for p in range(n) for s in range(len(S))}
L = {(p, q, c): var() for (p, q) in pairs for c in range(len(CELLS))}
Age = {(p, q, a): var() for (p, q) in pairs for a in range(2, 5)}      # a(p,q) >= a, a=2..4
Bge = {(p, q, b): var() for (p, q) in pairs for b in range(2, 7)}      # b(p,q) >= b, b=2..6
def age(p, q, a):   # returns literal or True/False constant
    return True if a <= 1 else (False if a >= 5 else Age[(p, q, a)])
def bge(p, q, b):
    return True if b <= 1 else (False if b >= 7 else Bge[(p, q, b)])
def clause(*lits):
    """add clause; literals may be True/False constants (True satisfies, False dropped)."""
    out_ = []
    for l in lits:
        if l is True:
            return
        if l is False:
            continue
        out_.append(l)
    assert out_, 'empty clause'
    add(out_)
def neg(l):
    return (not l) if isinstance(l, bool) else -l

# signotope: monotone sequence o(ijk), o(ijl), o(ikl), o(jkl)
for i, j, k, l in itertools.combinations(range(n), 4):
    s = [o[(i, j, k)], o[(i, j, l)], o[(i, k, l)], o[(j, k, l)]]
    for a, b, c in itertools.combinations(range(4), 3):
        add([-s[a], s[b], -s[c]])
        add([s[a], -s[b], s[c]])
# injective state map
for p in range(n):
    add([x[(p, s)] for s in range(len(S))])
    for s1, s2 in itertools.combinations(range(len(S)), 2):
        add([-x[(p, s1)], -x[(p, s2)]])
for s in range(len(S)):
    for p, q in pairs:
        add([-x[(p, s)], -x[(q, s)]])
# labels
for p, q in pairs:
    add([L[(p, q, c)] for c in range(len(CELLS))])
    for c1, c2 in itertools.combinations(range(len(CELLS)), 2):
        add([-L[(p, q, c1)], -L[(p, q, c2)]])
    for c, (a, b) in enumerate(CELLS):
        for s, f in enumerate(S):
            if inI(f, a, b):
                add([-L[(p, q, c)], -x[(p, s)]])
            else:
                add([-L[(p, q, c)], -x[(q, s)]])
            if FCW and a <= 3 and f[a] >= 6:             # f_{a+1}(state q) = 6 forbidden
                add([-L[(p, q, c)], -x[(q, s)]])
            if BCW and b >= 2 and f[0] < b - 1:          # f_1(state p) < b-1 forbidden
                add([-L[(p, q, c)], -x[(p, s)]])
    # order variables, both directions
    for a in range(2, 5):
        ge = [L[(p, q, c)] for c, (a2, b2) in enumerate(CELLS) if a2 >= a]
        add([-Age[(p, q, a)]] + ge)
        for lit in ge:
            add([-lit, Age[(p, q, a)]])
    for b in range(2, 7):
        ge = [L[(p, q, c)] for c, (a2, b2) in enumerate(CELLS) if b2 >= b]
        add([-Bge[(p, q, b)]] + ge)
        for lit in ge:
            add([-lit, Bge[(p, q, b)]])
# growth
for p, q, r in itertools.combinations(range(n), 3):
    for a in range(1, 5):          # cap: a(p,q) >= a  =>  a(q,r) >= a+1
        clause(o[(p, q, r)], neg(age(p, q, a)), age(q, r, a + 1))
    for b in range(1, 7):          # cup: b(p,q) >= b  =>  b(q,r) >= b+1
        clause(-o[(p, q, r)], neg(bge(p, q, b)), bge(q, r, b + 1))
# chains with explicit start: Cap[i,m,j,k] = a cap starting at i, last two vertices m<j, >= k vertices
CAPMAX, CUPMAX = 6, 8
Cap, Cup = {}, {}
for i, m, j in itertools.combinations(range(n), 3):
    for k in range(3, CAPMAX + 1):
        Cap[(i, m, j, k)] = var()
    for k in range(3, CUPMAX + 1):
        Cup[(i, m, j, k)] = var()
for i, m, j in itertools.combinations(range(n), 3):
    add([o[(i, m, j)], Cap[(i, m, j, 3)]])
    add([-o[(i, m, j)], Cup[(i, m, j, 3)]])
    for l in range(i + 1, m):
        for k in range(3, CAPMAX):
            add([-Cap[(i, l, m, k)], o[(l, m, j)], Cap[(i, m, j, k + 1)]])
        for k in range(3, CUPMAX):
            add([-Cup[(i, l, m, k)], -o[(l, m, j)], Cup[(i, m, j, k + 1)]])
CapE, CupE = {}, {}
for i, j in pairs:
    for k in range(3, CAPMAX + 1):
        CapE[(i, j, k)] = var()
        for m in range(i + 1, j):
            add([-Cap[(i, m, j, k)], CapE[(i, j, k)]])
    for k in range(3, CUPMAX + 1):
        CupE[(i, j, k)] = var()
        for m in range(i + 1, j):
            add([-Cup[(i, m, j, k)], CupE[(i, j, k)]])
    add([-CapE[(i, j, 6)]])                       # no 6-cap
    add([-CupE[(i, j, 8)]])                       # no 8-cup (cap = bare edge)
    for k in range(3, 6):                         # cap k + cup (10-k): 8 vertices
        add([-CapE[(i, j, k)], -CupE[(i, j, 10 - k)]])
with open(out, 'w') as fh:
    fh.write(f'p cnf {nv} {len(clauses)}\n')
    for c in clauses:
        fh.write(' '.join(map(str, c)) + ' 0\n')
json.dump({'K': K, 'n': n, 'S': S, 'support': supp, 'cells': CELLS,
           'o': {f'{a},{b},{c}': v for (a, b, c), v in o.items()},
           'x': {f'{p},{s}': v for (p, s), v in x.items()},
           'L': {f'{p},{q},{c}': v for (p, q, c), v in L.items()}}, open(out + '.map.json', 'w'))
print(json.dumps({'K': K, 'n': n, 'fcw': FCW, 'bcw': BCW, 'vars': nv, 'clauses': len(clauses)}))
