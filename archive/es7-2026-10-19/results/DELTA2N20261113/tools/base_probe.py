import sys, time
from cegar import Model
from pysat.solvers import Cadical153
a, n = int(sys.argv[1]), int(sys.argv[2])
for m in map(int, sys.argv[3:]):
    t0 = time.time(); M = Model(a, n, m, False)
    with Cadical153(bootstrap_with=M.base) as s:
        r = s.solve()
    print(a, n, m, 'base', 'SAT' if r else 'UNSAT', len(M.base), 'clauses', '%.1fs' % (time.time() - t0), flush=True)
