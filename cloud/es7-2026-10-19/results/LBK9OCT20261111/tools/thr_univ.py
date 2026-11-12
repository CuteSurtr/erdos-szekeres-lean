"""Exploration: 2-layer threshold forms; which threshold orders are the same for all sampled monotone phase vectors."""
import sys, math, os
import numpy as np
sys.path.insert(0, 'tools'); import lpc8
base = lpc8.Base(16, 'cnf/chord_m8t16.clauses')
rng = np.random.default_rng(3)
nt = base.nt
# 2-layer vars: layers sets of size 2
lays = [sorted(set(base.lay[v])) for v in range(nt + 1)]
two = [v for v in range(1, nt + 1) if len(lays[v]) == 2]
print('2-layer vars', len(two))
NS = 150
C = np.zeros((NS, len(two)))
for s in range(NS):
    th = np.concatenate([[0.0], np.sort(rng.uniform(0, math.pi / 4, 15))])
    A = base.forms(th)
    for q, v in enumerate(two):
        i, j = lays[v]
        a, b = A[v, i], A[v, j]
        # literal 'v true' iff a u_i + b u_j > 0 iff (b>0: rho > -a/b) ; store signed threshold: +c if v-true means rho>c, -c if v-true means rho<c
        c = -a / b
        C[s, q] = c if b > 0 else -c
# per pair, count consistent strict orders among |thresholds| > 1 (free) for all samples
from collections import defaultdict
bypair = defaultdict(list)
for q, v in enumerate(two):
    bypair[tuple(lays[v])].append(q)
tot = cons = 0
for key, qs in bypair.items():
    X = np.abs(C[:, qs]); free = np.all(X > 1.0001, axis=0)
    idx = [qs[k] for k in range(len(qs)) if free[k]]
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            d = np.abs(C[:, idx[a]]) - np.abs(C[:, idx[b]])
            tot += 1
            if np.all(d > 0) or np.all(d < 0):
                cons += 1
print('pairs of always-free 2-layer thresholds on the same layer pair:', tot, 'with a sample-universal order:', cons)
