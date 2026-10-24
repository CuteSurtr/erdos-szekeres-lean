#!/usr/bin/env python3
"""Projection of total two-level cube-and-conquer cost for (7,5,7)@27.

Two-stage sample: top cubes (depth-14 march_cu) drawn uniformly; for each, march_cu -d 10 on the
sub-CNF and a uniform random sample of its second-level cubes solved by incremental CaDiCaL with a
per-cube cap (time-outs counted AT the cap, so the estimate is a lower bound wherever caps bite).
  E_top = march_s + n_sub * mean(sampled sub-cube seconds)
  total = top_march_s + N_top * mean(E_top)      (+ 95% bootstrap interval over top cubes)
usage: project.py N_TOP TOP_MARCH_S TOPJSONL [TOPJSONL ...] [--partial DIR=TOPID ...]"""
import json, random, statistics as st, sys
ntop, topm = int(sys.argv[1]), float(sys.argv[2])
recs, extra = [], []
for arg in sys.argv[3:]:
    if "=" in arg:  # partial logs: path=topid:march_s:n_sub
        path, spec = arg.split("=")
        tid, ms, ns = spec.split(":")
        rows = [l.split() for l in open(path) if not l.startswith("#")]
        ts = [float(r[2]) for r in rows]
        recs.append({"id": int(tid), "march_s": float(ms), "n_sub": int(ns), "n_done": len(ts),
                     "solve_s": sum(ts), "n_T": sum(r[1] == "T" for r in rows), "ts": ts, "src": "partial"})
    else:
        for l in open(arg):
            r = json.loads(l)
            if r.get("n_done") or r["n_sub"] == 0:
                r.setdefault("n_done", 0); recs.append(r)
E = []
allts = []
for r in recs:
    e = r["march_s"] + (r["n_sub"] * r["solve_s"] / r["n_done"] if r["n_done"] else 0.0)
    r["E"] = e; E.append(e)
    if "ts" in r: allts += r["ts"]
m = st.mean(E)
rng = random.Random(1)
boots = sorted(st.mean(rng.choices(E, k=len(E))) for _ in range(4000))
lo, hi = boots[100], boots[3899]
f = lambda s: s / 3600
out = {"n_top_sampled": len(E), "N_top": ntop,
       "mean_E_top_s": round(m, 1), "median_E_top_s": round(st.median(E), 1),
       "total_core_h": round(f(topm + ntop * m)), "ci95_core_h": [round(f(topm + ntop * lo)), round(f(topm + ntop * hi))],
       "march_share": round(sum(r["march_s"] for r in recs) / sum(E), 3),
       "sub_cubes_solved": sum(r["n_done"] for r in recs), "sub_timeouts": sum(r.get("n_T", 0) for r in recs),
       "mean_n_sub": round(st.mean(r["n_sub"] for r in recs), 1),
       "projected_leaf_cubes": round(ntop * st.mean(r["n_sub"] for r in recs))}
print(json.dumps(out, indent=1))
