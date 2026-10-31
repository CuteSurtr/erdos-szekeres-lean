#!/usr/bin/env python3
"""Build results/Mii-S/cases.jsonl from the run logs in results/Mii-S (see README)."""
import json, os, sys
D = sys.argv[1]
sys.path.insert(0, os.path.join(D, "scripts")); import hullsplit as H
def jl(name):
    p = os.path.join(D, name)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
cases = {}
for (U, L) in H.cases():
    nm = H.name(U, L)
    cases[nm] = {"case": nm, "U": list(U), "L": list(L), "spec": ",".join(map(str, U)) + "/" + ",".join(map(str, L)),
                 "hull_ccw": H.hull_ccw(U, L), "nlits": len(H.cube(U, L)), "status": "OPEN"}
for r in jl("sweep10.jsonl"):
    c = cases[r["case"]]; c["cnf_sha256"] = r["cnf_sha256"]; c["cadical_10s"] = r["result"]
for r in jl("pass2_lrat.jsonl"):
    c = cases[r["case"]]; assert c["cnf_sha256"] == r["cnf_sha256"]
    if r["result"] == "UNSAT" and r["cake_lpr"] == "s VERIFIED UNSAT":
        c.update(status="UNSAT_VERIFIED", method="direct", solve_s=r["solve_s"], check_s=r["check_s"],
                 proof_bytes=r["proof_bytes"])
spec2name = {c["spec"]: n for n, c in cases.items()}
for r in jl("two_direct_partial.jsonl"):
    if r["result"] == "UNKNOWN": cases[spec2name[r["spec"]]]["cadical_60s"] = "UNKNOWN"
for f in ("est_one.jsonl", "est_two.jsonl"):
    for r in jl(f):
        if ";" not in r["spec"]:
            c = cases[spec2name[r["spec"]]]
            c["layer_probe"] = {"est_core_s": r["est_s"], "censored": r["censored"], "root_attempt": r["result"],
                                "nchildren": r.get("nchildren"), "sampled_children": r.get("child_results")}
for r in jl("probes.jsonl"):
    nm = r["case"]
    if nm in cases:
        cases[nm].setdefault("march_probes", []).append({k: r[k] for k in ("depth", "ncubes", "march_s", "timeout", "closed", "est_core_s_censored")} |
                                                         {"sample_s": [s["s"] for s in r["samples"]], "sample_rc": [s["rc"] for s in r["samples"]]})
for f in sorted(os.listdir(D)):
    if f.startswith("cnc_") and f.endswith(".json"):
        r = json.load(open(os.path.join(D, f))); c = cases[r["case"]]
        assert c["cnf_sha256"] == r["cnf_sha256"]
        c["cnc"] = r
        if r.get("covered") and r.get("all_verified"): c.update(status="UNSAT_VERIFIED", method="cube-and-conquer")
with open(os.path.join(D, "cases.jsonl"), "w") as f:
    for c in cases.values(): f.write(json.dumps(c) + "\n")
import collections
print(collections.Counter(c["status"] for c in cases.values()))
