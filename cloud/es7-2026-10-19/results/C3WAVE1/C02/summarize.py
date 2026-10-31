#!/usr/bin/env python3
"""Per-root and per-depth summary of a close_tree.py OUT.jsonl.
usage (from the C3-S tools dir at 8dc27c3): summarize.py OUT.jsonl ROOTS.txt"""
import json, sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "..", "..", "C3a")); sys.path.insert(0, os.getcwd())
from hullcase import tree_children, layers_name, parse_layers
from collections import defaultdict
recs = [json.loads(l) for l in open(sys.argv[1])]
roots = [l.strip() for l in open(sys.argv[2]) if l.strip()]
cert = {r["node"]: r for r in recs if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"}
split = {r["node"] for r in recs if r.get("split")}
solved = defaultdict(list)
for r in recs:
    if "status" in r:
        solved[r["node"]].append(r)
bad = [r for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")]
sat = [r for r in recs if r.get("status") == "SATISFIABLE"]
D = lambda n: len(parse_layers(n))
tot = defaultdict(lambda: [0, 0, 0])
rows = []
for root in roots:
    st = {"cert": defaultdict(int), "split": defaultdict(int), "open": defaultdict(int), "solve": 0.0, "check": 0.0}
    def walk(n):
        for r in solved.get(n, []):
            st["solve"] += r.get("solve_s", 0); st["check"] += r.get("check_s", 0) or 0
        d = D(n)
        if n in cert:
            st["cert"][d] += 1; return True
        if n in split:
            st["split"][d] += 1
            ok = True
            for c in tree_children(11, 7, parse_layers(n)):
                ok = walk(layers_name(c)) and ok
            return ok
        st["open"][d] += 1; return False
    closed = walk(root)
    for k, i in (("cert", 0), ("split", 1), ("open", 2)):
        for d, v in st[k].items():
            tot[d][i] += v
    rows.append((root, closed, st))
print("| root | status | certified by depth | splits | open leaves | solve s | check s |")
print("|---|---|---|---|---|---|---|")
for root, closed, st in rows:
    f = lambda m: ", ".join(f"d{d}:{v}" for d, v in sorted(m.items())) or "-"
    print(f"| {root} | {'closed' if closed else 'open'} | {f(st['cert'])} | {sum(st['split'].values())} | {f(st['open'])} | {st['solve']:.0f} | {st['check']:.0f} |")
print()
print("| depth | certified | split | open |"); print("|---|---|---|---|")
for d in sorted(tot):
    print(f"| {d} | {tot[d][0]} | {tot[d][1]} | {tot[d][2]} |")
print()
print(f"roots closed: {sum(1 for r in rows if r[1])} / {len(rows)}; certified nodes: {len(cert)}; SAT records: {len(sat)}; UNSAT-not-certified records: {[r['node'] for r in bad]}")
