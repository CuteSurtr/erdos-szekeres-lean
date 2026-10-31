#!/usr/bin/env python3
"""Progress of the parallelogram cases P1..P8 of the central 34-point formula from all certified records: the P8 pilot
(results/C2C34/logs/p8_units.tsv), the C2P and C2P2 machines (results/C2P*/M*/out.jsonl) and local runs
(results/C2P*/LOCAL*/out.jsonl). A unit counts as certified when both lrat-check and cake_lpr accepted its proof.
A certified subcase closes its reflection orbit (orbits/P<a>.tsv), so a certified partner counts for its representative.
usage: summary.py RESULTS_DIR   (prints a table per case and the open orbit representatives)"""
import collections, glob, json, os, sys
R = sys.argv[1]
cert, tried = set(), collections.defaultdict(list)
for l in list(open(f"{R}/C2C34/logs/p8_units.tsv"))[1:]:
    f = l.rstrip("\n").split("\t")
    tried[f[0]].append(f[3])
    if f[9] == "c VERIFIED" and f[11] == "s VERIFIED UNSAT": cert.add(f[0])
for p in sorted(glob.glob(f"{R}/C2P*/M*/out.jsonl") + glob.glob(f"{R}/C2P*/LOCAL*/out.jsonl")):
    for l in open(p):
        if not l.strip(): continue
        r = json.loads(l); tried[r["unit"]].append(r["status"])
        if r.get("certified"): cert.add(r["unit"])
rep = {}
for a in range(1, 9):
    for l in list(open(f"{R}/C2P/orbits/P{a}.tsv"))[1:]:
        sub, r = l.rstrip("\n").split("\t")[:2]; rep[sub] = r.strip()
crep = {rep[u] for u in cert if u in rep}
trep = collections.defaultdict(list)
for u, s in tried.items():
    if u in rep: trep[rep[u]] += s
print("case  cover  reps certified/287 (Q /56, H /231)  no answer yet (not certified)")
tot = 0
for a in range(1, 9):
    reps = sorted({l.split("\t")[1].strip() for l in list(open(f"{R}/C2P/orbits/P{a}.tsv"))[1:]})
    q = [n for n in reps if n.count("-") == 1]; h = [n for n in reps if n.count("-") == 2]
    cq = sum(n in crep for n in q); ch = sum(n in crep for n in h); tot += cq + ch
    cov = "yes" if f"P{a}_cover" in cert else "no"
    unk = sorted(n for n in reps if n not in crep and any(s != "UNSATISFIABLE" for s in trep.get(n, [])))
    print(f"P{a}    {cov:5}  {cq + ch:3d} ({cq:2d} Q, {ch:3d} H)                  {len(unk)}: {' '.join(unk[:8])}{' ...' if len(unk) > 8 else ''}")
l3 = sorted(u for u in cert if "/" in u and not u.endswith("/cover"))
l3c = sorted(u for u in cert if u.endswith("/cover"))
print(f"total certified representatives: {tot} of {8 * 287}; covers: {sum(f'P{a}_cover' in cert for a in range(1, 9))} of 8;"
      f" third-layer units certified: {len(l3)}, third-layer covers: {len(l3c)}")
