"""Rule learning for weak Delta: 4-cap-free Delta meeting every polygon of the given types."""
import sys, json, time
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from rule_learn import find_cap4, feats
from typewit import type_witness

def learn(sets, types, mode, tmax=900):
    data = []
    for P in sets:
        P = sorted(tuple(p) for p in P); A = Analysis(P); data.append((P, feats(A, mode)))
    allf = sorted({f for _, F in data for f in F}); fid = {f: i for i, f in enumerate(allf)}
    hit = set(); nocap = set(); t0 = time.time(); it = 0
    while True:
        it += 1
        m = cp_model.CpModel(); y = [m.NewBoolVar('y%d' % i) for i in range(len(allf))]
        for c in hit: m.AddBoolOr([y[i] for i in c])
        for c in nocap: m.AddBoolOr([y[i].Not() for i in c])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return 'INFEASIBLE', None, len(hit), len(nocap), it
        F = {allf[i] for i in range(len(allf)) if s.Value(y[i])}
        new = 0
        for P, Fe in data:
            D = [i for i in range(len(P)) if Fe[i] in F]
            K = find_cap4(P, D)
            if K is not None:
                c = frozenset(fid[Fe[i]] for i in K)
                if c not in nocap: nocap.add(c); new += 1
            rest = [i for i in range(len(P)) if Fe[i] not in F]
            W = type_witness(P, rest, types)
            if W is not None:
                c = frozenset(fid[Fe[i]] for i in W)
                if c not in hit: hit.add(c); new += 1
        if new == 0: return 'RULE', sorted(F), len(hit), len(nocap), it
        if time.time() - t0 > tmax: return 'TIMEOUT', None, len(hit), len(nocap), it

if __name__ == '__main__':
    types = [tuple(map(int, t.split(','))) for t in sys.argv[1].split(';')]
    mode = sys.argv[2]; sets = []
    for fn in sys.argv[3:]:
        sets += [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    print(learn(sets, types, mode))
