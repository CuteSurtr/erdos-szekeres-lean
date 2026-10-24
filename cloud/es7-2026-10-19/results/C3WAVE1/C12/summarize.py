#!/usr/bin/env python3
"""Summarize C12 out.jsonl per root and per depth. usage: summarize.py OUT.jsonl ROOTS.txt (run with C3-S/tools on sys.path)"""
import json, sys, collections
sys.path.insert(0, "/opt/c3s/cloud/es7-2026-10-19/results/C3a"); sys.path.insert(0, "/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools")
from hullcase import parse_layers, layers_name, tree_children
recs = [json.loads(l) for l in open(sys.argv[1])]
roots = [l.split()[1] for l in open(sys.argv[2])]
cert = {r["node"]: r for r in recs if r.get("certified") and r.get("cake_lpr") == "s VERIFIED UNSAT"}
split = {r["node"] for r in recs if r.get("split")}
solved = collections.defaultdict(list)
for r in recs:
    if "status" in r: solved[r["node"]].append(r)
bad = [r for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")]
sat = [r for r in recs if r.get("status") == "SATISFIABLE"]
def walk(n, acc):
    d = len(parse_layers(n)); acc["nodes"].add(n)
    for r in solved.get(n, []):
        acc["solve"] += r.get("solve_s", 0); acc["check"] += r.get("check_s", 0) or 0
    if n in cert: acc["cert"][d] += 1; return True
    if n in split:
        acc["split"][d] += 1
        return all([walk(layers_name(c), acc) for c in tree_children(11, 7, parse_layers(n))])
    if n in solved: acc["timeout_open"][d] += 1
    else: acc["untried"][d] += 1
    return False
tot = {k: collections.Counter() for k in ("cert", "split", "timeout_open", "untried")}
ts = tc = 0; nclosed = 0
print("| idx | root | closed | certified by depth | splits by depth | open (tried, not yet split) | untried | solve s | check s |")
print("|---|---|---|---|---|---|---|---|---|")
for line in open(sys.argv[2]):
    i, r = line.split()
    acc = {"nodes": set(), "solve": 0.0, "check": 0.0, **{k: collections.Counter() for k in tot}}
    ok = walk(r, acc); nclosed += ok
    if not (acc["cert"] or acc["split"] or acc["timeout_open"]): status = "not started"
    else: status = "CLOSED" if ok else "open"
    for k in tot: tot[k].update(acc[k])
    ts += acc["solve"]; tc += acc["check"]
    f = lambda c: ", ".join(f"d{d}:{c[d]}" for d in sorted(c)) or "-"
    print(f"| {i} | {r} | {status} | {f(acc['cert'])} | {f(acc['split'])} | {f(acc['timeout_open'])} | {f(acc['untried'])} | {acc['solve']:.0f} | {acc['check']:.0f} |")
print(f"\nroots fully closed: {nclosed} of {len(roots)}; total solve {ts:.0f} s, check {tc:.0f} s")
print("\n| depth | certified | split | open (tried) | untried children |\n|---|---|---|---|---|")
for d in sorted(set().union(*tot.values())):
    print(f"| {d} | {tot['cert'][d]} | {tot['split'][d]} | {tot['timeout_open'][d]} | {tot['untried'][d]} |")
print(f"\nSAT records: {len(sat)}; UNSAT-but-not-certified records: {len(bad)}")
