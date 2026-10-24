#!/usr/bin/env python3
"""Per-root and per-depth summary of a close_tree OUT.jsonl for a list of roots.
usage (from C3-S/tools of commit 8dc27c3): python3 summarize_c16.py OUT.jsonl ROOTS.tsv"""
import json, sys
from collections import defaultdict
from hullcase import layers_name, parse_layers, tree_children

out, roots = sys.argv[1], [l.split()[1] for l in open(sys.argv[2]) if l.strip()]
cert, split, recs = set(), set(), defaultdict(list)
for l in open(out):
    r = json.loads(l)
    recs[r["node"]].append(r)
    if r.get("certified"):
        cert.add(r["node"])
    if r.get("split"):
        split.add(r["node"])
depth = lambda n: len(parse_layers(n))
kids = lambda n: [layers_name(c) for c in tree_children(11, 7, parse_layers(n))]
memo = {}
def closed(n):
    if n not in memo:
        memo[n] = n in cert or (n in split and all(closed(c) for c in kids(n)))
    return memo[n]
def sub(n):  # nodes reached in the tree below n (certified/split/open leaves)
    yield n
    if n not in cert and n in split:
        for c in kids(n):
            yield from sub(c)
tot = defaultdict(lambda: [0, 0, 0])
print("root\tclosed\tcertified_by_depth\tsplits\topen_leaves\tsolve_s\tcheck_s")
nclosed = 0
for rt in roots:
    cd, ns, no, ts, tc = defaultdict(int), 0, 0, 0.0, 0.0
    for n in sub(rt):
        for r in recs.get(n, []):
            ts += r.get("solve_s", 0) or 0; tc += r.get("check_s", 0) or 0
        d = depth(n)
        if n in cert:
            cd[d] += 1; tot[d][0] += 1
        elif n in split:
            ns += 1; tot[d][1] += 1
        else:
            no += 1; tot[d][2] += 1
    c = closed(rt); nclosed += c
    print(f"{rt}\t{'closed' if c else 'open'}\t{dict(sorted(cd.items()))}\t{ns}\t{no}\t{ts:.0f}\t{tc:.0f}")
print(f"\nroots closed: {nclosed}/{len(roots)}")
print("depth\tcertified\tsplit\topen(leaf not certified, incl. never started)")
for d in sorted(tot):
    print(f"{d}\t{tot[d][0]}\t{tot[d][1]}\t{tot[d][2]}")
