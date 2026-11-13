"""Adversarial walk for the a=4 decomposition at n=7: 4-cap-free heptagon-free sets of maximal size (16 = Baek),
test: exists a cup Delta (3-cap-free, hexagon-free) meeting every convex hexagon."""
import sys, json, random, time
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import quick
from delta_strong_a import delta_strong_a
def valid(P):
    g, mc, mu = quick(P)
    return g >= 0 and g <= 6 and mc <= 3
if __name__ == '__main__':
    seed, minutes = int(sys.argv[1]), float(sys.argv[2]); random.seed(seed); R = 10**6
    sets = [json.loads(l)['P'] for l in open('pool_a4n7.jsonl')]
    sets.sort(key=len, reverse=True)
    P = [tuple(p) for p in random.choice(sets[:10])]
    t0 = time.time(); tested = 0; fails = 0; sizes = {}
    while time.time() - t0 < minutes * 60:
        Q = list(P); r = random.random()
        if r < 0.3: Q.append((random.randint(-R, R), random.randint(-R, R)))
        elif r < 0.9:
            i = random.randrange(len(Q)); x, y = Q[i]; s = random.choice([300, 3000, 30000, 300000])
            Q[i] = (x + random.randint(-s, s), y + random.randint(-s, s))
        else:
            Q.pop(random.randrange(len(Q))); Q.append((random.randint(-R, R), random.randint(-R, R)))
        if len({q[0] for q in Q}) < len(Q) or not valid(Q): continue
        if len(Q) < len(P): continue
        P = Q; tested += 1; sizes[len(P)] = sizes.get(len(P), 0) + 1
        D, st = delta_strong_a(P, 6, 4)
        if st != 'OK':
            fails += 1; print('FAIL', st, len(P), json.dumps(sorted(P)), flush=True)
            if st == 'INFEASIBLE': break
    print('done seed', seed, 'tested', tested, 'fails', fails, 'sizes', sizes, flush=True)
