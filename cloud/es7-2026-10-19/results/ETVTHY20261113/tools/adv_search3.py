"""Adversarial search v3: maximize the number of doubly hard saturated pairs (u in R4, v in L4, cap+cup = 9),
the configurations where the endpoint-based Deltas fail; test weak and strong Conj(8) at every accepted step."""
import sys, json, random, time, math
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from delta_strong import delta_strong
from delta_test2 import delta

def valid(P):
    g, mc, mu = quick(P)
    return g >= 0 and g <= 7 and mc <= 4

def score(P):
    A = Analysis(P); n = A.n
    hard = sum(1 for u in range(n) for v in range(u+1, n)
               if A.capB[u, v] + A.cupB[u, v] >= 9 and A.cap_end[u] == 4 and A.cap_start[v] == 4)
    return hard

if __name__ == '__main__':
    seed, minutes, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    pools = sys.argv[4:]
    random.seed(seed); R = 10**6
    sets = []
    for fn in pools:
        sets += [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    cand = sorted(((score([tuple(p) for p in Q]), Q) for Q in sets), key=lambda t: -t[0])[:10]
    P = [tuple(p) for p in random.choice(cand)[1]]
    cur = score(P); best = cur; t0 = time.time(); tested = 0; fails = 0
    while time.time() - t0 < minutes * 60:
        Q = list(P); r = random.random()
        if r < 0.35: Q.append((random.randint(-R, R), random.randint(-R, R)))
        elif r < 0.85:
            i = random.randrange(len(Q)); x, y = Q[i]; s = random.choice([300, 3000, 30000, 300000])
            Q[i] = (x + random.randint(-s, s), y + random.randint(-s, s))
        elif r < 0.95:
            Q.pop(random.randrange(len(Q))); Q.append((random.randint(-R, R), random.randint(-R, R)))
        else:
            if len(Q) > 15: Q.pop(random.randrange(len(Q)))
        if len({q[0] for q in Q}) < len(Q) or not valid(Q): continue
        sc = score(Q)
        if sc < cur and random.random() > 0.02: continue
        if len(Q) < len(P) - 1: continue
        P, cur = Q, sc; best = max(best, cur); tested += 1
        D, st, rounds = delta_strong(P, 7)
        if st != 'OK':
            Dw, nh, nc, stw, rw = delta(P, 7)
            fails += 1
            print('STRONG', st, 'WEAK', stw, 'n', len(P), 'hard', cur, flush=True)
            with open(out, 'a') as f: f.write(json.dumps({'seed': seed, 'strong': st, 'weak': stw, 'hard': cur, 'P': sorted(P)}) + '\n')
            if stw == 'INFEASIBLE': break
    print('done seed', seed, 'tested', tested, 'strong_fail', fails, 'final n', len(P), 'hard', cur, 'best hard', best, flush=True)
