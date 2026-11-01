"""Probe 8: 'divide by symmetry'.  For a transversal X of the fixed-point-free involution C
(or TC), every feasible h has h(CX) = (h o C)(X) >= min h(X), so sum h >= 2 * min h(X).
Integer exclusion of h(X) <= 32 would give sum h >= 66.  First test: LP value of min h(X)
for natural transversals, and a local search over transversals maximising it."""
import sys, json, random, time
import numpy as np
from scipy.optimize import linprog
from common import *
from sym import perms

states, rows = load(BAL_V2)
n = len(states)
T, C = perms(states)
TC = [C[T[i]] for i in range(n)]
A, b = matrix(n, rows)
base_A, base_b = matrix(n, rows[:2685])


def lpmin(X, AA=A, bb=b):
    c = np.zeros(n); c[list(X)] = 1
    r = linprog(c, A_ub=-AA, b_ub=-bb, bounds=[(0, 1)] * n, method='highs')
    return r.fun


out = {}
for name, P in [('C', C), ('TC', TC)]:
    assert all(P[i] != i for i in range(n))
    pairs = sorted({tuple(sorted((i, P[i]))) for i in range(n)})
    cells = lambda i: sum(states[i])
    # natural transversal: smaller cell count (ties: smaller index)
    X = [min(p, key=lambda i: (cells(i), i)) for p in pairs]
    v = lpmin(X)
    out[name] = {'pairs': len(pairs), 'X_small_cells_lp': v}
    # local search: flip pairs to maximise LP min h(X)
    rng = random.Random(1)
    cur = list(X); best = v; t0 = time.time()
    while time.time() - t0 < 120:
        k = rng.randrange(len(pairs)); a, bb_ = pairs[k]
        trial = list(cur); trial[k] = bb_ if cur[k] == a else a
        tv = lpmin(trial)
        if tv >= best - 1e-9:
            cur, best = trial, tv
    out[name]['local_search_best_lp'] = best
    out[name]['best_X'] = sorted(cur)
    print(name, {k: v for k, v in out[name].items() if k != 'best_X'}, flush=True)
json.dump(out, open('p8_halves.json', 'w'))
