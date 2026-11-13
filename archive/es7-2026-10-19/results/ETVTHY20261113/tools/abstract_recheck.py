"""Re-decide an abstract (signotope) instance with more rounds and several witnesses per round."""
import sys, random, time
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from abstract_conj import sample, caps4, weak_gon_witness
from ortools.sat.python import cp_model

def many(n, sg, idx, k, reps=10):
    out = []; pts = list(idx); rnd = random.Random(len(idx))
    for r in range(reps):
        W = weak_gon_witness(n, sg, pts, k, True)
        if W is None: break
        out.append(tuple(W)); drop = rnd.choice(W); pts = [i for i in pts if i != drop]
    return out

def decide(n, sg, k=7, strong=True, maxit=5000):
    caps = caps4(n, sg, range(n)); hit = set(); inside = set()
    for it in range(maxit):
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for K in caps: m.AddBoolOr([x[i].Not() for i in K])
        for H in hit: m.AddBoolOr([x[i] for i in H])
        for H in inside: m.AddBoolOr([x[i].Not() for i in H])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return 'INFEASIBLE', it, len(hit), len(inside)
        D = [i for i in range(n) if s.Value(x[i])]
        W = many(n, sg, [i for i in range(n) if i not in set(D)], k)
        Win = many(n, sg, D, k) if strong else []
        if not W and not Win: return 'OK', it, len(hit), len(inside)
        hit.update(W); inside.update(Win)
    return 'ROUNDS', it, len(hit), len(inside)

if __name__ == '__main__':
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time(); sg = sample(n, True, seed)
    print(n, seed, decide(n, sg), '%.0fs' % (time.time() - t0), flush=True)
