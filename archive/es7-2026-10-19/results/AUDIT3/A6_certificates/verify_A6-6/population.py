#!/usr/bin/env python3
"""A6-6 check: describe the population from which C2FINAL/sample/sample.txt could have been drawn, and check that
each sampled unit@source exists as a certified cloud record, its kind (H/Q), and whether the repository's out.jsonl
records it.
usage: population.py RESULTS_DIR"""
import glob, json, os, sys
from collections import Counter, defaultdict

RES = sys.argv[1]
recs = []
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for i, l in enumerate(open(f)):
        if l.strip():
            r = json.loads(l)
            recs.append((src, i, r))
print("records total", len(recs))
print("sources", len({s for s, _, _ in recs}), "LOCAL sources", sorted({s for s, _, _ in recs if "LOCAL" in s}))
cnt = Counter()
for s, _, r in recs:
    cnt[(r.get("case"), r.get("kind"), r.get("status"), bool(r.get("certified")), "LOCAL" in s)] += 1
for k in sorted(cnt, key=str):
    print(" ", k, cnt[k])

byunitsrc = {(r["unit"], s): r for s, _, r in recs}
smp = [l.strip() for l in open(os.path.join(RES, "C2FINAL", "sample", "sample.txt")) if l.strip()]
ext = [l.strip() for l in open(os.path.join(RES, "C2FINAL", "sample", "extra_sample.txt")) if l.strip()]
out = [json.loads(l) for l in open(os.path.join(RES, "C2FINAL", "sample", "out.jsonl")) if l.strip()]
eout = [json.loads(l) for l in open(os.path.join(RES, "C2FINAL", "sample", "extra_out.jsonl")) if l.strip()]
done = {(o["unit"], o["record_source"]) for o in out}
edone = {(o["unit"], o["record_source"]) for o in eout}
print("\nmain sample:", len(smp), "units; out.jsonl lines:", len(out))
missing = []
for u in smp:
    unit, src = u.split("@")
    r = byunitsrc.get((unit, src))
    k = r.get("kind") if r else None
    ok = (unit, src) in done
    o = next((o for o in out if o["unit"] == unit and o["record_source"] == src), None)
    rep = (o.get("cnf_matches_record"), o.get("proof_reproduces_record"), o.get("certified"), o.get("roundtrip")) if o else None
    print(f"  {u:22s} kind={k} certified_record={r.get('certified') if r else None} in_out={ok} {rep if rep else ''}")
    if not ok:
        missing.append((u, k))
print("missing from out.jsonl:", missing)
print("extra records in out.jsonl not in sample:", sorted({(o['unit'], o['record_source']) for o in out} - {tuple(u.split('@')) for u in smp}))
print("\nextra sample:", len(ext), "units; extra_out.jsonl lines:", len(eout))
for u in ext:
    unit, src = u.split("@")
    r = byunitsrc.get((unit, src))
    o = next((o for o in eout if o["unit"] == unit and o["record_source"] == src), None)
    print(f"  {u:22s} kind={r.get('kind') if r else None} in_out={o is not None}",
          (o.get("cnf_matches_record"), o.get("proof_reproduces_record"), o.get("certified")) if o else "")
# per-case counts of H and Q in sample
pc = defaultdict(Counter)
for u in smp:
    unit, src = u.split("@"); pc[unit.split("_")[0]][byunitsrc[(unit, src)]["kind"]] += 1
print("\nper-case kinds in main sample:", {c: dict(v) for c, v in sorted(pc.items())})
