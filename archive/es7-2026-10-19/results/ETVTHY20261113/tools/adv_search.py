"""Adversarial search for counterexamples to the Delta-reduction conjecture:
5-cap-free set without convex (k+1)-gon, but no 4-cap-free Delta meets every convex k-gon.
Random walk over valid sets, biased to more k-gons/4-caps; full CP-SAT check each step."""
import sys, json, random, time, math
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from delta_test2 import delta

def valid(P, gonmax):
    g, mc, mu = quick(P)
    return g >= 0 and g <= gonmax and mc <= 4

def score(P, k):
    A = Analysis(P); n = A.n
    sat = sum(1 for u in range(n) for v in range(u+1, n) if A.capB[u, v] + A.cupB[u, v] >= k + 2)
    return sat

if __name__ == '__main__':
    seed, k, minutes, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    init = sys.argv[5] if len(sys.argv) > 5 else None
    random.seed(seed); R = 10**6
    if init:
        lines = [json.loads(l)['P'] for l in open(init)] if init.endswith('.jsonl') else [json.load(open(init))]
        P = [tuple(p) for p in random.choice(lines)]
    else:
        P = []
    t0 = time.time(); tested = 0; cur = score(P, k) if len(P) > 2 else 0
    while time.time() - t0 < minutes * 60:
        Q = list(P); r = random.random()
        if r < 0.4 or len(Q) < 8:
            Q.append((random.randint(-R, R), random.randint(-R, R)))
        elif r < 0.9:
            i = random.randrange(len(Q)); x, y = Q[i]; s = random.choice([3000, 30000, 300000])
            Q[i] = (x + random.randint(-s, s), y + random.randint(-s, s))
        else:
            Q.pop(random.randrange(len(Q)))
        if len({q[0] for q in Q}) < len(Q) or not valid(Q, k): continue
        sc = score(Q, k)
        if sc + 0.5 * len(Q) < cur + 0.5 * len(P) and random.random() > 0.15: continue
        P, cur = Q, sc
        D, nh, nc, st, rounds = delta(P, k)
        tested += 1
        if st != 'OK':
            print('CANDIDATE', st, len(P), flush=True)
            with open(out, 'a') as f: f.write(json.dumps({'seed': seed, 'k': k, 'status': st, 'P': sorted(P)}) + '\n')
            if st == 'INFEASIBLE': break
    print('done seed', seed, 'tested', tested, 'final n', len(P), 'sat pairs', cur, flush=True)
