#!/usr/bin/env python3
"""Decode and brute-force check a SAT model of m33k7int.sub.cnf.

usage: verify_sat.py <model.txt> [N=33] [K=7]

Expands each orientation variable from its mirror-orbit representative (as mirgen.py
substitutes), then checks independently of the CNF: signotope axioms on every quadruple,
mirror identity X(i,j,k) = X(m-k,m-j,m-i), m = N+1, the axis point (N+1)/2 not extreme, and
the largest subset in convex position (4-point test, exact DFS, tools/trackB/sigcheck.py)
together with the cap/cup DP.  Writes <model>.signotope.txt (x-sorted triples with +/-).
"""
import sys, os, itertools, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../tools/trackB'))
import sigcheck
path = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 33; K = int(sys.argv[3]) if len(sys.argv) > 3 else 7
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
m = N + 1
rep = {v: min(v, idx[tuple(sorted((m - k, m - j, m - i)))]) for (i, j, k), v in idx.items()}
vals = {}
for line in open(path):
    if line.startswith('v '):
        for t in line.split()[1:]:
            v = int(t)
            if v: vals[abs(v)] = v > 0
sig = {t: (1 if vals.get(rep[v], False) else -1) for t, v in idx.items()}
res = {}
ok, bad = sigcheck.is_signotope(sig, N); res['signotope'] = ok; res['signotope_bad_quad'] = bad
res['mirror_violations'] = sum(1 for (i, j, k) in idx if sig[(i, j, k)] != sig[(m - k, m - j, m - i)])
c = (N + 1) // 2
vs = [sig[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
res['axis_not_extreme'] = (1 in vs) and (-1 in vs)
res['X123'] = sig[(1, 2, 3)]
res['max_convex_capcup'] = sigcheck.max_convex_capcup(sig, N)
res['max_convex_4pt'] = sigcheck.max_convex_4pt(sig, N)
res['no_convex_%dgon' % K] = res['max_convex_4pt'] < K and res['max_convex_capcup'] < K
with open(path + '.signotope.txt', 'w') as f:
    f.write('%d\n' % N)
    for t in itertools.combinations(range(1, N + 1), 3): f.write('%d %d %d %s\n' % (t + ('+' if sig[t] > 0 else '-',)))
print(json.dumps(res))
