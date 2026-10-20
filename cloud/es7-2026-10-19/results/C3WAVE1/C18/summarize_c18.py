#!/usr/bin/env python3
"""Per-root and per-depth summary of out.jsonl (C18).  Run with the C3-S tools dir on sys.path."""
import json, sys, collections
sys.path.insert(0, "/opt/c3s/cloud/es7-2026-10-19/results/C3a"); sys.path.insert(0, "/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools")
from hullcase import tree_children, parse_layers, layers_name
out, roots = sys.argv[1], [l.split()[1] for l in open(sys.argv[2]) if len(l.split()) == 2]
recs = [json.loads(l) for l in open(out)]
cert, split, tried = {}, set(), {}
for r in recs:
    if r.get("certified"): cert[r["node"]] = r
    if r.get("split"): split.add(r["node"])
    if "status" in r: tried.setdefault(r["node"], []).append(r)
memo = {}
def closed(n):
    if n not in memo:
        memo[n] = n in cert or (n in split and all(closed(layers_name(c)) for c in tree_children(11, 7, parse_layers(n))))
    return memo[n]
def sub(n):
    yield n
    if n in split:
        for c in tree_children(11, 7, parse_layers(n)): yield from sub(layers_name(c))
dep = lambda n: len(parse_layers(n))
tot = collections.defaultdict(lambda: [0, 0, 0])
print("root\tstatus\tcertified_by_depth\tsplits\tsolve_s\tcheck_s\topen_leaves")
for R in roots:
    if R not in tried and R not in split and R not in cert: continue
    cd, ns, so, ch, op = collections.Counter(), 0, 0.0, 0.0, 0
    for n in sub(R):
        for t in tried.get(n, []): so += t.get("solve_s", 0); ch += t.get("check_s", 0) or 0
        d = dep(n)
        if n in cert: cd[d] += 1; tot[d][0] += 1
        elif n in split: ns += 1; tot[d][1] += 1
        else: op += 1; tot[d][2] += 1
    print(f"{R}\t{'CLOSED' if closed(R) else 'open'}\t{dict(sorted(cd.items()))}\t{ns}\t{so:.0f}\t{ch:.0f}\t{op}")
print("\ndepth\tcertified\tsplit\topen")
for d in sorted(tot): print(f"{d}\t{tot[d][0]}\t{tot[d][1]}\t{tot[d][2]}")
print("\nSAT records:", [r["node"] for r in recs if r.get("status") == "SATISFIABLE"])
print("UNSAT not certified:", [r["node"] for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")])
