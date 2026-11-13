"""Test the Delta-reduction conjecture on ABSTRACT configurations (signotopes, or arbitrary triple colourings):
sample a configuration with no 5-cap and no weak octagon by SAT (random phases), then search a 4-cap-free Delta
meeting every weak heptagon (lazy CP-SAT). Weak (a,b)-gon = a-cap and b-cup with common endpoints."""
import sys, itertools, random, time, json
sys.path.insert(0, '/home/jay/research/data/theory310-20261113')
from pysat.solvers import Cadical153

def encode(n, signotope=True, maxcap=4, maxcup=7, gon=8):
    nv = 0
    def new():
        nonlocal nv; nv += 1; return nv
    O = {t: new() for t in itertools.combinations(range(n), 3)}
    SU = {b: {t: new() for t in itertools.combinations(range(n), 3)} for b in range(3, maxcup + 1)}
    SC = {b: {t: new() for t in itertools.combinations(range(n), 3)} for b in range(3, maxcap + 1)}
    pairs = list(itertools.combinations(range(n), 2))
    U = {b: {p: new() for p in pairs} for b in range(3, maxcup + 1)}
    K = {a: {p: new() for p in pairs} for a in range(3, maxcap + 1)}
    cl = []
    if signotope:
        for i, j, k, l in itertools.combinations(range(n), 4):
            seq = [O[(i, j, k)], O[(i, j, l)], O[(i, k, l)], O[(j, k, l)]]
            for a, b, c in itertools.combinations(range(4), 3):
                x, y, z = seq[a], seq[b], seq[c]
                cl.append((-x, y, -z)); cl.append((x, -y, z))
    for s, j, k in itertools.combinations(range(n), 3):
        cl.append((-O[(s, j, k)], SU[3][(s, j, k)])); cl.append((O[(s, j, k)], SC[3][(s, j, k)]))
    for s, i, j, k in itertools.combinations(range(n), 4):
        o = O[(i, j, k)]
        for b in range(4, maxcup + 1): cl.append((-SU[b - 1][(s, i, j)], -o, SU[b][(s, j, k)]))
        cl.append((-SU[maxcup][(s, i, j)], -o))
        for a in range(4, maxcap + 1): cl.append((-SC[a - 1][(s, i, j)], o, SC[a][(s, j, k)]))
        cl.append((-SC[maxcap][(s, i, j)], o))
    for s, j, t in itertools.combinations(range(n), 3):
        for b in range(3, maxcup + 1): cl.append((-SU[b][(s, j, t)], U[b][(s, t)]))
        for a in range(3, maxcap + 1): cl.append((-SC[a][(s, j, t)], K[a][(s, t)]))
    for p in pairs:
        for a in range(3, maxcap + 1):
            b = gon + 2 - a
            if 3 <= b <= maxcup: cl.append((-K[a][p], -U[b][p]))
    return O, cl

