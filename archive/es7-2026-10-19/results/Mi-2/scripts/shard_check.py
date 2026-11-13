#!/usr/bin/env python3
"""Coverage check of a shard run.

usage: shard_check.py <cubes.icnf> <leaves.jsonl> [shard=2]

For every shard root cube (line i, i % 4 == shard): the node is closed if it has a leaf record
with status UNSATISFIABLE and lrat VERIFIED, or a split record whose children form a complete
binary partition (check_tree-style `covers`) and every child node (parent + child literals) is
closed.  Prints per-root status and totals.
"""
import sys, json
sys.setrecursionlimit(100000)
cubesf, leavesf = sys.argv[1], sys.argv[2]
SHARD = int(sys.argv[3]) if len(sys.argv) > 3 else 2
lines = [l.split() for l in open(cubesf)]
roots = [(i, [int(x) for x in t[1:-1]]) for i, t in enumerate(lines) if i % 4 == SHARD]
leaf, split = {}, {}
for l in open(leavesf):
    r = json.loads(l)
    (leaf if r["kind"] == "leaf" else split)[tuple(r["cube"])] = r

def covers(cubes, d):
    if any(len(c) == d for c in cubes): return True
    vs = set(abs(c[d]) for c in cubes)
    if len(vs) != 1: return False
    pos = [c for c in cubes if c[d] > 0]; neg = [c for c in cubes if c[d] < 0]
    return bool(pos) and bool(neg) and covers(pos, d + 1) and covers(neg, d + 1)

tot = {"leaves_unsat_verified": 0, "leaves_unsat_unverified": 0, "leaves_sat": 0, "open": 0,
       "splits": 0, "split_partition_ok": 0, "gap_checks_verified": 0}
def node(c):
    k = tuple(c)
    if k in leaf:
        r = leaf[k]
        if r["status"] == "UNSATISFIABLE" and r["lrat"] == "VERIFIED":
            tot["leaves_unsat_verified"] += 1; return "closed"
        if r["status"] == "UNSATISFIABLE": tot["leaves_unsat_unverified"] += 1; return "unsat-unverified"
        if r["status"] == "SATISFIABLE": tot["leaves_sat"] += 1; return "SAT"
    if k in split:
        s = split[k]; tot["splits"] += 1
        ok = covers([list(x) for x in s["children"]], 0)
        tot["split_partition_ok"] += ok
        g = s.get("gap_check") or {}
        tot["gap_checks_verified"] += g.get("status") == "UNSATISFIABLE" and g.get("lrat") == "VERIFIED"
        res = [node(c + ch) for ch in s["children"]]
        if "SAT" in res: return "SAT"
        if ok and all(x == "closed" for x in res): return "closed"
        return "open"
    tot["open"] += 1; return "open"
per = {i: node(c) for i, c in roots}
out = {"shard": SHARD, "roots": len(roots),
       "roots_closed": sum(v == "closed" for v in per.values()),
       "roots_open": sorted(i for i, v in per.items() if v == "open"),
       "roots_sat": sorted(i for i, v in per.items() if v == "SAT"),
       "roots_unsat_unverified": sorted(i for i, v in per.items() if v == "unsat-unverified"), **tot}
print(json.dumps(out))
