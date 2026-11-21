#!/usr/bin/env python3
"""cover35.py -- coverage check for the 4-case split of rung N = 35 (owner model (3,5,7,35), --nosig).

Uncubed CNF F: base.cnf (= owner.py 3 5 7 35 --names --nosig: clauses of README section 2.2, with the
cardinality family K = "at most 56-35 = 21 holes" = "at least 35 occupied") + addrows rows
S1<=25, S2<=25, B1<=16, B2<=16, ALL<=35.  ALL<=35 is "at most 35 of the 56 occ variables true"
(sequential counter over occ[0..55]); with K it makes "exactly 35 occupied".

Counts of occupied states: r = #B2 = {f1 = 5} (21 states), t = #S1 = {f1 <= 4} (35 states),
q = #B1 = {f3 = 0} (21 states), u = #S2 = {f3 >= 1} (35 states).  With exactly 35 occupied:
r + t = 35 and q + u = 35, so the four rows of F give 10 <= r <= 16 and 10 <= q <= 16.

Cases (each replaces two bounds of F by smaller ones, nothing else):
  A c35_rle12_qle12 : B2<=12, B1<=12     (r <= 12, q <= 12)
  B c35_rle12_ule22 : B2<=12, S2<=22     (r <= 12, q >= 13)
  C c35_tle22_qle12 : S1<=22, B1<=12     (r >= 13, q <= 12)
  D c35_tle22_ule22 : S1<=22, S2<=22     (r >= 13, q >= 13)

Checks:
 (1) re-derive the four families; S1|B2 and B1|S2 are partitions of the 56 states; every row family
     is a union of the four blocks X = B2&B1, Y = B2&S2, Z = S1&B1, W = S1&S2 (so the rows depend only
     on the block counts);
 (2) arithmetic: every block-count vector (x,y,z,w), 0 <= x <= |X|, ..., x+y+z+w = 35, that satisfies
     the rows of F satisfies the rows of at least one case (and here: of exactly one);
 (3) the row specifications written into each case CNF (.names.pkl) equal F's except for the two
     stated bounds; the families stored there equal the re-derived ones; N, CA, CB, G = 35, 3, 5, 7;
 (4) each case CNF (and F) = header + base.cnf body byte for byte + appended row clauses; header
     counts consistent;
 (5) the appended clauses of each row mention only occ variables of its family and its own counter
     variables, and they say exactly "at most K": for random occupancy vectors with <= K occupied the
     standard counter values satisfy every clause; for vectors with K+1 or more occupied, unit
     propagation of the row clauses alone reaches a conflict (also for every vector with K+1 occupied
     drawn at random, 300 per row);
 (6) the base family K: clauses on the cnt variables say "at least 35 occupied" (same test, on holes).
"""
import sys, os, pickle, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cat_common, addrows

N = 35
CA, CB, G = 3, 5, 7
states = cat_common.make(CA, CB)[0]
NS = len(states)
fam = {k: set(addrows.family(k, CA, CB)) for k in ('S1', 'S2', 'B1', 'B2', 'ALL')}
# ---- (1)
assert fam['S1'] | fam['B2'] == set(range(NS)) and not fam['S1'] & fam['B2'], 'S1/B2 not a partition'
assert fam['B1'] | fam['S2'] == set(range(NS)) and not fam['B1'] & fam['S2'], 'B1/S2 not a partition'
assert fam['ALL'] == set(range(NS))
for k, f in (('S1', lambda s: s[0] <= 4), ('B2', lambda s: s[0] == 5), ('B1', lambda s: s[2] == 0), ('S2', lambda s: s[2] >= 1)):
    assert fam[k] == {i for i, s in enumerate(states) if f(s)}, k
X = fam['B2'] & fam['B1']; Y = fam['B2'] & fam['S2']; Z = fam['S1'] & fam['B1']; W = fam['S1'] & fam['S2']
blocks = {'X': X, 'Y': Y, 'Z': Z, 'W': W}
assert X | Y | Z | W == set(range(NS)) and sum(map(len, (X, Y, Z, W))) == NS
comp = {'S1': 'ZW', 'B2': 'XY', 'B1': 'XZ', 'S2': 'YW', 'ALL': 'XYZW'}
for k, bl in comp.items():
    assert fam[k] == set().union(*(blocks[b] for b in bl)), k
print('(1) families: |S1|,|B2|,|B1|,|S2| =', len(fam['S1']), len(fam['B2']), len(fam['B1']), len(fam['S2']),
      '; blocks |X|,|Y|,|Z|,|W| =', len(X), len(Y), len(Z), len(W), 'OK')

