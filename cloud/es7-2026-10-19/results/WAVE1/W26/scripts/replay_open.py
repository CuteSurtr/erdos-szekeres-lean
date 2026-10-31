#!/usr/bin/env python3
"""replay_open.py OUTDIR: rebuild OUTDIR/open.icnf from top.icnf + leaves.jsonl (same rules as resume)."""
import json, sys
d = sys.argv[1]; rs = [json.loads(l) for l in open(f"{d}/leaves.jsonl")]
done = {tuple(r["cube"]) for r in rs if "cube" in r and r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"}
splits = {tuple(r["cube"]): r["subs"] for r in rs if r.get("status") == "SPLIT"}
op = []
def ex(c):
    t = tuple(c)
    if t in done: return
    if t in splits:
        for s in splits[t]: ex(c + s)
    else: op.append(c)
for l in open(f"{d}/top.icnf"):
    if l.startswith("a"): ex(list(map(int, l.split()[1:-1])))
with open(f"{d}/open.icnf", "w") as f:
    for c in sorted(op, key=len): f.write("a " + " ".join(map(str, c + [0])) + "\n")
print(len(done), "verified", len(op), "open")
