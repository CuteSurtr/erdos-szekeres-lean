import sys, time, itertools, json
sys.path.insert(0, '.')
import etv7, cubes
from pysat.formula import CNF
from pysat.solvers import Solver
n, A, B, G = map(int, sys.argv[1:5])
cnf = sys.argv[5]
tl = float(sys.argv[6]) if len(sys.argv) > 6 else 1e9
F = CNF(from_file=cnf)
tot = 0; res = []
for H, sm in cubes.reduced_hulls(n, A):
    units = [s * etv7.ovar(n, *t) for t, s in cubes.hull_units(n, H)]
    s = Solver(name='cadical153', bootstrap_with=F.clauses)
    for u in units: s.add_clause([u])
    if sm: s.add_clause([-etv7.ovar(n, 0, 1, 2), etv7.ovar(n, n-3, n-2, n-1)])
    t0 = time.time(); r = s.solve(); dt = time.time() - t0
    st = s.accum_stats() if hasattr(s, 'accum_stats') else {}
    tot += dt; res.append((H, r, round(dt, 2)))
    print(H, r, round(dt, 2), flush=True)
    s.delete()
print('TOTAL', round(tot, 1), 'cubes', len(res), 'SAT', sum(1 for x in res if x[1]))
