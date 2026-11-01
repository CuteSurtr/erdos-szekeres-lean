#!/usr/bin/env python3
"""Per-root and per-depth summary of a close_tree.py OUT.jsonl.
usage: summarize_c09.py C3S_TOOLS_DIR ROOTS.txt OUT.jsonl
A node is closed iff it is certified (both checkers), or it was split and every child is closed.
A node reachable from a root through split records that is neither certified nor split is open."""
import collections
import json
import sys

sys.path.insert(0, sys.argv[1] + "/../../C3a")
sys.path.insert(0, sys.argv[1])
from hullcase import layers_name, parse_layers, tree_children  # noqa: E402

roots = [l.split()[1] for l in open(sys.argv[2]) if l.strip()]
cert, split, solved = {}, set(), collections.defaultdict(list)
for l in open(sys.argv[3]):
    r = json.loads(l)
    n = layers_name(parse_layers(r["node"]))
    if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
        cert[n] = r
    if r.get("split"):
        split.add(n)
    if "status" in r:
        solved[n].append(r)


def walk(n, acc):
    d = len(parse_layers(n))
    for r in solved.get(n, []):
        acc["solve_s"] += r.get("solve_s", 0)
        acc["check_s"] += r.get("check_s", 0)
        acc["solve_runs"] += 1
        if r["status"] == "SATISFIABLE":
            acc["sat"].append(n)
        if r["status"] == "UNSATISFIABLE" and not r.get("certified"):
            acc["rejected"].append(n)
    if n in cert:
        acc["cert"][d] += 1
        return True
    if n in split:
        acc["split"][d] += 1
        ok = True
        for c in tree_children(11, 7, parse_layers(n)):
            ok &= walk(layers_name(c), acc)
        return ok
    acc["open"][d] += 1
    return False


tot = {k: collections.Counter() for k in ("cert", "split", "open")}
rows = []
for r in roots:
    acc = {"cert": collections.Counter(), "split": collections.Counter(), "open": collections.Counter(),
           "solve_s": 0.0, "check_s": 0.0, "solve_runs": 0, "sat": [], "rejected": []}
    closed = walk(r, acc)
    for k in tot:
        tot[k].update(acc[k])
    rows.append((r, closed, acc))

fmt = lambda c: ", ".join(f"d{d}:{c[d]}" for d in sorted(c)) or "-"
print("| root | status | certified by depth | splits by depth | open by depth | solve s | check s | SAT | rejected |")
print("|---|---|---|---|---|---|---|---|---|")
for r, closed, a in rows:
    st = "closed" if closed else ("open" if a["solve_runs"] or a["split"] else "not started")
    print(f"| {r} | {st} | {fmt(a['cert'])} | {fmt(a['split'])} | {fmt(a['open'])} | {a['solve_s']:.0f} | {a['check_s']:.0f} "
          f"| {len(a['sat'])} | {len(a['rejected'])} |")
print()
print(f"roots closed: {sum(c for _, c, _ in rows)} / {len(rows)}")
print()
print("| depth | certified | split | open |")
print("|---|---|---|---|")
for d in sorted(set(tot["cert"]) | set(tot["split"]) | set(tot["open"])):
    print(f"| {d} | {tot['cert'][d]} | {tot['split'][d]} | {tot['open'][d]} |")
