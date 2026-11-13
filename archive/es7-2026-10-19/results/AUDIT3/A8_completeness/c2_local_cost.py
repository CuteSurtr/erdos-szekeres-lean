#!/usr/bin/env python3
"""Cost (from the records) of re-solving the central-34 facts that rest only on Mac (LOCAL) records, and the covers.
usage: c2_local_cost.py RESULTS_DIR"""
import glob, itertools, json, os, sys
from collections import defaultdict
RES = sys.argv[1]; T = 17
best = defaultdict(list)
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for l in open(f):
        if l.strip():
            r = json.loads(l)
            if r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                best[r["unit"]].append((src, r["solve_s"], r["lrat_check_s"], r["cake_s"], r["proof_bytes"], r.get("solve_rss_mb")))
local_only = []
for a in range(1, 9):
    inner = [o for o in range(1, T) if o != a]; seen = set()
    for h in (2, 3):
        for V in itertools.combinations(inner, h):
            n = f"P{a}_" + "-".join(map(str, V)); m = f"P{a}_" + "-".join(map(str, sorted((a - i) % T for i in V)))
            k = frozenset((n, m))
            if k in seen: continue
            seen.add(k)
            recs = [(u, x) for u in k for x in best.get(u, [])]
            if recs and all("LOCAL" in x[0] for u, x in recs):
                local_only.append(min(recs, key=lambda t: t[1][1]))
tot = lambda xs: sum(x[1] + x[2] + x[3] for _, x in xs)
print("orbits resting only on LOCAL records:", len(local_only))
print("  their cheapest supporting records: solve %.1f h, lrat %.2f h, cake %.1f h, total %.1f h; proofs %.0f GB; max RSS %.1f GB" % (
    sum(x[1] for _, x in local_only)/3600, sum(x[2] for _, x in local_only)/3600, sum(x[3] for _, x in local_only)/3600,
    tot(local_only)/3600, sum(x[4] for _, x in local_only)/1e9, max((x[5] or 0) for _, x in local_only)/1e3))
print("  solve time range %.0f..%.0f s" % (min(x[1] for _, x in local_only), max(x[1] for _, x in local_only)))
covers = [(u, x) for u in (f"P{a}_cover" for a in range(1, 8)) for x in best.get(u, [])]
print("covers P1..P7:", len(covers), "solve %.2f h + lrat %.2f h + cake %.2f h = %.2f h; proofs %.1f GB; RSS max %.1f GB" % (
    sum(x[1] for _, x in covers)/3600, sum(x[2] for _, x in covers)/3600, sum(x[3] for _, x in covers)/3600, tot(covers)/3600,
    sum(x[4] for _, x in covers)/1e9, max((x[5] or 0) for _, x in covers)/1e3))
