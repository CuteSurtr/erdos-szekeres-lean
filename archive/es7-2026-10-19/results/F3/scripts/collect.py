#!/usr/bin/env python3
"""Summarize an F3 run directory into results/F3/data: generator statistics, realized 26-sets,
fingerprint duplicates, and both 32-point saturation conventions.  Copies the small per-set files
(no CNF, no scratch).  Prints ALERT lines for any 32-set that is not saturated or not verified.
usage: collect.py RUNDIR DATADIR"""
import sys, os, json, glob, shutil, collections
run, data = sys.argv[1:3]; os.makedirs(data, exist_ok=True)
def jl(f):
    try: return [json.loads(l) for l in open(f) if l.strip()]
    except FileNotFoundError: return []
S = {"generators": {}, "sets": []}
gg = []
for f in sorted(glob.glob(f"{run}/gg/guided_*.jsonl")): gg += jl(f)
S["generators"]["grow_guided"] = {"seeds": sorted(os.path.basename(f)[7:-6] for f in glob.glob(f"{run}/gg/guided_*.jsonl")),
    "chains": len(gg), "reached26": sum(r.get("reached") == 26 for r in gg),
    "reached_hist": dict(sorted(collections.Counter(r.get("reached") for r in gg).items()))}
af = []
for f in sorted(glob.glob(f"{run}/armF_*.jsonl")): af += jl(f)
S["generators"]["arm_f"] = {"restarts": len(af), "complete": sum("points" in r for r in af),
    "complete_exact_ok": sum(bool(r.get("exact_ok")) for r in af),
    "fail_at_hist": dict(sorted(collections.Counter(r.get("fail_at", 26) for r in af).items()))}
kp = []
for f in sorted(glob.glob(f"{run}/kph/real_*.jsonl")): kp += jl(f)
cpu = sum(r.get("cpu") or 0 for r in kp)
S["generators"]["kph_style"] = {"models_realize_attempted": len(kp), "realized": sum(bool(r.get("realized")) for r in kp),
    "realized_exact_ok": sum(bool(r.get("exact_check")) for r in kp), "realizer_cpu_s": round(cpu),
    "models_generated": sum(len(open(f).read().split()) for f in glob.glob(f"{run}/kph/models_*.txt"))}
alerts = []
for d in sorted(glob.glob(f"{run}/proc/*/")):
    n = os.path.basename(d.rstrip("/")); od = f"{data}/sets/{n}"; os.makedirs(od, exist_ok=True)
    for f in glob.glob(f"{d}*.json*") + glob.glob(f"{d}*.pts") + glob.glob(f"{d}*.log"):
        shutil.copy(f, od)
    for sub in ("convA", "convB"):
        if os.path.isdir(d + sub):
            os.makedirs(f"{od}/{sub}", exist_ok=True)
            for f in glob.glob(f"{d}{sub}/*"):
                if os.path.getsize(f) < 5_000_000: shutil.copy(f, f"{od}/{sub}")
    st = (jl(f"{d}status.json") or [{}])[0]; fp = (jl(f"{d}fp.jsonl") or [{}])[0]
    v = (jl(f"{d}verify26.json") or [{}])[0]
    rec = {"id": n, "fp": fp.get("fp"), "duplicate": st.get("duplicate"), "done": st.get("done", False),
           "verify26": {k: v.get(k) for k in ("general_position", "cap_cup", "lcs", "brute_axviol_cap_cup_lcs")}}
    A = jl(f"{d}convA/sat32.jsonl")
    rec["convA"] = [{"id": r["id"], "geom_saturated": r.get("geom_saturated"), "faces": r.get("geom", {}).get("faces_euler"), "geom_run": r.get("geom_run", True),
                     "bad": r.get("geom", {}).get("bad_candidates"), "geom_error": r.get("geom", {}).get("error"),
                     "abs_unsat": r["abs"]["UNSAT"], "abs_sat": r["abs"]["SAT"], "abs_unknown": r["abs"]["UNKNOWN"],
                     "abs_saturated": r["abs_saturated"]} for r in A]
    try: rec["convA_brute32"] = open(f"{d}convA/brute32.txt").read().split("\n")[:-1]
    except FileNotFoundError: pass
    B = jl(f"{d}convB_check32.jsonl")
    rec["convB"] = [{k: r.get(k) for k in ("file", "general_position", "largest_convex_subset", "brute_kgon", "sat_c",
                     "ext_sat", "ext_unknown", "ext_unsat", "abstract_saturated", "geom_saturated")} for r in B]
    for r in rec["convA"]:
        if r["abs_sat"] or r["abs_unknown"] or (r["bad"] or 0) > 0: alerts.append(f"ALERT convA {n} {r}")
    for r in B:
        bad = (r.get("ext_sat") or r.get("ext_unknown") or r.get("ext_positions") != 33 or not r.get("general_position")
               or r.get("largest_convex_subset") != 6 or "convex_K_subsets=0" not in str(r.get("brute_kgon"))
               or (isinstance(r.get("sat_c"), dict) and not r.get("geom_saturated")))
        if bad: alerts.append(f"ALERT convB {n} {json.dumps(r)[:600]}")
    S["sets"].append(rec)
S["new_distinct_26"] = sum(1 for r in S["sets"] if r["duplicate"] is False)
S["alerts"] = alerts
json.dump(S, open(f"{data}/summary.json", "w"), indent=1)
print(json.dumps(S["generators"])); print(json.dumps([{k: r[k] for k in ("id", "duplicate", "done")} for r in S["sets"]]))
for a in alerts: print(a)
