#!/usr/bin/env python3
"""Summarize C07 out.jsonl: per root closed/open, per-depth counts. usage: summarize.py OUT.jsonl ROOTS.txt
Run from the C3-S tools dir of 8dc27c3 (imports hullcase)."""
import json, sys, collections
sys.path.insert(0, '../../C3a'); sys.path.insert(0, '.')
from hullcase import parse_layers, layers_name, tree_children
recs = [json.loads(l) for l in open(sys.argv[1])]
roots = [l.strip() for l in open(sys.argv[2]) if l.strip()]
cert, split, tried = set(), set(), {}
for r in recs:
    if r.get("certified"): cert.add(r["node"])
    if r.get("split"): split.add(r["node"])
    if "status" in r: tried.setdefault(r["node"], []).append(r)
memo = {}
def closed(n):
    if n in memo: return memo[n]
    if n in cert: v = True
    elif n in split: v = all(closed(layers_name(c)) for c in tree_children(11, 7, parse_layers(n)))
    else: v = False
    memo[n] = v; return v
def sub(root):
    out, st = [], [root]
    while st:
        n = st.pop(); out.append(n)
        if n in split and n not in cert: st += [layers_name(c) for c in tree_children(11, 7, parse_layers(n))]
    return out
dep = lambda n: len(parse_layers(n))
tot = collections.defaultdict(lambda: collections.Counter())
print("root\tstatus\tcertified_by_depth\tsplits\tsolved_nodes\tsolve_s\tcheck_s")
for rt in roots:
    ns = sub(rt); cb = collections.Counter(); sp = 0; ss = cs = 0.0; nt = 0
    started = rt in tried or rt in split
    for n in ns:
        d = dep(n)
        for r in tried.get(n, []):
            ss += r.get("solve_s", 0); cs += r.get("check_s", 0) or 0; nt += 1
        if n in cert: cb[d] += 1; tot[d]["certified"] += 1
        elif n in split: sp += 1; tot[d]["split"] += 1
        else: tot[d]["open"] += 1
    st = "closed" if closed(rt) else ("open" if started else "not started")
    print(f"{rt}\t{st}\t{dict(sorted(cb.items()))}\t{sp}\t{nt}\t{ss:.0f}\t{cs:.0f}")
print("\ndepth\tcertified\tsplit\topen(leaf, not certified)")
for d in sorted(tot): print(f"{d}\t{tot[d]['certified']}\t{tot[d]['split']}\t{tot[d]['open']}")
print("\nroots closed:", sum(closed(r) for r in roots), "of", len(roots))
print("status counts:", collections.Counter(r["status"] for r in recs if "status" in r))
print("uncertified UNSAT records:", [r["node"] for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")])
