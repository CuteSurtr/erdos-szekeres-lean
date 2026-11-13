"""Stronger Delta test: 4-cap-free vertex cover of saturated pairs {(u,v): cap(u,v)+cup(u,v) = k+2}."""
import sys, json, time
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from delta_test2 import all_caps4
from collections import Counter

def cover(P, k, extra=None):
    P = sorted(P); A = Analysis(P); n = A.n
    pairs = [(u, v) for u in range(n) for v in range(u+1, n) if A.capB[u, v] + A.cupB[u, v] >= k + 2]
    caps = all_caps4(P)
    m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
    for u, v in pairs: m.AddBoolOr([x[u], x[v]])
    for K in caps: m.AddBoolOr([x[i].Not() for i in K])
    if extra == 'min': m.Minimize(sum(x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 1
    st = s.Solve(m)
    D = [i for i in range(n) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and s.Value(x[i])]
    return s.StatusName(st), len(pairs), len(caps), D, A

if __name__ == '__main__':
    k = int(sys.argv[1]); st = Counter()
    for fn in sys.argv[2:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for si, P in enumerate(sets):
            P = [tuple(p) for p in P]
            status, npairs, ncaps, D, A = cover(P, k, 'min')
            st[status] += 1
            if status != 'OPTIMAL': print('FAIL', fn, si, len(P), status, npairs, ncaps, flush=True)
    print(dict(st))
