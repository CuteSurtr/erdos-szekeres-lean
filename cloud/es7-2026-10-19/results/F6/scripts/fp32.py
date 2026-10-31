#!/usr/bin/env python3
"""Order-type fingerprints (chiro.canonical_form, relabelling + reflection, sha1[:16]) of 32-point sets,
to count distinct order types among the deep-below sets of both conventions.
usage: fp32.py a.pts ... sets32.jsonl(points_exact) ...   -> JSON lines {set, fp}"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../tools/realizer"))
from chiro import canonical_form, chirotope_of
for f in sys.argv[1:]:
    if f.endswith(".jsonl"):
        L = [(f"{os.path.basename(f)}:{json.loads(l)['id']}", json.loads(l)) for l in open(f) if l.strip()]
        L = [(n, [tuple(p) for p in (r["points_exact"] if "points_exact" in r else r["points"])]) for n, r in L]
    else:
        L = [(os.path.basename(f), [tuple(map(int, l.split())) for l in open(f) if l.strip()])]
    for n, P in L:
        print(json.dumps({"set": n, "fp": hashlib.sha1(canonical_form(chirotope_of(P), len(P)).encode()).hexdigest()[:16]}), flush=True)
