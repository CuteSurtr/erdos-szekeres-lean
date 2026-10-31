#!/usr/bin/env python3
"""Build results/F/summary.json from results/F/data (run from results/F: python3 realizer/make_summary.py).
Also re-verifies every committed realized point file exactly against its model."""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from chiro import read_models, verify_exact, largest_convex_subset  # noqa: E402
from realize import default_methods  # noqa: E402

F = os.path.dirname(HERE)
D = os.path.join(F, "data")


def jl(path):
    return [json.loads(l) for l in open(path) if l.strip()]


METHOD_OVERRIDE = {"run2_explicit/pool32_methods_insff_lp_free_polish": ["ins-ff", "lp", "free", "polish"]}


def calib_family(path):
    rows = jl(path)
    summ = next((r["summary"] for r in rows if "summary" in r), None)
    rows = [r for r in rows if "summary" not in r]
    ok = [r for r in rows if r["realized"]]
    st = sorted(r["cpu_seconds"] for r in ok)
    meth = {}
    for r in ok:
        meth[r["method"]] = meth.get(r["method"], 0) + 1
    out = {"family": rows[0]["family"], "n": rows[0]["n"], "m": rows[0]["m"],
           "trials": len(rows), "realized": len(ok), "rate": round(len(ok) / len(rows), 3),
           "cpu_budget_s": summ["cpu_budget_s"] if summ else None,
           "median_cpu_s_realized": st[len(st) // 2] if st else None,
           "max_cpu_s_realized": st[-1] if st else None,
           "realized_by_method": meth}
    if summ:
        mm = summ["methods"]
        key = os.path.join(os.path.basename(os.path.dirname(path)), os.path.basename(path)[:-6])
        if key in METHOD_OVERRIDE:
            # this run recorded "auto" while the auto portfolio was ins-ff,lp,free,polish
            mm = METHOD_OVERRIDE[key]
        elif mm == ["auto"]:
            mm = ["auto"] + default_methods(summ["m"] if summ["family"] in ("sym", "sympool") else 1,
                                            summ.get("center", False) and summ["family"] == "sym")
        out["methods"] = mm
        out["complete"] = True
    else:
        out["complete"] = False
    return out


S = {"task": "F: calibrated realizer (cloud/es7-2026-10-19)",
     "machine": {"cores": 15, "note": "15-core Mac shared with other sessions (load average 120-130), "
                 "processes niced; budgets and times are CPU seconds (time.process_time); wall time "
                 "was about 8-10x larger"},
     "exact_check": "every realized point set re-checked with Fraction arithmetic: all C(n,3) "
                    "orientations equal the model, no collinear triple"}

# calibration (a)
S["calibration_a_known_realizable"] = {}
for run in sorted(glob.glob(os.path.join(D, "calib_a", "*"))):
    S["calibration_a_known_realizable"][os.path.basename(run)] = {
        os.path.basename(p)[:-6]: calib_family(p) for p in sorted(glob.glob(os.path.join(run, "*.jsonl")))}

# calibration (b)
pub = {"m4": {"published": "66 abstract 4-fold solutions, 18 realizable, 9 up to isomorphism "
                           "(Subercaseaux-Mackey-Qian-Heule, arXiv 2506.00224)",
              "labelled_multiplicity": 8, "P": 16, "m": 4, "center": False, "file": "n16k6m4.all"},
       "m5": {"published": "948 (also stated as 932) abstract 5-fold solutions, 92 realizable, 46 up to "
                           "isomorphism (same paper)",
              "labelled_multiplicity": 3, "P": 16, "m": 5, "center": True, "file": "n16k6m5c.all"}}
S["calibration_b_symmetric_16_point"] = {}
for tag, info in pub.items():
    d = json.load(open(os.path.join(D, "sym16", tag, "summary.json")))
    per = d.pop("per_model")
    res = jl(os.path.join(D, "sym16", tag, "results.jsonl"))
    models = read_models(os.path.join(D, "enum", info["file"]), info["P"], info["m"], info["center"])
    rever = []
    for r in res:
        if not r["realized"]:
            continue
        pts = [tuple(map(int, l.split())) for l in open(os.path.join(D, "sym16", tag, r["name"] + ".pts"))]
        ok, bad, zero = verify_exact(pts, models[int(r["name"][5:]) - 1])
        rever.append({"name": r["name"], "exact_ok": ok, "largest_convex_subset": largest_convex_subset(pts)})
    d["reverified_point_files"] = len(rever)
    d["reverified_all_ok"] = all(x["exact_ok"] for x in rever)
    d["largest_convex_subset_values"] = sorted({x["largest_convex_subset"] for x in rever})
    d["realized_class_representatives"] = sorted((x["name"] for x in rever), key=lambda s: int(s[5:]))
    d["solutions_in_published_counting"] = {"total": d["models"] // info["labelled_multiplicity"],
                                            "realized": d["realized_models"] // info["labelled_multiplicity"]}
    d["realized_model_names"] = [p["name"] for p in per if p["realized"]]
    sp = os.path.join(D, "sym16", tag, "saturation.jsonl")
    if os.path.exists(sp):
        sr = jl(sp)
        d["saturation_control"] = {
            "note": "sat.c on every realized hexagon-free 16-point set (K=6); ES(6)=17 predicts all saturated",
            "sets": len(sr), "saturated": sum(bool(r.get("saturated")) for r in sr),
            "all_faces_covered": all(r.get("faces_covered") for r in sr)}
    d.update({k: v for k, v in info.items() if k in ("published", "labelled_multiplicity")})
    S["calibration_b_symmetric_16_point"][tag] = d

# application: two-fold 32-point models
A = {}
cls = json.load(open(os.path.join(D, "m32", "classes32.json")))
A["isomorphism_classes"] = {"models": cls["models"], "classes": cls["classes"]}
per = {}
for run in ("pass1", "pass1_seeds", "pass2", "pass2_seeds", "pass3"):
    p = os.path.join(D, "m32", run, "summary.json")
    if not os.path.exists(p):
        continue
    d = json.load(open(p))
    d.pop("per_model")
    A[run] = d
    src = "n32k7m2_seeds" if "seeds" in run else "n32k7m2"
    for r in jl(os.path.join(D, "m32", run, "results.jsonl")):
        key = f"{src}:{r['name']}"
        e = per.setdefault(key, {"model": key, "class": cls["per_model"][key]["class"], "attempts": []})
        e["attempts"].append({"run": run, **{k: v for k, v in r.items() if k != "name"}})
for e in per.values():
    e["realized"] = any(a["realized"] for a in e["attempts"])
    e["total_cpu_seconds"] = round(sum(a["cpu_seconds"] for a in e["attempts"]), 1)
    e["min_penalty_violations"] = min((a["best_violations"] for a in e["attempts"] if a.get("best_violations") is not None), default=None)
    e["max_orbits_placed_symmetric_insertion"] = max((a["insertion_max_orbits_placed"] for a in e["attempts"] if "insertion_max_orbits_placed" in a), default=None)
    e["max_points_placed_free_insertion"] = max((a["insertion_ff_max_points_placed"] for a in e["attempts"] if "insertion_ff_max_points_placed" in a), default=None)
    e["min_lp_slack"] = min((a["lp_best_slack"] for a in e["attempts"] if "lp_best_slack" in a), default=None)
A["per_model"] = sorted(per.values(), key=lambda e: (e["model"].split(":")[0], int(e["model"].split("model")[1])))
A["realized"] = sum(e["realized"] for e in per.values())
A["models"] = len(per)
sat = os.path.join(D, "m32", "saturation.jsonl")
A["saturation"] = jl(sat) if os.path.exists(sat) else "not run: no 32-point model was realized"
S["application_32_point_two_fold"] = A
json.dump(S, open(os.path.join(F, "summary.json"), "w"), indent=1)
print("wrote summary.json")
