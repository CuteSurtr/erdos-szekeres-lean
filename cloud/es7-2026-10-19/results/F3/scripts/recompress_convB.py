#!/usr/bin/env python3
"""Post-pass for convention B (F2 process26.py) 32-sets without a <2^27 realization: run the validated
realizer on the exact chirotope (seeds 200.., budget B), accept only after chiro.verify_exact and
|coord| < 2^27, write <name>_small.pts next to it; the caller then runs check32.py on the new files.
usage: recompress_convB.py BUDGET SEEDS a.pts [b.pts ...]"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../F/realizer"))
import chiro, realize as R
budget, seeds = float(sys.argv[1]), int(sys.argv[2])
for fn in sys.argv[3:]:
    if fn.endswith("_small.pts") or os.path.exists(fn[:-4] + "_small.pts"): continue
    P = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]; chi = chiro.chirotope_of(P)
    out = {"file": os.path.basename(fn), "found": False}
    for seed in range(200, 200 + seeds):
        z = R.realize(chi, len(P), budget=budget, seed=seed)
        if z["realized"]:
            Q = [tuple(p) for p in z["points"]]; mx = max(max(abs(x), abs(y)) for x, y in Q)
            if chiro.verify_exact(Q, chi)[0] and mx < 2 ** 27:
                open(fn[:-4] + "_small.pts", "w").write("".join(f"{x} {y}\n" for x, y in Q))
                out.update(found=True, seed=seed, max_abs=mx); break
    print(json.dumps(out), flush=True)
