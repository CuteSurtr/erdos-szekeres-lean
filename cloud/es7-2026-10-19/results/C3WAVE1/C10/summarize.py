#!/usr/bin/env python3
"""Per-root and per-depth summary of a close_tree.py OUT.jsonl. Run from C3-S/tools of 8dc27c3.
usage: summarize.py OUT.jsonl ROOTS.txt"""
import json, sys, os
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "..", "..", "C3a"))
from hullcase import tree_children, parse_layers, layers_name
from collections import defaultdict
recs = [json.loads(l) for l in open(sys.argv[1])]
roots = [l.split()[1] for l in open(sys.argv[2]) if l.strip()]
cert = {r["node"]: r for r in recs if r.get("certified") and r.get("cake_lpr") == "s VERIFIED UNSAT"}
split = {r["node"] for r in recs if r.get("split")}
tried = defaultdict(list)
for r in recs:
    if "status" in r: tried[r["node"]].append(r)
bad = [r for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")]
rechecked = [r for r in bad if r["node"] in cert]
bad = [r for r in bad if r["node"] not in cert]
sat = [r for r in recs if r.get("status") == "SATISFIABLE"]
memo = {}
def walk(n, acc):
    """returns covered?; accumulates per-depth stats"""
    d = len(parse_layers(n))
    if n in cert:
        acc["cert"][d] += 1; acc["solve"] += cert[n]["solve_s"]; acc["check"] += cert[n].get("check_s", 0); return True
    for r in tried.get(n, []): acc["solve"] += r.get("solve_s", 0)
    if n in split:
        acc["split"][d] += 1
        return all([walk(layers_name(c), acc) for c in tree_children(11, 7, parse_layers(n))])
    acc["open"][d] += 1; return False
tot = {k: defaultdict(int) for k in ("cert", "split", "open")}
print("| root | status | certified by depth | splits | open by depth | solve s | check s |\n|---|---|---|---|---|---|---|")
nclosed = 0
for R in roots:
    acc = {"cert": defaultdict(int), "split": defaultdict(int), "open": defaultdict(int), "solve": 0.0, "check": 0.0}
    ok = walk(R, acc); nclosed += ok
    for k in tot:
        for d, v in acc[k].items(): tot[k][d] += v
    f = lambda x: " ".join(f"d{d}:{v}" for d, v in sorted(x.items())) or "-"
    print(f"| {R} | {'CLOSED' if ok else 'open'} | {f(acc['cert'])} | {sum(acc['split'].values())} | {f(acc['open'])} | {acc['solve']:.0f} | {acc['check']:.0f} |")
print(f"\nroots closed: {nclosed}/{len(roots)}\n\n| depth | certified | split | open |\n|---|---|---|---|")
for d in sorted(set(tot['cert']) | set(tot['split']) | set(tot['open'])):
    print(f"| {d} | {tot['cert'][d]} | {tot['split'][d]} | {tot['open'][d]} |")
print(f"\nSAT records: {len(sat)}; UNSAT records not certified: {len(bad)}")
for r in bad: print("  rejected:", r["node"], r.get("lrat_check"), r.get("cake_lpr"))
for r in rechecked: print("  first check failed, later certified:", r["node"], r.get("lrat_check"), r.get("cake_lpr"))
