#!/usr/bin/env python3
"""Collect one-heptagon 33-point sets from the annealing logs (distinct order
types, re-counted with cgon) as walk seeds in nearfull format
"label 1 33 x1 y1 ...".   usage: anneal_seeds.py RUNSDIR OUTFILE"""
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib, walk

runs, outp = sys.argv[1], sys.argv[2]
recs = []
for f in sorted(glob.glob(os.path.join(runs, "anneal", "anneal_w*.jsonl"))):
    for line in open(f):
        r = json.loads(line)
        if r.get("recount7") == 1:
            recs.append(r)
sigs = dlib.canon([r["pts"] for r in recs])
seen = set(); n = 0
with open(outp, "w") as f:
    for r, (c, cm) in zip(recs, sigs):
        k = walk.h(cm)
        if k in seen:
            continue
        cg = dlib.cgon_count(r["pts"], 8)
        if cg[7] != 1:
            continue
        seen.add(k)
        f.write(f"A{r['w']}_{r['run']}_{r['family']} 1 33 " + " ".join(f"{x} {y}" for x, y in r["pts"]) + "\n")
        n += 1
print(n, "distinct one-heptagon sets")
