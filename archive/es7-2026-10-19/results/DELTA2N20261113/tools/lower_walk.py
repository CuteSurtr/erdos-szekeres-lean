"""Adversarial random walk for the lower-chain form on real point sets (HEURISTIC; exact test at every accepted step).
Moves as in adv_search2.py of ETVTHY20261113 (add / move / replace a point; keep the set valid; prefer more saturated
pairs).  usage: lower_walk.py seed a n minutes out.jsonl pool1 [pool2 ...]"""
import sys, json, random, time
from lower_lib import lower_delta, Analysis
seed, a, n, minutes, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
random.seed(seed); R = 10**6; sets = []
for fn in sys.argv[6:]:
    sets += [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
sets.sort(key=len, reverse=True)
def analyse(P):
    P = sorted(P)
    if len({p[0] for p in P}) < len(P): return None
    try: A = Analysis(P)
    except ValueError: return None
    if max(A.cap_end) > a - 1 or A.gon() > n - 1: return None
    return A
def nsat(A):
    m = A.n; return sum(1 for u in range(m) for v in range(u + 1, m) if A.capB[u, v] + A.cupB[u, v] == n + 1)
P = [tuple(p) for p in random.choice(sets[:max(3, len(sets) // 4)])]; A = analyse(P); cur = nsat(A)
t0 = time.time(); tested = 0; fails = 0; sizes = []
while time.time() - t0 < minutes * 60:
    Q = list(P); r = random.random()
    if r < 0.3: Q.append((random.randint(-R, R), random.randint(-R, R)))
    elif r < 0.95:
        i = random.randrange(len(Q)); x, y = Q[i]; s = random.choice([100, 1000, 10000, 100000])
        Q[i] = (x + random.randint(-s, s), y + random.randint(-s, s))
    else:
        Q.pop(random.randrange(len(Q))); Q.append((random.randint(-R, R), random.randint(-R, R)))
    AQ = analyse(Q)
    if AQ is None or len(Q) < len(P): continue
    sc = nsat(AQ)
    if sc < cur and random.random() > 0.3: continue
    P, cur = Q, sc; tested += 1; sizes.append(len(P))
    st, D, rounds = lower_delta(P, n, a - 1, AQ)
    if st != 'OK':
        fails += 1; print('LOWER-CHAIN FAILS:', st, len(P), 'points', flush=True)
        with open(out, 'a') as f: f.write(json.dumps({'seed': seed, 'a': a, 'n': n, 'status': st, 'P': sorted(P)}) + '\n')
        if st == 'NONE': break
print('walk seed %d (a=%d, n=%d): %d accepted steps tested, %d failures; sizes %d-%d, final %d points, %d saturated pairs; %.0fs' % (seed, a, n, tested, fails, min(sizes or [0]), max(sizes or [0]), len(P), cur, time.time() - t0), flush=True)
