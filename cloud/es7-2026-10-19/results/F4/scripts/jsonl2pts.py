#!/usr/bin/env python3
"""Write every record with "points" of arm_f / realize_models JSONL files as OUTDIR/<id>.pts.
usage: jsonl2pts.py OUTDIR a.jsonl [b.jsonl ...]"""
import json, os, sys
for path in sys.argv[2:]:
    for line in open(path):
        r = json.loads(line)
        if "points" not in r: continue
        name = r.get("id") or f"am{r['model']}"
        fn = os.path.join(sys.argv[1], name + ".pts")
        if os.path.exists(fn): continue
        with open(fn, "w") as f:
            for x, y in r["points"]: f.write(f"{x} {y}\n")
        print(fn)
