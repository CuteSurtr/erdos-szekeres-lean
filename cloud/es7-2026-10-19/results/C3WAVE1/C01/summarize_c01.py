#!/usr/bin/env python3
"""Per-root and per-depth summary of out.jsonl (run from C3-S/tools at 8dc27c3)."""
import json, sys, os, collections
sys.path.insert(0, os.path.join(os.getcwd(), "..", "..", "C3a")); sys.path.insert(0, os.getcwd())
from hullcase import tree_children, layers_name, parse_layers
D = os.path.dirname(os.path.abspath(__file__))
recs = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, "out.jsonl"))]
cert = {r["node"] for r in recs if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"}
split = {r["node"] for r in recs if r.get("split")}
solved = {}
for r in recs:
    if "status" in r: solved.setdefault(r["node"], []).append(r)
roots = [l.split("\t")[1].strip() for l in open(os.path.join(D, "roots.txt"))]
def dep(n): return len(parse_layers(n))
def walk(n, acc):
    acc["nodes"].add(n)
    if n in cert: return True
    if n in split:
        ok = True
        for c in tree_children(11, 7, parse_layers(n)):
            ok &= walk(layers_name(c), acc)
        return ok
    return False
tot = collections.defaultdict(lambda: collections.Counter())
print("| root | status | certified by depth | splits | open leaves | solve s | check s |")
print("|---|---|---|---|---|---|---|")
for rt in roots:
    acc = {"nodes": set()}
    ok = walk(rt, acc)
    ns = acc["nodes"]
    if not any(n in cert or n in split or n in solved for n in ns): continue
    cbd = collections.Counter(dep(n) for n in ns if n in cert)
    sp = sum(1 for n in ns if n in split)
    op = [n for n in ns if n not in cert and n not in split]
    st = sum(r.get("solve_s", 0) for n in ns for r in solved.get(n, []))
    ck = sum(r.get("check_s", 0) for n in ns for r in solved.get(n, []))
    for n in ns:
        tot[dep(n)]["certified" if n in cert else "split" if n in split else "open"] += 1
    print(f"| {rt} | {'CLOSED' if ok else 'open'} | {dict(sorted(cbd.items()))} | {sp} | {len(op)} | {st:.0f} | {ck:.0f} |")
print("\n| depth | certified | split | open |\n|---|---|---|---|")
for d in sorted(tot): print(f"| {d} | {tot[d]['certified']} | {tot[d]['split']} | {tot[d]['open']} |")
bad = [r["node"] for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")]
print("UNSAT records not accepted:", bad, "; of these later certified:", [n for n in bad if n in cert])
bad = [n for n in bad if n not in cert]
sat = [r["node"] for r in recs if r.get("status") == "SATISFIABLE"]
print("\nproof rejections:", bad, " SAT:", sat)
