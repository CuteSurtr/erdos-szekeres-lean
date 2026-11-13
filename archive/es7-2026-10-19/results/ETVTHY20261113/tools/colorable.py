"""Is the 4-cap hypergraph on a subset X of S c-colorable (no monochromatic 4-cap)? (CP-SAT)"""
import sys, json
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from delta_test2 import all_caps4
from collections import Counter

def colorable(P, X, c):
    X = set(X); caps = [K for K in all_caps4(P) if all(i in X for i in K)]
    m = cp_model.CpModel(); col = {i: [m.NewBoolVar(f'c{i}_{j}') for j in range(c)] for i in X}
    for i in X: m.AddExactlyOne(col[i])
    for K in caps:
        for j in range(c): m.AddBoolOr([col[i][j].Not() for i in K])
    if X: m.Add(col[min(X)][0] == 1)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 1
    st = s.Solve(m)
    return s.StatusName(st)

if __name__ == '__main__':
    what = sys.argv[1]; c = int(sys.argv[2]); st = Counter()
    for fn in sys.argv[3:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for si, P in enumerate(sets):
            P = sorted(tuple(p) for p in P); A = Analysis(P); n = A.n
            if what == 'S': X = range(n)
            elif what == 'DR': X = [i for i in range(n) if A.cap_end[i] + A.cup_end[i] >= 9]
            r = colorable(P, X, c); st[r] += 1
            if r != 'OPTIMAL' and r != 'FEASIBLE': print(fn, si, n, r, flush=True)
    print(what, c, dict(st))