BASE_ROWS = {'S1': 25, 'S2': 25, 'B1': 16, 'B2': 16, 'ALL': N}
CASES = [('A', 'c35_rle12_qle12', {'B2': 12, 'B1': 12}),
         ('B', 'c35_rle12_ule22', {'B2': 12, 'S2': 22}),
         ('C', 'c35_tle22_qle12', {'S1': 22, 'B1': 12}),
         ('D', 'c35_tle22_ule22', {'S1': 22, 'S2': 22})]
want = {}
for c, name, ch in CASES:
    w = dict(BASE_ROWS)
    for k, v in ch.items():
        assert v < BASE_ROWS[k], 'a case must only tighten'
        w[k] = v
    assert len(ch) in (1, 2)
    want[name] = w

# ---- (2)
def counts(x, y, z, w):
    return {'S1': z + w, 'B2': x + y, 'B1': x + z, 'S2': y + w, 'ALL': x + y + z + w}
nvec = 0; cover = {c: set() for c, _, _ in CASES}; mult = {}
for x in range(len(X) + 1):
    for y in range(len(Y) + 1):
        for z in range(len(Z) + 1):
            w = N - x - y - z
            if not 0 <= w <= len(W):
                continue
            cn = counts(x, y, z, w)
            if not all(cn[k] <= BASE_ROWS[k] for k in BASE_ROWS):
                continue
            nvec += 1
            hit = [c for c, name, _ in CASES if all(cn[k] <= want[name][k] for k in want[name])]
            assert hit, ('uncovered', x, y, z, w, cn)
            mult[len(hit)] = mult.get(len(hit), 0) + 1
            for c in hit:
                cover[c].add((cn['B2'], cn['B1']))
rq = sorted({p for s in cover.values() for p in s})
print('(2) block-count vectors satisfying the rows of F:', nvec, '; covered by exactly k cases:', mult)
print('    (r,q) range of F:', 'r in', sorted({p[0] for p in rq}), 'q in', sorted({p[1] for p in rq}))
for c, name, ch in CASES:
    rs = sorted({p[0] for p in cover[c]}); qs = sorted({p[1] for p in cover[c]})
    print('    case', c, name, 'tightens', ch, '-> (r,q) cells', len(cover[c]), 'r in', rs, 'q in', qs)

# ---- (3)-(6)
def read_cnf(path):
    with open(path, 'rb') as f:
        hdr = f.readline()
        body = f.read()
    p, cnf, nv, nc = hdr.split()
    return int(nv), int(nc), body

def parse(b):
    cls = []
    for line in b.decode().splitlines():
        if not line or line[0] in 'cp':
            continue
        lits = list(map(int, line.split()))
        assert lits[-1] == 0
        cls.append(lits[:-1])
    return cls

def up_conflict(clauses, assign):
    """unit propagation; assign: dict var -> bool (modified).  True iff a conflict is reached."""
    changed = True
    while changed:
        changed = False
        for cl in clauses:
            unassigned = None; nun = 0; sat = False
            for l in cl:
                v = assign.get(abs(l))
                if v is None:
                    nun += 1; unassigned = l
                elif v == (l > 0):
                    sat = True; break
            if sat:
                continue
            if nun == 0:
                return True
            if nun == 1:
                assign[abs(unassigned)] = unassigned > 0; changed = True
    return False

def check_counter(clauses, xs, cvar, K, label, rng, neg=False):
    """xs: list of occ variables in counter order; cvar[(i,j)] counter variables; row = at most K of
    the literals (occ, or -occ if neg) true."""
    allowed = set(xs) | set(cvar.values())
    for cl in clauses:
        assert all(abs(l) in allowed for l in cl), (label, 'foreign variable', cl)
    m = len(xs)
    def lit_true(vec, i):
        return vec[i] if not neg else not vec[i]
    ntests = 0
    for trial in range(300):
        for over in (False, True):
            if over:
                k = K + 1 + (0 if trial < 200 else rng.randrange(0, m - K)) if K < m else None
            else:
                k = rng.randrange(0, K + 1) if trial >= 3 else (0, K, min(K, m))[trial]
            if k is None or k > m:
                continue
            on = set(rng.sample(range(m), k))
            vec = [((i in on) if not neg else (i not in on)) for i in range(m)]
            if not over:
                a = {xs[i]: vec[i] for i in range(m)}
                pref = 0
                for i in range(1, m + 1):
                    pref += lit_true(vec, i - 1)
                    for j in range(1, min(i, K) + 1):
                        if (i, j) in cvar:
                            a[cvar[(i, j)]] = pref >= j
                for cl in clauses:
                    assert any(a[abs(l)] == (l > 0) for l in cl), (label, 'semantic counter violates', cl, k)
            else:
                a = {xs[i]: vec[i] for i in range(m)}
                assert up_conflict(clauses, a), (label, 'no UP conflict with', k, 'true')
            ntests += 1
    return ntests

