"""Real point sets of the first-layer class FL(a,b): simulated annealing maximizing |E| (ends of (b-1)-cups),
|A| (ends of (a-1)-caps), |EuA|, |EnA| or the size.  Exact integer arithmetic (esgeo).
usage: anneal_ab.py a b what seed iters out.jsonl"""
import sys, random, json, math, time
import numpy as np
from esgeo import Analysis
def evaluate(P, a, b, what):
    try: A = Analysis(P)
    except ValueError: return None
    n = A.n
    if n < 2: return 0.01 * n
    if A.capB.max() > a - 1 or A.cupB.max() > b - 1: return None
    if ((A.capB >= a - 1) & (A.cupB >= b - 1)).any(): return None
    ce = A.capE.max(axis=0); ue = A.cupE.max(axis=0)
    E = ue >= b - 1; Aa = ce >= a - 1
    v = {'E': int(E.sum()), 'A': int(Aa.sum()), 'EuA': int((E | Aa).sum()), 'EnA': int((E & Aa).sum()), 'size': n}[what]
    return v + 0.01 * n
def run(a, b, what, seed, iters, R=10**6, T0=0.5):
    rng = random.Random(seed); P = []; cur = 0; best = (0, [])
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.02; r = rng.random(); Q = list(P)
        if r < 0.40 or len(Q) < 4: Q.append((rng.randint(-R, R), rng.randint(-R, R)))
        elif r < 0.80:
            k = rng.randrange(len(Q)); x, y = Q[k]; s = rng.choice([100, 1000, 10000, 100000, R])
            Q[k] = (x + rng.randint(-s, s), y + rng.randint(-s, s))
        elif r < 0.90: Q[rng.randrange(len(Q))] = (rng.randint(-R, R), rng.randint(-R, R))
        else: Q.pop(rng.randrange(len(Q)))
        if len({q[0] for q in Q}) < len(Q): continue
        v = evaluate(Q, a, b, what)
        if v is None: continue
        if v >= cur or rng.random() < math.exp((v - cur) / T):
            P, cur = Q, v
            if cur > best[0]: best = (cur, list(P))
    return best
if __name__ == '__main__':
    a, b, what, seed, iters, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    t0 = time.time(); v, P = run(a, b, what, seed, iters)
    print(f'FL({a},{b}) max {what}: value {v:.2f} n {len(P)} seed {seed} {time.time()-t0:.0f}s', flush=True)
    with open(out, 'a') as f: f.write(json.dumps({'a': a, 'b': b, 'what': what, 'seed': seed, 'value': v, 'P': sorted(P)}) + '\n')
