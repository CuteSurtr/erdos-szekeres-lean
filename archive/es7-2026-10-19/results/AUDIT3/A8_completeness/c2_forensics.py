#!/usr/bin/env python3
"""Completeness review: cheap forensic plausibility checks over all central-34 run records (C2P*/*/out.jsonl and the
C2C34 pilot table), of the kind A2 ran for the threefold records. Reads only small record files.
Checks: duplicate proof hashes across different (unit, CNF) pairs; one unit with several CNF hashes; checker
throughput (proof bytes per second) outliers; certified records with tiny proofs or zero times; field layouts.
usage: c2_forensics.py RESULTS_DIR"""
import csv, glob, json, os, statistics as st, sys
from collections import defaultdict, Counter

RES = sys.argv[1]
rows = []
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for line in open(f):
        if line.strip():
            r = json.loads(line); r["_src"] = src; rows.append(r)
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")), delimiter="\t"):
    r = dict(r); r["_src"] = "C2C34/pilot"; rows.append(r)
f = lambda x: float(x) if x not in (None, "") else None
cert = [r for r in rows if r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
        and r.get("cake_lpr") == "s VERIFIED UNSAT"]
print("records", len(rows), "certified", len(cert))
layouts = Counter(tuple(k for k in r if not k.startswith("_")) for r in rows)
print("field layouts:", len(layouts))
for k, v in layouts.most_common():
    print("  ", v, len(k), k[:6], "...")
# duplicates
by_proof = defaultdict(set)
by_unit_cnf = defaultdict(set)
for r in cert:
    if r.get("proof_sha256"):
        by_proof[r["proof_sha256"]].add((r["unit"], r.get("cnf_sha256", "")))
    if r.get("cnf_sha256"):
        by_unit_cnf[r["unit"]].add(r["cnf_sha256"])
dupp = {p: s for p, s in by_proof.items() if len(s) > 1}
print("proof hashes shared by different (unit, CNF) pairs:", len(dupp), list(dupp.items())[:5])
multi = {u: s for u, s in by_unit_cnf.items() if len(s) > 1}
print("units with more than one CNF hash among certified records:", len(multi), list(multi.items())[:5])
# throughput
lr, ck, sv = [], [], []
odd = []
for r in cert:
    pb, ls, cs, ss = f(r.get("proof_bytes")), f(r.get("lrat_check_s")), f(r.get("cake_s")), f(r.get("solve_s"))
    if pb is None:
        odd.append(("no proof_bytes", r["_src"], r["unit"])); continue
    if pb < 1e6:
        odd.append(("proof < 1 MB", r["_src"], r["unit"], pb))
    if ls:
        lr.append((pb / ls / 1e6, r["_src"], r["unit"]))
    else:
        odd.append(("lrat time 0/None", r["_src"], r["unit"]))
    if cs:
        ck.append((pb / cs / 1e6, r["_src"], r["unit"]))
    else:
        odd.append(("cake time 0/None", r["_src"], r["unit"]))
    if ss:
        sv.append((pb / ss / 1e6, r["_src"], r["unit"]))
for name, xs in (("lrat-check MB/s", lr), ("cake_lpr MB/s", ck), ("proof MB per solve s", sv)):
    v = sorted(x[0] for x in xs)
    print(f"{name}: n={len(v)} min {v[0]:.1f} median {st.median(v):.1f} p99 {v[int(.99*len(v))]:.1f} max {v[-1]:.1f}")
    print("   top 3:", sorted(xs, reverse=True)[:3])
print("odd records:", len(odd), odd[:10])
# per-source medians of cake throughput (a bad machine would stand out)
per = defaultdict(list)
for x, s, u in ck:
    per[s.split("/")[0] + ("/LOCAL" if "LOCAL" in s else "/cloud")].append(x)
for s, v in sorted(per.items()):
    print(f"   cake MB/s {s}: n={len(v)} median {st.median(v):.1f} max {max(v):.1f}")
