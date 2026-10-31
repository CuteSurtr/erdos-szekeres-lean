#!/usr/bin/env python3
"""Find a realization with |coordinates| < 2^27 (sat.c's bound) of the exact labelled chirotope of a
32-point set, with the validated realizer; accepted only after an exact re-check (verify_exact).
Writes <file>_small.pts.  usage: compress32.py BUDGET a.pts [b.pts ...]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
from chiro import chirotope_of, verify_exact  # noqa
from realize import realize  # noqa
budget = float(sys.argv[1])
for fn in sys.argv[2:]:
    P = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
    chi = chirotope_of(P); out = {"file": os.path.basename(fn), "found": False}
    for seed in range(2):
        res = realize(chi, len(P), budget=budget, seed=seed)
        if res["realized"]:
            Q = [tuple(p) for p in res["points"]]
            mx = max(max(abs(x), abs(y)) for x, y in Q)
            out.update(method=res["method"], max_abs=mx)
            if verify_exact(Q, chi)[0] and mx < 2 ** 27:
                with open(fn.replace(".pts", "_small.pts"), "w") as f:
                    for x, y in Q: f.write(f"{x} {y}\n")
                out["found"] = True; break
    print(json.dumps(out), flush=True)
