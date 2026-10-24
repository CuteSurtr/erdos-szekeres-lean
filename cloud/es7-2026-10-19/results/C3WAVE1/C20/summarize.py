#!/usr/bin/env python3
"""Per-root and per-depth summary of out.jsonl for the C20 roots (run from C3-S/tools of 8dc27c3)."""
import json, sys, collections
sys.path.insert(0, "../../C3a"); sys.path.insert(0, ".")
from hullcase import layers_name, parse_layers, tree_children
out, roots_file = sys.argv[1], sys.argv[2]
roots = [l.split()[1] for l in open(roots_file)]
recs = [json.loads(l) for l in open(out)]
cert = {r["node"] for r in recs if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"}
split = {r["node"] for r in recs if r.get("split")}
solved = {}
for r in recs:
    if "status" in r:
        solved.setdefault(r["node"], []).append(r)
memo = {}
def closed(n):
    if n not in memo:
        memo[n] = n in cert or (n in split and all(closed(layers_name(c)) for c in tree_children(11, 7, parse_layers(n))))
    return memo[n]
def walk(n, acc):
    d = len(parse_layers(n))
    for r in solved.get(n, []):
        acc["solve"] += r.get("solve_s", 0); acc["check"] += r.get("check_s", 0)
    if n in cert:
        acc["cert"][d] += 1
    elif n in split:
        acc["split"][d] += 1
        for c in tree_children(11, 7, parse_layers(n)):
            walk(layers_name(c), acc)
    else:
        acc["open"][d] += 1
tot = {k: collections.Counter() for k in ("cert", "split", "open")}
print("| root | status | certified by depth | split by depth | open by depth | solve s | check s |")
print("|---|---|---|---|---|---|---|")
nclosed = 0
for rt in roots:
    acc = {"cert": collections.Counter(), "split": collections.Counter(), "open": collections.Counter(), "solve": 0.0, "check": 0.0}
    walk(rt, acc)
    c = closed(rt); nclosed += c
    tried = rt in solved or rt in split
    st = "closed" if c else ("open" if tried else "not started")
    f = lambda C: ", ".join(f"d{d}: {C[d]}" for d in sorted(C)) or "-"
    print(f"| {rt} | {st} | {f(acc['cert'])} | {f(acc['split'])} | {f(acc['open'])} | {acc['solve']:.0f} | {acc['check']:.0f} |")
    for k in tot:
        tot[k].update(acc[k])
print(f"\nroots closed: {nclosed} of {len(roots)}\n")
print("| depth | certified | split | open |\n|---|---|---|---|")
for d in sorted(set(tot["cert"]) | set(tot["split"]) | set(tot["open"])):
    print(f"| {d} | {tot['cert'][d]} | {tot['split'][d]} | {tot['open'][d]} |")
rej = [r["node"] for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")]
sat = [r["node"] for r in recs if r.get("status") == "SATISFIABLE"]
print(f"\nUNSAT records not accepted: {rej}\nSAT records: {sat}")
