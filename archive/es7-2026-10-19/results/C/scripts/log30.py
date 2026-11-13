#!/usr/bin/env python3
"""Append the latest checkpoint of each cnc2 run to one log every 30 minutes.
usage: log30.py <out.jsonl> <stop-epoch> <rundir> [<rundir> ...]"""
import sys, json, time, os
out, stop, dirs = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
while True:
    with open(out, "a") as f:
        for d in dirs:
            try:
                rec = json.load(open(os.path.join(d, "latest.json")))
                rec = {k: rec[k] for k in ("wall", "open", "open_min_depth", "open_max_depth", "open_depth_hist", "closed",
                                           "closed_weight", "closed_weight_float", "jobs", "splits", "sat")}
                f.write(json.dumps({"run": os.path.basename(d.rstrip("/")), "logged": time.strftime("%H:%M:%S"), **rec}) + "\n")
            except Exception as e:
                f.write(json.dumps({"run": d, "error": str(e)}) + "\n")
    if time.time() > stop: break
    time.sleep(1800)
