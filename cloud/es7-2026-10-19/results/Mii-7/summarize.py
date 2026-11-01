#!/usr/bin/env python3
"""Summarize leaves.jsonl of shard.py: per top-level cube, whether it is closed.

usage: summarize.py <leaves.jsonl> <cubes.icnf> <mod> <rem>

A task is closed-by-LRAT iff it is UNSAT with lrat VERIFIED, or it was SPLIT and every child
(sub-cubes and the gap task) is closed-by-LRAT.  Weight of a cube = 2^-len(cube) relative to
its top-level cube (gap tasks carry no weight of their own; they close the refuted branches).
"""
import sys, json
from fractions import Fraction
leaves, icnf, mod, rem = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
recs = {}
for line in open(leaves):
    if line.strip():
        r = json.loads(line)
        if r["status"] != "ERROR": recs[r["id"]] = r
top = [l.split()[1:-1] for l in open(icnf) if l.startswith('a')]
ids = ["c%d" % i for i in range(len(top)) if i % mod == rem]

def closed(tid):
    r = recs.get(tid)
    if r is None: return False
    if r["status"] == "UNSAT": return r["lrat"] == "VERIFIED"
    if r["status"] == "SPLIT": return all(closed(c["id"]) for c in r["children"])
    return False

def weight(tid, base):   # closed weight fraction of this node's subtree
    r = recs.get(tid)
    if r is None: return Fraction(0)
    if r["status"] == "UNSAT": return Fraction(1) if r["lrat"] == "VERIFIED" else Fraction(0)
    if r["status"] == "SPLIT":
        w = Fraction(0)
        for c in r["children"]:
            if c["kind"] == "cube":
                w += Fraction(1, 2 ** (len(c["cube"]) - base)) * weight(c["id"], len(c["cube"]))
        if closed(tid): return Fraction(1)
        return w
    return Fraction(0)

cnt = {}
for r in recs.values():
    k = (r["kind"], r["status"], r.get("lrat"))
    cnt[str(k)] = cnt.get(str(k), 0) + 1
tops = []
for t in ids:
    r = recs.get(t)
    L = len(r["cube"]) if r else 7
    tops.append({"id": t, "closed": closed(t), "status": r["status"] if r else "pending",
                 "closed_weight": float(weight(t, L))})
unsat = [r for r in recs.values() if r["status"] == "UNSAT"]
out = {"top_cubes": len(ids), "top_closed": sum(1 for x in tops if x["closed"]),
       "shard_closed_weight": sum(x["closed_weight"] for x in tops) / len(ids),
       "records": len(recs), "by_kind_status_lrat": cnt,
       "unsat_leaves": len(unsat), "unsat_lrat_verified": sum(1 for r in unsat if r["lrat"] == "VERIFIED"),
       "sat_leaves": [r["id"] for r in recs.values() if r["status"] == "SAT"],
       "open_leaves": [r["id"] for r in recs.values() if r["status"] == "OPEN"],
       "per_top": tops}
print(json.dumps(out, indent=1))
