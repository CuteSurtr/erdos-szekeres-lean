#!/usr/bin/env python3
"""Summarize results_K{K}.jsonl and seen files: per run and totals."""
import collections, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for K in (6, 7):
    files = sorted(glob.glob(os.path.join(ROOT, "logs", f"results_K{K}*.jsonl")))
    if not files:
        continue
    per = collections.OrderedDict()
    tot = collections.Counter()
    ids = set()
    for l in (l for fn in files for l in open(fn)):
        r = json.loads(l)
        p = per.setdefault(r["run"], collections.Counter())
        p["tested"] += 1; p["saturated"] += r["saturated"]; p["bad_faces"] += r["bad"]
        p["face_mismatch"] += r["faces"] != r["hit"]; p["cpu"] += r["cpu"]
        tot["tested"] += 1; tot["saturated"] += r["saturated"]; tot["bad_faces"] += r["bad"]
        tot["face_mismatch"] += r["faces"] != r["hit"]; tot["cpu"] += r["cpu"]
        ids.add(r["canonm"])
        tot["faces_min"] = min(tot["faces_min"] or 10**9, r["faces"]); tot["faces_max"] = max(tot["faces_max"], r["faces"])
    n_or = len(set(x for fn in glob.glob(os.path.join(ROOT, "data", f"seen_or_K{K}*.txt")) for x in open(fn).read().split()))
    print(f"K={K}: distinct order types up to reflection tested={tot['tested']} (unique ids {len(ids)}), "
          f"saturated={tot['saturated']}, bad_faces={tot['bad_faces']}, face_count_mismatch={tot['face_mismatch']}, "
          f"sat_cpu={tot['cpu']:.1f}s, faces range [{tot['faces_min']},{tot['faces_max']}], "
          f"distinct orientation-preserving order types seen={n_or}")
    for run, p in per.items():
        print(f"   {run}: tested={p['tested']} saturated={p['saturated']} bad={p['bad_faces']} mism={p['face_mismatch']} cpu={p['cpu']:.1f}")
