"""Control for the lower-chain tools on small REAL point sets: the lazy test lower_lib.lower_delta (C library esgeo,
saturated pairs, lazy SAT) against brute force from coordinates (convex position by the monotone-chain hull, cup part
= vertices below the chord, all 2^m subsets Delta).  Also checks the identity "cup parts of gons = longest cups of
saturated pairs" through the two answers.   usage: control_lower.py seed"""
import sys, random, itertools
from lower_lib import lower_delta, Analysis
comb = itertools.combinations
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def convex_position(pts):
    lo = []; up = []
    for p in pts:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return len(lo) + len(up) - 2 == len(pts)
def brute(P, a, n):
    m = len(P)
    caps = [sum(1 << i for i in K) for K in comb(range(m), a - 1) if all(orient(P[K[i]], P[K[i + 1]], P[K[i + 2]]) < 0 for i in range(a - 3))]
    lows = set()
    for G in comb(range(m), n - 1):
        if convex_position([P[i] for i in G]):
            u, v = G[0], G[-1]
            lows.add(sum(1 << x for x in [u] + [x for x in G[1:-1] if orient(P[u], P[x], P[v]) > 0] + [v]))
    for D in range(1 << m):
        if any(D & c == c for c in caps): continue
        if all(D & q for q in lows): return True, len(lows)
    return False, len(lows)
def randset(m, style):
    while True:
        if style == 0: P = [(rnd.randrange(10**6), rnd.randrange(10**6)) for _ in range(m)]
        elif style == 1: P = [(x, x * x + rnd.randrange(-40, 41) * m) for x in rnd.sample(range(-60, 61), m)]
        else: P = [(x, -x * x + rnd.randrange(-60, 61) * m) for x in rnd.sample(range(-60, 61), m)]
        P = sorted(set(P))
        if len(P) == m and len({p[0] for p in P}) == m and all(orient(*t) != 0 for t in comb(P, 3)): return P
stats = {}
for (a, n) in [(5, 6), (5, 7), (4, 6), (4, 5), (6, 6), (5, 8)]:
    done = agree = with_gons = 0; tries = 0
    while done < 60 and tries < 20000:
        tries += 1; m = rnd.randrange(n - 1, 13); P = randset(m, tries % 3); A = Analysis(P)
        if max(A.cap_end) > a - 1 or A.gon() > n - 1: continue
        ex, nl = brute(P, a, n); st, D, r = lower_delta(P, n, a - 1, A)
        assert ex == (st == 'OK'), ('mismatch', a, n, P)
        done += 1; with_gons += nl > 0
    stats[(a, n)] = (done, with_gons)
print('control_lower OK: lazy lower-chain test == brute force on', {k: '%d sets (%d with gons)' % v for k, v in stats.items()}, flush=True)
