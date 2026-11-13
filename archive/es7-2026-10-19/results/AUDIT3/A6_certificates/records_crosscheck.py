#!/usr/bin/env python3
"""A6 audit: cross-check the C2FINAL re-solve records against the original run records.

- sample/out.jsonl and sample/extra_out.jsonl: for each row, find the certified record(s) of the same unit in
  results/<record_source>/out.jsonl and compare cnf_sha256, proof_sha256, proof_bytes; also check that the row itself
  says UNSAT + c VERIFIED + s VERIFIED UNSAT + certified + roundtrip verified, and that the unit is in sample.txt /
  extra_sample.txt with the same source.
- pilot/out.jsonl: compare proof_sha256/bytes with C2C34/logs/p8_units.tsv (the pilot records) and
  cnf_sha256_expected with hashmatch.json computed_for_no_hash; the row's own cnf_sha256 must equal the expected one.
usage: records_crosscheck.py RESULTS_DIR
"""
import csv, glob, json, os, sys
from collections import defaultdict

RES = sys.argv[1]
C = os.path.join(RES, "C2FINAL")
problems = []

recs = defaultdict(list)  # (src, unit) -> records
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for l in open(f):
        if l.strip():
            r = json.loads(l)
            recs[(src, r["unit"])].append(r)

for fn, sfn in (("out.jsonl", "sample.txt"), ("extra_out.jsonl", "extra_sample.txt")):
    drawn = [l.strip() for l in open(os.path.join(C, "sample", sfn)) if l.strip()]
    rows = [json.loads(l) for l in open(os.path.join(C, "sample", fn)) if l.strip()]
    print(f"== {fn}: {len(rows)} rows; {sfn}: {len(drawn)} units")
    seen = set()
    for r in rows:
        key = f'{r["unit"]}@{r["record_source"]}'
        seen.add(key)
        orig = recs.get((r["record_source"], r["unit"]), [])
        cert = [o for o in orig if o.get("certified")]
        ok_self = (r["status"] == "UNSATISFIABLE" and r["lrat_check"] == "c VERIFIED" and r["cake_lpr"] == "s VERIFIED UNSAT"
                   and r["certified"] is True and r["roundtrip"] == "verified" and r["cnf_matches_record"] is True
                   and r["proof_reproduces_record"] is True)
        if len(cert) != 1:
            problems.append(f"{fn} {key}: {len(cert)} certified original records ({len(orig)} total)")
        o = cert[0] if cert else {}
        m_cnf = o.get("cnf_sha256") == r["cnf_sha256"]
        m_proof = o.get("proof_sha256") == r["proof_sha256"] and o.get("proof_bytes") == r["proof_bytes"]
        o_cert = (o.get("status") == "UNSATISFIABLE" and o.get("lrat_check") == "c VERIFIED"
                  and o.get("cake_lpr") == "s VERIFIED UNSAT")
        tag = "in-draw" if key in drawn else "repro-test"
        print(f"  {key:28s} {tag:10s} self_ok={ok_self} cnf_eq_orig={m_cnf} proof_eq_orig={m_proof} orig_verdicts_ok={o_cert}"
              f" kind={o.get('kind')}")
        if not (ok_self and m_cnf and m_proof and o_cert):
            problems.append(f"{fn} {key}: self_ok={ok_self} cnf={m_cnf} proof={m_proof} orig={o_cert}")
    missing = [d for d in drawn if d not in seen]
    print(f"  drawn but not in {fn}: {missing}")
    kinds = defaultdict(int)
    for r in rows:
        key = f'{r["unit"]}@{r["record_source"]}'
        if key in drawn:
            o = [x for x in recs[(r["record_source"], r["unit"])] if x.get("certified")]
            kinds[o[0].get("kind") if o else None] += 1
    print(f"  finished drawn units by kind: {dict(kinds)}")

print("== pilot/out.jsonl")
hm = json.load(open(os.path.join(C, "hashmatch.json")))
exp = hm["computed_for_no_hash"]
p8 = {r["unit"]: r for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")), delimiter="\t")}
for l in open(os.path.join(C, "pilot", "out.jsonl")):
    if not l.strip():
        continue
    r = json.loads(l)
    u = r["unit"]
    pr = p8.get(u, {})
    same_proof = pr.get("proof_sha256") == r["proof_sha256"] and str(pr.get("proof_bytes")) == str(r["proof_bytes"])
    exp_ok = exp.get(u) == r["cnf_sha256_expected"] == r["cnf_sha256"]
    ok_self = (r["status"] == "UNSATISFIABLE" and r["lrat_check"] == "c VERIFIED" and r["cake_lpr"] == "s VERIFIED UNSAT"
               and r["certified"] is True and r["roundtrip"] == "verified")
    print(f"  {u:12s} self_ok={ok_self} cnf==hashmatch.computed_for_no_hash={exp_ok} same_proof_as_pilot_record={same_proof}"
          f" pilot_record_cnf_sha='{pr.get('cnf_sha256', '')[:12]}' pilot_verdicts=({pr.get('lrat_check')}, {pr.get('cake_lpr')})")
    if not (ok_self and exp_ok):
        problems.append(f"pilot {u}: self_ok={ok_self} exp_ok={exp_ok}")
print("no_hash list in hashmatch.json:", hm.get("no_hash"))
print("PROBLEMS:", problems if problems else "none")
