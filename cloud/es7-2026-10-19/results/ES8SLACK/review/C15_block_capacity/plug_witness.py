"""Encoder validation: extend a witness JSON to a full assignment of an enc_c15.py CNF (auxiliary
order and chain variables set to their intended meaning) and count violated clauses, classifying
them by type. Usage: plug_witness.py witness.json file.cnf"""
import sys, json, itertools
wf, cnf = sys.argv[1:3]
w = json.load(open(wf))
mp = json.load(open(cnf + '.map.json'))
n = w['n']
assert n == mp['n'] and w['row'] == mp['K']
S = [tuple(s) for s in mp['S']]
cells = [tuple(c) for c in mp['cells']]
pos = set(map(tuple, w['orientation_positive']))
val = {}
for k, v in mp['o'].items():
    val[v] = tuple(map(int, k.split(','))) in pos
for k, v in mp['x'].items():
    p, s = map(int, k.split(','))
    val[v] = tuple(w['states'][p]) == S[s]
for k, v in mp['L'].items():
    p, q, c = map(int, k.split(','))
    val[v] = tuple(w['labels'][f'{p},{q}']) == cells[c]
# reconstruct the numbering of the auxiliary variables exactly as in enc_c15.py
nv = max(val)
pairs = list(itertools.combinations(range(n), 2))
lab = {(p, q): tuple(w['labels'][f'{p},{q}']) for p, q in pairs}
for p, q in pairs:
    for a in range(2, 5):
        nv += 1; val[nv] = lab[(p, q)][0] >= a
for p, q in pairs:
    for b in range(2, 7):
        nv += 1; val[nv] = lab[(p, q)][1] >= b
# NOTE: enc_c15 allocates Age for all pairs, then Bge for all pairs (dict comprehensions in order)
sgn = lambda i, j, k: (i, j, k) in pos
def exact(sign):
    E = {}
    for i, m, j in itertools.combinations(range(n), 3):
        E[(i, m, j)] = set()
    for i, m, j in sorted(itertools.combinations(range(n), 3), key=lambda t: t[2]):
        if sgn(i, m, j) == sign:
            E[(i, m, j)].add(3)
        for l in range(i + 1, m):
            if sgn(l, m, j) == sign:
                E[(i, m, j)] |= {k + 1 for k in E[(i, l, m)]}
    return E
capx, cupx = exact(False), exact(True)
for i, m, j in itertools.combinations(range(n), 3):
    for k in range(3, 7):
        nv += 1; val[nv] = k in capx[(i, m, j)]
    for k in range(3, 9):
        nv += 1; val[nv] = k in cupx[(i, m, j)]
for i, j in pairs:
    for k in range(3, 7):
        nv += 1; val[nv] = any(k in capx[(i, m, j)] for m in range(i + 1, j))
    for k in range(3, 9):
        nv += 1; val[nv] = any(k in cupx[(i, m, j)] for m in range(i + 1, j))
hdr = open(cnf).readline().split()
assert int(hdr[2]) == nv, (hdr, nv)
xvars = set(mp['x'].values()); Lvars = set(mp['L'].values())
bad = 0; kinds = {}
for line in open(cnf):
    if line[0] in 'pc':
        continue
    lits = list(map(int, line.split()))[:-1]
    if not any(val[abs(l)] == (l > 0) for l in lits):
        bad += 1
        kind = 'L-x pair' if len(lits) == 2 and abs(lits[0]) in Lvars and abs(lits[1]) in xvars else 'other'
        kinds[kind] = kinds.get(kind, 0) + 1
print(json.dumps({'witness': wf.split('/')[-1], 'cnf': cnf.split('/')[-1], 'violated': bad, 'kinds': kinds}))
