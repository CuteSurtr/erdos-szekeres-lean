"""For each set: minimum |Delta ∩ L4| over 4-cap-free heptagon-hitting Delta; classes of the L4 points used."""
import sys, json, random
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis
from delta_test2 import all_caps4, many_witnesses
from collections import Counter
random.seed(0)
def run(P, k=7):
    P = sorted(P); A = Analysis(P); n = A.n
    L4 = {i for i in range(n) if A.cap_start[i] == 4}
    caps = all_caps4(P); hit = set()
    while True:
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for K in caps: m.AddBoolOr([x[i].Not() for i in K])
        for H in hit: m.AddBoolOr([x[i] for i in H])
        m.Minimize(sum(x[i] for i in L4) * 100 + sum(x))
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 30; s.parameters.num_workers = 1
        st = s.Solve(m)
        D = {i for i in range(n) if s.Value(x[i])}
        W = many_witnesses(P, [i for i in range(n) if i not in D], k)
        if not W: break
        hit.update(W)
    used = sorted(D & L4)
    cls = [(A.cup_end[i], A.cap_end[i], A.cap_start[i], A.cup_start[i]) for i in used]
    return len(used), cls, len(D)
dist = Counter(); clsc = Counter()
for fn in sys.argv[1:]:
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for P in sets:
        k, cls, nd = run([tuple(p) for p in P]); dist[k] += 1
        for c in cls: clsc[c] += 1
print('min |Delta ∩ L4| distribution:', sorted(dist.items()))
print('classes (beta, c-, c+, omega) of forced L4 points:', clsc.most_common(12))
