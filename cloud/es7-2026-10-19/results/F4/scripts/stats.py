#!/usr/bin/env python3
"""Summary counts of the F4 logs.  usage: stats.py LOGDIR (results/F4/data/logs)"""
import glob, json, os, sys, collections
L = sys.argv[1]; out = {}
R = [json.loads(l) for l in open(os.path.join(L, "am/realize.jsonl"))]
out["abstract_models_attempted"] = len(R); out["abstract_models_realized"] = sum(r["realized"] for r in R)
out["realizer_cpu_s_total"] = round(sum(r["cpu"] for r in R))
out["ins_ff_placed_hist"] = dict(sorted(collections.Counter(r["ins_ff_placed"] for r in R).items()))
for f in sorted(glob.glob(os.path.join(L, "af/*.jsonl"))):
    A = [json.loads(l) for l in open(f)]
    out[os.path.basename(f)] = {"restarts": len(A), "complete_26": sum("points" in a for a in A),
                                "maxk_hist": dict(sorted(collections.Counter(a.get("maxk", 26) for a in A).items()))}
for f in sorted(glob.glob(os.path.join(L, "gg/*.jsonl"))):
    G = [json.loads(l) for l in open(f)]
    out[os.path.basename(f)] = {"chains": len(G), "reached_26": [(g["name"], g["via"]) for g in G if g["reached"] == 26],
                                "max_reached_hist": dict(sorted(collections.Counter(g["max_reached"] for g in G).items())),
                                "hours": round(sum(g["secs"] for g in G) / 3600, 2)}
print(json.dumps(out, indent=1))
