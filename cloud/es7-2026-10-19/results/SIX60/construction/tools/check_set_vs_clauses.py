#!/usr/bin/env python3
"""Exact: compute the encoder's variable assignment (triple orbit signs + phase order Y) of an exact sixfold set given by
integer oblique seeds in the encoding convention, and evaluate clause files on it.  A clause violated by a REAL
configuration is unsound.  Also: encoder A with all 5746 values as unit assumptions must be SAT (chain variables).
Usage: check_set_vs_clauses.py SEEDS.json CLAUSEFILE...   (SEEDS.json from verify_float_config.py, layer order)"""
import sys, json, os, importlib.util, itertools, math
RES = os.environ.get('ES_RESULTS', '<results-dir>')
s = importlib.util.spec_from_file_location('enc', RES + '/C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(6, 8, 10)
seeds = [tuple(map(int, x)) for x in json.load(open(sys.argv[1]))['seeds']]
def rot(p, k):
    for _ in range(k % 6): p = (-p[1], p[0] + p[1])
    return p
pts = [rot(sd, k) for sd in seeds for k in range(6)]
def o2(P, Q, R): return sum(pa * qb - pb * qa for (pa, pb), (qa, qb) in ((P, Q), (Q, R), (R, P)))
val = {}
for T, v in E.tvar.items():
    o = o2(pts[T[0]], pts[T[1]], pts[T[2]]); assert o != 0
    val[v] = o > 0
# convention checks (exact): layer 0 seed on positive real axis; others with a>0, b>0 (angle in (0,60)); radii decreasing
assert seeds[0][1] == 0 and seeds[0][0] > 0
for a, b in seeds[1:]: assert a > 0 and b > 0, 'theta not in (0,60)'
r2 = [a * a + a * b + b * b for a, b in seeds]; assert all(r2[i] > r2[i + 1] for i in range(9))
# phase order exactly: theta_i < theta_j  <=>  det(z_i, z_j) > 0 (both in (0,60)): det in oblique = a_i b_j - b_i a_j
for (i, j), v in E.Y.items():
    ai, bi = seeds[i]; aj, bj = seeds[j]; d = ai * bj - bi * aj; assert d != 0
    val[v] = d > 0
pos = sorted(v for v, t in val.items() if t)
json.dump(pos, open(sys.argv[1].replace('.json', '_model.json'), 'w'))
tot = 0; bad = 0
for f in sys.argv[2:]:
    nb = 0; n = 0; first = None
    for line in open(f):
        if not line.strip() or line[0] in 'cp': continue
        lits = [int(x) for x in line.split()[:-1]]
        if any(abs(l) > 5746 for l in lits): continue
        n += 1
        if not any(val[abs(l)] == (l > 0) for l in lits):
            nb += 1
            if first is None: first = line.strip()
    tot += n; bad += nb
    print('%-80s clauses %8d  VIOLATED %d %s' % (f[-80:], n, nb, ('first: ' + first[:120]) if first else ''), flush=True)
print('TOTAL clauses', tot, 'violated', bad)
