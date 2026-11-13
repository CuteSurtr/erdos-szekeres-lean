#!/usr/bin/env python3
"""Encoder B: compare 'chain family satisfied' with brute-force 'no convex K-gon' on random configurations."""
import sys, json, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from validate import layers_to_points, random_layers
from validate_b import assignment, check
from test_bruteforce import has_convex_k
cnf = sys.argv[1]; mp = json.load(open(cnf + '.map.json')); N = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
st = {'free_both': 0, 'kgon_both': 0, 'UNSOUND': 0, 'inexact': 0, 'geom_viol': 0}
for s in range(N):
    layers = random_layers(mp['m'], mp['t'], rng, ['free', 'needle'][s % 2])
    A, mind = assignment(mp, layers)
    if mind < 1e-9:
        continue
    o, c = check(cnf, mp, A)
    pts, lay = layers_to_points(mp['m'], layers)
    kg = has_convex_k(pts, mp['K'])
    st['geom_viol'] += (o > 0)
    if not kg and c == 0: st['free_both'] += 1
    elif kg and c > 0: st['kgon_both'] += 1
    elif not kg: st['UNSOUND'] += 1
    else: st['inexact'] += 1
print(cnf, st)
