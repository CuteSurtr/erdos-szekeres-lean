#!/usr/bin/env python3
"""Summarize a leaves.jsonl: counts, certified weight (exact, relative to the cube file's root),
solve/check time statistics.  usage: summarize_leaves.py LEAVES.jsonl [ROOT_WEIGHT e.g. 1/4096]"""
import json, statistics, sys
from fractions import Fraction
rows = [json.loads(l) for l in open(sys.argv[1])]
root = Fraction(sys.argv[2]) if len(sys.argv) > 2 else Fraction(1)
last = {}
for r in rows:
    if r["idx"] not in last or r.get("certified") or r["status"] == "SATISFIABLE":
        last[r["idx"]] = r
cert = [r for r in last.values() if r.get("certified")]
uns_unc = [r for r in last.values() if r["status"] == "UNSATISFIABLE" and not r.get("certified")]
sat = [r for r in last.values() if r["status"] == "SATISFIABLE"]
unk = [r for r in last.values() if r["status"] not in ("UNSATISFIABLE", "SATISFIABLE")]
w = sum(Fraction(r["weight"]) for r in cert)
st = [r["solve_s"] for r in cert]
ct = [r["check_s"] for r in cert]
out = {"leaves_seen": len(last), "certified_unsat": len(cert), "unsat_not_certified": len(uns_unc),
       "sat": len(sat), "unknown": len(unk), "certified_weight_rel": str(w),
       "certified_weight_abs": str(w * root), "certified_weight_abs_float": float(w * root)}
if st:
    out.update({"solve_s_mean": round(statistics.mean(st), 1), "solve_s_min": min(st), "solve_s_max": max(st),
                "check_s_mean": round(statistics.mean(ct), 1),
                "proof_GB_mean": round(statistics.mean(r["proof_bytes"] for r in cert) / 1e9, 2)})
if unk:
    out["unknown_limits_s"] = sorted({round(r["solve_s"]) for r in unk})
print(json.dumps(out))