def sample(n, signotope, seed):
    O, cl = encode(n, signotope)
    rnd = random.Random(seed)
    with Cadical153(bootstrap_with=cl) as s:
        # random phases via assumptions on a random subset of orientation variables (soft: retry without)
        vars_ = list(O.values()); rnd.shuffle(vars_)
        assum = [v if rnd.random() < 0.5 else -v for v in vars_[:len(vars_)//12]]
        ok = s.solve(assumptions=assum)
        if not ok: ok = s.solve()
        if not ok: return None
        m = set(l for l in s.get_model() if l > 0)
    return {t: (1 if O[t] in m else -1) for t in O}   # +1 = cup, -1 = cap

def chains_abs(n, sg, idx):
    """capB/cupB between endpoints inside index subset idx (sorted)."""
    idx = sorted(idx); m = len(idx)
    capB = {}; cupB = {}
    for si in range(m):
        Dc = {}; Du = {}
        for tj in range(si+1, m): Dc[si, tj] = 2; Du[si, tj] = 2
        for tj in range(si+1, m):
            for ti in range(si+1, tj):
                bc = bu = 0
                for h in range(si, ti):
                    o = sg[(idx[h], idx[ti], idx[tj])]
                    if o < 0 and Dc.get((h, ti), 0): bc = max(bc, Dc[h, ti] + 1)
                    if o > 0 and Du.get((h, ti), 0): bu = max(bu, Du[h, ti] + 1)
                Dc[ti, tj] = bc; Du[ti, tj] = bu
        for tj in range(si+1, m):
            capB[si, tj] = max(Dc.get((ti, tj), 0) for ti in range(si, tj))
            cupB[si, tj] = max(Du.get((ti, tj), 0) for ti in range(si, tj))
    return idx, capB, cupB

def chain_vertices(n, sg, idx, s, t, length, sign):
    """Reconstruct a chain (indices into idx) from s to t with exactly `length` points."""
    D = {}; B = {}
    for j in range(s+1, t+1): D[s, j] = 2; B[s, j] = None
    for j in range(s+1, t+1):
        for i in range(s+1, j):
            best = 0; bp = None
            for h in range(s, i):
                if D.get((h, i), 0) and (sg[(idx[h], idx[i], idx[j])] > 0) == (sign > 0):
                    if D[h, i] + 1 > best: best = D[h, i] + 1; bp = h
            D[i, j] = best; B[i, j] = bp
    cands = [(D[i, t], i) for i in range(s, t) if D.get((i, t), 0) >= length]
    L, i = max(cands); ch = [t, i]; j = t
    while i != s: h = B[i, j]; ch.append(h); j = i; i = h
    ch = ch[::-1]
    while len(ch) > length: ch.pop(1)   # sub-chains of signotope chains are chains
    return ch

def weak_gon_witness(n, sg, idx, k, signotope):
    idx2, capB, cupB = chains_abs(n, sg, idx)
    for (s, t), a in capB.items():
        b = cupB[s, t]
        if a + b - 2 >= k:
            aa = min(a, k); bb = k + 2 - aa
            if bb < 2: aa = k; bb = 2
            if not signotope:   # without signotope axioms sub-chains need not be chains: take exact lengths if available
                pass
            K = chain_vertices(n, sg, idx2, s, t, aa, -1); D = chain_vertices(n, sg, idx2, s, t, bb, +1)
            return sorted({idx2[i] for i in K} | {idx2[i] for i in D})
    return None

def caps4(n, sg, idx):
    idx = sorted(idx); out = []
    for b, c in itertools.combinations(idx, 2):
        L = [a for a in idx if a < b and sg[(a, b, c)] < 0]
        if not L: continue
        R = [d for d in idx if d > c and sg[(b, c, d)] < 0]
        for a in L:
            for d in R: out.append((a, b, c, d))
    return out

def delta_abs(n, sg, k=7, strong=False, signotope=True):
    from ortools.sat.python import cp_model
    caps = caps4(n, sg, range(n)); hit = []; inside = []
    for it in range(400):
        m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
        for K in caps: m.AddBoolOr([x[i].Not() for i in K])
        for H in hit: m.AddBoolOr([x[i] for i in H])
        for H in inside: m.AddBoolOr([x[i].Not() for i in H])
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 30; s.parameters.num_workers = 1
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return 'INFEASIBLE', it
        D = [i for i in range(n) if s.Value(x[i])]
        W = weak_gon_witness(n, sg, [i for i in range(n) if i not in set(D)], k, signotope)
        Win = weak_gon_witness(n, sg, D, k, signotope) if strong and len(D) >= 3 else None
        if W is None and Win is None: return 'OK', it
        if W is not None: hit.append(W)
        if Win is not None: inside.append(Win)
    return 'ROUNDS', it

if __name__ == '__main__':
    n = int(sys.argv[1]); signotope = sys.argv[2] == 'sig'; reps = int(sys.argv[3]); seed0 = int(sys.argv[4])
    for r in range(reps):
        t0 = time.time(); sg = sample(n, signotope, seed0 + r)
        if sg is None: print('UNSAT sample', n); break
        st_w, itw = delta_abs(n, sg, 7, False, signotope)
        st_s, its = delta_abs(n, sg, 7, True, signotope)
        print(n, 'sig' if signotope else 'gen', 'seed', seed0 + r, 'weak', st_w, itw, 'strong', st_s, its, '%.0fs' % (time.time()-t0), flush=True)
