"""Search REAL point sets of FL(a,b) with n points that have no strong (Pascal) split.
Random walk over real n-point sets of the class (exact validity at every step); every new order type is
tested with split.split (and a positive answer re-checked by check_split).
usage: real_nosplit_search.py a b n seed steps out.json"""
import sys, random, json, itertools, time, math
import numpy as np
from esgeo import Analysis
import split, anneal_ab
a, b, n, seed, steps, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
rng = random.Random(seed)
def valid(P):
    try: A = Analysis(P)
    except ValueError: return False
    if A.capB.max() > a - 1 or A.cupB.max() > b - 1: return False
    return not ((A.capB >= a - 1) & (A.cupB >= b - 1)).any()
# start: anneal for size until n points
P = None
for att in range(50):
    v, Q = anneal_ab.run(a, b, 'size', rng.randrange(10**9), 40000)
    if len(Q) >= n:
        Q = sorted(Q)
        # drop points while valid (subsets stay in the class)
        while len(Q) > n: Q.pop(rng.randrange(len(Q)))
        P = Q; break
if P is None: raise SystemExit('no start set')
T = list(itertools.combinations(range(n), 3))
def signature(P):
    P = sorted(P)
    return ''.join('+' if (P[j][0]-P[i][0])*(P[k][1]-P[i][1]) - (P[j][1]-P[i][1])*(P[k][0]-P[i][0]) > 0 else '-' for i, j, k in T)
seen = set(); tested = 0; t0 = time.time(); R = 10**6
for it in range(steps):
    Q = list(P); k = rng.randrange(n); x, y = Q[k]
    r = rng.random()
    if r < 0.8:
        s = rng.choice([100, 1000, 10000, 100000, R]); Q[k] = (x + rng.randint(-s, s), y + rng.randint(-s, s))
    else: Q[k] = (rng.randint(-R, R), rng.randint(-R, R))
    if len({q[0] for q in Q}) < n or not valid(Q): continue
    P = Q; sg = signature(P)
    if sg in seen: continue
    seen.add(sg); tested += 1
    f = split.sig_fn(n, sg)
    ok, S1, ncl = split.split(n, f, a, b)
    if ok: assert split.check_split(n, f, a, b, S1)
    else:
        print(f'REAL COUNTEREXAMPLE after {tested} order types: {sorted(P)}', flush=True)
        json.dump({'a': a, 'b': b, 'n': n, 'sig': sg, 'P': sorted(P)}, open(out, 'w')); break
    if tested % 500 == 0: print(f'seed {seed}: {tested} order types tested, all split, {time.time()-t0:.0f}s', flush=True)
print(f'seed {seed}: done, {tested} distinct real order types tested, {time.time()-t0:.0f}s', flush=True)
