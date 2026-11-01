#!/usr/bin/env python3
"""Cross-check the C program lcs_dp (both DPs) against brute force on random sets in general position."""
import os, random, subprocess, sys, tempfile
from test_algorithms import random_gp_set
from geom_check import brute_largest
here = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 9)
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 150
fails = 0
with tempfile.TemporaryDirectory(dir=here) as td:
    fn = os.path.join(td, "p.txt")
    for t in range(trials):
        n = rng.randint(4, 13)
        P = random_gp_set(n, rng.choice([5, 8, 30, 10 ** 6]), rng)
        with open(fn, "w") as f:
            f.writelines("%d %d\n" % p for p in P)
        out = subprocess.run([os.path.join(here, "lcs_dp"), fn], capture_output=True, text=True).stdout
        A = int(out.split("(A) angular DP: largest convex subset = ")[1].split()[0])
        wok = "convex by triangle test = 1" in out
        B = int(out.split("(B) cup+cap DP: largest convex subset = ")[1].split()[0])
        c = brute_largest(P)
        if not (A == B == c and wok):
            fails += 1
            print("MISMATCH", P, A, B, c, wok)
print("C lcs_dp vs brute force: trials=%d failures=%d" % (trials, fails))
sys.exit(1 if fails else 0)
