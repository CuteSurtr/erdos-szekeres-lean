#!/usr/bin/env python3
"""List the distinct closed cubes of a cnc2 run that have no VERIFIED LRAT record yet.

usage: reconcile.py <closed.txt> <out.txt> <lrat.jsonl> [<lrat.jsonl> ...]
Writes the unchecked cubes to out.txt in closed.txt format (time -1) for lrat_spot.py, and
prints a JSON summary.  A cube counts as checked only if some record lists exactly that cube
(same literals, same order) with lrat_check == VERIFIED.
"""
import sys, json
closed, out, logs = sys.argv[1], sys.argv[2], sys.argv[3:]
cubes = []
seen = set()
for line in open(closed):
    t = line.split()
    if not t: continue
    c = tuple(int(x) for x in t[1:-1])
    if c not in seen: seen.add(c); cubes.append(c)
ver, notver = set(), 0
for p in logs:
    for line in open(p):
        r = json.loads(line)
        if r.get("lrat_check") == "VERIFIED": ver.add(tuple(r["cube"]))
        else: notver += 1
todo = [c for c in cubes if c not in ver]
with open(out, "w") as f:
    for c in todo: f.write("-1 " + " ".join(map(str, c)) + " 0\n")
print(json.dumps({"closed_distinct": len(cubes), "verified_distinct": len(seen & ver), "unchecked": len(todo),
                  "non_verified_records": notver}))
