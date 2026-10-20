#!/usr/bin/env python3
"""Summarize Mii-4 leaves: per top cube closed/open, LRAT coverage, closed weight (fraction of shard)."""
import json, sys
from fractions import Fraction
D = sys.argv[1]
recs = {}
for l in open(D + "/leaves.jsonl"):
    r = json.loads(l); recs[r["id"]] = r
st = json.load(open(D + "/state.json"))
jobs = {j["id"]: j for j in st["jobs"]}
def closed(jid):
    r = recs.get(jid)
    if r is None: return False
    if r["status"] == "UNSATISFIABLE": return r.get("lrat") == "VERIFIED"
    if r["status"] == "SPLIT": return all(closed(c) for c in r["children"])
    return False
def weight(jid, base):  # closed fraction of the parent, counting each sub-cube by 2^-(depth below parent)
    r = recs.get(jid)
    if r is None: return Fraction(0)
    if r["status"] == "UNSATISFIABLE" and r.get("lrat") == "VERIFIED": return Fraction(1)
    if r["status"] != "SPLIT": return Fraction(0)
    subs = [jobs[c] for c in r["children"] if jobs[c]["kind"] == "cube"]
    rem = [c for c in r["children"] if jobs[c]["kind"] == "remainder"][0]
    w = sum(Fraction(1, 2 ** (len(s["cube"]) - len(jobs[jid]["cube"]))) * weight(s["id"], 0) for s in subs)
    tot = sum(Fraction(1, 2 ** (len(s["cube"]) - len(jobs[jid]["cube"]))) for s in subs)
    return w + ((1 - tot) if closed(rem) else 0)
tops = [j for j in st["jobs"] if len(j["cube"]) == 7 and j["kind"] == "cube"]
out = {"tops": []}
for t in sorted(tops, key=lambda j: j["top"]):
    out["tops"].append({"line": t["top"], "closed": closed(t["id"]), "closed_weight": float(weight(t["id"], 0))})
leaf = [r for r in recs.values() if r["status"] != "SPLIT"]
out["leaf_jobs_finished"] = len(leaf)
out["unsat_lrat_verified"] = sum(r["status"] == "UNSATISFIABLE" and r.get("lrat") == "VERIFIED" for r in leaf)
out["unsat_lrat_not_verified"] = sum(r["status"] == "UNSATISFIABLE" and r.get("lrat") != "VERIFIED" for r in leaf)
out["sat"] = sum(r["status"] == "SATISFIABLE" for r in leaf)
out["other"] = sum(r["status"] not in ("UNSATISFIABLE", "SATISFIABLE") for r in leaf)
out["splits"] = sum(r["status"] == "SPLIT" for r in recs.values())
out["jobs_pending"] = sum(1 for j in st["jobs"] if j["id"] not in recs)
out["top_cubes_closed"] = sum(t["closed"] for t in out["tops"])
out["shard_closed_weight_fraction"] = sum(t["closed_weight"] for t in out["tops"]) / 16
out["shard_closed"] = all(t["closed"] for t in out["tops"])
print(json.dumps(out, indent=1))
