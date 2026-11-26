#!/usr/bin/env python3
"""n66-resolve-20261125: tally the re-solve against the receipts (PLAN.md, Outcome).
A leaf counts only if its certify.jsonl has verdict "s VERIFIED UNSAT", its cnf_sha256 equals the receipt's
trim_cnf_sha256_recorded, the kept .lrat.zst exists, and the cake output holds the exact line "s VERIFIED UNSAT".
usage: tally.py  (writes tally.json; exit 0 only when all 105 leaves count)"""
import json, os, sys

O = "/home/jay/research/data/n66-resolve-20261125"
done, bad, todo = [], [], []
for line in open(f"{O}/leaves.tsv"):
    d, want, _ = line.rstrip("\n").split("\t")
    lid = d.removeprefix("p2/").removesuffix("/it1").replace("/", "_")
    j = f"{O}/out/{lid}/certify.jsonl"
    if not os.path.exists(j):
        todo.append(lid); continue
    recs = [json.loads(x) for x in open(j) if x.strip()]
    r = recs[-1]
    cake = f"{O}/out/{lid}/trim.cake.out"
    ok = (r.get("verdict") == "s VERIFIED UNSAT" and r.get("cnf_sha256") == want
          and os.path.exists(r.get("proof", "")) and os.path.exists(cake)
          and "s VERIFIED UNSAT" in open(cake).read().splitlines())
    (done if ok else bad).append({"leaf": lid, "verdict": r.get("verdict"), "cnf_ok": r.get("cnf_sha256") == want,
                                  "lrat_sha256": r.get("lrat_sha256"), "cadical_s": r.get("cadical_s"),
                                  "cake_s": r.get("cake_s"), "attempts": len(recs)})
res = {"leaves": len(done) + len(bad) + len(todo), "certified": len(done), "not_accepted": bad, "pending": len(todo),
       "cadical_h": round(sum(x["cadical_s"] or 0 for x in done) / 3600, 1),
       "cake_h": round(sum(x["cake_s"] or 0 for x in done) / 3600, 1), "certified_leaves": done}
json.dump(res, open(f"{O}/tally.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "certified_leaves"}, indent=1))
assert res["leaves"] == 105, res["leaves"]
sys.exit(0 if res["certified"] == 105 else 1)
