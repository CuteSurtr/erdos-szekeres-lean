#!/usr/bin/env python3
"""Closure status of closesgn.py trees. A node is closed if its own refutation was accepted by both checkers, or if
its split's cover proof was accepted by both checkers and every child is closed.  usage: treesum.py TREEDIR..."""
import json, sys
for d in sys.argv[1:]:
    rs = [json.loads(l) for l in open(f"{d}/results.jsonl")]
    node = {}; cover = {}; kids = {}
    for r in rs:
        (node if r["kind"] == "node" else cover)[r["node"]] = r
    names = [l.split()[0] for l in open(f"{d}/tree.cubes")]
    for nm in names:
        if "/" in nm: kids.setdefault(nm.rsplit("/", 1)[0], []).append(nm)
    memo = {}
    def closed(nm):
        if nm in memo: return memo[nm]
        r = node.get(nm); c = cover.get(nm)
        v = bool(r and r.get("closed")) or bool(c and c.get("checked") and all(closed(k) for k in kids.get(nm, [])))
        memo[nm] = v; return v
    roots = [nm for nm in names if nm.rsplit("/", 1)[0] not in names]
    n_nodes = len(node); n_ok = sum(1 for r in node.values() if r.get("closed"))
    n_unk = sum(1 for r in node.values() if r["status"] == "UNKNOWN"); n_sat = sum(1 for r in node.values() if r["status"] == "SATISFIABLE")
    pending = [nm for nm in names if nm not in node]
    print(f"{d}: nodes run {n_nodes}, refuted and checked {n_ok}, split {n_unk}, SAT {n_sat}, covers checked "
          f"{sum(1 for c in cover.values() if c.get('checked'))}/{len(cover)}, not yet run {len(pending)}")
    for rt in roots: print(f"  root {rt}: {'CLOSED' if closed(rt) else 'open'}")
