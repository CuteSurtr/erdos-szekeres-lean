"""Is there a 4-cap-free Delta INSIDE Delta_R = {capend + cupend >= k+2} meeting every convex k-gon? (strong: also k-gon-free)"""
import sys, json, random, time
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from delta_test2 import all_caps4, many_witnesses
from collections import Counter
random.seed(0)
def test(P, k, strong, side):
    P = sorted(P); A = Analysis(P); n = A.n
    if side == 'R': DR = {i for i in range(n) if A.cap_end[i] + A.cup_end[i] >= k + 2}
    elif side == 'L': DR = {i for i in range(n) if A.cap_start[i] + A.cup_start[i] >= k + 2}
    elif side == 'r1': DR = {i for i in range(n) if (A.cap_start[i] + A.cup_start[i] >= k + 2 and A.cap_end[i] <= 3) or (A.cap_end[i] + A.cup_end[i] >= k + 2 and A.cap_start[i] <= 3)}
    else: DR = {i for i in range(n) if A.cap_start[i] + A.cup_start[i] >= k + 2 or A.cap_end[i] + A.cup_end[i] >= k + 2}
    caps = [K for K in all_caps4(P) if all(i in DR for i in K)]
    hit = set(); inside = set(); t0 = time.time()
    while True:
        m = cp_model.CpModel(); x = {i: m.NewBoolVar('x%d' % i) for i in DR}
        for K in caps: m.AddBoolOr([x[i].Not() for i in K])
        for H in hit:
            lits = [x[i] for i in H if i in DR]
            if not lits: return 'INFEASIBLE'
            m.AddBoolOr(lits)
        for H in inside: m.AddBoolOr([x[i].Not() for i in H])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 30; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return 'INFEASIBLE'
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return 'UNKNOWN'
        D = sorted(i for i in DR if s.Value(x[i]))
        W = many_witnesses(P, [i for i in range(n) if i not in set(D)], k)
        Win = many_witnesses(P, D, k) if strong and len(D) >= k else []
        if not W and not Win: return 'OK'
        hit.update(W); inside.update(Win)
        if time.time() - t0 > 120: return 'TIMEOUT'
if __name__ == '__main__':
    k = int(sys.argv[1]); strong = sys.argv[2] == 'strong'; side = sys.argv[3]
    st = Counter()
    for fn in sys.argv[4:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for si, P in enumerate(sets):
            r = test([tuple(p) for p in P], k, strong, side); st[r] += 1
            if r != 'OK': print(fn, si, len(P), r, flush=True)
    print(dict(st))
