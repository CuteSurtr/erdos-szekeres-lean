"""For sets where Delta_R has 4-caps: find a 4-cap-free heptagon-hitting Delta closest to Delta_R; report the exchanges."""
import sys, json, random
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from delta_test2 import all_caps4, many_witnesses
from alphafeat import baek_alpha
random.seed(0)
def closest(P, k=7):
    P = sorted(P); A = Analysis(P); n = A.n
    DR = {i for i in range(n) if A.cap_end[i] + A.cup_end[i] >= k + 2}
    caps = all_caps4(P); hit = set()
    while True:
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for K in caps: m.AddBoolOr([x[i].Not() for i in K])
        for H in hit: m.AddBoolOr([x[i] for i in H])
        m.Minimize(sum(x[i].Not() if i in DR else x[i] for i in range(n)))
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 30; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return None
        D = {i for i in range(n) if s.Value(x[i])}
        W = many_witnesses(P, [i for i in range(n) if i not in D], k)
        if not W: break
        hit.update(W)
    feat = lambda i: (A.cup_end[i], A.cap_end[i], A.cap_start[i], A.cup_start[i])
    dropped = sorted(DR - D); added = sorted(D - DR)
    return n, len(DR), len(D), [(i, feat(i)) for i in dropped], [(i, feat(i)) for i in added]
cnt = 0
for l in open('pool_main.jsonl'):
    P = [tuple(p) for p in json.loads(l)['P']]
    r = closest(P)
    if r and (r[3] or r[4]):
        print('n', r[0], '|DR|', r[1], '|D|', r[2]); print('  dropped (beta,c-,c+,omega):', r[3]); print('  added:', r[4])
        cnt += 1
    if cnt >= 8: break
