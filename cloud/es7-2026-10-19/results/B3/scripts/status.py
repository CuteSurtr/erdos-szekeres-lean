#!/usr/bin/env python3
"""Progress of the two-level run: per top cube (done or in progress) sub-cubes solved/total,
summed solve time, timeouts. usage: status.py TLDIR"""
import glob, json, os, sys
D = sys.argv[1]
done = {}
if os.path.exists(f"{D}/top.jsonl"):
    for l in open(f"{D}/top.jsonl"):
        r = json.loads(l); done[r["id"]] = r
for d in sorted(glob.glob(f"{D}/c*")):
    cid = int(os.path.basename(d)[1:])
    if cid in done: continue
    w = f"{d}/w0.log"
    if not os.path.exists(w): print(cid, "marching"); continue
    rows = [l.split() for l in open(w) if not l.startswith("#")]
    tot = open(w).readline().split("total_cubes=")[1].split()[0]
    print(cid, "solving", f"{len(rows)}/{tot}", "sum_s=%.0f" % sum(float(r[2]) for r in rows),
          "T=%d" % sum(r[1] == "T" for r in rows), "S=%d" % sum(r[1] == "S" for r in rows))
for r in done.values():
    print(r["id"], r["status"], "march=%.0f n_sub=%d solve=%.0f max=%.0f T=%d wall=%.0f" %
          (r["march_s"], r["n_sub"], r["solve_s"], r["max_sub_s"], r["n_T"], r["wall_s"]))
