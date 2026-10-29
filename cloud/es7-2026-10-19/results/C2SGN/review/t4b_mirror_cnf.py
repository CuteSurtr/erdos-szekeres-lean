#!/usr/bin/env python3
"""--mirror I J K on real 7-gon-free sets (antipodal subsets of the 32-point set with m odd, perturbed to generic nu):
both L(S) and L(R(S)) satisfy every clause except possibly the mirror unit, and exactly one satisfies it too."""
import os, random, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
from cnfeval import build
from t4_mirror import gen_small, nu_ties, perturb
rng = random.Random(int(sys.argv[1])); st = dict(pairs=0, exactly_one=0, bad=0)
for tr in range(int(sys.argv[2])):
    n = rng.choice([30, 26, 22, 18]); trip = sorted(rng.sample(range(3, n - 1), 3))
    F = build(n, 7, par=True, centre=True, rs=True, mirror=trip)
    P = gen_small(rng, n)
    if max_convex(P) >= 7: continue
    S, info = par_normal_form(P, rs=True)
    if nu_ties(S, info):
        P = perturb(P, rng); S, info = par_normal_form(P, rs=True); assert not nu_ties(S, info)
    RS, _ = par_normal_form(reflect(P), rs=True)
    b1, _ = F.evaluate(S); b2, _ = F.evaluate(RS)
    unit = (-F.ov[tuple(trip)],) if tuple(trip) in F.ov else None
    st["pairs"] += 1
    fs = [len(b1), len(b2)]
    # the only possibly-falsified clause is the mirror unit, in exactly one of the two
    allbad = b1 + b2
    if sorted(fs) == [0, 1] and len(allbad) == 1 and len(allbad[0]) == 1 and abs(allbad[0][0]) <= F.no:
        st["exactly_one"] += 1
    else:
        st["bad"] += 1; print("BAD", n, trip, [[F.describe(l) for l in c] for c in allbad][:4])
print(json.dumps(st))
