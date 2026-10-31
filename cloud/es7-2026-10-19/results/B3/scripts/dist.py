#!/usr/bin/env python3
"""Distribution of second-level cube solve times (incremental CaDiCaL) over all sampled logs.
usage: dist.py LOG [LOG ...]"""
import json, sys
ts, nT, nU, nS = [], 0, 0, 0
for p in sys.argv[1:]:
    for l in open(p):
        if l.startswith("#"): continue
        _, r, s, _ = l.split(); ts.append(float(s)); nT += r == "T"; nU += r == "U"; nS += r == "S"
ts.sort(); n = len(ts)
q = lambda f: round(ts[min(n - 1, int(f * n))], 3)
bins = [0.1, 1, 10, 60, 299.9, 1e9]
lab = ["<0.1s", "0.1-1s", "1-10s", "10-60s", "60-300s", "timeout(300s)"]
cnt = [0] * len(bins); lo = 0
for t in ts:
    for i, b in enumerate(bins):
        if t < b: cnt[i] += 1; break
print(json.dumps({"n": n, "U": nU, "S": nS, "T": nT, "mean_s": round(sum(ts) / n, 2),
                  "quantiles": {f"p{int(f*100)}": q(f) for f in (0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99)},
                  "histogram": dict(zip(lab, cnt)),
                  "share_of_time_in_cubes_over_60s": round(sum(t for t in ts if t >= 60) / sum(ts), 3)}, indent=1))
