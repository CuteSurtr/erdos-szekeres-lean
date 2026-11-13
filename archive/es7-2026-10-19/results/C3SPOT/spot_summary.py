#!/usr/bin/env python3
"""Summarise the spot-check (work6): per source directory, re-solved units, certified, CNF hash equal to the record's,
solve-time statistics; anything else listed. usage: spot_summary.py WORK6 UNITS6.tsv"""
import collections, glob, json, statistics, sys
W, U = sys.argv[1:3]
exp = {}
for l in open(U):
    a = l.rstrip("\n").split("\t"); exp[a[1]] = (a[3], a[4])
recs = [json.loads(l) for f in sorted(glob.glob(W + "/out*.jsonl")) for l in open(f) if l.strip()]
solved = [r for r in recs if "status" in r]
src = lambda f: f.split("/")[0] + ("/LOCAL" if "LOCAL" in f else "")
by = collections.defaultdict(list); bad = []
for r in solved:
    e = exp.get(r["node"])
    ok = r.get("status") == "UNSATISFIABLE" and r.get("certified") and r.get("lrat_check") == "c VERIFIED" \
         and r.get("cake_lpr") == "s VERIFIED UNSAT" and e is not None and r.get("cnf_sha256") == e[0]
    by[src(e[1]) if e else "?"].append((ok, r.get("solve_s", 0)))
    if not ok: bad.append(r)
print("| record source | re-solved | all checks pass | median solve s |")
print("|---|---|---|---|")
for s in sorted(by):
    v = by[s]; print(f"| {s} | {len(v)} | {sum(o for o, _ in v)} | {statistics.median(t for _, t in v):.0f} |")
print(f"\ntotal re-solved {len(solved)}, all checks pass {len(solved) - len(bad)}, other {len(bad)}; split records (timeouts) {sum(1 for r in recs if r.get('split'))}")
for r in bad[:20]: print("NOT OK:", json.dumps(r)[:300])
