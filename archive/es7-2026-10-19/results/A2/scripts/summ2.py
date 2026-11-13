#!/usr/bin/env python3
"""Summarize an nbhd2.py run and verify every SAT model.

usage: summ2.py WORKDIR BASES.jsonl RUNDIR OUT.json [MODELS.jsonl]
Counts per (src group, kind, mode): answers SAT/UNSAT/UNKNOWN, conflicts mean/max, ms mean/max.
Per deletion set: at least one SAT? (needed for --control runs). Every W model is checked with
A's check_model (old triples as assumed, Python signotope axioms, brute_kgon violations and
convex 7-subsets) and written to MODELS.jsonl with the realization job fields.
"""
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'A', 'scripts'))
from sigutil import parse_outputs, check_model, parse_tag_new, triples  # noqa: E402

T32 = triples(32)


def grp(src):
    return 'nearmiss' if src.startswith('NM') else ('alphaevolve' if src == 'AEdel' else 'pool')


def main():
    wd, bfile, rd, out = sys.argv[1:5]
    mout = sys.argv[5] if len(sys.argv) > 5 else None
    bases = {}
    for l in open(bfile):
        b = json.loads(l)
        bases[b["id"]] = b
    run = json.load(open(os.path.join(rd, 'run.json'))) if os.path.exists(os.path.join(rd, 'run.json')) else {}
    M = run.get("M", 33)
    agg = defaultdict(lambda: {"answers": 0, "SAT": 0, "UNSAT": 0, "UNKNOWN": 0, "conf_sum": 0, "conf_max": 0,
                               "ms_sum": 0.0, "ms_max": 0.0, "deletion_sets": set()})
    per_del = defaultdict(lambda: {"SAT": 0, "n": 0})
    models = []
    seen = set()  # a job answered twice (helper workers re-running a lagging worker's tail) counts once
    for rec in parse_outputs(rd):
        if (rec[0], rec[1], rec[2]) in seen:
            continue
        seen.add((rec[0], rec[1], rec[2]))
        if rec[0] == 'W':
            models.append(rec)
            continue
        _, lab, tag, st, c, d, ms = rec
        bid, kind, D = lab.split(':')
        mode = tag.split('@')[0]
        for key in [(grp(bases[bid]["src"]), kind, mode), ('ALL', kind, mode), ('ALL', 'ALL', mode), ('ALL', 'ALL', 'ALL'),
                    ('src:' + bases[bid]["src"], 'ALL', 'ALL')]:
            a = agg[key]
            a["answers"] += 1
            a[st] += 1
            a["conf_sum"] += c
            a["conf_max"] = max(a["conf_max"], c)
            a["ms_sum"] += ms
            a["ms_max"] = max(a["ms_max"], ms)
            a["deletion_sets"].add(lab)
        per_del[lab]["n"] += 1
        per_del[lab]["SAT"] += st == 'SAT'
    res = {}
    for k, a in sorted(agg.items()):
        n = a["answers"]
        res["|".join(k)] = {"deletion_sets": len(a["deletion_sets"]), "answers": n, "SAT": a["SAT"],
                            "UNSAT": a["UNSAT"], "UNKNOWN": a["UNKNOWN"],
                            "conflicts_mean": round(a["conf_sum"] / n, 1), "conflicts_max": a["conf_max"],
                            "ms_mean": round(a["ms_sum"] / n, 1), "ms_max": round(a["ms_max"], 1)}
    checked = {"ok": 0, "FAIL": 0}
    mf = open(mout, 'w') if mout else None
    for _, lab, tag, model in models:
        bid, kind, D = lab.split(':')
        D = [int(v) for v in D.split('-')]
        b = bases[bid]
        keep = [a for a in range(1, 33) if a not in D]
        ks = set(keep)
        old = ''.join(c for t, c in zip(T32, b["signs"]) if t[0] in ks and t[1] in ks and t[2] in ks)
        chk = check_model(os.path.join(wd, 'brute_kgon'), M, model, len(keep), old, tag, os.path.join(wd, 'tmp'))
        ok = chk["old_triples_agree"] and chk["py_signotope"] and chk["brute_violations"] == 0 and chk["brute_convex"] == 0
        checked["ok" if ok else "FAIL"] += 1
        if mf:
            mf.write(json.dumps({"label": lab, "tag": tag, "set": bid, "kind": kind, "D": D, "M": M, "model": model,
                                 "old_pts": [b["pts"][a - 1] for a in keep], "new": parse_tag_new(tag),
                                 "check": chk, "verified": ok}) + "\n")
    summary = {"run": run, "per_group": res, "sat_models": len(models), "sat_models_checked": checked,
               "deletion_sets_with_SAT": sum(1 for v in per_del.values() if v["SAT"]),
               "deletion_sets_total": len(per_del)}
    json.dump(summary, open(out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != 'per_group'}))
    print(json.dumps(res.get('ALL|ALL|ALL')))


if __name__ == '__main__':
    main()
