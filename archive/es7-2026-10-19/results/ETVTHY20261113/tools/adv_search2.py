"""Adversarial search v2 (strong Delta form): start from large valid sets, perturb, keep size large.
Test: exists Delta 4-cap-free AND convex-k-gon-free meeting every convex k-gon (strong); if strong fails, test weak."""
import sys, json, random, time
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, quick
from delta_strong import delta_strong
from delta_test2 import delta

def valid(P, gonmax):
    g, mc, mu = quick(P)
    return g >= 0 and g <= gonmax and mc <= 4

def nsat(P, k):
    A = Analysis(P); n = A.n
    return sum(1 for u in range(n) for v in range(u+1, n) if A.capB[u, v] + A.cupB[u, v] >= k + 2)

if __name__ == '__main__':
    seed, k, minutes, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    pools = sys.argv[5:]
    random.seed(seed); R = 10**6
    sets = []
    for fn in pools:
        sets += [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
    sets.sort(key=len, reverse=True)
    P = [tuple(p) for p in random.choice(sets[:max(3, len(sets)//10)])]
    cur = nsat(P, k); t0 = time.time(); tested = 0; strong_fail = 0
    while time.time() - t0 < minutes * 60:
        Q = list(P); r = random.random()
        if r < 0.3:
            Q.append((random.randint(-R, R), random.randint(-R, R)))
        elif r < 0.95:
            i = random.randrange(len(Q)); x, y = Q[i]
            s = random.choice([100, 1000, 10000, 100000])
            Q[i] = (x + random.randint(-s, s), y + random.randint(-s, s))
        else:
            Q.pop(random.randrange(len(Q))); Q.append((random.randint(-R, R), random.randint(-R, R)))
        if len({q[0] for q in Q}) < len(Q) or not valid(Q, k): continue
        sc = nsat(Q, k)
        if len(Q) < len(P): continue
        if sc < cur and random.random() > 0.3: continue
        P, cur = Q, sc
        tested += 1
        D, st, rounds = delta_strong(P, k)
        if st != 'OK':
            strong_fail += 1
            Dw, nh, nc, stw, rw = delta(P, k)
            print('STRONG', st, 'WEAK', stw, 'n', len(P), flush=True)
            with open(out, 'a') as f: f.write(json.dumps({'seed': seed, 'k': k, 'strong': st, 'weak': stw, 'P': sorted(P)}) + '\n')
            if stw == 'INFEASIBLE': break
    print('done seed', seed, 'tested', tested, 'strong_fail', strong_fail, 'final n', len(P), 'sat', cur, flush=True)
