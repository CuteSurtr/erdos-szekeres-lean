"""Strong Delta test (ETV recursion form): Delta 4-cap-free AND free of convex k-gons, meeting every convex k-gon.
Lazy CP-SAT (k-gons inside Delta forbidden lazily)."""
import sys, json, time, random
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import gon_witness
from delta_test2 import all_caps4, many_witnesses

def delta_strong(P, k, tl=30):
    P = sorted(P); n = len(P); caps = all_caps4(P)
    hit = set(); inside = set(); t0 = time.time(); rounds = 0
    while True:
        rounds += 1
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for K in caps: m.AddBoolOr([x[i].Not() for i in K])
        for H in hit: m.AddBoolOr([x[i] for i in H])
        for H in inside: m.AddBoolOr([x[i].Not() for i in H])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return None, 'INFEASIBLE', rounds
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return None, s.StatusName(st), rounds
        D = sorted(i for i in range(n) if s.Value(x[i]))
        rest = [i for i in range(n) if i not in set(D)]
        W = many_witnesses(P, rest, k)
        Win = many_witnesses(P, D, k) if len(D) >= k else []
        if not W and not Win: return D, 'OK', rounds
        hit.update(W); inside.update(Win)
        if time.time() - t0 > 240: return None, 'TIMEOUT', rounds

if __name__ == '__main__':
    random.seed(0); k = int(sys.argv[1])
    from collections import Counter
    st = Counter()
    for fn in sys.argv[2:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for si, P in enumerate(sets):
            D, status, rounds = delta_strong([tuple(p) for p in P], k)
            st[status] += 1
            if status != 'OK': print('NOT OK', fn, si, len(P), status, flush=True)
    print(dict(st))
