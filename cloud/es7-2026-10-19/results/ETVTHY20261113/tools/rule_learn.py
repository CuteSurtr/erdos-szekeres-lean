"""Learn a feature-based Delta rule: Delta = {p : feat(p) in F}, F chosen (CP-SAT) so that in every test set
Delta is 4-cap-free and meets every convex k-gon. Lazy clause generation."""
import sys, json, time, random
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, gon_witness, orient

def feats_alpha(A, mode):
    from alphafeat import baek_alpha
    al, ao = baek_alpha(A)
    if mode == 'alpha': return al
    if mode == 'alpha2': return [al[i] + ao[i] for i in range(A.n)]
    if mode == 'mirror': return ao

def feats(A, mode):
    n = A.n
    cm, cp, be, om = A.cap_end, A.cap_start, A.cup_end, A.cup_start
    if mode == 'ccbo': return [(cm[i], cp[i], be[i], om[i]) for i in range(n)]
    if mode == 'ccb': return [(cm[i], cp[i], be[i]) for i in range(n)]
    if mode in ('alpha','alpha2','mirror'): return feats_alpha(A, mode)
    raise ValueError

def find_cap4(P, idx):
    idx = sorted(idx); S = set(idx)
    for bi in range(len(idx)):
        for ci in range(bi+1, len(idx)):
            b, c = idx[bi], idx[ci]
            L = [a for a in idx[:bi] if orient(P[a], P[b], P[c]) < 0]
            if not L: continue
            R = [d for d in idx[ci+1:] if orient(P[b], P[c], P[d]) < 0]
            if R: return (L[0], b, c, R[0])
    return None

def learn(sets, k, mode, tmax=1500):
    data = []
    for P in sets:
        P = sorted(tuple(p) for p in P); A = Analysis(P); data.append((P, feats(A, mode)))
    allf = sorted({f for _, F in data for f in F})
    fid = {f: i for i, f in enumerate(allf)}
    hit = set(); nocap = set()
    t0 = time.time(); it = 0
    while True:
        it += 1
        m = cp_model.CpModel(); y = [m.NewBoolVar('y%d' % i) for i in range(len(allf))]
        for c in hit: m.AddBoolOr([y[i] for i in c])
        for c in nocap: m.AddBoolOr([y[i].Not() for i in c])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE:
            return 'INFEASIBLE', None, len(hit), len(nocap), it
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return s.StatusName(st), None, len(hit), len(nocap), it
        F = {allf[i] for i in range(len(allf)) if s.Value(y[i])}
        new = 0
        for P, Fe in data:
            D = [i for i in range(len(P)) if Fe[i] in F]
            K = find_cap4(P, D)
            if K is not None:
                c = frozenset(fid[Fe[i]] for i in K)
                if c not in nocap: nocap.add(c); new += 1
            rest = [i for i in range(len(P)) if Fe[i] not in F]
            W = gon_witness([P[i] for i in rest], k) if len(rest) >= k else None
            if W is not None:
                c = frozenset(fid[Fe[rest[i]]] for i in W)
                if c not in hit: hit.add(c); new += 1
        if new == 0:
            return 'RULE', sorted(F), len(hit), len(nocap), it
        if time.time() - t0 > tmax:
            return 'TIMEOUT', None, len(hit), len(nocap), it

if __name__ == '__main__':
    k = int(sys.argv[1]); mode = sys.argv[2]; fns = sys.argv[3:]
    sets = []
    for fn in fns:
        sets += [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    st, F, nh, nc, it = learn(sets, k, mode)
    print(st, 'hitclauses', nh, 'capclauses', nc, 'iters', it)
    if F: print('F =', F)
