"""Directed search for a REAL FL(5,5) set on 14 points without a strong (Pascal) split:
annealing over real 14-point sets of the class, minimizing the number of valid strong splits
(counted exactly over all 2^14 partitions with numpy bitmask tests).
usage: real_nosplit_anneal.py seed steps out.json"""
import sys, random, json, itertools, time, math
import numpy as np
from esgeo import Analysis
import anneal_ab
a, b, n = 5, 5, 14
seed, steps, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed)
ALL = np.arange(1 << n, dtype=np.int64); FULL = (1 << n) - 1
T3 = list(itertools.combinations(range(n), 3)); T4 = list(itertools.combinations(range(n), 4))
def valid(P):
    try: A = Analysis(P)
    except ValueError: return False
    if A.capB.max() > a - 1 or A.cupB.max() > b - 1: return False
    return not ((A.capB >= a - 1) & (A.cupB >= b - 1)).any()
def count_splits(P):
    P = sorted(P)
    sg = {}
    for (i, j, k) in T3:
        sg[i, j, k] = 1 if (P[j][0]-P[i][0])*(P[k][1]-P[i][1]) - (P[j][1]-P[i][1])*(P[k][0]-P[i][0]) > 0 else -1
    caps4 = [t for t in T4 if sg[t[0], t[1], t[2]] < 0 and sg[t[1], t[2], t[3]] < 0]
    cups4 = [t for t in T4 if sg[t[0], t[1], t[2]] > 0 and sg[t[1], t[2], t[3]] > 0]
    caps3 = [t for t in T3 if sg[t] < 0]; cups3 = [t for t in T3 if sg[t] > 0]
    m = lambda s: sum(1 << p for p in s)
    def gons(caps, cups):
        by = {}
        for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
        return [m(set(c) | set(u)) for c in caps for u in by.get((c[0], c[-1]), [])]
    bad1 = set(m(c) for c in caps4) | set(gons(caps3, cups4))     # must not lie inside S1
    bad2 = set(m(c) for c in cups4) | set(gons(caps4, cups3))     # must not lie inside S2
    ok = np.ones(1 << n, dtype=bool)
    for x in bad1: ok &= (ALL & x) != x
    comp = FULL ^ ALL
    for x in bad2: ok &= (comp & x) != x
    return int(ok.sum())
P = None
T0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.6
if len(sys.argv) > 4 and sys.argv[4] != '-':
    P = [tuple(p) for p in json.load(open(sys.argv[4]))['P']]
else:
    for att in range(50):
        v, Q = anneal_ab.run(a, b, 'size', rng.randrange(10**9), 40000)
        if len(Q) >= n:
            Q = sorted(Q)
            while len(Q) > n: Q.pop(rng.randrange(len(Q)))
            P = Q; break
cur = count_splits(P); best = cur; t0 = time.time(); R = 10**6; acc = 0
print(f'seed {seed}: start with {cur} valid splits', flush=True)
for it in range(steps):
    Tm = T0 * (1 - it / steps) + 0.05
    Q = list(P); k = rng.randrange(n); x, y = Q[k]
    if rng.random() < 0.85:
        s = rng.choice([100, 1000, 10000, 100000, R]); Q[k] = (x + rng.randint(-s, s), y + rng.randint(-s, s))
    else: Q[k] = (rng.randint(-R, R), rng.randint(-R, R))
    if len({q[0] for q in Q}) < n or not valid(Q): continue
    c = count_splits(Q)
    if c <= cur or rng.random() < math.exp((math.log(cur + 1) - math.log(c + 1)) / Tm):
        P, cur = Q, c; acc += 1
        if cur < best:
            best = cur; print(f'seed {seed}: it {it} valid splits {cur} ({time.time()-t0:.0f}s)', flush=True)
            json.dump({'a': a, 'b': b, 'n': n, 'valid_splits': cur, 'P': sorted(P)}, open(f'nosplit_best_{seed}.json', 'w'))
        if cur == 0:
            print('REAL COUNTEREXAMPLE', sorted(P), flush=True)
            json.dump({'a': a, 'b': b, 'n': n, 'P': sorted(P)}, open(out, 'w')); break
print(f'seed {seed}: done, best {best}, accepted {acc}, {time.time()-t0:.0f}s', flush=True)
