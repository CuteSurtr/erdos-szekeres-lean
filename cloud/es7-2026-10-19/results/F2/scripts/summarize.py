#!/usr/bin/env python3
"""Collect F2 numbers from the run directory into summary.json.  usage: summarize.py RUNDIR OUT.json"""
import collections, glob, json, os, sys
rd, out = sys.argv[1:3]
J = lambda f: [json.loads(l) for l in open(f) if l.strip().startswith("{")]
S = {}
# stream A: pure abstract models through the realizer
q = [l.split()[:2] for l in open(os.path.join(rd, "queue.txt"))]
R = J(os.path.join(rd, "real", "results.jsonl"))
mode = {f"{h}_m{m}": m for h, m in q}
byM = collections.Counter(mode[r["tag"]] for r in R)
S["streamA"] = {"models_verified_distinct": len(open(os.path.join(rd, "seen.txt")).read().split()),
                "models_queued": len(q), "models_attempted": len(R), "attempted_by_phase_mode": dict(byM),
                "realized": sum(r["realized"] for r in R), "cpu_budget_s": 4,
                "ins_ff_max_points_placed": dict(sorted(collections.Counter(r.get("insertion_ff_max_points_placed") for r in R if r.get("insertion_ff_max_points_placed")).items())),
                "lp_best_slack_median": sorted(r["lp_best_slack"] for r in R if "lp_best_slack" in r)[len(R) // 2] if R else None}
# stream B: guided growth
G = []
for d in ("ggrun", "ggdfs", "ggw", "ggs"):
    for f in glob.glob(os.path.join(rd, d, "guided_*.jsonl")):
        G += [dict(r, run=d) for r in J(f)]
S["streamB"] = {run: {"chains": sum(1 for r in G if r["run"] == run),
                      "max_reached": dict(sorted(collections.Counter(r["max_reached"] for r in G if r["run"] == run).items())),
                      "cpu_s_total": round(sum(r["secs"] for r in G if r["run"] == run))} for run in ("ggrun", "ggdfs", "ggw", "ggs")}
S["sets26"] = J(os.path.join(rd, "verify26.jsonl"))
S["process26"] = J(os.path.join(rd, "process26.jsonl"))
chk = []
for f in glob.glob(os.path.join(rd, "new32_check_*.jsonl")) + [os.path.join(rd, "new32_check.jsonl")]:
    chk += J(f)
chk = {r["file"]: r for r in chk}
rot = {}
for f in glob.glob(os.path.join(rd, "new32r_check*.jsonl")):
    for r in J(f): rot[r["file"]] = r
sm = {r["file"]: r for r in J(os.path.join(rd, "small_check.jsonl"))}
S["sets32"] = {"count": len(chk),
               "heptagon_free_exact": sum(r["general_position"] and r["largest_convex_subset"] == 6 and "convex_K_subsets=0" in r["brute_kgon"] for r in chk.values()),
               "abstract_saturated_x": sum(r["abstract_saturated"] for r in chk.values()),
               "abstract_saturated_rot90": sum(r["abstract_saturated"] for r in rot.values()), "rot90_tested": len(rot),
               "ext_SAT": {k: r["ext_sat"] for k, r in list(chk.items()) + list(rot.items()) if r["ext_sat"]},
               "ext_UNKNOWN": {k: r["ext_unknown"] for k, r in list(chk.items()) + list(rot.items()) if r["ext_unknown"]},
               "small_realizations_tested_with_satc": len(sm),
               "satc_saturated": sum(bool(r.get("geom_saturated")) for r in sm.values()),
               "satc_bad_candidates_total": sum(r["sat_c"].get("bad_candidates", 0) for r in sm.values() if isinstance(r["sat_c"], dict)),
               "small_also_abstract_saturated": sum(r["abstract_saturated"] for r in sm.values())}
nv = os.path.join(rd, "novelty_final.json")
if os.path.exists(nv): S["novelty"] = json.load(open(nv))
json.dump(S, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in S.items() if k not in ("sets26", "process26")}, indent=1))
