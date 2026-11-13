#!/usr/bin/env python3
"""Non-parallelogram hulls: random centrally symmetric sets (any hull), plain x-sorted labelling, formula
sgn.py n K --sym [--centre] with K = maxconv+1 (every clause must hold) and K = maxconv (only K-gon witnesses may fail)."""
import os, random, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
from cnfeval import build
from t2_cnf import check, summarize
rng = random.Random(int(sys.argv[1])); resA, resB = [], []; hulls = collections.Counter()
for tr in range(int(sys.argv[2])):
    m = rng.randint(4, 10); span = rng.choice([30, 1000, 10 ** 6])
    P = []
    for _ in range(m):
        p = (rng.randint(-span, span), rng.randint(-span, span)); P += [p, neg(p)]
    if not symmetric(P) or not general_position(P): continue
    hulls[len(hull_ccw(P))] += 1
    S = x_normal_form(P); n = len(S); mc = max_convex(S)
    centre = rng.random() < 0.7
    if mc + 1 <= n:
        resA.append(check(build(n, mc + 1, centre=centre), S, use_sat=(tr % 3 == 0)))
    if mc >= 4:
        resB.append(check(build(n, mc, centre=centre), S))
summarize(resA, "non-par, K=maxconv+1 (all clauses must hold)"); summarize(resB, "non-par, K=maxconv (witness-only failures)")
print("hull sizes", sorted(hulls.items()))
