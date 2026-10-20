#!/usr/bin/env python3
"""Summarize leaves.jsonl for shard Mii-1: per-root closed/open status, LRAT coverage."""
import json, os, sys
from fractions import Fraction
here = os.path.dirname(os.path.abspath(__file__))
recs = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "leaves.jsonl")) if l.strip()]
leaf, split, gap = {}, {}, {}
for r in recs:
    k = tuple(r.get("cube", ()))
    if r["kind"] == "leaf": leaf[k] = r
    elif r["kind"] == "split": split[k] = r
    elif r["kind"] == "gap": gap[k] = r
roots = [(i, tuple(int(x) for x in l.split()[1:-1])) for i, l in enumerate(open(os.path.join(here, "logs", "cubes.icnf"))) if i % 8 == 1]
def node(c):
    """returns (closed, all_lrat_verified, n_unsat_leaves, n_sat, n_open, open_weight rel. to c)"""
    if c in split:
        g = gap.get(c)
        ok = g is not None and g["status"] == "UNSAT"
        lr = ok and g.get("lrat") == "VERIFIED"
        res = [ok, lr, 0, 0, 0 if ok else 0, Fraction(0) if ok else Fraction(0)]
        if not ok and not split[c]["subs"]:
            res[4] += 1; res[5] += 1
        for s in split[c]["subs"]:
            sc, sl, su, ss, so, sw = node(c + tuple(s))
            res[0] &= sc; res[1] &= sl; res[2] += su; res[3] += ss; res[4] += so
            res[5] += sw / 2 ** len(s)
        return tuple(res)
    r = leaf.get(c)
    if r and r["status"] == "UNSAT":
        return (True, r.get("lrat") == "VERIFIED", 1, 0, 0, Fraction(0))
    if r and r["status"] == "SAT":
        return (False, False, 0, 1, 0, Fraction(0))
    return (False, False, 0, 0, 1, Fraction(1))
out = {"roots": {}, "n_roots_seen": len(roots)}
tot = {"closed_roots": 0, "closed_lrat_roots": 0, "unsat_leaves": 0, "sat_leaves": 0, "open_nodes": 0,
       "splits": len(split), "gaps": len(gap), "lrat_failed": sum(1 for r in recs if str(r.get("lrat", "")).startswith("FAILED")),
       "cpu_solve_s": round(sum(r.get("solve_s", 0) for r in recs), 1), "cpu_lrat_s": round(sum(r.get("lrat_s", 0) for r in recs), 1)}
for root, c in roots:
    cl, lr, u, s, o, w = node(c)
    out["roots"][root] = {"cube": list(c), "closed": cl, "lrat_all_verified": lr, "unsat_leaves": u, "sat": s, "open_nodes": o, "open_fraction": str(w)}
    tot["closed_roots"] += cl; tot["closed_lrat_roots"] += cl and lr; tot["unsat_leaves"] += u; tot["sat_leaves"] += s; tot["open_nodes"] += o
out["total"] = tot
print(json.dumps(out, indent=1))
