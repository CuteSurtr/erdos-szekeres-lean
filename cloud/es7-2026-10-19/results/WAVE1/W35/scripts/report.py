#!/usr/bin/env python3
"""Per-case summary of results/WAVE1/W35: closed/open, leaf counts, covercheck, CPU seconds.
  report.py W35DIR  -> writes W35DIR/summary.jsonl, prints a markdown table"""
import hashlib, json, os, subprocess, sys
R = sys.argv[1]; CC = os.path.join(R, "../../Mii-S/scripts/covercheck.py")
e = json.load(open(os.path.join(R, "entry_W35.json")))
rows = []
for c in e["cases"]:
    n = c["case"]; d = os.path.join(R, n); p = os.path.join(d, "leaves.jsonl")
    rs = [json.loads(l) for l in open(p)] if os.path.exists(p) and os.path.getsize(p) else []
    whole = [r for r in rs if r.get("whole")]; top = [r for r in rs if r.get("top")]
    cubes = [r for r in rs if "cube" in r and not r.get("whole")]
    ver = sum(r["status"] == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT" for r in cubes)
    cpu = sum(r.get(k, 0) for r in rs for k in ("solve_s", "check_s", "split_s", "march_s"))
    nopen = sum(1 for l in open(os.path.join(d, "open.icnf")) if l.startswith("a")) if os.path.exists(os.path.join(d, "open.icnf")) else None
    cov = None
    if os.path.exists(os.path.join(d, "leaves.icnf")) and os.path.getsize(os.path.join(d, "leaves.icnf")):
        cov = subprocess.run(["python3", CC, os.path.join(d, "leaves.icnf")], capture_output=True, text=True).stdout.strip()
    closed = nopen == 0 and cov is not None and cov.startswith("s COVERED")
    row = {"case": n, "cnf_sha256": c["cnf_sha256"], "status": "CLOSED" if closed else ("OPEN" if rs else "NOT_STARTED"),
           "whole_60s": whole[0]["status"] if whole else None,
           "top_cubes": top[0]["ncubes"] if top else None, "top_refuted": top[0]["refuted"] if top else None,
           "top_sha256": top[0]["top_sha256"] if top else None,
           "splits": sum(r["status"] == "SPLIT" for r in cubes), "leaves_verified": ver,
           "unsat_unchecked": sum(r["status"] == "UNSAT_UNCHECKED" for r in cubes),
           "sat": sum(r.get("status") == "SAT" for r in rs), "open_cubes": nopen, "covercheck": cov, "cpu_s": round(cpu)}
    rows.append(row)
with open(os.path.join(R, "summary.jsonl"), "w") as f:
    for r in rows: f.write(json.dumps(r) + "\n")
print("| case | status | whole 60 s | top cubes (refuted) | splits | cake_lpr-verified leaves | open cubes | covercheck | CPU s |")
print("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    if r["status"] == "NOT_STARTED": continue
    print(f"| {r['case']} | {r['status']} | {r['whole_60s']} | {r['top_cubes']} ({r['top_refuted']}) | {r['splits']} | "
          f"{r['leaves_verified']} | {r['open_cubes']} | {r['covercheck']} | {r['cpu_s']} |")
ns = [r["case"] for r in rows if r["status"] == "NOT_STARTED"]
print(f"\nNot started ({len(ns)}): " + ", ".join(ns))
print(f"\nCLOSED {sum(r['status']=='CLOSED' for r in rows)}, OPEN {sum(r['status']=='OPEN' for r in rows)}, "
      f"NOT_STARTED {len(ns)}, SAT {sum(r['sat'] for r in rows)}, total CPU s {sum(r['cpu_s'] for r in rows)}")
