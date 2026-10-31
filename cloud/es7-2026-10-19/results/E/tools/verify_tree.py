#!/usr/bin/env python3
"""Check that the closed and open cubes of a cnc2 run partition the search space.

Cubes are root-to-leaf paths of a binary tree in which every internal node splits on one
variable v into the children (.., -v) and (.., v).  This script rebuilds the tree from
OUTDIR/closed.jsonl and the open cubes in OUTDIR/state.json and checks:
  * no cube is listed twice and no cube is a prefix of another (leaves are disjoint);
  * every internal node has exactly two children, labelled -v and v for one variable v that
    does not already occur on the path (so the two children are complementary);
  * the exact weight sum over all leaves of 2^-depth equals 1.
If all hold, every total assignment extends exactly one leaf, so "all leaves closed" would mean
the CNF is UNSAT (modulo the correctness of each closed-leaf answer).
usage: verify_tree.py OUTDIR
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

out = Path(sys.argv[1])
closed = [tuple(json.loads(l)["cube"]) for l in open(out / "closed.jsonl") if l.strip()]
st = json.loads((out / "state.json").read_text())
opened = [tuple(c) for c, _ in st["open"]]
leaves = closed + opened
errors = []
if len(set(leaves)) != len(leaves):
    errors.append("duplicate leaves")
children = {}
leafset = set(leaves)
for c in leaves:
    for d in range(len(c)):
        pre = c[:d]
        children.setdefault(pre, set()).add(c[d])
        if pre in leafset:
            errors.append(f"leaf {list(pre)} is a prefix of {list(c)}")
for pre, ch in children.items():
    if len(ch) != 2:
        errors.append(f"node {list(pre)} has children {sorted(ch)}")
        continue
    a, b = sorted(ch)
    if a != -b:
        errors.append(f"node {list(pre)} children not complementary {a} {b}")
    if abs(a) in {abs(x) for x in pre}:
        errors.append(f"node {list(pre)} splits on a variable already on its path")
if not leaves:
    errors.append("no leaves")
D = max(len(c) for c in leaves) if leaves else 0
total = sum(1 << (D - len(c)) for c in leaves)
wc = Fraction(sum(1 << (D - len(c)) for c in closed), 1 << D)
res = {"closed_leaves": len(closed), "open_leaves": len(opened), "internal_nodes": len(children),
       "max_depth": D, "weights_sum_to_one": total == (1 << D),
       "closed_weight": f"{wc.numerator}/{wc.denominator}", "closed_weight_float": float(wc),
       "errors": errors[:20], "n_errors": len(errors), "partition_ok": not errors and total == (1 << D)}
print(json.dumps(res))
sys.exit(0 if res["partition_ok"] else 1)
