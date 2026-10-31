#!/usr/bin/env python3
"""Copy trimmed logs from the work directory into results/B/logs and write summary.json.
usage: collect.py CACHE_DIR RESULTS_B_DIR"""
import json, shutil, subprocess, sys
from pathlib import Path

C = Path(sys.argv[1]).resolve(); R = Path(sys.argv[2]).resolve()
S = Path(__file__).resolve().parent
L = R / "logs"; L.mkdir(parents=True, exist_ok=True)
for f in ("controls_plain.json", "controls_sb.json", "sbcheck.json", "lrat_controls.json", "glue_controls.json", "calib.json"):
    if (C / f).exists():
        shutil.copy(C / f, L / f)
summary = {"machine": {}, "controls": {}, "instances": {}}
try:
    summary["machine"]["hw.ncpu"] = int(subprocess.run(["sysctl", "-n", "hw.ncpu"], capture_output=True, text=True).stdout)
    summary["machine"]["perf_cores"] = int(subprocess.run(["sysctl", "-n", "hw.perflevel0.physicalcpu"], capture_output=True, text=True).stdout)
    summary["machine"]["efficiency_cores"] = int(subprocess.run(["sysctl", "-n", "hw.perflevel1.physicalcpu"], capture_output=True, text=True).stdout)
except Exception as e:  # noqa
    summary["machine"]["error"] = str(e)
for f in ("controls_plain.json", "controls_sb.json", "sbcheck.json", "lrat_controls.json", "glue_controls.json", "calib.json"):
    p = C / f
    if p.exists():
        d = json.loads(p.read_text())
        if isinstance(d, list):  # calib.json
            summary["controls"][f[:-5]] = [{k: r[k] for k in ("instance", "jobs", "budget_conflicts", "cpu_s", "wall_s")} for r in d]
        else:
            summary["controls"][f[:-5]] = d.get("summary") or {k: v for k, v in d.items() if k in ("all_ok", "all_pass", "all_verified", "negative_test")}
INST = {"k7a5u6N26": (2600, "(7,5,6) at 26 points: no 5-cap, no 6-cup, no convex 7-gon"),
        "k7a5u7N27": (2925, "(7,5,7) at 27 points: no 5-cap, no convex 7-gon")}
for tag, (nx, desc) in INST.items():
    run = C / "runs" / tag
    if not run.exists():
        continue
    dst = L / tag; dst.mkdir(exist_ok=True)
    for f in ("progress.jsonl", "report30.jsonl", "lrat.jsonl", "state.json", "final.json"):
        if (run / f).exists():
            shutil.copy(run / f, dst / f)
    ev = run / "events.jsonl"
    if ev.exists():
        if ev.stat().st_size < 20e6:
            shutil.copy(ev, dst / "events.jsonl")
        else:
            subprocess.run(["gzip", "-c", str(ev)], stdout=open(dst / "events.jsonl.gz", "wb"), check=True)
    cov = subprocess.run([sys.executable, str(S / "cover.py"), str(run), str(nx), str(dst / "cover.json")], capture_output=True, text=True)
    est = subprocess.run([sys.executable, str(S / "estimate.py"), str(dst / "cover.json"), "10000", "1.25",
                          str(C / "calib.json"), tag] +
                         ([str(p) for p in sorted((C / "knuth").glob(f"{tag}_s*.jsonl"))]),
                         capture_output=True, text=True)
    (dst / "estimate.json").write_text(est.stdout)
    c = json.loads(cov.stdout); fin = json.loads((run / "final.json").read_text()) if (run / "final.json").exists() else {}
    lr = [json.loads(l) for l in open(run / "lrat.jsonl")] if (run / "lrat.jsonl").exists() else []
    summary["instances"][tag] = {
        "description": desc, "status": fin.get("finished", "running/stopped (no final.json)"),
        "jobs": sum(v["n"] for v in c["per_depth"].values()), "closed_cubes": c["closed_leaves"],
        "open_cubes": c["open_leaves"], "sat_cubes": c["sat_leaves"],
        "closed_weight_exact": c["closed_weight_exact"], "closed_weight": c["closed_weight"],
        "open_depth_hist": c["open_depth_hist"], "tree_replay_ok": c["events_ok"] and c["partition_sum_is_1"] and c["open_matches_state"] and c["closed_weight_matches_state"],
        "lrat_sampled": len(lr), "lrat_verified": sum(1 for r in lr if r.get("lrat") == "VERIFIED"),
        "lrat_failed": sum(1 for r in lr if r.get("lrat") == "FAILED"),
        "bb_xcheck_unsat": sum(1 for r in lr if r.get("xcheck_rc") == 20),
        "bb_xcheck_other": sum(1 for r in lr if "xcheck_rc" in r and r["xcheck_rc"] != 20),
        "sat_check": fin.get("sat_check")}
kd = C / "knuth"
if kd.exists():
    dst = L / "knuth"; dst.mkdir(exist_ok=True)
    for p in kd.glob("*.jsonl"):
        shutil.copy(p, dst / p.name)
(R / "summary.json").write_text(json.dumps(summary, indent=1))
print(json.dumps(summary, indent=1))
