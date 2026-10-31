#!/usr/bin/env python3
"""Summarise out.jsonl per node: K=3 and refined (6-bit) cubes certified/open, costs, closure."""
import itertools, json, statistics, sys
out, nodes = sys.argv[1], sys.argv[2]
recs = [json.loads(l) for l in open(out)]
rows = [l.rstrip("\n").split("\t") for l in open(nodes)][1:]
print("row\tnode\tstratum\tK3_cert\tK3_open\tK6_run\tK6_cert\tK6_open_of_run\tK6_not_run\tsolve_s\tcheck_s\tmax_cube_s\tclosed\tspent_core_s\topen_nodes")
for row, node, units, h, stratum, status, spent, opn in [r + [""] * (8 - len(r)) for r in rows]:
    rs = [x for x in recs if x.get("node") == node and "cube" in x]
    if not rs:
        print(f"{row}\t{node}\t{stratum}\tnot reached"); continue
    k3 = [x for x in rs if len(x["cube"]) == 3]; k6 = [x for x in rs if len(x["cube"]) == 6]
    c3 = sum(1 for x in k3 if x.get("certified") is True)
    open3 = [tuple(x["cube"].values()) for x in k3 if x.get("certified") is not True] + [None] * (8 - len(k3))
    c6 = sum(1 for x in k6 if x.get("certified") is True)
    need = 8 * (8 - c3)
    solve = sum(x["solve_s"] for x in rs); check = sum(x.get("check_s", 0) for x in rs)
    mx = max(x["solve_s"] + x.get("check_s", 0) for x in rs)
    closed = c3 == 8 or (len(k3) == 8 and c6 == need)
    print(f"{row}\t{node}\t{stratum}\t{c3}\t{8-c3}\t{len(k6)}\t{c6}\t{len(k6)-c6}\t{need-len(k6)}\t{solve:.1f}\t{check:.1f}\t{mx:.1f}\t{closed}\t{spent}\t{opn}")
