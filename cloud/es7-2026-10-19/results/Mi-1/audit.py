#!/usr/bin/env python3
"""Audit leaves.jsonl: every shard cube (i % 4 == 1 of cubes.icnf) must be closed, i.e. an UNSAT
record with lrat VERIFIED, or a SPLIT record whose cover check is UNSAT + VERIFIED and whose
children are all closed (recursively).  usage: audit.py <cubes.icnf> <leaves.jsonl>
"""
import sys, json
cubes = [[int(x) for x in l.split()[1:-1]] for l in open(sys.argv[1]) if l.startswith('a')]
shard = [c for i, c in enumerate(cubes) if i % 4 == 1]
rec = {}
for l in open(sys.argv[2]):
    r = json.loads(l); rec.setdefault(tuple(r["cube"]), []).append(r)
stats = {"shard_cubes": len(shard), "records": sum(map(len, rec.values())), "unsat_leaves_verified": 0,
         "splits_cover_verified": 0, "open": [], "sat": [], "lrat_failed": 0, "total_solve_s": 0.0}
for rs in rec.values():
    for r in rs:
        stats["total_solve_s"] += r["solve_s"]
        if r["status"] == "UNSAT" and r.get("lrat") != "VERIFIED": stats["lrat_failed"] += 1
def closed(c):
    for r in rec.get(tuple(c), []):
        if r["status"] == "SAT": stats["sat"].append(c); return False
        if r["status"] == "UNSAT" and r.get("lrat") == "VERIFIED":
            stats["unsat_leaves_verified"] += 1; return True
        if r["status"] == "SPLIT":
            cc = r["cover_check"]
            ok = cc["status"] == "UNSAT" and cc.get("lrat") == "VERIFIED"
            ok = all([closed(k) for k in r["children"]]) and ok
            if ok: stats["splits_cover_verified"] += 1
            return ok
    stats["open"].append(c); return False
stats["shard_closed"] = sum(closed(c) for c in shard)
stats["entire_shard_closed"] = stats["shard_closed"] == len(shard) and not stats["sat"]
stats["total_solve_s"] = round(stats["total_solve_s"], 1)
print(json.dumps(stats))
