"""Independent check of a CaDiCaL model against its CNF, plus decoding of the block-capacity witness.
Usage: p11_verify.py row n file.cnf file.out"""
import sys, itertools, json
from common import *

K, n, cnf, outf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
val = {}
for line in open(outf):
    if line.startswith('v '):
        for t in line.split()[1:]:
            x = int(t)
            if x: val[abs(x)] = x > 0
bad = 0; ncl = 0
with open(cnf) as f:
    for line in f:
        if line.startswith('p') or line.startswith('c'):
            continue
        lits = [int(t) for t in line.split()[:-1]]
        ncl += 1
        if not any(val.get(abs(l), False) == (l > 0) for l in lits):
            bad += 1
print('clauses', ncl, 'violated', bad)
# decode with the same numbering as p11_blockcap.py
states, rows = load(RES_2650)
S = [tuple(states[i][:4]) for i in rows[K][0]]
cells = [(a, b) for a in range(1, 5) for b in range(1, 7) if (a, b) != (1, 6)]
v = 0
sig = {}
for t in itertools.combinations(range(n), 3):
    v += 1; sig[t] = val[v]
stv = {}
for p in range(n):
    for s in range(len(S)):
        v += 1; stv[(p, s)] = val[v]
labv = {}
for p, q in itertools.combinations(range(n), 2):
    for c in range(len(cells)):
        v += 1; labv[(p, q, c)] = val[v]
state_of = [next(S[s] for s in range(len(S)) if stv[(p, s)]) for p in range(n)]
label_of = {(p, q): cells[next(c for c in range(len(cells)) if labv[(p, q, c)])] for p, q in itertools.combinations(range(n), 2)}
# exact re-check of the semantic constraints from the decoded objects
I = lambda f: {(a, b) for a in range(1, 5) for b in range(1, 7) if b <= f[a - 1]}
ok_dom = all(label_of[(p, q)] in I(state_of[q]) - I(state_of[p]) for p, q in label_of)
ok_inj = len(set(state_of)) == n
ok_growth = all((label_of[(p, q)][1] < label_of[(q, r)][1]) if sig[(p, q, r)] else (label_of[(p, q)][0] < label_of[(q, r)][0])
                for p, q, r in itertools.combinations(range(n), 3))
ok_sign = all(not ((x and not y and z) or (not x and y and not z))
              for i, j, k, l in itertools.combinations(range(n), 4)
              for (x, y, z) in itertools.combinations([sig[(i, j, k)], sig[(i, j, l)], sig[(i, k, l)], sig[(j, k, l)]], 3))
# brute-force octagon check on the abstract triple system: 8 owners whose x-sorted sequence splits into
# a cap and a cup with common endpoints (convex position for points); check via longest chains
def chains_ok():
    # longest cap/cup between i and j through consecutive-triple signs (DP over last edges)
    import functools
    best = 0
    capl = {}; cupl = {}
    for j in range(n):
        for m in range(j):
            for i in range(m + 1):
                pass
    # DP: L[i][m][j] longest cap starting at i with last edge (m,j)
    capL = {}; cupL = {}
    for i in range(n):
        for j in range(i + 1, n):
            capL[(i, i, j)] = 2; cupL[(i, i, j)] = 2
    for i in range(n):
        for m in range(i + 1, n):
            for j in range(m + 1, n):
                c1 = max([capL[(i, l, m)] for l in range(i, m) if (i, l, m) in capL and (l == i or not sig[(l, m, j)]) and (l != i or not sig[(i, m, j)])] or [0])
                c2 = max([cupL[(i, l, m)] for l in range(i, m) if (i, l, m) in cupL and (l == i or sig[(l, m, j)]) and (l != i or sig[(i, m, j)])] or [0])
                if c1: capL[(i, m, j)] = c1 + 1
                if c2: cupL[(i, m, j)] = c2 + 1
    worst = 0
    for i in range(n):
        for j in range(i + 1, n):
            ca = max(v for (a, m, b), v in capL.items() if a == i and b == j)
            cu = max(v for (a, m, b), v in cupL.items() if a == i and b == j)
            worst = max(worst, ca + cu - 2)
    return worst
mx = chains_ok()
print(json.dumps({'row': K, 'n': n, 'states_used': sorted(state_of), 'domain_ok': ok_dom, 'injective': ok_inj,
                  'growth_ok': ok_growth, 'signotope_ok': ok_sign, 'max_cap_plus_cup_vertices': mx}))
json.dump({'row': K, 'n': n, 'states': state_of, 'labels': {f'{p},{q}': label_of[(p, q)] for p, q in label_of},
           'orientation_positive': [list(t) for t in sig if sig[t]]}, open(f'p11_witness_row{K}_n{n}.json', 'w'))
