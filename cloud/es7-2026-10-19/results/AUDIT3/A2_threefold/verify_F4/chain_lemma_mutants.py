#!/usr/bin/env python3
"""F4 check 1b: the checker in chain_lemma_check.py has teeth.  Each mutant of the chain
fixpoint should produce SOUNDNESS failures (fixpoint violated on a k-gon-free set) or
completeness failures.  Usage: chain_lemma_mutants.py SEED TRIALS"""
import itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chain_lemma_check import orient, gen_points, has_convex_kset

def fixpoint(P, k, mut):
    n = len(P)
    B = (lambda x, c: True) if mut == "noB" else (lambda x, c: P[x][0] < P[c][0])
    ccw = lambda a, b, c: orient(P[a], P[b], P[c]) > 0
    turn = (lambda a, b, c: True) if mut == "noturn" else ccw
    kk = k - 1 if mut == "short" else k
    Y = {(x, b, c) for x in range(n) for b in range(n) for c in range(n)
         if len({x, b, c}) == 3 and B(x, c) and ccw(x, b, c)}
    W = {(x, a, b) for (x, a, b) in Y if B(x, a)}
    if kk - 2 < 2:
        raise ValueError
    for r in range(2, kk - 1):
        nxt, viol = set(), False
        for (x, a, b) in W:
            for c in range(n):
                if c in (x, a, b):
                    continue
                if (x, b, c) in Y and turn(a, b, c):
                    if r + 1 <= kk - 2:
                        nxt.add((x, b, c))
                    else:
                        viol = True
        if r == kk - 2:
            return viol
        W = nxt

seed, trials = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
for mut in ["none", "noB", "noturn", "short"]:
    fs = fc = 0
    for t in range(trials):
        shape = rng.choice(["box", "box", "parab", "clusters"])
        n = rng.randint(7, 12)
        k = rng.randint(5, 7)
        P = gen_points(rng, n, shape)
        v = fixpoint(P, k, mut)
        real = has_convex_kset(P, k)
        fs += (v and not real)
        fc += (real and not v)
    print(f"mutant={mut:7s} trials={trials} soundness_failures={fs} completeness_failures={fc}")
