#!/usr/bin/env python3
"""Summarize leaves.jsonl of shard_driver.py.

usage: summarize.py <cubes.icnf> <shard> <nshards> <leaves.jsonl>

A cube is CLOSED iff cadical said UNSAT and lrat-check VERIFIED it, or it was split, its gap
formula (CNF + cube + negations of all children) is UNSAT with lrat-check VERIFIED, and every
child is CLOSED.  Weights: a top cube has weight 1; a child of a split node at local depth d
has weight 2^-d relative to that node (march_cu subcubes are a binary tree).
"""
import sys, json
from fractions import Fraction
cubes, shard, nsh, leaves = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
top = []
for i, line in enumerate(open(cubes)):
    if i % nsh == shard: top.append([int(x) for x in line.split()[1:-1]])
rec = {}
for line in open(leaves):
    if line.strip():
        r = json.loads(line); rec[(r["kind"], tuple(r["cube"]))] = r
cnt = {"leaf_unsat_verified": 0, "leaf_unsat_check_failed": 0, "sat": 0, "open_unsolved": 0,
       "split_nodes": 0, "gaps_verified": 0, "gaps_open": 0}
solve_s = 0.0
def visit(c):
    """returns (closed?, closed weight fraction of c)"""
    global solve_s
    r = rec.get(("cube", tuple(c)))
    if r is None: cnt["open_unsolved"] += 1; return False, Fraction(0)
    solve_s += r["solve_s"]
    if r["status"] == "SATISFIABLE": cnt["sat"] += 1; return False, Fraction(0)
    if r["status"] == "UNSATISFIABLE":
        if r.get("lrat_check") == "VERIFIED": cnt["leaf_unsat_verified"] += 1; return True, Fraction(1)
        cnt["leaf_unsat_check_failed"] += 1; return False, Fraction(0)
    sp = rec.get(("split", tuple(c)))
    if sp is None: cnt["open_unsolved"] += 1; return False, Fraction(0)
    cnt["split_nodes"] += 1
    g = rec.get(("gap", tuple(c)))
    gok = g is not None and g["status"] == "UNSATISFIABLE" and g.get("lrat_check") == "VERIFIED"
    if g is not None: solve_s += g["solve_s"]
    cnt["gaps_verified" if gok else "gaps_open"] += 1
    ok, w = gok, Fraction(0)
    ch = sp["children"]
    for x in ch:
        cok, cw = visit(x)
        ok = ok and cok; w += cw / 2 ** (len(x) - len(c))
    if not ch and gok: w = Fraction(1)
    return ok, (Fraction(1) if ok else w)
per = []
tw = Fraction(0)
for c in top:
    ok, w = visit(c); per.append({"cube": c, "closed": ok, "closed_weight": float(w)}); tw += w
out = {"shard": shard, "nshards": nsh, "top_cubes": len(top),
       "top_cubes_closed": sum(p["closed"] for p in per), "counts": cnt,
       "closed_weight_of_shard": float(tw / len(top)), "cadical_seconds": round(solve_s),
       "shard_closed": all(p["closed"] for p in per), "per_top_cube": per}
print(json.dumps(out, indent=1))
