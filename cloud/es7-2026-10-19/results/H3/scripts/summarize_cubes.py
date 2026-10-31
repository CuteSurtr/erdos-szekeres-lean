#!/usr/bin/env python3
"""Summarise check_cubes.sh output against a closed.txt cube list.
usage: summarize_cubes.py CLOSED.txt RESULT.jsonl [RESULT.jsonl ...]"""
import json, sys
from fractions import Fraction
closed = {tuple(int(t) for t in l.split()[1:-1]) for l in open(sys.argv[1]) if l.strip()}
res = {}
for f in sys.argv[2:]:
    for l in open(f):
        x = json.loads(l); res[tuple(x["cube"])] = x
ok = {c for c, x in res.items() if x["cake_lpr"] == "s VERIFIED UNSAT"}
bad = {c: x["cake_lpr"] for c, x in res.items() if c not in ok}
w = lambda S: sum(Fraction(1, 2 ** len(c)) for c in S)
print(json.dumps({
    "closed_cubes": len(closed), "checked": len(set(res) & closed),
    "cake_lpr_verified": len(ok & closed), "not_verified": len(bad), "not_verified_examples": list(bad.items())[:3],
    "verified_weight": float(w(ok & closed)), "closed_weight": float(w(closed)),
    "solve_s": round(sum(x["solve_s"] for x in res.values()), 1),
    "check_s": round(sum(x["check_s"] for x in res.values()), 1),
    "max_proof_bytes": max((x["proof_bytes"] for x in res.values()), default=0),
    "total_proof_bytes": sum(x["proof_bytes"] for x in res.values())}, indent=1))
