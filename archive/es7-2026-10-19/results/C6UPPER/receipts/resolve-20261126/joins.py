#!/usr/bin/env python3
"""joins.py (26 Nov 2026): the d1 re-solve against the pushed records. Read-only; prints joins.txt.
Usage: python3 -I joins.py QUEUE_D1_DIR REPO_RESULTS_DIR"""
import csv, glob, json, re, sys
Q, RES = sys.argv[1], sys.argv[2]
C = RES + "/C6UPPER"
new = {}
for f in glob.glob(Q + "/out/*/certify.jsonl"):
    ok = [json.loads(x) for x in open(f) if '"s VERIFIED UNSAT"' in x]
    if ok: new[f.split("/")[-2]] = ok[-1]
cake = sum(1 for f in glob.glob(Q + "/out/*/*.cake.out") if any(l.rstrip("\n") == "s VERIFIED UNSAT" for l in open(f)))
rc = {r["id"].replace("/", "_"): r for r in csv.DictReader(open(C + "/receipts/c6upper_proofs_20261124.tsv"), delimiter="\t")}
print("joins (d1 re-solve, 26 Nov 2026) against the pushed records")
print(f"cake.out files with the exact line 's VERIFIED UNSAT': {cake}; certify.jsonl verdict lines: {len(new)}")
print(f"receipt C6UPPER/receipts/c6upper_proofs_20261124.tsv: {len(rc)} rows; ids = re-solved ids: {set(rc) == set(new)}")
print("  cnf sha256 = receipt cnf_sha256:", sum(new[k]["cnf_sha256"] == rc[k]["cnf_sha256"] for k in new), "/", len(new))
print("  cnf path = receipt cnf_kept:", sum(new[k]["cnf"] == rc[k]["cnf_kept"] for k in new), "/", len(new))
print("  new LRAT sha256 = receipt lrat_sha256_recorded (the deleted proofs):",
      sum(new[k]["lrat_sha256"] == rc[k]["lrat_sha256_recorded"] for k in new), "/", len(new))
bind = {}
for l in open(RES + "/ENCBLEAN/logs/m9_review_fix_hash_binding.log"):
    m = re.match(r"MATCH cube I=(\d+) ([cn]\d{5}) .* sha=([0-9a-f]{64})", l)
    if m: bind[m.group(2)] = m.group(3)
eb = {k.split("_")[-1]: v["cnf_sha256"] for k, v in new.items() if k.startswith(("c6r_B_", "c6n_"))}
print(f"ENCBLEAN M9 binding of CubesUnsat64 (logs/m9_review_fix_hash_binding.log): {len(bind)} cubes; "
      f"encoder-B re-solves {len(eb)}; names equal: {set(bind) == set(eb)}; "
      f"every cnf sha256 = printed text sha256: {all(bind[k] == eb.get(k) for k in bind)}")
rp = {r["cube"]: r["cnf_sha256"] for r in csv.DictReader(open(C + "/replay-2026-11-06/results.tsv"), delimiter="\t") if r["enc"] == "A"}
ea = {k.split("_")[-1]: v["cnf_sha256"] for k, v in new.items() if k.startswith("c6r_A_")}
print(f"encoder A against replay-2026-11-06/results.tsv enc A rows: {len(rp)} rows, {len(ea)} re-solves; "
      f"names equal: {set(rp) == set(ea)}; hashes equal: {all(rp[k] == ea.get(k) for k in rp)} (encoder A has no Lean printer)")
lr = {}
for k, v in new.items(): lr.setdefault(v["lrat_sha256"], []).append(k)
print("proofs shared by several cubes (same LRAT bytes, each checked against its own CNF):",
      {h[:12]: sorted(ks) for h, ks in lr.items() if len(ks) > 1})
