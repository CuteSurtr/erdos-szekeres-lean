"""Random 5-cap-free, octagon-free sets by greedy insertion + local improvement (exact)."""
import sys, random, json, time
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import quick

def valid(P, capmax=4, gonmax=7, cupmax=7):
    g, mc, mu = quick(P)
    return g >= 0 and g <= gonmax and mc <= capmax and mu <= cupmax

def greedy(cands, capmax=4, gonmax=7, cupmax=7):
    P = []
    xs = set()
    for p in cands:
        if p[0] in xs: continue
        Q = P + [p]
        if valid(Q, capmax, gonmax, cupmax):
            P = Q; xs.add(p[0])
    return P

def improve(P, gen, iters, capmax=4, gonmax=7, cupmax=7):
    """Try to add points; when stuck, swap one point (remove random, add 2)."""
    P = list(P)
    for it in range(iters):
        p = gen()
        if p[0] in {q[0] for q in P}: continue
        if valid(P + [p], capmax, gonmax, cupmax):
            P.append(p); continue
        # swap move: remove a random point, try adding p
        k = random.randrange(len(P)); Q = P[:k] + P[k+1:] + [p]
        if valid(Q, capmax, gonmax, cupmax):
            P = Q
    return P

if __name__ == '__main__':
    seed = int(sys.argv[1]); mode = sys.argv[2]; iters = int(sys.argv[3]); out = sys.argv[4]
    capmax, gonmax, cupmax = (4, 7, 7) if len(sys.argv) < 6 else tuple(map(int, sys.argv[5].split(',')))
    random.seed(seed)
    R = 10**6
    if mode == 'box':
        gen = lambda: (random.randint(-R, R), random.randint(-R, R))
    elif mode == 'para':
        def gen():
            x = random.randint(-R, R); return (x, (x*x)//R + random.randint(-R//3, R//3))
    elif mode == 'circ':
        import math
        def gen():
            t = random.uniform(0, 2*math.pi); r = R*(1+random.uniform(-0.3, 0.3))
            return (int(r*math.cos(t)), int(r*math.sin(t)))
    elif mode == 'gauss':
        def gen():
            return (int(random.gauss(0, R)), int(random.gauss(0, R)))
    t0 = time.time()
    P = greedy([gen() for _ in range(400)], capmax, gonmax, cupmax)
    P = improve(P, gen, iters, capmax, gonmax, cupmax)
    print(seed, mode, len(P), quick(P), '%.1fs' % (time.time()-t0), flush=True)
    with open(out, 'a') as f:
        f.write(json.dumps({'seed': seed, 'mode': mode, 'caps': [capmax, gonmax, cupmax], 'P': sorted(P)}) + '\n')
