#!/usr/bin/env python3
"""Extract the triple-orbit and Y values of a CaDiCaL model (v-lines) for gen.py Enc(8, 9, t).
usage: model2json.py SOLVER_OUT t OUT.json"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
t = int(sys.argv[2])
E = gen.Enc(8, 9, t)
need = set(E.tvar.values()) | set(E.Y.values())
val = {}
for line in open(sys.argv[1]):
    if line.startswith('v '):
        for x in line.split()[1:]:
            v = int(x)
            if abs(v) in need:
                val[abs(v)] = v > 0
assert len(val) == len(need), (len(val), len(need))
ph = sorted(range(1, t), key=lambda i: sum(1 for j in range(1, t) if j != i and
                                           (val[E.Y[(j, i)]] if j < i else not val[E.Y[(i, j)]])))
json.dump({'t': t, 'val': {str(k): v for k, v in val.items()}, 'phase_order': ph}, open(sys.argv[3], 'w'))
print('phase order', ph)
