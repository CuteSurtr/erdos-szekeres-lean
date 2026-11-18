#!/usr/bin/env python3
"""randsets.py MAXCAP MAXCUP G COUNT SEED OUTPREFIX [target] -- random real point sets (integer
coordinates, general position, distinct x) with caps <= MAXCAP points, cups <= MAXCUP points and
no convex G-gon, grown greedily by random insertion.  Each final set is re-validated with the
independent brute-force convex-position test of geom.py."""
import sys, random, json, itertools
sys.path.insert(0, '.')
import geom

def valid(P, maxcap, maxcup, G):
    P = sorted(P)
    n = len(P)
    if n < 3:
        return True
    S = {}
    for i, j, k in itertools.combinations(range(n), 3):
        d = geom.det(P[i], P[j], P[k])
        if d == 0:
            return False
        S[(i, j, k)] = 1 if d > 0 else -1
    # longest cap / cup from s to t for all s<t (anchored DP)
    best = {1: {}, -1: {}}
    for sgn in (1, -1):
        lim = maxcup if sgn == 1 else maxcap
        for s in range(n):
            L = {}
            for j in range(s + 1, n):
                L[(s, j)] = 2
            for k in range(s + 2, n):
                for j in range(s + 1, k):
                    b = 0
                    if S[(s, j, k)] == sgn:
                        b = 3
                    for i in range(s + 1, j):
                        if S[(i, j, k)] == sgn and (i, j) in L and L[(i, j)] >= 3 and L[(i, j)] + 1 > b:
                            b = L[(i, j)] + 1
                    L[(j, k)] = b if b else 0
                    if b > lim:
                        return False
                    if b > best[sgn].get((s, k), 2):
                        best[sgn][(s, k)] = b
    for (s, t), a in best[-1].items():
        b = best[1].get((s, t), 2)
        if a >= 3 and b >= 3 and a + b - 2 >= G:
            return False
    return True

def grow(rng, maxcap, maxcup, G, target, kind):
    P = []
    xs = set()
    fails = 0
    while len(P) < target and fails < 400:
        if kind == 0:
            p = (rng.randrange(1, 10**6), rng.randrange(1, 10**6))
        elif kind == 1:   # perturbed parabola (cup-ish)
            x = rng.randrange(1, 10**6); p = (x, (x - 5 * 10**5) ** 2 // 10**6 + rng.randrange(-60000, 60000))
        elif kind == 2:   # perturbed cap-ish arc
            x = rng.randrange(1, 10**6); p = (x, -((x - 5 * 10**5) ** 2) // (3 * 10**6) + rng.randrange(-40000, 40000))
        else:             # clusters
            cx = rng.choice([10**5, 4 * 10**5, 7 * 10**5]); p = (cx + rng.randrange(0, 2 * 10**5), rng.randrange(0, 10**6))
        if p[0] in xs:
            continue
        if valid(P + [p], maxcap, maxcup, G):
            P.append(p); xs.add(p[0]); fails = 0
        else:
            fails += 1
    return sorted(P)

if __name__ == '__main__':
    maxcap, maxcup, G, count, seed = map(int, sys.argv[1:6])
    pre = sys.argv[6]
    target = int(sys.argv[7]) if len(sys.argv) > 7 else 99
    rng = random.Random(seed)
    for c in range(count):
        P = grow(rng, maxcap, maxcup, G, target, c % 4)
        S = geom.orient(P)
        cap, cup = geom.longest_cap_cup(P, S)
        assert cap <= maxcap and cup <= maxcup
        assert not geom.brute_convex_gon(P, G, S), 'brute force found a G-gon'
        json.dump([list(p) for p in P], open(f'{pre}_{c}.json', 'w'))
        print(c, 'kind', c % 4, 'n', len(P), 'cap', cap, 'cup', cup, flush=True)
