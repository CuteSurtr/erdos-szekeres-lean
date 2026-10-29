#!/usr/bin/env python3
"""Negative controls for the clause evaluator: deliberately wrong labellings of the real 32-point set must falsify
clauses of the expected families (shows the checker has teeth)."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
from cnfeval import build
from t2_cnf import load32
P = load32(); n = 32
F = build(32, 7, par=True, centre=True, rs=True)
def fam(F, c):
    kinds = sorted({(F.mean[abs(l)][0] if abs(l) > F.no else 'o') for l in c})
    return f"len{len(c)}:" + "+".join(kinds)
def run(name, S):
    bad, val = F.evaluate(S)
    print(name, "falsified", len(bad), dict(collections.Counter(fam(F, c) for c in bad).most_common(6)))
S, info = par_normal_form(P, rs=True)
run("correct", S)
# 1: tilt towards V1 (swap n-1,n and 1,2)
W = S[:]; W[-1], W[-2] = W[-2], W[-1]; W[0], W[1] = W[1], W[0]; run("tilt-wrong", W)
# 2: minority edge class (rs violated): use rs=False and pick the edge with class 4
for ch in range(4):
    S2, inf2 = par_normal_form(P, rs=False, choice=ch)
    if inf2["class"] < (inf2["m"] + 1) // 2:
        run(f"minority-edge(class {inf2['class']})", S2); break
# 3: sorted by plain x (not the par normal form) -> par units fail
run("x-sorted", x_normal_form(P))
# 4: swap two inner labels (not a sort by any direction)
W = S[:]; W[5], W[9] = W[9], W[5]; W[n-6], W[n-10] = W[n-10], W[n-6]; run("swap-inner", W)
# 5: reflected set with the SAME labels (orientations all negated) -> par units fail
run("reflected-same-labels", [(-x, y) for x, y in S])
