#!/usr/bin/env python3
"""Read hc34/results.jsonl (records may be split by a stray newline after '"process') and print valid JSON lines."""
import json, sys
txt = open(sys.argv[1]).read().replace('"process\n', '"')
for line in txt.splitlines():
    if line.strip():
        r = json.loads(line)
        if isinstance(r.get("solve_s"), str):
            r["solve_s"] = float(r["solve_s"].split()[-1]) if r["solve_s"].strip() else None
        print(json.dumps(r))
