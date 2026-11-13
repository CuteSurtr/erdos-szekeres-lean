#!/usr/bin/env python3
"""Cross-check the C enumerator dfs_convex against brute-force counts on random sets in general position."""
import os
import random
import subprocess
import sys
import tempfile
from test_algorithms import random_gp_set, brute_counts

here = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 100
fails = 0
with tempfile.TemporaryDirectory(dir=here) as td:
    for t in range(trials):
        n = rng.randint(4, 12)
        P = random_gp_set(n, rng.choice([5, 8, 30, 10 ** 6]), rng)
        fn = os.path.join(td, "p.txt")
        with open(fn, "w") as f:
            for x, y in P:
                f.write("%d %d\n" % (x, y))
        out = subprocess.run([os.path.join(here, "dfs_convex"), fn, str(n)], capture_output=True, text=True).stdout
        got = {}
        for line in out.splitlines():
            if line.startswith("convex subsets of size"):
                s, c = line.split("size ")[1].split(": ")
                got[int(s)] = int(c)
        bc = brute_counts(P, n)
        if any(got.get(L, -1) != bc[L] for L in range(3, n + 1)):
            fails += 1
            print("MISMATCH", P, got, bc)
print("C enumerator vs brute force: trials=%d failures=%d" % (trials, fails))
sys.exit(1 if fails else 0)
