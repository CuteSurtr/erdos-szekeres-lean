#!/usr/bin/env python3
"""rows-search exact control for the witness rows and the early-point rows (own code, exact integers).
For every point v and every corner (a,b) of f_v: some u < v has labels exactly (a,b), and f_u satisfies
R_1 >= a-1, f_u(0) >= b-1, f_u(a-1) <= b-1. For the j-th point: every corner (a,b) of its state has a + b <= j.
usage: wit_control.py NSUB SEED"""
import sys, random
sys.path.insert(0, '<scratch>/agents/rows-search')
from chain_control import cupcap, labels, states, R
from witness_rows import corners
nsub, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
X = cupcap(7, 7); st = dict(sets=0, corners=0, early=0, maxn=0)
for t in range(nsub):
    Q = sorted(p for p in X if rng.random() < rng.uniform(0.06, 0.25))
    if len(Q) < 6: continue
    n = len(Q); cap, cup, _, _ = labels(Q); F = states(n, cap, cup)
    assert len(set(F)) == n
    for v in range(n):
        for a, b in corners(F[v]):
            assert a + b <= v + 1, 'early fails'; st['early'] += 1
            ws = [u for u in range(v) if cap[u][v] == a and cup[u][v] == b]
            assert ws, 'corner not attained exactly'
            assert any(R(F[u], 1) >= a - 1 and F[u][0] >= b - 1 and F[u][a - 1] <= b - 1 for u in ws), 'witness fails'
            assert all(R(F[u], 1) >= a - 1 and F[u][0] >= b - 1 and F[u][a - 1] <= b - 1 for u in ws), 'witness fails (all)'
            st['corners'] += 1
    st['sets'] += 1; st['maxn'] = max(st['maxn'], n)
print('DONE', st, flush=True)
