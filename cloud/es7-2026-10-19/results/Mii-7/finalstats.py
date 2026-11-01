#!/usr/bin/env python3
"""Final statistics for leaves.jsonl (usage: finalstats.py leaves.jsonl state.json)."""
import sys, json
recs = {}
for l in open(sys.argv[1]):
    if l.strip():
        r = json.loads(l)
        if r["status"] != "ERROR": recs[r["id"]] = r
st = json.load(open(sys.argv[2]))
u = [r for r in recs.values() if r["status"] == "UNSAT"]
sp = [r for r in recs.values() if r["status"] == "SPLIT"]
out = {
 "records": len(recs), "unsat": len(u),
 "unsat_cube": sum(1 for r in u if r["kind"] == "cube"), "unsat_gap": sum(1 for r in u if r["kind"] == "gap"),
 "lrat_verified": sum(1 for r in u if r["lrat"] == "VERIFIED"),
 "lrat_failed": sum(1 for r in u if r["lrat"] != "VERIFIED"),
 "sat": sum(1 for r in recs.values() if r["status"] == "SAT"),
 "open_timeout": sum(1 for r in recs.values() if r["status"] == "OPEN"),
 "split": len(sp), "split_children": sum(len(r["children"]) for r in sp),
 "pending_tasks": len(st["pending"]),
 "unsat_solve_s_total": round(sum(r["solve_s"] for r in u)), "unsat_solve_s_max": max(r["solve_s"] for r in u),
 "lrat_check_s_total": round(sum(r["lrat_s"] for r in u)),
 "proof_GB_total": round(sum(r["proof_bytes"] for r in u) / 1e9, 2),
 "split_cadical_s_total": round(sum(r["solve_s"] for r in sp)), "split_march_s_total": round(sum(r["split_s"] for r in sp)),
 "max_depth": max(len(r["cube"]) for r in recs.values()),
}
print(json.dumps(out, indent=1))
