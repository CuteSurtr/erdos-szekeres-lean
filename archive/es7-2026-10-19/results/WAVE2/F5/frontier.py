#!/usr/bin/env python3
"""frontier.py DIR OUT.icnf: frontier of a wave-1 case directory (DIR/top.icnf + DIR/leaves.jsonl).
Created cubes = top cubes + parent+sub for each SPLIT record; frontier = created cubes that are
neither closed (status UNSAT with cake_lpr exactly `s VERIFIED UNSAT`) nor split.
Written sorted by Python list order on the integer literal lists. Malformed lines are rejected."""
import json, sys
d, out = sys.argv[1], sys.argv[2]
def cubes(path):
    cs = []
    for l in open(path):
        assert l.startswith("a ") and l.endswith(" 0\n"), l
        cs.append(tuple(map(int, l.split()[1:-1])))
    return cs
top = cubes(d + "/top.icnf")
created, closed, split = set(top), set(), set()
for l in open(d + "/leaves.jsonl"):
    if not l.endswith("\n"): continue      # line still being written
    r = json.loads(l)
    if "cube" not in r: continue
    c = tuple(r["cube"])
    if r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT": closed.add(c)
    elif r.get("status") == "SPLIT":
        split.add(c); created.update(c + tuple(s) for s in r["subs"])
fr = sorted(list(c) for c in created - closed - split)
with open(out, "w") as f:
    for c in fr: f.write("a " + " ".join(map(str, c)) + " 0\n")
print(f"top {len(top)} created {len(created)} closed {len(closed)} split {len(split)} frontier {len(fr)}"
      f" closed_not_created {len(closed - created)}")
import os
if os.path.exists(d + "/open.icnf"):
    op = set(cubes(d + "/open.icnf")); fs = set(map(tuple, fr))
    print(f"open.icnf {len(op)}: in open not frontier {len(op - fs)}, in frontier not open {len(fs - op)}")
