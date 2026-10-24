#!/usr/bin/env python3
"""Summary of the B2 runs: C&C frontier (from state.json / progress) and Knuth probe estimates.
Knuth's estimator is unbiased for the fixed-budget tree but heavy-tailed; we report the mean,
the median, min/max and a bootstrap 90% interval of the mean, in nodes and in core-hours
(wall seconds of one dedicated worker process; the session ran 4 processes on 4 cores).
usage: summarize.py WORK_DIR OUT.json"""
import json, random, statistics, sys
from fractions import Fraction
from pathlib import Path

W = Path(sys.argv[1]); out = {}
for tag in ("k7a5u7N27", "k7a5u6N26", "k6a5u6N16"):
    d = W / "runs" / tag
    if not (d / "state.json").exists():
        continue
    st = json.loads((d / "state.json").read_text())
    hist = {}
    for c, _ in st["open"]:
        hist[len(c)] = hist.get(len(c), 0) + 1
    ow = sum((Fraction(1, 2 ** len(c)) for c, _ in st["open"]), Fraction(0))
    out[tag] = {"jobs": st["jobs"], "splits": st["splits"], "closed": st["closed"], "open": len(st["open"]),
                "closed_weight_exact": st["closed_weight"], "open_weight_exact": f"{ow.numerator}/{ow.denominator}",
                "open_depth_hist": {str(k): hist[k] for k in sorted(hist)}, "sat": st["sat"]}
for f in sorted((W / "runs" / "knuth").glob("*_s[0-9]*.jsonl")):
    P = [json.loads(l) for l in open(f)]
    fin = [p for p in P if p["end"] == "closed"]
    if not fin:
        continue
    nodes = [p["est_nodes"] for p in fin]; cost_h = [p["est_cost_s"] / 3600 for p in fin]
    rng = random.Random(0); boots = []
    for _ in range(2000):
        s = [rng.choice(cost_h) for _ in cost_h]; boots.append(sum(s) / len(s))
    boots.sort()
    out[f.stem] = {"probes": len(P), "closed_probes": len(fin), "censored": sum(p["end"] == "censored" for p in P),
                   "sat_probes": sum(p["end"] == "SAT" for p in P),
                   "leaf_depths": [p["leaf_depth"] for p in fin],
                   "nodes_mean": statistics.mean(nodes), "nodes_median": statistics.median(nodes),
                   "nodes_min": min(nodes), "nodes_max": max(nodes),
                   "core_h_mean": round(statistics.mean(cost_h)), "core_h_median": round(statistics.median(cost_h)),
                   "core_h_min": round(min(cost_h)), "core_h_max": round(max(cost_h)),
                   "core_h_boot90": [round(boots[100]), round(boots[1900])],
                   "mean_node_s": round(statistics.mean(s for p in fin for s in p["secs"]), 2)}
Path(sys.argv[2]).write_text(json.dumps(out, indent=1)); print(json.dumps(out, indent=1))
