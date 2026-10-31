#!/usr/bin/env python3
"""Baseline for the relocation walk: plain random restarts of gen.c's near mode
(anneal 33 random points to E <= 1, then a random walk with E <= 1 emitting the
heptagon-free 32-point deletions every EMIT accepted moves).  One start per
call, repeated until the deadline; CPU from gen's own clock() report.

usage: baseline.py OUTDIR ID SECONDS SEED
"""
import os, sys, json, time, random, subprocess, resource
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dlib import b

outdir, wid, seconds, seed = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
out = os.path.join(outdir, f"baseline_b{wid}.txt")
log = open(os.path.join(outdir, f"baseline_b{wid}.jsonl"), "a")
deadline = time.time() + seconds
n = 0
while time.time() < deadline:
    s = rng.randrange(1 << 40)
    r = subprocess.run([b("gen"), "near", "7", "33", str(s), "1", "random:1000000", "300000", "1.0", "0.01",
                        "2000", "200", out], capture_output=True, text=True)
    cpu = None
    for tok in r.stdout.split():
        if tok.startswith("cpu="):
            cpu = float(tok[4:].rstrip("s"))
    log.write(json.dumps({"b": wid, "start": n, "seed": s, "cpu": cpu, "stderr": r.stderr.strip()[-200:]}) + "\n")
    log.flush()
    n += 1
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
json.dump({"b": wid, "starts": n, "child_cpu": round(ru.ru_utime + ru.ru_stime, 1)},
          open(os.path.join(outdir, f"baseline_b{wid}_summary.json"), "w"))
