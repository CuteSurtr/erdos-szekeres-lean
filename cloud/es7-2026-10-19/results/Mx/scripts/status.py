#!/usr/bin/env python3
"""Summarize a leaves.jsonl against its root cube file: closed weight (exact), LRAT coverage."""
import sys, json
from fractions import Fraction
from collections import Counter
cubes = [tuple(int(x) for x in l.split()[1:] if x != '0') for l in open(sys.argv[1]) if l.startswith('a')]
L = {}
for l in open(sys.argv[2]):
    d = json.loads(l); L[tuple(d['cube'])] = d
tot = sum(Fraction(1, 2 ** len(c)) for c in cubes)
closed = Fraction(0); open_w = Fraction(0); nleaf = Counter(); t = 0.0
def walk(c):
    global closed, open_w, t
    d = L.get(c)
    if d is None: open_w += Fraction(1, 2 ** len(c)); nleaf['open'] += 1; return
    t += d['solve_s']
    if d['status'] == 'UNSAT' and d.get('lrat') == 'VERIFIED':
        closed += Fraction(1, 2 ** len(c)); nleaf['unsat_verified'] += 1
    elif d['status'] == 'SPLIT':
        nleaf['split'] += 1
        sub = [tuple(c) + tuple(s) for s in d['children']]
        # weight march refuted while re-splitting counts as closed only after the coverage check
        for s in sub: walk(s)
    else:
        nleaf[d['status']] += 1; open_w += Fraction(1, 2 ** len(c))
for c in cubes: walk(c)
print(json.dumps(dict(root_cubes=len(cubes), root_weight=str(tot), leaves=dict(nleaf),
      closed_weight_of_root=float(closed / tot), open_weight_of_root=float(open_w / tot),
      solver_seconds=round(t, 1), sat=[list(c) for c, d in L.items() if d['status'] == 'SAT'])))
