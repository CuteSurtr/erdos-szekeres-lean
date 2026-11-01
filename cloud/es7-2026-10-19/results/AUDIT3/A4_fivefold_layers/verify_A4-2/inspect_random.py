#!/usr/bin/env python3
"""Re-run the --random generator of check_layers_exact.py and print every set whose unit check did not pass."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_layers_exact as C
nsets, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed); tested = 0
while tested < nsets:
    t = rng.randint(2, 6)
    P = C.random_set(rng, t, rng.choice([3, 6, 20, 60]), rng.random() < 0.3)
    if len(set(P)) != len(P):
        continue
    r = C.analyse(P, "random", verbose=False)
    if not r["GP"]:
        continue
    tested += 1
    if "units" in r and r["units"] != "all hold":
        print(r)
        reps = sorted({min(C.rot(p, k) for k in range(5)) for p in P})
        print("orbit representatives:", reps)
