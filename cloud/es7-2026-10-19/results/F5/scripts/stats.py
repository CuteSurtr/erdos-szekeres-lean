#!/usr/bin/env python3
"""Generator statistics: restarts / chains, histogram of the largest partial realization, completions.
usage: stats.py RUNDIR"""
import glob, json, os, sys, collections
run = sys.argv[1]; out = {}
for f in sorted(glob.glob(os.path.join(run, "armF_*.jsonl"))):
    L = [json.loads(l) for l in open(f)]
    c = collections.Counter(26 if "points" in r else r["maxk"] for r in L)
    out[os.path.basename(f)] = {"restarts": len(L), "realized26": sum("points" in r for r in L),
                                "props": sum(r.get("props", 0) for r in L), "prop_sat": sum(r.get("prop_sat", 0) for r in L),
                                "maxk_hist": dict(sorted(c.items())), "last_t": L[-1]["t"] if L else 0}
for f in sorted(glob.glob(os.path.join(run, "gg*/guided_*.jsonl"))):
    L = [json.loads(l) for l in open(f)]
    out[os.path.basename(f)] = {"chains": len(L), "realized26": sum(r["reached"] == 26 for r in L),
                                "queries": sum(r["queries"] for r in L), "secs": sum(r["secs"] for r in L),
                                "max_reached_hist": dict(sorted(collections.Counter(r["max_reached"] for r in L).items()))}
print(json.dumps(out, indent=1))
