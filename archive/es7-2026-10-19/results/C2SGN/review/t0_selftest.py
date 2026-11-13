#!/usr/bin/env python3
"""Self-test of rv.py: angular-DP max convex subset vs brute force; DP cups vs brute-force cups; hull vs brute."""
import itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
rng = random.Random(7); c1 = c2 = c3 = 0
for trial in range(300):
    n = rng.randint(4, 11); span = rng.choice([4, 20, 500])
    P = list({(rng.randint(-span, span), rng.randint(-span, span)) for _ in range(n)})
    if len(P) < 4 or not general_position(P): continue
    assert max_convex(P) == max_convex_brute(P), P; c1 += 1
    S = sorted(P); o = orient_table(S); K = len(S)
    assert exact_cups(o, len(S), K) == exact_cups_brute(o, len(S), K); c2 += 1
    H = hull_ccw(P); hs = set(H)
    for q in P:  # q is a hull vertex iff not inside a triangle of other points
        inside = any(det(a,b,q) > 0 and det(b,c,q) > 0 and det(c,a,q) > 0 or det(a,b,q) < 0 and det(b,c,q) < 0 and det(c,a,q) < 0
                     for a, b, c in itertools.combinations([x for x in P if x != q], 3))
        assert (q in hs) == (not inside)
    c3 += 1
print("max_convex==brute", c1, "cups==brute", c2, "hull ok", c3)
