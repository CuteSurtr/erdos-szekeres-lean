#!/usr/bin/env python3
"""Collect the task-E logs into summary.json.  usage: make_summary.py RESULTS_DIR"""
import glob
import json
import os
import re
import sys

R = sys.argv[1]
L = os.path.join(R, "logs")


def jl(path):
    out = []
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line.startswith("{"):
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


summary = {"task": "E", "date": "2026-10-19"}
env = os.path.join(L, "environment.json")
if os.path.exists(env):
    summary["environment"] = json.load(open(env))
ctl = []
p = os.path.join(L, "controls.log")
if os.path.exists(p):
    for line in open(p):
        m = re.match(r"(\S+) expected=(\S+) got=(\S*) time=(\d+)s verdict=(\S+) check=(\S*) reason=(\S+)", line.strip())
        if m:
            tag, exp, got, t, v, chk, why = m.groups()
            ctl.append({"cnf": tag, "expected": exp, "got": got, "seconds": int(t), "verdict": v,
                        "model_check": json.loads(chk) if chk.startswith("{") else None, "reason": why.replace("_", " ")})
summary["controls"] = ctl
summary["controls_extra"] = jl(os.path.join(L, "controls_extra.jsonl"))
summary["saved_models"] = jl(os.path.join(L, "saved_models.jsonl"))
val = []
for f in sorted(glob.glob(os.path.join(L, "val_*.json"))):
    for d in jl(f):
        d.pop("cnfeval_stderr", None)
        val.append(d)
val += jl(os.path.join(L, "val_small.jsonl"))
summary["exact_symmetric_validation"] = val
summary["c3refl_small_agreement"] = jl(os.path.join(L, "c3refl_small.jsonl"))
summary["realizable_set_checks"] = jl(os.path.join(L, "check_set_n27k7d3.json"))
p = os.path.join(L, "enum16.log")
if os.path.exists(p):
    summary["labelled_model_counts"] = [l.strip() for l in open(p) if l.strip()]
lr = {}
for f in sorted(glob.glob(os.path.join(L, "lrat_*.log")) + glob.glob(os.path.join(L, "solve_*.log"))):
    txt = open(f).read()
    lr[os.path.basename(f)] = {
        "sha256": next((l.split()[1] for l in txt.splitlines() if l.startswith("sha256")), None),
        "solver_result": next((l.strip() for l in txt.splitlines() if l.startswith("s ")), None),
        "proof_bytes": next((int(l.split()[1]) for l in txt.splitlines() if l.startswith("proof_bytes")), None),
        "lrat_check": "c VERIFIED" if "c VERIFIED" in txt.splitlines() else ("NOT VERIFIED" if "NOT VERIFIED" in txt else None),
        "lrat_check_exit": next((int(l.split()[1]) for l in txt.splitlines() if l.startswith("lrat_check_exit")), None)}
summary["whole_cnf_solves"] = lr
summary["mutation_tests"] = jl(os.path.join(L, "mutation_tests.jsonl"))
summary["anneal_controls"] = []
for f in sorted(glob.glob(os.path.join(L, "anneal_*.json"))):
    for d in jl(f):
        if d.get("free_set"):
            d["free_set"] = "found (see log)"
        summary["anneal_controls"].append(d)
runs = {}
for rd in sorted(glob.glob(os.path.join(R, "runs", "*"))):
    name = os.path.basename(rd)
    prog = jl(os.path.join(rd, "progress.log"))
    runs[name] = {
        "progress_records": len(prog),
        "first": prog[0] if prog else None,
        "last": prog[-1] if prog else None,
        "verify_tree": (jl(os.path.join(rd, "verify_tree.json")) or [None])[-1],
        "lrat_spot_checks": jl(os.path.join(rd, "lrat.jsonl")),
        "events_sat": [e for e in jl(os.path.join(rd, "events.log")) if e.get("event") == "SAT"],
        "model_checks": jl(os.path.join(rd, "model_checks.jsonl")),
    }
    for k in ("lrat_spot_checks",):
        runs[name]["lrat_verified"] = sum(1 for x in runs[name][k] if x.get("lrat_verified"))
        runs[name]["lrat_attempted"] = len(runs[name][k])
summary["runs"] = runs
json.dump(summary, open(os.path.join(R, "summary.json"), "w"), indent=1)
print("wrote", os.path.join(R, "summary.json"))
