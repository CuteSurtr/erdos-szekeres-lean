#!/usr/bin/env python3
"""Whole-case attempt: cadical --lrat -t 60 on CASE.cnf, UNSAT accepted only with cake_lpr
`s VERIFIED UNSAT`.  Appends a {"whole_case": true, ...} record to OUTDIR/leaves.jsonl and,
when verified, writes leaves.icnf = `a 0` (the empty cube) and an empty open.icnf."""
import hashlib, json, os, subprocess, sys, time
BIN = os.environ.get("BIN", "/opt/es7tools/bin")
case, out, work = sys.argv[1], sys.argv[2], sys.argv[3]; T = int(sys.argv[4]) if len(sys.argv) > 4 else 60
os.makedirs(out, exist_ok=True); os.makedirs(work, exist_ok=True); p = os.path.join(work, "whole.lrat")
r = {"whole_case": True, "case_sha256": hashlib.sha256(open(case, "rb").read()).hexdigest(), "timeout": T}
t = time.time()
rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(T), case, p],
                    stdout=subprocess.DEVNULL).returncode
r.update(rc=rc, solve_s=round(time.time() - t, 2))
r["status"] = {20: "UNSAT", 10: "SAT", 0: "UNKNOWN"}.get(rc, "ERROR")
if rc == 20:
    r["proof_bytes"] = os.path.getsize(p); t = time.time()
    o = subprocess.run([os.path.join(BIN, "cake_lpr"), case, p], capture_output=True, text=True).stdout
    r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-200:]); r["check_s"] = round(time.time() - t, 2)
    if r["cake_lpr"] == "s VERIFIED UNSAT":
        open(os.path.join(out, "leaves.icnf"), "w").write("a 0\n"); open(os.path.join(out, "open.icnf"), "w").write("")
if os.path.exists(p): os.remove(p)
with open(os.path.join(out, "leaves.jsonl"), "a") as f: f.write(json.dumps(r) + "\n")
print(json.dumps(r))
