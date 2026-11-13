#!/usr/bin/env python3
"""Soundness test of clsat.py: build the assignment induced by a REAL cluster and check every clause.
Profile clauses are checked too when the cluster satisfies Prop. C (i); otherwise only structural clauses."""
import sys, math, random, subprocess
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from profile import cluster
from itertools import combinations

def assignment(pts, m):
    # radial frame (x outward, y ccw tangent) -> inward frame by rotation by pi; sort by x'
    P = sorted([(-x, -y) for x, y in pts])
    n = len(P)
    t = {}
    for i, j in combinations(range(n), 2):
        a = math.degrees(math.atan2(P[j][1] - P[i][1], P[j][0] - P[i][0]))
        t[i, j] = (a + 90.0) / (180.0 / m)
    def orient(i, j, k):
        return (P[j][0]-P[i][0])*(P[k][1]-P[i][1]) - (P[j][1]-P[i][1])*(P[k][0]-P[i][0])
    return P, t, orient

def check(pts, m, full):
    P, t, orient = assignment(pts, m)
    n = len(P)
    if any(not (1 < v < m - 1) or abs(v - round(v)) < 1e-9 for v in t.values()):
        return 'skip (direction in forbidden zone or on a bin boundary)'
    subprocess.run(['python3', 'tools/clsat.py', str(m), str(n), 'out/sat/sound.cnf'], capture_output=True)
    # rebuild variable numbering exactly as clsat.py does
    B = m - 2; nv = 0; L = {}; T = {}; G = {}; H = {}
    for i, j in combinations(range(n), 2):
        for v in range(1, B): nv += 1; L[i, j, v] = nv
    for tr in combinations(range(n), 3): nv += 1; T[tr] = nv
    for x in range(1, m):
        for a in range(2, n + 1): nv += 1; G[x, a] = nv; nv += 1; H[x, a] = nv
    val = {}
    for (i, j, v), var in L.items(): val[var] = math.floor(t[i, j]) <= v
    for (i, j, k), var in T.items(): val[var] = orient(i, j, k) > 0
    # real profile g(x), h(x): longest cup with all t < x, longest cap with all t > m - x
    def longest(kind, ok):
        best = 1
        dp = {}
        for j in range(n):
            for i in range(j):
                if not ok(t[i, j]): continue
                b = 2
                for k in range(i):
                    if (k, i) in dp and ok(t[k, i]):
                        turn = orient(k, i, j) > 0
                        if (kind == 'cup') == turn: b = max(b, dp[k, i] + 1)
                dp[i, j] = b; best = max(best, b)
        return best
    g = {x: longest('cup', lambda v, x=x: v < x) for x in range(1, m)}
    h = {x: longest('cap', lambda v, x=x: v > m - x) for x in range(1, m)}
    for (x, a), var in G.items(): val[var] = g[x] >= a
    for (x, a), var in H.items(): val[var] = h[x] >= a
    sat_i = all(g[x] + h[x] <= x + 1 for x in range(1, m))
    bad = 0; total = 0
    with open('out/sat/sound.cnf') as f:
        f.readline()
        for line in f:
            lits = [int(z) for z in line.split()[:-1]]
            prof = any(abs(l) in G.values() or abs(l) in H.values() for l in lits) and all(
                (abs(l) in G.values() or abs(l) in H.values()) for l in lits)
            if prof and not full: continue
            total += 1
            if not any((l > 0) == val[abs(l)] for l in lits):
                bad += 1
    return 'n=%d clauses checked=%d violated=%d  (profile g=%s h=%s satisfies (i): %s)' % (
        n, total, bad, [g[x] for x in range(1, m)], [h[x] for x in range(1, m)], sat_i)

if __name__ == '__main__':
    pts7 = cluster([(3, 3, -36.84161, 0.0, 0.0), (3, 2, -34.44983, -1.30368, 1.57440)])
    print('m=7 compound cluster (full CNF):', check(pts7, 7, True))
    rng = random.Random(3)
    for trial in range(6):
        m = rng.choice([6, 7, 8]); n = rng.randint(5, 9)
        pts = [(rng.uniform(-1, 1), rng.uniform(-0.15, 0.15)) for _ in range(n)]   # steep-free-ish random sets
        print('random m=%d:' % m, check(pts, m, False))
