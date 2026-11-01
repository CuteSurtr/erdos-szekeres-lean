"""Probe 9: diversity of 33-hole residual witnesses (2,650 rows, state 0 occupied).
Random linear objectives over {h feasible, sum h <= 33}; exact replay of every solution found."""
import sys, json, random, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from common import *

runs, secs = int(sys.argv[1]), float(sys.argv[2])
states, rows = load(RES_2650)
n = len(states)
A, b = matrix(n, rows)
from scipy.sparse import vstack, csr_matrix
A2 = vstack([A, csr_matrix(np.ones((1, n)))])
lo = np.concatenate([b, [0]]); hi = np.concatenate([np.full(len(b), np.inf), [33]])
ub = np.ones(n); ub[0] = 0
sols = []
rng = np.random.default_rng(5)
for r in range(runs):
    c = rng.random(n)
    res = milp(c, integrality=np.ones(n), bounds=Bounds(np.zeros(n), ub),
               constraints=[LinearConstraint(A2, lo, hi)], options={'time_limit': secs, 'disp': False})
    if res.x is None:
        print('run', r, 'no solution', res.message); continue
    holes = sorted(i for i in range(n) if res.x[i] > 0.5)
    ok = not check_exact(rows, holes) and 0 not in holes
    sols.append(holes)
    print('run', r, len(holes), 'exact_ok', ok, flush=True)
U = set().union(*map(set, sols)); I = set(sols[0]).intersection(*map(set, sols))
distinct = {tuple(s) for s in sols}
pair = [len(set(a) & set(b_)) for k, a in enumerate(sols) for b_ in sols[k + 1:]]
out = {'solutions': sols, 'distinct': len(distinct), 'union_size': len(U), 'intersection': sorted(I),
       'pairwise_common_min_max': [min(pair), max(pair)] if pair else None}
json.dump(out, open('p9_res_diversity.json', 'w'))
print({k: v for k, v in out.items() if k != 'solutions'})
