#!/usr/bin/env python3
"""Offline re-verification of a cnc2.py cube tree from its event log.

Replays events.jsonl from the root cube (): each event must refer to a current open leaf;
'U' closes it, 'K' with a literal splits it into cube+[l], cube+[-l] (l must be an
orientation variable not already decided in the cube), 'K' with 0 keeps it open, 'S' marks
it satisfiable. At the end the leaves partition the search space (sum of 2^-depth = 1,
exactly, with Fractions), and the open leaves must equal the open list in state.json.
Also writes per-depth statistics used by estimate.py.

usage: cover.py RUN_DIR NX [out.json]
"""
import json, sys
from fractions import Fraction
from pathlib import Path

run, nX = Path(sys.argv[1]), int(sys.argv[2])
leaves = {(): "open"}
bad = []
per_depth = {}
for line in open(run / "events.jsonl"):
    e = json.loads(line)
    c = tuple(e["cube"])
    if leaves.get(c) != "open":
        bad.append(("not an open leaf", e["id"])); continue
    d = len(c)
    pd = per_depth.setdefault(d, {"n": 0, "U": 0, "K": 0, "S": 0, "secs": 0.0, "secs_U": 0.0, "secs_K": 0.0})
    pd["n"] += 1; pd[e["r"]] += 1; pd["secs"] += e["s"]; pd["secs_" + e["r"]] = pd.get("secs_" + e["r"], 0.0) + e["s"]
    # conflict budget of the job (exact for split jobs, an upper bound for closed / SAT jobs)
    pd["conf_" + e["r"]] = pd.get("conf_" + e["r"], 0) + e["limit"]
    if e["r"] == "U":
        leaves[c] = "closed"
    elif e["r"] == "S":
        leaves[c] = "sat"
    else:
        l = e["lit"]
        if l == 0:
            continue
        if not (1 <= abs(l) <= nX) or l in c or -l in c:
            bad.append(("bad split literal", e["id"], l)); continue
        del leaves[c]
        leaves[c + (l,)] = "open"; leaves[c + (-l,)] = "open"
tot = sum((Fraction(1, 2 ** len(c)) for c in leaves), Fraction(0))
cw = sum((Fraction(1, 2 ** len(c)) for c, s in leaves.items() if s == "closed"), Fraction(0))
open_leaves = {c for c, s in leaves.items() if s == "open"}
st = json.loads((run / "state.json").read_text())
st_open = {tuple(c) for c, _ in st["open"]}
hist = {}
for c in open_leaves:
    hist[len(c)] = hist.get(len(c), 0) + 1
res = {"events_ok": not bad, "bad": bad[:10], "leaves": len(leaves), "partition_sum_is_1": tot == 1,
       "closed_leaves": sum(1 for s in leaves.values() if s == "closed"),
       "sat_leaves": sum(1 for s in leaves.values() if s == "sat"),
       "open_leaves": len(open_leaves), "open_matches_state": open_leaves == st_open,
       "closed_weight_exact": f"{cw.numerator}/{cw.denominator}", "closed_weight": float(cw),
       "state_closed_weight": st["closed_weight"], "closed_weight_matches_state": f"{cw.numerator}/{cw.denominator}" == st["closed_weight"],
       "open_depth_hist": {str(k): hist[k] for k in sorted(hist)},
       "per_depth": {str(k): {kk: (round(v, 1) if isinstance(v, float) else v) for kk, v in per_depth[k].items()} for k in sorted(per_depth)}}
print(json.dumps(res, indent=1))
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps(res, indent=1))
