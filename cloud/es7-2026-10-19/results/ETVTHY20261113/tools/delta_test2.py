"""Delta-reduction test v2: exists Delta, 4-cap-free (or (cap-1)-free), with S - Delta free of convex k-gons?
All 4-caps as hard constraints; k-gons added lazily (several per round). CP-SAT, 1 worker."""
import sys, json, time, random
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import gon_witness, orient

def all_caps4(P):
    n = len(P); out = []
    for b in range(n):
        for c in range(b+1, n):
            L = [a for a in range(b) if orient(P[a], P[b], P[c]) < 0]
            if not L: continue
            R = [d for d in range(c+1, n) if orient(P[b], P[c], P[d]) < 0]
            for a in L:
                for d in R: out.append((a, b, c, d))
    return out

def many_witnesses(P, rest, k, reps=12):
    found = []
    pts = list(rest)
    for r in range(reps):
        W = gon_witness([P[i] for i in pts], k)
        if W is None: break
        H = tuple(pts[i] for i in W); found.append(H)
        drop = random.choice(H); pts = [i for i in pts if i != drop]
    return found

def delta(P, k, minimize=False, tl=30):
    P = sorted(P); n = len(P)
    caps = all_caps4(P)
    hepts = set()
    t0 = time.time(); rounds = 0
    while True:
        rounds += 1
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for K in caps: m.AddBoolOr([x[i].Not() for i in K])
        for H in hepts: m.AddBoolOr([x[i] for i in H])
        if minimize: m.Minimize(sum(x))
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE:
            return None, len(hepts), len(caps), 'INFEASIBLE', rounds
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None, len(hepts), len(caps), s.StatusName(st), rounds
        D = {i for i in range(n) if s.Value(x[i])}
        rest = [i for i in range(n) if i not in D]
        W = many_witnesses(P, rest, k)
        if not W:
            return sorted(D), len(hepts), len(caps), 'OK', rounds
        hepts.update(W)
        if time.time() - t0 > 240: return None, len(hepts), len(caps), 'TIMEOUT', rounds

if __name__ == '__main__':
    random.seed(0)
    k = int(sys.argv[1]); fns = sys.argv[2:]
    for fn in fns:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for si, P in enumerate(sets):
            P = [tuple(p) for p in P]; t0 = time.time()
            D, nh, nc, st, rounds = delta(P, k)
            print(fn, si, len(P), st, '|Delta|', len(D) if D is not None else None, 'kgons', nh, 'caps4', nc, 'rounds', rounds, '%.1fs' % (time.time()-t0), flush=True)
