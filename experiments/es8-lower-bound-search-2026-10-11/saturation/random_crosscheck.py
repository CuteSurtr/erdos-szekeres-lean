#!/usr/bin/env python3
"""Random small instances: compare `sat sat` with independent.py (bad face sets and face counts)."""
import random, subprocess, sys, os, json
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brute_test import gp, convex_position, BUILD
HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
fails = 0; tot_bad = 0; tot_faces = 0
for t in range(trials):
    n = rng.randint(6, 9); R = rng.choice([5, 12, 50, 10**6])
    while True:
        S = [(rng.randint(-R, R), rng.randint(-R, R)) for _ in range(n)]
        if len(set(S)) == n and gp(S): break
    c = max(k for k in range(3, n + 1) if any(convex_position(list(s)) for s in combinations(S, k)))
    path = os.path.join(BUILD, "tmp_rand.txt"); open(path, "w").write("".join(f"{x} {y}\n" for x, y in S))
    for K in sorted({c, c + 1, min(c + 2, n + 1)}):
        if K < 4: continue
        badp = os.path.join(BUILD, "tmp_rand_bad.txt")
        certp = os.path.join(BUILD, "tmp_rand_cert.txt"); uncp = os.path.join(BUILD, "tmp_rand_unc.txt")
        cout = json.loads(subprocess.run([os.path.join(BUILD, "sat"), "sat", path, str(K), badp, certp], capture_output=True, text=True, check=True).stdout)
        vout = json.loads(subprocess.run([os.path.join(BUILD, "verify"), path, str(K), certp, uncp], capture_output=True, text=True, check=True).stdout)
        vunc = {l.strip() for l in open(uncp) if l.strip()}
        r = subprocess.run([sys.executable, os.path.join(HERE, "independent.py"), path, str(K), badp], capture_output=True, text=True)
        iout = json.loads(r.stdout)
        ok = (r.returncode == 0 and vunc == {l.split()[-1] for l in open(badp) if l.strip()} and vout["uncovered_distinct_faces"] == iout["bad_faces"] and vout["faces_E_minus_V_plus_1"] == vout["distinct_faces_hit"] == iout["faces_euler"] and cout["faces_euler"] == cout["faces_hit_by_valid_candidates"] == iout["faces_enumerated"] == iout["faces_euler"])
        tot_bad += iout["bad_faces"]; tot_faces += iout["faces_enumerated"]
        if not ok:
            fails += 1; print("FAIL", S, K, cout, iout)
print(json.dumps({"trials": trials, "fails": fails, "total_faces_compared": tot_faces, "total_bad_faces_matched": tot_bad}))
sys.exit(1 if fails else 0)
