#!/usr/bin/env python3
"""Convention A follow-up to F2/s2 build32.py.  For each 32-set record (with points_exact) that has
no compressed realization ("points"), retry the validated realizer on its exact chirotope with more
seeds and a longer budget; accept only after chiro.verify_exact and |coord| < 2^27.  If that still
fails, the record keeps "points" = points_exact and "compressed_ok" = false: saturate32.py then runs
the abstract test on the exact set and sat.c reports the coordinate bound (geometric test not run).
usage: conva_fix.py IN_sets32_full.jsonl OUT.jsonl [budget] [seeds]"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../F/realizer"))
import chiro, realize as R
inp, outp = sys.argv[1:3]; budget = float(sys.argv[3]) if len(sys.argv) > 3 else 120; ns = int(sys.argv[4]) if len(sys.argv) > 4 else 6
out = open(outp, "w")
for l in open(inp):
    r = json.loads(l)
    if "points_exact" not in r: continue
    if "points" not in r or not r.get("compressed_ok") or r.get("compressed_max", 1 << 60) >= 2 ** 27:
        r["compressed_ok"] = False
        P = [tuple(p) for p in r["points_exact"]]; chi = chiro.chirotope_of(P); r["compress_retry"] = False
        for seed in range(11, 11 + ns):
            z = R.realize(chi, len(P), budget=budget, seed=seed)
            if z["realized"]:
                Q = [tuple(p) for p in z["points"]]; mx = max(max(abs(x), abs(y)) for x, y in Q)
                if chiro.verify_exact(Q, chi)[0] and mx < 2 ** 27:
                    r.update(points=[list(p) for p in Q], compressed_ok=True, compressed_max=mx, compress_retry=True); break
        if not r.get("compressed_ok"):
            r.update(points=r["points_exact"], compressed_ok=False)
    out.write(json.dumps(r) + "\n")
    print(json.dumps({k: v for k, v in r.items() if "points" not in k}), flush=True)
