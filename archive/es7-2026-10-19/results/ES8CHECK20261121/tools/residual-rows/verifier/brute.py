"""Brute-force cross-check of geo.py on small sets: chains by enumerating all increasing index subsets,
convex position by exact point-in-triangle tests (no DP shared with geo.py)."""
import itertools, random, sys
from geo import Conf

def o(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def is_chain(P, idx, sgn):
    return all((o(P[idx[t]], P[idx[t+1]], P[idx[t+2]]) > 0) == (sgn > 0) for t in range(len(idx)-2))

def in_tri(p, a, b, c):
    s1, s2, s3 = o(a, b, p), o(b, c, p), o(c, a, p)
    return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)

def convex_pos(P, idx):
    pts = [P[i] for i in idx]
    for p in pts:
        others = [q for q in pts if q is not p]
        for a, b, c in itertools.combinations(others, 3):
            if in_tri(p, a, b, c):
                return False
    return True

def brute(P):
    n = len(P)
    Ep = {}; Fm = {}; Fp = {}
    longcap = longcup = 1 if n else 0
    for r in range(2, n+1):
        for idx in itertools.combinations(range(n), r):
            if is_chain(P, idx, +1):
                longcup = max(longcup, r)
                k = (idx[-2], idx[-1]); Ep[k] = max(Ep.get(k, 0), r)
                k = (idx[0], idx[1]); Fp[k] = max(Fp.get(k, 0), r)
            if is_chain(P, idx, -1):
                longcap = max(longcap, r)
                k = (idx[0], idx[1]); Fm[k] = max(Fm.get(k, 0), r)
    gon = 0
    for r in range(n, 2, -1):
        if any(convex_pos(P, idx) for idx in itertools.combinations(range(n), r)):
            gon = r; break
    return Ep, Fm, Fp, longcap, longcup, gon

rng = random.Random(int(sys.argv[1]))
N = int(sys.argv[2]); bad = 0
for rep in range(N):
    while True:
        n = rng.randint(5, 11)
        xs = sorted(rng.sample(range(-1000, 1000), n))
        mode = rep % 3
        P = []
        for i, x in enumerate(xs):
            if mode == 0: y = rng.randint(-1000, 1000)
            elif mode == 1: y = x*x//1000 + rng.randint(-40, 40)
            else: y = (1 if i % 2 else -1)*x*x//1000 + rng.randint(-40, 40)
            P.append((x, y))
        try:
            C = Conf(P); break
        except ValueError:
            continue
    Ep, Fm, Fp, lcap, lcup, gon = brute(P)
    ok = lcap == C.longcap and lcup == C.longcup and gon == C.gon()
    for u in range(n):
        for v in range(u+1, n):
            ok &= Ep[(u, v)] == C.Ep[u][v] and Fm[(u, v)] == C.Fm[u][v] and Fp[(u, v)] == C.Fp[u][v]
    if not ok:
        bad += 1; print('MISMATCH', P)
print('brute cross-check sets', N, 'mismatches', bad)
