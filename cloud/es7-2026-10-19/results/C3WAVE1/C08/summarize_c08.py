#!/usr/bin/env python3
"""Per-root and per-depth summary of C08's out.jsonl.
usage: summarize_c08.py OUT.jsonl ROOTS.txt  (run with the 8dc27c3 C3-S tools on sys.path)"""
import json, sys, collections, functools
T = "/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools"
sys.path.insert(0, T + "/../../C3a"); sys.path.insert(0, T)
from hullcase import parse_layers, layers_name, tree_children

recs = [json.loads(l) for l in open(sys.argv[1])]
cert, split, solved = set(), set(), {}
rejected = []
for r in recs:
    if r.get("certified"): cert.add(r["node"])
    if r.get("split"): split.add(r["node"])
    if "status" in r:
        solved.setdefault(r["node"], []).append(r)
        if r["status"] == "UNSATISFIABLE" and not r.get("certified"): rejected.append(r["node"])
        if r["status"] == "SATISFIABLE": print("SAT", r["node"])
kids = lambda n: [layers_name(c) for c in tree_children(11, 7, parse_layers(n))]

@functools.lru_cache(None)
def closed(n):
    return n in cert or (n in split and all(closed(c) for c in kids(n)))

def subtree(n):
    out = [n]
    if n in split and n not in cert:
        for c in kids(n): out += subtree(c)
    return out

roots = [l.split("\t")[1].strip() for l in open(sys.argv[2]) if l.strip()]
tot = collections.defaultdict(lambda: collections.Counter())
print("| idx | root | status | certified by depth | splits | open | solve s | check s |")
print("|---|---|---|---|---|---|---|---|")
for line in open(sys.argv[2]):
    if not line.strip(): continue
    idx, root = line.split("\t"); root = root.strip()
    if root not in solved and root not in split:
        print(f"| {idx} | `{root}` | not started | | | | | |"); continue
    nodes = subtree(root)
    cd = collections.Counter(); ns = no = 0; ss = cs = 0.0
    for n in nodes:
        d = len(parse_layers(n))
        for r in solved.get(n, []):
            ss += r.get("solve_s", 0); cs += r.get("check_s", 0) or 0
        if n in cert: cd[d] += 1; tot[d]["certified"] += 1
        elif n in split: ns += 1; tot[d]["split"] += 1
        else: no += 1; tot[d]["open"] += 1
    st = "closed" if closed(root) else "open"
    print(f"| {idx} | `{root}` | {st} | {', '.join(f'd{d}: {c}' for d, c in sorted(cd.items()))} | {ns} | {no} | {ss:.0f} | {cs:.0f} |")
print()
print("| depth | certified | split | open |"); print("|---|---|---|---|")
for d in sorted(tot): print(f"| {d} | {tot[d]['certified']} | {tot[d]['split']} | {tot[d]['open']} |")
print()
print("closed roots:", sum(closed(r) for r in roots), "of", len(roots))
print("UNSAT records not certified (driver PROOF NOT ACCEPTED):", rejected, "; of these never certified later:", [n for n in rejected if n not in cert])
print("total solve s (all records):", round(sum(r.get('solve_s', 0) for v in solved.values() for r in v)),
      "check s:", round(sum(r.get('check_s', 0) or 0 for v in solved.values() for r in v)))
