#!/usr/bin/env python3
"""Summarize C04's out.jsonl per root and per depth. Run from the C3-S tools dir of commit 8dc27c3.
usage: summarize_c04.py OUT.jsonl ROOTS.txt"""
import json, sys, collections
sys.path.insert(0, "../../C3a"); sys.path.insert(0, ".")
from hullcase import parse_layers, layers_name, tree_children

recs = [json.loads(l) for l in open(sys.argv[1])]
roots = [l.split("\t")[1].strip() for l in open(sys.argv[2]) if l.strip()]
cert, split, tried = set(), set(), collections.defaultdict(list)
for r in recs:
    if r.get("certified"): cert.add(r["node"])
    if r.get("split"): split.add(r["node"])
    if "status" in r: tried[r["node"]].append(r)
dep = lambda n: len(parse_layers(n))
memo = {}
def covered(n):
    if n not in memo:
        memo[n] = n in cert or (n in split and all(covered(layers_name(c)) for c in tree_children(11, 7, parse_layers(n))))
    return memo[n]
def open_leaves(n, acc):
    if n in cert: return
    if n in split:
        for c in tree_children(11, 7, parse_layers(n)): open_leaves(layers_name(c), acc)
    else: acc.append(n)
under = lambda n, R: n == R or n.startswith(R + "_")
tot = collections.defaultdict(lambda: [0, 0, 0])
out = {"roots": []}
for R in roots:
    nodes = {r["node"] for r in recs if under(r["node"], R)}
    if not nodes:
        out["roots"].append({"root": R, "state": "not started"}); continue
    cd = collections.Counter(dep(n) for n in nodes if n in cert)
    sd = collections.Counter(dep(n) for n in nodes if n in split)
    ol = []; open_leaves(R, ol)
    od = collections.Counter(dep(n) for n in ol)
    for d, c in cd.items(): tot[d][0] += c
    for d, c in sd.items(): tot[d][1] += c
    for d, c in od.items(): tot[d][2] += c
    rs = [x for n in nodes for x in tried[n]]
    out["roots"].append({"root": R, "state": "closed" if covered(R) else "open",
        "certified_by_depth": dict(sorted(cd.items())), "split_by_depth": dict(sorted(sd.items())),
        "open_leaves_by_depth": dict(sorted(od.items())), "presplit": sum(1 for r in recs if r.get("presplit") and under(r["node"], R)),
        "timeouts": sum(1 for x in rs if x["status"] == "UNKNOWN"), "unsat_not_certified": sum(1 for x in rs if x["status"] == "UNSATISFIABLE" and not x.get("certified")),
        "solve_s": round(sum(x.get("solve_s", 0) for x in rs), 1), "check_s": round(sum(x.get("check_s", 0) for x in rs), 1)})
out["per_depth"] = {d: dict(zip(("certified", "split", "open"), v)) for d, v in sorted(tot.items())}
out["closed_roots"] = [x["root"] for x in out["roots"] if x["state"] == "closed"]
out["sat"] = [r["node"] for r in recs if r.get("status") == "SATISFIABLE"]
print(json.dumps(out, indent=1))
