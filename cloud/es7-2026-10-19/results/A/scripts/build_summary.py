#!/usr/bin/env python3
"""Collect the task-A results into one summary JSON.

usage: build_summary.py WORKDIR OUT.json
Reads (when present): pool.meta.json, pool_brute.jsonl, extra/extra_meta.json, controls.json,
main_summary.json, nf_summary.json, cert_sample.jsonl, nb*_r*.json / nb*_r*/run.json,
c1_real.jsonl, c1_orig_real.jsonl, models_*.jsonl, real_*.jsonl, env.json.
"""
import glob
import json
import os
import sys
from collections import Counter


def jload(p):
    return json.load(open(p)) if os.path.exists(p) else None


def jlines(p):
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def main():
    wd, out = sys.argv[1:3]
    S = {"env": jload(os.path.join(wd, 'env.json'))}
    S["conversion"] = jload(os.path.join(wd, 'pool.meta.json'))
    b = jlines(os.path.join(wd, 'pool_brute.jsonl'))
    S["pool_brute_kgon"] = {"checked": len(b), "signotope_axiom_violations": sum(r.get("violations", 1) for r in b),
                            "sets_with_convex7": sum(1 for r in b if r.get("convex", 1)),
                            "errors": sum(1 for r in b if "error" in r)}
    S["extra_sets"] = jload(os.path.join(wd, 'extra', 'extra_meta.json'))
    c = jload(os.path.join(wd, 'controls.json'))
    if c:
        c = dict(c)
        c["C1"] = {k: v for k, v in c["C1"].items() if k != "per_set"}
    S["controls"] = c
    S["one_point_extension_main"] = jload(os.path.join(wd, 'main_summary.json'))
    S["one_point_extension_nearfull_derived"] = jload(os.path.join(wd, 'nf_summary.json'))
    cs = jlines(os.path.join(wd, 'cert_sample.jsonl'))
    S["drat_sample"] = {
        "unsat_instances": sum(1 for r in cs if r["expect"] == "UNSAT"),
        "unsat_cadical_20": sum(1 for r in cs if r["expect"] == "UNSAT" and r["cadical_exit"] == 20),
        "unsat_drat_trim_verified": sum(1 for r in cs if r["expect"] == "UNSAT" and r.get("drat_trim") == "VERIFIED"),
        "sat_controls": sum(1 for r in cs if r["expect"] == "SAT"),
        "sat_controls_cadical_10": sum(1 for r in cs if r["expect"] == "SAT" and r["cadical_exit"] == 10)}
    nb = {}
    for p in sorted(glob.glob(os.path.join(wd, 'nb*_r*.json'))):
        name = os.path.basename(p)[:-5]
        rec = jload(p)
        run = jload(os.path.join(wd, name, 'run.json'))
        rec = {k: v for k, v in rec.items()}
        rec["run"] = run
        nb[name] = rec
    S["neighbourhood"] = nb
    for name in ('c1_orig_real', 'c1_real'):
        rr = jlines(os.path.join(wd, name + '.jsonl'))
        S["realizer_calibration_" + name] = {"models": len(rr), "realized": sum(r["realized"] for r in rr),
                                             "by_method": dict(Counter(r.get("method") for r in rr if r["realized"]))}
    models = []
    for p in sorted(glob.glob(os.path.join(wd, 'models_*.jsonl'))):
        for r in jlines(p):
            models.append({"label": r["label"], "tag": r["tag"], "verified": r["verified"], "check": r["check"]})
    S["sat_models"] = {"count": len(models), "verified": sum(m["verified"] for m in models), "list": models[:200]}
    reals = []
    for p in sorted(glob.glob(os.path.join(wd, 'real_*.jsonl'))):
        reals += jlines(p)
    S["sat_model_realization"] = {"attempted": len(reals), "realized": sum(r["realized"] for r in reals),
                                  "realized_list": [r for r in reals if r["realized"]]}
    json.dump(S, open(out, 'w'), indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) or len(json.dumps(v)) < 300 else '...') for k, v in S.items()}))


if __name__ == '__main__':
    main()
