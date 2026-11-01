#!/usr/bin/env python3
"""Auditor A5: cube-level mutation test of the (B) partner rule and of the (A) case rule.
With the correct sigma_B, pairing V with a WRONG partner must fail for (almost) every subcase; with the correct sigma_A,
P_b must not map onto P_(18-b) or P_(16-b).  usage: A5_MAP=base.json cubemut.py RESULTS_DIR"""
import os, sys
sys.path.insert(0, '.')
import symmaps_lib as L
from a5lib import load_cubes, T
RES = sys.argv[1]
hull, _ = load_cubes(os.path.join(RES, "C2C34", "cubes.txt"))
img = lambda sg, lits: {(sg[abs(l)] if l > 0 else -sg[abs(l)]) for l in lits}
for a in (3, 8):
    L2, _ = load_cubes(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt"))
    sg = L.sigma(L.pi_B(a), -1)
    for name, rule in [("correct (a-i)", lambda i: (a - i) % T), ("wrong (a+1-i)", lambda i: (a + 1 - i) % T),
                       ("wrong (-i)", lambda i: (-i) % T), ("identity", lambda i: i)]:
        bad = 0; tot = 0
        for n, c in L2.items():
            V = [int(x) for x in n.split("_")[1].split("-")]
            W = sorted(rule(i) for i in V)
            m = f"P{a}_" + "-".join(map(str, W))
            tot += 1
            if m not in L2 or img(sg, L2[m]) != set(c):
                bad += 1
        print(f"(B) a={a} partner rule {name}: mismatches {bad} of {tot}")
for b in (2, 8):
    sg = L.sigma(L.pi_A(17 - b), +1)
    for tgt in (17 - b, 18 - b, 16 - b):
        if 1 <= tgt <= 16:
            print(f"(A) b={b}: sigma_A(P{b}) == P{tgt}: {img(sg, hull[f'P{b}']) == set(hull[f'P{tgt}'])}")
