#!/usr/bin/env python3
"""Summarise out.jsonl per node and level (C3SIG2 step 4). usage: summ.py out.jsonl nodes.tsv"""
import json, sys
recs = [json.loads(l) for l in open(sys.argv[1])]
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[2])][1:]
print("| row | node | stratum | K=3 cert/open | K=3 solve+check s | refined cubes (8 ext. each): cert/recorded/64 | level-2 solve+check s | largest cube s | K=3 cubes closed by refinement | node closed | total s | spent_core_s / open_nodes |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    n = r[1]
    c3 = [x for x in recs if x.get("node") == n and len(x.get("cube", {})) == 3]
    c6 = [x for x in recs if x.get("node") == n and len(x.get("cube", {})) == 6]
    cost = lambda xs: sum(x.get("solve_s", 0) + x.get("check_s", 0) for x in xs)
    big = max((x.get("solve_s", 0) + x.get("check_s", 0) for x in c3 + c6), default=0)
    k3c = sum(1 for x in c3 if x.get("certified"))
    opn = [x["cube"] for x in c3 if not x.get("certified")] + [None] * (8 - len(c3))
    closed_by = 0
    for c in opn:
        if c is None: continue
        ext = [x for x in c6 if all(x["cube"][k] == v for k, v in c.items())]
        if sum(1 for x in ext if x.get("certified")) == 8: closed_by += 1
    k6c = sum(1 for x in c6 if x.get("certified"))
    closed = k3c + closed_by == 8
    tot = cost(c3) + cost(c6)
    print(f"| {r[0]} | {n} | {r[4]} | {k3c}/{8-k3c} | {cost(c3):.0f} | {k6c}/{len(c6)}/{8*len(opn)} | {cost(c6):.0f} | {big:.0f} | {closed_by}/{len(opn)} | {'yes' if closed else 'no'} | {tot:.0f} | {r[6] or '-'} / {r[7] or '-'} |")
