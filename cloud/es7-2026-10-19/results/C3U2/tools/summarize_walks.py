#!/usr/bin/env python3
"""Summarize knuth_adaptive.py walks: Knuth estimates of total solver time (core-seconds) and
solver calls for the whole layer tree, by policy (budgets), with standard errors, split by top case
type, and with the H3 mirror reduction applied (walks through H3 are scaled by 100/190, the ratio of
kept to all H3 layer-2 options; this assumes mirror-image subtrees cost the same, which holds in
expectation only approximately).  usage: summarize_walks.py WALKS.jsonl [...]"""
import json
import math
import sys
from collections import defaultdict


def stats(xs):
    n = len(xs)
    mu = sum(xs) / n
    se = math.sqrt(sum((x - mu) ** 2 for x in xs) / (n - 1) / n) if n > 1 else float("nan")
    return mu, se


pol = defaultdict(list)
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        if r["outcome"] != "closed":
            continue
        top = r["path"][0]["case"].split("_")[0] if r["path"] else "?"
        pol[tuple(r["budgets"])].append((top, r["est_seconds"], r["est_solver_calls"], max(p["d"] for p in r["path"])))
out = []
for b, ws in pol.items():
    raw = [w[1] for w in ws]
    mir = [w[1] * (100 / 190 if w[0] == "0s0" else 1) for w in ws]
    h3 = [w for w in ws if w[0] == "0s0"]
    mu, se = stats(raw)
    mm, ms = stats(mir)
    rec = {"budgets": list(b), "walks": len(ws), "walks_through_H3": len(h3),
           "est_core_hours": round(mu / 3600), "se_core_hours": round(se / 3600) if se == se else None,
           "est_core_hours_mirror": round(mm / 3600), "se_core_hours_mirror": round(ms / 3600) if ms == ms else None,
           "est_solver_calls": round(sum(w[2] for w in ws) / len(ws)),
           "max_depth_hist": {d: sum(1 for w in ws if w[3] == d) for d in sorted({w[3] for w in ws})},
           "H3_share_of_estimate": round(sum(w[1] for w in h3) / sum(raw), 3) if raw else None}
    out.append(rec)
    print(json.dumps(rec))
