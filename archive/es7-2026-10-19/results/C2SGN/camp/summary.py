#!/usr/bin/env python3
"""Summarize compact-encoding runs (camp/results.jsonl) into units.tsv and summary.txt.  usage: summary.py CAMP OUTDIR"""
import json, os, sys
D, O = sys.argv[1:3]; os.makedirs(O, exist_ok=True)
recs = [json.loads(l) for l in open(f"{D}/results.jsonl") if l.strip()]
cols = ["unit", "status", "cap_s", "solve_s", "proof_bytes", "proof_sha256", "lrat_check", "lrat_check_s", "cake_lpr",
        "cake_s", "cake_heap_mb", "proof_kept", "cube_literals", "cnf_sha256", "finished"]
with open(f"{O}/units.tsv", "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in recs: f.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")
both = lambda r: r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"
groups = {"cover of the second-layer split": lambda u: u == "COVER",
          "cover of the third-layer split of Q3.11": lambda u: u == "Q3.11_layer3",
          "second layer, hexagonal": lambda u: u.startswith("H"),
          "second layer, quadrilateral": lambda u: u.startswith("Q") and "/" not in u and not u.endswith("_layer3"),
          "third layer under Q3.11": lambda u: u.startswith("Q3.11/")}
out = []
for g, f in groups.items():
    rs = [r for r in recs if f(r["unit"])]
    if not rs: continue
    un = [r for r in rs if r["status"] == "UNSATISFIABLE"]; ok = [r for r in un if both(r)]
    unk = [r for r in rs if r["status"] == "UNKNOWN"]; sat = [r for r in rs if r["status"] == "SATISFIABLE"]
    ts = sorted(r["solve_s"] for r in un if r.get("solve_s") is not None)
    s = f"{g}: {len(rs)} run, {len(un)} UNSAT ({len(ok)} accepted by both checkers), {len(unk)} no answer within the cap, {len(sat)} SAT"
    if ts: s += f"; solve time min {ts[0]:.0f} s, median {ts[len(ts)//2]:.0f} s, max {ts[-1]:.0f} s"
    out.append(s)
out.append(f"proofs deleted after both checks: {sum(1 for r in recs if r.get('proof_kept') is False)}; kept: {sum(1 for r in recs if r.get('proof_kept') is True)}")
open(f"{O}/summary.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