base_nv, base_nc, base_body = read_cnf(os.path.join(HERE, 'base.cnf'))
bmeta = pickle.load(open(os.path.join(HERE, 'base.cnf.names.pkl'), 'rb'))
assert (bmeta['N'], bmeta['CA'], bmeta['CB'], bmeta['G']) == (N, CA, CB, G)
bnames = bmeta['names']
assert len(bnames) == base_nv
occv = [bnames[('occ', s)] for s in range(NS)]
rng = random.Random(20261121)
# (6) base cardinality family K (cnt variables) = at most 21 holes
cntv = {(k[1], k[2]): v for k, v in bnames.items() if k[0] == 'cnt'}
cntset = set(cntv.values())
assert NS - N > 0 and cntset == set(range(min(cntset), base_nv + 1)), 'cnt variables are not the top block'
T = min(cntset)
kcl = []; units = set(); nbody = 0
for line in base_body.split(b'\n'):           # streaming scan of all base clauses
    if not line or line[:1] in (b'c', b'p'):
        continue
    nbody += 1
    lits = list(map(int, line.split()))
    assert lits[-1] == 0
    lits.pop()
    if len(lits) == 1:
        units.add(lits[0])
    if any(abs(l) >= T for l in lits):
        kcl.append(lits)
assert nbody == base_nc
n6 = check_counter(kcl, occv, cntv, NS - N, 'base K (holes)', rng, neg=True)
print('(6) base family K: %d clauses on %d cnt variables = "at most %d holes" = "at least %d occupied": %d tests OK'
      % (len(kcl), len(cntv), NS - N, N, n6))
# (not needed for coverage) the F units occ[0], occ[1]
print('    unit clauses in base:', sorted(units), '(occ[0], occ[1] =', occv[0], occv[1], ')')

for name in ['c35_full'] + [n for _, n, _ in CASES]:
    path = os.path.join(HERE, 'run', name + '.cnf')
    meta = pickle.load(open(path + '.names.pkl', 'rb'))
    rows = {k: v[1] for k, v in meta['rows'].items()}
    w = BASE_ROWS if name == 'c35_full' else want[name]
    assert rows == w, (name, rows, w)
    assert (meta['N'], meta['CA'], meta['CB'], meta['G']) == (N, CA, CB, G)
    for k, (fm, K) in meta['rows'].items():
        assert fm == addrows.family(k, CA, CB), (name, k)
        assert set(fm) == fam[k]
    nv, nc, body = read_cnf(path)
    assert body[:len(base_body)] == base_body, (name, 'base body differs')
    tail = parse(body[len(base_body):])
    assert nc == base_nc + len(tail), (name, 'clause count')
    names = meta['names']
    assert nv == len(names), (name, 'variable count')
    for k0, v in bnames.items():
        assert names[k0] == v
    ntot = 0
    for k, (fm, K) in meta['rows'].items():
        cv = {(kk[2], kk[3]): v for kk, v in names.items() if kk[0] == 'rc' and kk[1] == k}
        cs = set(cv.values())
        assert all(v > base_nv for v in cs)
        cl_k = [cl for cl in tail if any(abs(l) in cs for l in cl) or (K == 0 and len(cl) == 1)]
        ntot += len(cl_k)
        xs = [occv[s] for s in fm]
        check_counter(cl_k, xs, cv, K, name + ':' + k, rng)
    assert ntot == len(tail), (name, 'appended clauses not all attributed to rows', ntot, len(tail))
    print('(3-5)', name, 'rows', rows, '| vars', nv, 'clauses', nc, '= base', base_nc, '+', len(tail),
          '| prefix = base.cnf body | row clauses say "at most K" (UP/semantic tests) OK')
print('COVER OK: every assignment of F (exactly 35 occupied, rows S1<=25 S2<=25 B1<=16 B2<=16) satisfies the rows '
      'of at least one of the cases A, B, C, D (in fact of exactly one); each case CNF is F with only the stated '
      'bounds lowered.')
