#!/usr/bin/env python3
"""Convert anneal32 output lines "seed run startid snap c7 c6 | x,y ..." to pipeline JSONL.
usage: anneal2cands.py OUT.jsonl SETFILE..."""
import json, os, sys
with open(sys.argv[1], "w") as out:
    for f in sys.argv[2:]:
        tag = os.path.basename(f).replace(".sets", "")
        for l in open(f):
            if "|" not in l: continue
            h, t = l.split("|")
            seed, run, start, snap, c7, c6 = h.split()
            pts = [list(map(int, x.split(","))) for x in t.split()]
            if len(pts) != 32: continue
            gen = "anneal32-random" if start == "-1" else "anneal32-from-nearmiss"
            out.write(json.dumps({"id": f"{tag}:{seed}:{run}:{snap}", "gen": gen,
                                  "seed": f"seed {seed} run {run} start {start} snap {snap}", "pts": pts}) + "\n")
