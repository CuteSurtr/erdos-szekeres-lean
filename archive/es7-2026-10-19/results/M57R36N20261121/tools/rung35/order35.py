#!/usr/bin/env python3
"""order35.py -- cube split orders for the four N = 35 cases, by the heuristic visible in the r36 driver:
states of the tightened families with index >= 15, sorted by (positive occurrences desc, negative
occurrences desc) of occ[s] in the case CNF (r36: case A = B2 states, case B = S1 states, same key).
Occurrences: base.cnf (shared prefix) + the appended row clauses of the case CNF."""
import sys, os, pickle, collections, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import addrows
OCC0 = 32759
def counts(b, pos, neg):
    for line in b.split(b'\n'):
        if not line or line[:1] in (b'c', b'p'): continue
        for x in line.split()[:-1]:
            l = int(x); a = abs(l)
            if OCC0 <= a < OCC0 + 56:
                (pos if l > 0 else neg)[a - OCC0] += 1
base = open(os.path.join(HERE, 'base.cnf'), 'rb').read()
hdr, body = base.split(b'\n', 1)
pb, nb = collections.Counter(), collections.Counter()
counts(body, pb, nb)
CASES = [('A', 'c35_rle12_qle12', ('B2', 'B1')), ('B', 'c35_rle12_ule22', ('B2', 'S2')),
         ('C', 'c35_tle22_qle12', ('S1', 'B1')), ('D', 'c35_tle22_ule22', ('S1', 'S2'))]
out = {}
for c, name, fams in CASES:
    data = open(os.path.join(HERE, 'run', name + '.cnf'), 'rb').read()
    h, b = data.split(b'\n', 1)
    assert b[:len(body)] == body
    p, n = collections.Counter(pb), collections.Counter(nb)
    pt, nt = collections.Counter(), collections.Counter()
    counts(b[len(body):], pt, nt)
    assert not pt, 'row clauses contain positive occ literals?'
    n.update(nt)
    cand = sorted(set().union(*(set(addrows.family(f, 3, 5)) for f in fams)) - set(range(15)))
    order = sorted(cand, key=lambda s: (-p[s], -n[s]))
    out[c] = order
    print(c, name, 'tightened', fams, 'candidates', len(cand))
    print('  ORDER', order)
    print('  (pos,neg)', [(s, p[s], n[s]) for s in order[:8]])
json.dump(out, open(os.path.join(HERE, 'order35.json'), 'w'))
