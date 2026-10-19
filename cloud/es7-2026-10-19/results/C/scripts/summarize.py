#!/usr/bin/env python3
"""Collect Task C results into one summary JSON.
usage: summarize.py <workdir> <resultsdir>
workdir layout: runs/{i_hull,ii_interior,i_probe,ii_probe}, ann/{ctl32,m33}, val/, cnf/
"""
import sys, os, json, glob, re, statistics
W, R = sys.argv[1], sys.argv[2]
S = {}
S["machine"] = {"cores": os.cpu_count()}
S["part1"] = json.load(open(os.path.join(R, "logs", "part1_validate_report.json")))
cnc = {}
for name in ["i_hull", "ii_interior"]:
    d = os.path.join(W, "runs", name)
    if not os.path.exists(d): continue
    last = json.load(open(os.path.join(d, "latest.json")))
    prog = [json.loads(l) for l in open(os.path.join(d, "cnc.log"))]
    closed = [l.split() for l in open(os.path.join(d, "closed.txt")) if l.strip()]
    cnc[name] = {"final": last, "progress_records": len(prog), "closed_cubes": len(closed),
                 "closed_cube_depths": sorted(len(c) - 2 for c in closed)}
S["part2_cnc"] = cnc
probes = {}
for name in ["i_probe", "ii_probe"]:
    f = os.path.join(W, "runs", name, "probes.jsonl")
    if not os.path.exists(f): continue
    P = [json.loads(l) for l in open(f)]
    leaves = [p["leaf_depth"] for p in P if p["status"] == "leaf"]
    cens = [p["leaf_depth"] for p in P if p["status"] != "leaf"]
    est = [p["knuth_nodes"] for p in P if p["status"] == "leaf"]
    probes[name] = {"probes": len(P), "leaf_depths": leaves, "censored_depths": cens,
                    "statuses": sorted(set(p["status"] for p in P)),
                    "knuth_mean_nodes_leaf_probes_only": (sum(est) / len(est)) if est else None,
                    "median_leaf_depth": statistics.median(leaves) if leaves else None}
S["part2_knuth_probes"] = probes
ann = {}
for sub in ["ctl32", "m33"]:
    rows = []
    for f in sorted(glob.glob(os.path.join(W, "ann", sub, "*.log"))):
        for l in open(f):
            if l.startswith("run="):
                d = dict(t.split("=", 1) for t in l.split() if "=" in t)
                rows.append(d)
    if not rows: continue
    bests = [int(r["best"]) for r in rows]
    rec = {"runs": len(rows), "min_energy": min(bests), "energy_hist": {str(b): bests.count(b) for b in sorted(set(bests))},
           "cpu_s_total": round(sum(float(r["cpu"].rstrip("s")) for r in rows), 1)}
    if sub == "ctl32":
        z = [r for r in rows if r["best"] == "0"]
        rec["zero_runs"] = len(z)
        rec["zero_run_cpu_s"] = [float(r["cpu"].rstrip("s")) for r in z]
        rec["axis_scan_min_E"] = sorted(int(r["axis_min_E"]) for r in z if "axis_min_E" in r)
        rec["axis_zero_intervals_total"] = sum(int(r["axis_zero_intervals"]) for r in z if "axis_zero_intervals" in r)
    else:
        scans = []
        for f in glob.glob(os.path.join(W, "ann", sub, "*.scan")):
            for l in open(f):
                m = re.search(r"min_axis_E=(\d+)", l)
                if m: scans.append(int(m.group(1)))
        rec["pair_scans"] = len(scans)
        rec["pair_scan_min_E"] = min(scans) if scans else None
    ann[sub] = rec
p1 = os.path.join(W, "ann", "m33_phase1", "K7_P16_A1_s404.scan")
if os.path.exists(p1):
    v = [int(m.group(1)) for m in re.finditer(r"min_axis_E=(\d+)", open(p1).read())]
    e = [int(m.group(1)) for m in re.finditer(r"E33=(\d+)", open(p1).read())]
    ann["m33_phase1_unthrottled_scans"] = {"scans": len(v), "min_axis_E": min(v) if v else None, "min_E33": min(e) if e else None}
walks = {}
for f in sorted(glob.glob(os.path.join(W, "ann", "walk", "walk_*.log"))):
    L = open(f).read().split("\n")
    start = next((int(l.split("=")[1]) for l in L if l.startswith("start m=")), None)
    bests = [int(re.search(r"new_best_m=(\d+)", l).group(1)) for l in L if "new_best_m=" in l]
    walks[os.path.basename(f)] = {"start_m": start, "best_m": min([start] + bests) if start is not None else None,
                                  "improvements": len(bests), "end_line": next((l for l in L if l.startswith("end")), None)}
ann["axis_walks"] = walks
S["part3_anneal"] = ann
print(json.dumps(S, indent=1))
