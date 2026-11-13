"""Delta-reduction test: is there a 4-cap-free Delta with S - Delta free of convex k-gons?
(lazy CP-SAT). Usage: delta_test.py k file [maxsets]"""
import sys, json, time
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import gon_witness, Analysis, orient

def four_caps_within(P, idx):
    """Return one 4-cap (indices into P) inside idx or None."""
    idx = sorted(idx)
    for bi in range(len(idx)):
        for ci in range(bi+1, len(idx)):
            b, c = idx[bi], idx[ci]
            L = [a for a in idx[:bi] if orient(P[a], P[b], P[c]) < 0]
            if not L: continue
            R = [d for d in idx[ci+1:] if orient(P[b], P[c], P[d]) < 0]
            if R: return [L[0], b, c, R[0]]
    return None

def delta(P, k, capfree=4, minimize=True, tlimit=60):
    P = sorted(P); n = len(P)
    hepts = []; caps = []
    t0 = time.time()
    while True:
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for H in hepts: m.AddBoolOr([x[i] for i in H])
        for K in caps: m.Add(sum(x[i] for i in K) <= len(K)-1)
        if minimize: m.Minimize(sum(x))
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlimit; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None, len(hepts), len(caps), s.StatusName(st)
        D = [i for i in range(n) if s.Value(x[i])]
        K = four_caps_within(P, D) if capfree == 4 else None
        rest = [i for i in range(n) if i not in set(D)]
        H = gon_witness([P[i] for i in rest], k) if len(rest) >= k else None
        if K is None and H is None:
            return D, len(hepts), len(caps), 'OK'
        if K is not None: caps.append(K)
        if H is not None: hepts.append([rest[i] for i in H])
        if time.time() - t0 > 600: return None, len(hepts), len(caps), 'TIMEOUT'

if __name__ == '__main__':
    k = int(sys.argv[1]); fn = sys.argv[2]; maxsets = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    for si, P in enumerate(sets[:maxsets]):
        P = [tuple(p) for p in P]
        t0 = time.time()
        D, nh, nc, st = delta(P, k)
        print(si, len(P), st, 'minDelta', len(D) if D else None, 'rows', nh, nc, '%.1fs' % (time.time()-t0), flush=True)
