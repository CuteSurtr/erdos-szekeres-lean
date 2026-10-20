#!/usr/bin/env python3
"""Retry: find a realization with |coord| < 2^26 of the exact chirotope of 32-sets whose stored
compressed realization is missing or too large (realizer of results/F, more seeds and budget).
Every result is re-checked exactly against the chirotope of the exact deep-below set.
usage: recompress32.py IN_sets32.jsonl OUT.jsonl budget seeds"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../F/realizer"))
import chiro, realize as R
inp, outp, budget, seeds = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
out = open(outp, "a")
for line in open(inp):
    r = json.loads(line)
    if "points" in r and max(max(abs(x), abs(y)) for x, y in r["points"]) < 2 ** 27: continue
    P = [tuple(p) for p in r["points_exact"]]; chi = chiro.chirotope_of(P)
    for seed in range(100, 100 + seeds):
        res = R.realize(chi, len(P), budget=budget, seed=seed)
        if res["realized"]:
            Q = [tuple(p) for p in res["points"]]; mx = max(max(abs(x), abs(y)) for x, y in Q)
            ok = chiro.verify_exact(Q, chi)[0]
            print(r["id"], seed, ok, mx.bit_length(), flush=True)
            if ok and mx < 2 ** 27:
                rr = dict(r); rr["points"] = [list(p) for p in Q]; rr["compressed_ok"] = True; rr["compressed_max"] = mx
                rr["compressed_by"] = f"recompress32 seed {seed}"
                out.write(json.dumps(rr) + "\n"); out.flush(); break
