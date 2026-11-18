"""Eager version: one SAT instance with the pool = ALL subsets Delta of [m] (sizes lo..hi).
UNSAT => D(a,n,m) holds for all signotopes on m points.  SAT => exact check of the model."""
import sys, time, itertools, json
import numpy as np
from cegar import Model, find_delta, works
from pysat.solvers import Cadical153
import random
a, n, m, form = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
lo = int(sys.argv[5]) if len(sys.argv) > 5 else 0; hi = int(sys.argv[6]) if len(sys.argv) > 6 else m
t0 = time.time(); M = Model(a, n, m, form == 'strong')
sol = Cadical153(bootstrap_with=M.base + M.wit)
np_ = 0; nl = 0
for d in range(lo, hi + 1):
    for D in itertools.combinations(range(m), d):
        c = M.pool_clause(D); sol.add_clause(c); np_ += 1; nl += len(c)
print('pool clauses', np_, 'literals', nl, 'build %.1fs' % (time.time() - t0), flush=True)
r = sol.solve()
print(a, n, m, form, 'sizes', lo, hi, 'SAT' if r else 'UNSAT', '%.1fs' % (time.time() - t0), flush=True)
if r:
    mod = sol.get_model(); o = np.array([mod[i] > 0 for i in range(M.ntri)])
    caps, gons = M.analyse(o)
    D = find_delta(M, caps, gons, random.Random(1), 'first')
    print('model has', len(caps), 'caps', len(gons), 'gons; exact Delta:', D)
