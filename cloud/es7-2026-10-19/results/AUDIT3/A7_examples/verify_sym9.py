#!/usr/bin/env python3
"""Bonus: SYM2/sym9_128points.txt (k = 9, 128 points): central symmetry, general position, DP largest convex subset
(two orders), DP witness check, and DP-vs-exhaustive cross-checks on random subsets."""
import os, random, sys, time
from functools import cmp_to_key
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7lib as L
R = os.environ.get("ES7_RESULTS", ".")
t0 = time.time()
pts, an = L.parse(R + "/SYM2/sym9_128points.txt", "Z2")
n = len(pts)
S = set(pts)
print("n=%d distinct=%s anomalies=%s C2-invariant=%s origin_in_set=%s maxabs=%d" % (
    n, len(S) == n, an, all((-x, -y) in S for x, y in pts), (0, 0) in S, max(abs(c) for p in pts for c in p)))
O = L.orient_table(pts, "Z2")
col = sum(1 for a, b, c in combinations(range(n), 3) if O[a][b][c] == 0)
mB = sum(1 for a, b, c in combinations(range(n), 3) if L.orient_B(pts[a], pts[b], pts[c], "Z2") != O[a][b][c])
print("collinear=%d methodB_mismatch=%d (%.0fs)" % (col, mB, time.time() - t0), flush=True)
cmpf = L.lex_key_cmp("Z2")
order = sorted(range(n), key=cmp_to_key(lambda a, b: cmpf(pts[a], pts[b])))
order2 = sorted(range(n), key=lambda a: (pts[a][1], pts[a][0]))
for nm, od in (("lex(x,y)", order), ("lex(y,x)", order2)):
    d, w = L.max_convex_dp(O, od)
    print("DP %s: max_convex=%d witness_convex=%s (%.0fs)" % (nm, d, L.convex_position_halfplane(w, O), time.time() - t0), flush=True)
rng = random.Random(9)
cross = lambda o, a, b: L.orient_A(o, a, b, "Z2")
mism = 0
hist = {}
for t in range(40):
    m = rng.randint(10, 15)
    # bias toward hard subsets: take whole clusters' neighbourhoods by sampling a window in x-order plus random points
    if t % 2:
        st = rng.randint(0, n - m)
        sub = order[st:st + m]
    else:
        sub = rng.sample(range(n), m)
    od = sorted(sub, key=cmp_to_key(lambda a, b: cmpf(pts[a], pts[b])))
    d, w = L.max_convex_dp(O, od)
    ex_d = any(L.hull_is_convex_position([pts[i] for i in c], cmpf, cross) for c in combinations(sub, d))
    ex_d1 = d + 1 <= m and any(L.hull_is_convex_position([pts[i] for i in c], cmpf, cross) for c in combinations(sub, d + 1))
    if not ex_d or ex_d1:
        mism += 1
    hist[d] = hist.get(d, 0) + 1
print("random/window subsets: 40, mismatches=%d, dp histogram=%s (%.0fs)" % (mism, dict(sorted(hist.items())), time.time() - t0))
