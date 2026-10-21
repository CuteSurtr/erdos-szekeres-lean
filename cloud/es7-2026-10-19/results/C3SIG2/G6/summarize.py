#!/usr/bin/env python3
"""Summarize C3SIG2 out.jsonl: per node, K=3 and refined (6-bit) cubes certified / open, solve+check s, largest cube, closed?"""
import json, sys
recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
nodes = [l.split("\t") for l in open(sys.argv[2]).read().splitlines()[1:]]
print("row\tnode\tstratum\tk3_cert\tk3_open\tk6_run\tk6_cert\tk6_open\tk6_unrun\tk3_closed_by_refine\tsolve_s\tcheck_s\tmax_cube_s\tmax_cert_cube_s\tclosed\tspent_core_s\topen_nodes")
for row, node, _, _, stratum, status, spent, opn in nodes:
    R = [r for r in recs if r.get("node") == node and "cube" in r]
    k3 = [r for r in R if len(r["cube"]) == 3]; k6 = [r for r in R if len(r["cube"]) == 6]
    if not R:
        print(f"{row}\t{node}\t{stratum}\tnot reached"); continue
    c3 = {tuple(r["cube"].values()) for r in k3 if r.get("certified")}
    open3 = [c for c in ((a, b, d) for a in (0, 1) for b in (0, 1) for d in (0, 1)) if c not in c3]
    closed_by = 0
    for c in open3:
        ch = [r for r in k6 if tuple(r["cube"].values())[:3] == c and r.get("certified")]
        closed_by += len({tuple(r["cube"].values()) for r in ch}) == 8
    k6c = sum(1 for r in k6 if r.get("certified")); k6o = len(k6) - k6c
    sol = sum(r.get("solve_s", 0) for r in R); chk = sum(r.get("check_s", 0) for r in R)
    mx = max(r.get("solve_s", 0) + r.get("check_s", 0) for r in R)
    mc = max([r.get("solve_s", 0) + r.get("check_s", 0) for r in R if r.get("certified")] or [0])
    closed = len(open3) == closed_by
    print(f"{row}\t{node}\t{stratum}\t{len(c3)}\t{len(open3)}\t{len(k6)}\t{k6c}\t{k6o}\t{8*len(open3)-len(k6)}\t{closed_by}/{len(open3)}\t{sol:.1f}\t{chk:.1f}\t{mx:.1f}\t{mc:.1f}\t{'yes' if closed else 'no'}\t{spent}\t{opn}")
