"""a = n = 8 decomposition test on real octagon-free sets: can S be 2-coloured with no monochromatic convex
heptagon? (Lazy CP-SAT, witnesses by the exact C checker.)"""
import sys, json, time, random, os
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import gon_witness, quick

def many(P, idx, k, reps=20, rnd=None):
    out = []; pts = list(idx)
    for r in range(reps):
        if len(pts) < k: break
        W = gon_witness([P[i] for i in pts], k)
        if W is None: break
        H = tuple(pts[i] for i in W); out.append(H)
        drop = rnd.choice(H); pts = [i for i in pts if i != drop]
    return out

def split(P, k=7, tmax=600):
    P = sorted(P); n = len(P); rnd = random.Random(0)
    cons = set(); t0 = time.time(); it = 0
    while True:
        it += 1
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for H in cons:
            m.AddBoolOr([x[i] for i in H]); m.AddBoolOr([x[i].Not() for i in H])
        m.Add(x[0] == 1)
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return 'INFEASIBLE', it, len(cons), None
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return 'UNKNOWN', it, len(cons), None
        A = [i for i in range(n) if s.Value(x[i])]; B = [i for i in range(n) if not s.Value(x[i])]
        W = many(P, A, k, rnd=rnd) + many(P, B, k, rnd=rnd)
        if not W: return 'OK', it, len(cons), (len(A), len(B))
        cons.update(W)
        if time.time() - t0 > tmax: return 'TIMEOUT', it, len(cons), None

if __name__ == '__main__':
    files = sys.argv[1:]
    for fn in files:
        P = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
        g = quick(sorted(P))
        t0 = time.time(); r = split(P)
        print(os.path.basename(fn), len(P), 'gon', g[0], r[0], 'iters', r[1], 'cons', r[2], 'sizes', r[3], '%.0fs' % (time.time() - t0), flush=True)
