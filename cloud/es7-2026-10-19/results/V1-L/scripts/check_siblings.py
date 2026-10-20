#!/usr/bin/env python3
"""Check the sibling runs' per-leaf records against hull_leaves.icnf.

Usage: check_siblings.py ICNF V1-0/leaves_cake.jsonl ... > report.json

A leaf i (0-based line of ICNF) counts as verified if some record has "i" == i, the same cube
as line i, solver_exit 20 and cake_lpr exactly "s VERIFIED UNSAT" (cake_exit 0). Records
from a run other than V1-(i mod 4) are reported but still accepted if they match.
"""
import json, sys, collections

icnf, files = sys.argv[1], sys.argv[2:]
leaves = []
for line in open(icnf):
    t = line.split()
    if t:
        leaves.append([int(x) for x in t[1:-1]])
recs = collections.defaultdict(list)
bad_lines = []
for f in files:
    run = f.split('/')[-2] if '/' in f else f
    for n, l in enumerate(open(f), 1):
        try:
            r = json.loads(l)
        except Exception:
            bad_lines.append(f"{f}:{n}")
            continue
        r["_run"] = run
        recs[r.get("i")].append(r)
ok, fail, missing, cube_mismatch, wrong_run = [], [], [], [], []
for i, c in enumerate(leaves):
    rs = recs.get(i, [])
    if not rs:
        missing.append(i)
        continue
    good = [r for r in rs if r.get("cube") == c and r.get("solver_exit") == 20
            and r.get("cake_lpr") == "s VERIFIED UNSAT" and r.get("cake_exit", 0) == 0]
    if any(r.get("cube") != c for r in rs):
        cube_mismatch.append(i)
    if any(r["_run"] != f"V1-{i % 4}" for r in rs):
        wrong_run.append(i)
    (ok if good else fail).append(i)
by_run = collections.Counter(f"V1-{i % 4}" for i in ok)
out = {"leaves": len(leaves), "verified": len(ok), "verified_by_run": dict(sorted(by_run.items())),
       "failed_records_only": fail, "missing": len(missing),
       "missing_by_run": dict(sorted(collections.Counter(f"V1-{i % 4}" for i in missing).items())),
       "cube_mismatch": cube_mismatch, "record_from_other_run": wrong_run,
       "unparsable_lines": bad_lines,
       "cake_s_total": round(sum(r.get("cake_s", 0) for rs in recs.values() for r in rs), 1),
       "max_proof_bytes": max((r.get("proof_bytes", 0) for rs in recs.values() for r in rs), default=0)}
json.dump(out, sys.stdout, indent=1)
print()
