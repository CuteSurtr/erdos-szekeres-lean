#!/usr/bin/env python3
"""Aggregate logs/small.jsonl and logs/big.jsonl of ties.py."""
import json
import sys

tot = {}
by = {}
fails = []
rows = []
for path in sys.argv[1:]:
    for line in open(path):
        if not line.strip():
            continue
        d = json.loads(line)
        lab = d.get("path") or f"random m={d.get('m')}"
        if d.get("subsets"):
            lab += f" subsets({d['subsets']})"
        rows.append((lab, d["sets"], d["tie_frames"], d["generic_frames"], d["tied_pairs"],
                     d["tie_frames_strict_relation_misses_max_polygon"], len(d["fail"]),
                     {k: (v["gon"], v["nogon"]) for k, v in d["by"].items()}, d.get("secs")))
        for k in ("sets", "tie_frames", "generic_frames", "tied_pairs", "inv_differs_in_gap", "canonical_gaps",
                  "tie_frames_on_max_polygon_edge", "tie_frames_tie_changes_some_chain",
                  "tie_frames_tie_changes_max_chain", "tie_frames_strict_relation_misses_max_polygon",
                  "angular_order_failures", "tied_points_inside_some_Px"):
            tot[k] = tot.get(k, 0) + d[k]
        for k, v in d["by"].items():
            b = by.setdefault(k, {})
            for kk, vv in v.items():
                b[kk] = b.get(kk, 0) + vv
        fails += d["fail"]
for r in rows:
    print(r)
print(json.dumps(tot, indent=1))
print(json.dumps(by, indent=1))
print("FAILURES:", len(fails))
for f in fails[:10]:
    print(f)
