#!/usr/bin/env python3
"""Summarise leaves.jsonl: which shard nodes are closed, open or SAT.  usage: status.py leaves.jsonl"""
import json, sys, collections
recs = {}
for l in open(sys.argv[1]):
    r = json.loads(l); recs[r["key"]] = r
def closed(k):
    r = recs.get(k)
    if r is None: return False
    if r["status"] == "unsat": return r.get("lrat_check") == "VERIFIED"
    if r["status"] == "split":
        return all(closed("cube:" + " ".join(map(str, c))) for c in r["children"]) and closed("residual:" + r["key"][5:])
    return False
tops = [r for r in recs.values() if r["parent"] is None]
c = collections.Counter(r["status"] for r in recs.values())
leaves = [r for r in recs.values() if r["status"] in ("unsat", "sat")]
s = {"top_cubes_recorded": len(tops), "top_cubes_closed": sum(closed(r["key"]) for r in tops),
     "records_by_status": dict(c), "unsat_leaves": c["unsat"],
     "unsat_lrat_verified": sum(r.get("lrat_check") == "VERIFIED" for r in leaves),
     "sat_leaves": c["sat"], "split_nodes": c["split"],
     "open_unknown_records": c["unknown"],
     "max_depth": max((r["depth"] for r in recs.values()), default=0),
     "solve_cpu_s": round(sum(r.get("solve_s", 0) for r in recs.values())),
     "max_solve_s": max((r.get("solve_s", 0) for r in recs.values()), default=0)}
print(json.dumps(s, indent=1))
