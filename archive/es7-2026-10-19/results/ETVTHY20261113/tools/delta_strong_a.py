"""Strong Delta test for general cap size a: Delta (a-1)-cap-free AND convex-k-gon-free, meeting every convex k-gon,
in an a-cap-free set without convex (k+1)-gons. Lazy CP-SAT for both caps and k-gons."""
import sys, json, time, random
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import gon_witness, Analysis, orient
from delta_test2 import many_witnesses

def cap_witness(P, idx, L):
    """An L-cap inside idx (indices into sorted P), or None."""
    idx = sorted(idx)
    if len(idx) < L: return None
    Q = [P[i] for i in idx]; n = len(Q)
    # DP longest cap ending with edge, with back pointers
    E = {}; B = {}
    for j in range(n):
        for i in range(j):
            E[i, j] = 2; B[i, j] = None
            for h in range(i):
                if orient(Q[h], Q[i], Q[j]) < 0 and E[h, i] + 1 > E[i, j]: E[i, j] = E[h, i] + 1; B[i, j] = h
            if E[i, j] >= L:
                ch = [j, i]; a, b = i, j
                while len(ch) < L: h = B[a, b]; ch.append(h); b = a; a = h
                return [idx[t] for t in ch]
    return None

def delta_strong_a(P, k, a, tl=30):
    P = sorted(P); n = len(P)
    hit = set(); inside = set(); capc = set(); t0 = time.time()
    while True:
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for H in hit: m.AddBoolOr([x[i] for i in H])
        for H in inside | capc: m.AddBoolOr([x[i].Not() for i in H])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return None, 'INFEASIBLE'
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return None, s.StatusName(st)
        D = sorted(i for i in range(n) if s.Value(x[i]))
        rest = [i for i in range(n) if i not in set(D)]
        W = many_witnesses(P, rest, k); Win = many_witnesses(P, D, k) if len(D) >= k else []
        C = cap_witness(P, D, a - 1)
        if not W and not Win and C is None: return D, 'OK'
        hit.update(W); inside.update(Win)
        if C is not None: capc.add(tuple(sorted(C)))
        if time.time() - t0 > 240: return None, 'TIMEOUT'

if __name__ == '__main__':
    random.seed(0); k = int(sys.argv[1]); a = int(sys.argv[2])
    from collections import Counter
    st = Counter()
    for fn in sys.argv[3:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for si, P in enumerate(sets):
            D, status = delta_strong_a([tuple(p) for p in P], k, a)
            st[status] += 1
            if status != 'OK': print('NOT OK', fn, si, len(P), status, flush=True)
    print(dict(st))
