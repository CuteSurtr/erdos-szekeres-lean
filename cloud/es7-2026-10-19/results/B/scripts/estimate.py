#!/usr/bin/env python3
"""Tree-size estimate for a cube-and-conquer run from its frontier, plus Knuth probes.

Input: cover.py JSON of the run (per-depth processed / closed / split counts and conflict
budgets), the worker CPU calibration (calib.py: CPU seconds per conflict), and optional
Knuth probe logs (knuth.py).

Costs are counted in CONFLICTS (the job budget: exact for split jobs, an upper bound for
closed jobs) and converted to dedicated-core hours with the calibration, because wall seconds
on the shared, oversubscribed machine overstate core time by about 6-7x.

BFS frontier model: level d is complete when all 2*K_{d-1} children were processed.
q_d = K_d / n_d is the fraction of level-d cubes that did NOT close within their budget;
the frontier grows by g_d = 2 q_d per level (g_d >= 1: still expanding at that depth).
Projections beyond the last complete level D (budget(d) = base * GROW^d):
  pessimistic : q stays at q_D;
  central     : log-odds of q decline linearly at the slope fitted over complete levels
                with 0 < q < 1 (if no such fit or slope >= 0: same as pessimistic);
  optimistic  : log-odds decline at twice that slope.
With q = 1 at every observed level no slope can be fitted; the honest statement is then
"no closure observed up to depth D; divergent at the observed depths".
Knuth probes (fixed budget B per node): nodes ~ sum_{d<=L} 2^d; conflicts <= nodes * B.
usage: estimate.py cover.json BASE GROW calib.json INSTANCE [knuth1.jsonl ...]
"""
import json, math, statistics, sys

cov = json.load(open(sys.argv[1])); base = int(sys.argv[2]); grow = float(sys.argv[3])
cal = {r["instance"]: r for r in json.load(open(sys.argv[4]))}; inst = sys.argv[5]
cpc = cal[inst]["cpu_s"] / (cal[inst]["jobs"] * cal[inst]["budget_conflicts"])  # CPU s per conflict
pd = {int(k): v for k, v in cov["per_depth"].items()}
levels = []
for d in sorted(pd):
    n, K, U = pd[d]["n"], pd[d]["K"], pd[d]["U"]
    expected = 1 if d == 0 else 2 * pd.get(d - 1, {"K": 0})["K"]
    complete = n == expected and (d == 0 or levels[-1]["complete"])
    levels.append({"d": d, "n": n, "closed": U, "split": K, "q": K / n if n else None, "g": 2 * K / n if n else None,
                   "complete": complete, "budget": int(base * grow ** d),
                   "conflicts": pd[d].get("conf_K", 0) + pd[d].get("conf_U", 0) + pd[d].get("conf_S", 0)})
comp = [l for l in levels if l["complete"]]
out = {"instance": inst, "cpu_s_per_conflict": cpc, "levels": levels}
done_conf = sum(l["conflicts"] for l in levels)
out["done"] = {"jobs": sum(l["n"] for l in levels), "conflicts_upper": done_conf,
               "core_hours_dedicated_equiv": round(done_conf * cpc / 3600, 2)}
if comp:
    D = comp[-1]["d"]; last = comp[-1]
    pts = [(l["d"], math.log(l["q"] / (1 - l["q"]))) for l in comp if 0 < l["q"] < 1]
    slope = None
    if len(pts) >= 2:
        xs, ys = zip(*pts); mx, my = statistics.mean(xs), statistics.mean(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        slope = sum((x - mx) * (y - my) for x, y in pts) / sxx if sxx else None

    def project(sl):
        q = last["q"]; frontier = 2 * last["split"]; nodes = 0; conf = 0.0; d = D + 1
        lo = math.log(q / (1 - q)) if 0 < q < 1 else 30.0
        while d < D + 400:
            if sl is not None and sl < 0:
                lo += sl
            qd = 1 / (1 + math.exp(-lo)) if lo < 30 else 1.0
            nodes += frontier; conf += frontier * base * grow ** d
            frontier = frontier * 2 * qd
            if frontier < 0.5:
                return {"converges": True, "extra_nodes": round(nodes), "extra_conflicts": conf,
                        "extra_core_hours": round(conf * cpc / 3600, 1), "depth_reached": d}
            if nodes > 1e15:
                break
            d += 1
        return {"converges": False, "note": "divergent under this model (frontier never shrinks)"}

    out["last_complete_level"] = D
    out["q_at_last_complete_level"] = last["q"]
    out["logodds_slope_per_level"] = slope
    out["pessimistic_constant_q"] = project(None)
    out["central_fitted_slope"] = project(slope if slope is not None and slope < 0 else None)
    out["optimistic_double_slope"] = project(2 * slope if slope is not None and slope < 0 else None)
kn = []
for f in sys.argv[6:]:
    kn += [json.loads(l) for l in open(f)]
if kn:
    fin = [r for r in kn if r["end"] == "closed"]; cen = [r for r in kn if r["end"] != "closed"]

    def summ(v):
        v = sorted(v)
        return {"n": len(v), "mean": statistics.mean(v), "median": statistics.median(v), "min": v[0], "max": v[-1]} if v else None
    B = kn[0]["budget"]
    out["knuth"] = {"budget_per_node": B, "probes": len(kn), "closed_probes": len(fin), "censored_or_other": len(cen),
                    "leaf_depth": summ([r["leaf_depth"] for r in fin]),
                    "est_nodes": summ([r["est_nodes"] for r in fin]),
                    "est_core_hours_upper": summ([r["est_nodes"] * B * cpc / 3600 for r in fin]),
                    "censored_depths": [r["leaf_depth"] for r in cen],
                    "censored_est_nodes_lower_bounds": [r["est_nodes"] for r in cen]}
print(json.dumps(out, indent=1, default=str))
