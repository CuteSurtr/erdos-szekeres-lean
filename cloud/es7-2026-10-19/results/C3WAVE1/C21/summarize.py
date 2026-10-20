#!/usr/bin/env python3
"""Per-root and per-depth summary of out.jsonl (run from the C3-S tools dir of 8dc27c3, or with it on sys.path)."""
import collections, json, sys
sys.path.insert(0, "/opt/c3s/cloud/es7-2026-10-19/results/C3a"); sys.path.insert(0, "/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools")
from hullcase import layers_name, parse_layers, tree_children
out, roots = sys.argv[1], [l.split("\t")[1].strip() for l in open(sys.argv[2])]
recs = [json.loads(l) for l in open(out)]
cert = {r["node"]: r for r in recs if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"}
split = {r["node"] for r in recs if r.get("split")}
tried = collections.defaultdict(list)
for r in recs:
    if "status" in r: tried[r["node"]].append(r)
bad = [r for r in recs if r.get("status") == "UNSATISFIABLE" and not r.get("certified")]
sat = [r for r in recs if r.get("status") == "SATISFIABLE"]
D = lambda n: len(parse_layers(n))
def walk(n, acc):
    """returns covered?; collects stats in acc"""
    if n in cert:
        acc["cert"][D(n)] += 1; acc["solve"] += cert[n]["solve_s"]; acc["check"] += cert[n].get("check_s", 0)
        for r in tried[n]:
            if r is not cert[n]: acc["solve"] += r.get("solve_s", 0)
        return True
    for r in tried[n]: acc["solve"] += r.get("solve_s", 0)
    if n in split:
        acc["split"][D(n)] += 1
        ok = True
        for c in tree_children(11, 7, parse_layers(n)):
            ok &= walk(layers_name(c), acc)
        return ok
    acc["open"][D(n)] += 1
    return False
tot = {k: collections.Counter() for k in ("cert", "split", "open")}
print("| # | root | status | certified by depth | splits | open leaves | solve s | check s |")
print("|---|---|---|---|---|---|---|---|")
nclosed = 0; S = C = 0
for i, r in enumerate(roots):
    acc = {"cert": collections.Counter(), "split": collections.Counter(), "open": collections.Counter(), "solve": 0.0, "check": 0.0}
    started = r in cert or r in split or r in tried
    ok = walk(r, acc)
    st = "closed" if ok else ("open" if started else "not started")
    nclosed += ok; S += acc["solve"]; C += acc["check"]
    if started:
        for k in tot: tot[k].update(acc[k])
    else: nns = locals().get('nns', 0) + 1
    f = lambda c: ", ".join(f"d{d}:{c[d]}" for d in sorted(c)) or "-"
    print(f"| {i} | `{r}` | {st} | {f(acc['cert'])} | {sum(acc['split'].values())} | {sum(acc['open'].values()) if started else '-'} | {acc['solve']:.0f} | {acc['check']:.0f} |")
print(f"\nroots closed: {nclosed}/{len(roots)}; not started: {locals().get('nns', 0)}; total solve {S:.0f} s, check {C:.0f} s (wall per node, summed; 3-4 jobs ran in parallel)\n")
print("| depth | certified | split | open (tried or queued, not closed) |\n|---|---|---|---|")
for d in sorted(set(tot["cert"]) | set(tot["split"]) | set(tot["open"])):
    print(f"| {d} | {tot['cert'][d]} | {tot['split'][d]} | {tot['open'][d]} |")
print(f"\nSAT records: {len(sat)}; UNSAT records not certified: {len(bad)}, of which still uncertified after a re-check: {len([r for r in bad if r['node'] not in cert])}")
for r in bad: print(f"- `{r['node']}`: lrat_check={r.get('lrat_check')!r}, cake_lpr={r.get('cake_lpr')!r}; certified on re-check: {r['node'] in cert}")
