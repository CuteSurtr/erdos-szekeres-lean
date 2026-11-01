#!/usr/bin/env python3
"""Independent checker: largest convex subset = max over (a,b) of [longest cap a->b] + [longest cup a->b] - 2
(points sorted by x; distinct x required; general position).  Exact integers."""
import sys, itertools

def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])

def max_convex_cupcap(P):
    P = sorted(P); n = len(P)
    assert len({p[0] for p in P}) == n, 'need distinct x'
    best = min(n, 2)
    for ia in range(n):
        R = list(range(ia + 1, n))
        # cap[c][d]: longest cap starting at a with last edge c->d (c may be a); cup similarly
        cap = {}; cup = {}
        maxcap = {b: 2 for b in R}; maxcup = {b: 2 for b in R}
        for d in R:
            cap[(ia, d)] = 2; cup[(ia, d)] = 2
            for c in range(ia + 1, d):
                bc = 0; bu = 0
                for e in [ia] + list(range(ia + 1, c)):
                    vc = cap.get((e, c), 0); vu = cup.get((e, c), 0)
                    if vc >= 2 or vu >= 2:
                        o = orient(P[e], P[c], P[d])
                        if vc >= 2 and o < 0 and vc + 1 > bc: bc = vc + 1   # right turn: cap
                        if vu >= 2 and o > 0 and vu + 1 > bu: bu = vu + 1   # left turn: cup
                if bc: cap[(c, d)] = bc
                if bu: cup[(c, d)] = bu
                # store both dicts on same key set: cap/cup keys exist if chain exists
                if bc and bc > maxcap[d]: maxcap[d] = bc
                if bu and bu > maxcup[d]: maxcup[d] = bu
                if not bc: cap[(c, d)] = 0
                if not bu: cup[(c, d)] = 0
        for b in R:
            best = max(best, maxcap[b] + maxcup[b] - 2)
    return best

if __name__ == '__main__':
    import random
    sys.path.insert(0, __file__.rsplit('/', 1)[0])
    from maxconvex import max_convex, brute
    random.seed(11); bad = 0
    for trial in range(300):
        n = random.randint(4, 11)
        while True:
            P = list({(random.randint(-40, 40), random.randint(-40, 40)) for _ in range(n)})
            if len({p[0] for p in P}) == len(P) and all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3)): break
        x, y = max_convex_cupcap(P), brute(P)
        if x != y: bad += 1; print('MISMATCH', P, x, y)
    print('cupcap vs brute on 300 random sets, mismatches:', bad)
    for path in sys.argv[1:]:
        Q = [tuple(map(int, l.split()[:2])) for l in open(path) if l.strip() and not l.startswith('#')]
        print(path.rsplit('/', 1)[-1], len(Q), 'cupcap:', max_convex_cupcap(Q), ' angular DP:', max_convex(Q))
