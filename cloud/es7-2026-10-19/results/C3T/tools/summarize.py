#!/usr/bin/env python3
"""Build ../cases.jsonl (one record per top case) from the logs.
usage: summarize.py   (run from tools/; reads ../logs, ../manifest_depth2.tsv)"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hullcase import cases, case_name, legacy_to_layers, layers_name, parse_layers, tree_children  # noqa: E402

L = os.path.join(HERE, "..", "logs")
man = {}
for line in open(os.path.join(HERE, "..", "manifest_depth2.tsv")).read().splitlines()[1:]:
    d, n, u, h = line.split("\t")
    man[n] = (int(d), int(u), h)
short = {r["case"]: r for r in json.load(open(os.path.join(L, "short_summary.json")))}
cert = {}
for f in ("closures.jsonl", "tree_H6a4s0.jsonl"):
    p = os.path.join(L, f)
    if os.path.exists(p):
        for l in open(p):
            r = json.loads(l)
            if r.get("certified"):
                cert[layers_name(parse_layers(r["node"]))] = r
out = []
for c in cases(11, 7):
    lay = legacy_to_layers(c)
    nm = layers_name(lay)
    ch = [layers_name(x) for x in tree_children(11, 7, lay)]
    below = [n for n in cert if n.startswith(nm + "_")]
    d2 = [n for n in ch if n in cert]
    s = short.get(case_name(c), {})
    out.append({"case": case_name(c), "layer_name": nm, "cnf_sha256": man[nm][2], "units": man[nm][1],
                "vars": 168399, "clauses": 4154921 + man[nm][1],
                "short_run": {k: s.get(k) for k in ("status", "wall_s", "conflicts", "remaining_vars")},
                "depth2_children": len(ch), "depth2_children_certified": len(d2),
                "certified_nodes_below": len(below),
                "certified_solve_s": round(sum(cert[n]["solve_s"] for n in below), 1),
                "certified_check_s": round(sum(cert[n].get("check_s", 0) for n in below), 1),
                "closed": False})
with open(os.path.join(HERE, "..", "cases.jsonl"), "w") as f:
    for r in out:
        f.write(json.dumps(r) + "\n")
        print(json.dumps(r))
