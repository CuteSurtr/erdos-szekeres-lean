#!/usr/bin/env python3
"""Summarize the P8 pilot: per-unit records (p8/results.jsonl) into p8_units.tsv, plus counts by second-layer type.
usage: summary.py P8DIR OUTDIR"""
import json, os, sys
P8, O = sys.argv[1:3]; os.makedirs(O, exist_ok=True)
recs = [json.loads(l) for l in open(f"{P8}/results.jsonl") if l.strip()]
orb = dict(l.split() for l in open(f"{P8}/orbits.tsv").read().splitlines()[1:])
reps = sorted(set(orb.values()))
kind = lambda u: "cover" if u == "P8_cover" else ("quadrilateral" if u.count("-") == 1 else "hexagonal")
cols = ["unit", "kind", "representative", "status", "cap_s", "solve_s", "solve_rss_mb", "proof_bytes", "proof_sha256",
        "lrat_check", "lrat_check_s", "cake_lpr", "cake_s", "cake_heap_mb", "proof_kept", "cnf_sha256", "finished"]
with open(f"{O}/p8_units.tsv", "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in recs:
        r = dict(r); r["kind"] = kind(r["unit"]); r["representative"] = orb.get(r["unit"], "") == r["unit"] if r["unit"] != "P8_cover" else ""
        f.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")
both = lambda r: r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"
out = []
for k in ("cover", "hexagonal", "quadrilateral"):
    rs = [r for r in recs if kind(r["unit"]) == k]
    un = [r for r in rs if r["status"] == "UNSATISFIABLE"]; ok = [r for r in un if both(r)]
    unk = [r for r in rs if r["status"] == "UNKNOWN"]; sat = [r for r in rs if r["status"] == "SATISFIABLE"]
    ts = sorted(r["solve_s"] for r in un if r.get("solve_s") is not None)
    med = ts[len(ts) // 2] if ts else None
    out.append(f"{k}: {len(rs)} run, {len(un)} UNSAT ({len(ok)} accepted by both checkers), {len(unk)} no answer within the cap, {len(sat)} SAT"
               + (f"; solve time min {ts[0]:.0f} s, median {med:.0f} s, max {ts[-1]:.0f} s" if ts else ""))
done_reps = {r["unit"] for r in recs if r["unit"] in reps and both(r)}
nq = sum(1 for u in reps if u.count("-") == 1)
out.append(f"representatives closed by both checkers: {len(done_reps)} of {len(reps)} ({sum(1 for u in done_reps if u.count('-') == 1)} of {nq} quadrilateral, {sum(1 for u in done_reps if u.count('-') == 2)} of {len(reps) - nq} hexagonal)")
out.append(f"proofs deleted after both checks: {sum(1 for r in recs if r.get('proof_kept') is False)}; proofs kept (a check failed): {sum(1 for r in recs if r.get('proof_kept') is True)}")
open(f"{O}/p8_summary.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
