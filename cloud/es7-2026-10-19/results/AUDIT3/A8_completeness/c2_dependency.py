#!/usr/bin/env python3
"""Completeness review: which central-34 records does the closure depend on, and which of them had any chance of
being re-verified by the random re-solve sample (C2FINAL/sample) or the pilot re-solve (C2FINAL/pilot)?

Reads only small record files (JSONL/TSV) under RESULTS. A record counts as certified only with status
UNSATISFIABLE, lrat-check 'c VERIFIED' and cake_lpr 's VERIFIED UNSAT' (CNF hashes were checked by A5/C2FINAL).
usage: c2_dependency.py RESULTS_DIR"""
import csv, glob, itertools, json, os, sys
from collections import defaultdict, Counter

RES = sys.argv[1]
T = 17
recs = []  # (source, unit, certified, solve_s, proof_bytes, lrat_s, cake_s, cnf_sha)
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")), delimiter="\t"):
    c = r["status"] == "UNSATISFIABLE" and r["lrat_check"] == "c VERIFIED" and r["cake_lpr"] == "s VERIFIED UNSAT"
    recs.append(("C2C34/pilot", r["unit"], c, r["solve_s"], r["proof_bytes"], r["lrat_check_s"], r["cake_s"], r["cnf_sha256"]))
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for line in open(f):
        if line.strip():
            r = json.loads(line)
            c = (r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
                 and r.get("cake_lpr") == "s VERIFIED UNSAT")
            recs.append((src, r["unit"], c, r.get("solve_s"), r.get("proof_bytes"), r.get("lrat_check_s"),
                         r.get("cake_s"), r.get("cnf_sha256", "")))
reverified = {}
for name in ("pilot/out.jsonl", "sample/out.jsonl", "sample/extra_out.jsonl"):
    p = os.path.join(RES, "C2FINAL", name)
    for line in open(p):
        if line.strip():
            r = json.loads(line)
            ok = r.get("certified") is True or (r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT")
            if ok:
                reverified[r["unit"]] = name

cert = defaultdict(set)  # unit -> set of sources with a certified record
for src, unit, c, *_ in recs:
    if c and "/" not in unit:
        cert[unit].add(src)
print("records:", len(recs), " certified units:", len(cert), " re-verified (pilot+sample+extra):", len(reverified))
is_local = lambda s: "/LOCAL" in s
is_pilot = lambda s: s == "C2C34/pilot"

# covers
print("\n== covers")
for a in range(1, 9):
    u = f"P{a}_cover"
    rows = [(s, sv, pb, lc, ck) for s, un, c, sv, pb, lc, ck, h in recs if un == u]
    print(u, "certified sources:", sorted(cert.get(u, [])), " re-verified:", u in reverified, " rows:", rows)

# orbits
print("\n== orbits")
lane_load = Counter()      # lane -> number of orbits whose ONLY certified support is from that lane
lane_any = Counter()       # lane -> number of certified units with a record from that lane (used by closure)
lane_reverified = Counter()
dep_class = Counter()
only_local_orbits = []
only_pilot_orbits = []
orbits_with_reverified = Counter()
both_members = Counter()
for a in range(1, 9):
    inner = [o for o in range(1, T) if o != a]
    subs = []
    for h in (2, 3):
        for V in itertools.combinations(inner, h):
            subs.append(V)
    seen = set()
    for V in subs:
        n = f"P{a}_" + "-".join(map(str, V))
        W = tuple(sorted((a - i) % T for i in V))
        m = f"P{a}_" + "-".join(map(str, W))
        key = frozenset((n, m))
        if key in seen:
            continue
        seen.add(key)
        members = sorted(key)
        cm = [x for x in members if x in cert]
        if len(cm) == 2:
            both_members[a] += 1
        if not cm:
            print("OPEN ORBIT", a, members)
            continue
        srcs = set().union(*(cert[x] for x in cm))
        if any(x in reverified for x in cm):
            orbits_with_reverified[a] += 1
        if all(is_local(s) for s in srcs):
            only_local_orbits.append((a, members, sorted(srcs)))
            dep_class["only LOCAL"] += 1
        elif all(is_pilot(s) for s in srcs):
            only_pilot_orbits.append((a, members, sorted(srcs)))
            dep_class["only pilot (C2C34 p8_units)"] += 1
        elif all(is_local(s) or is_pilot(s) for s in srcs):
            dep_class["only LOCAL or pilot"] += 1
        else:
            dep_class["has a cloud record"] += 1
        if len(srcs) == 1:
            lane_load[next(iter(srcs))] += 1
for u, ss in cert.items():
    for s in ss:
        lane_any[s] += 1
        if u in reverified:
            lane_reverified[s] += 1
print("orbit dependency classes:", dict(dep_class))
print("orbits with both members certified per case:", dict(both_members))
print("orbits with a re-verified member per case:", dict(orbits_with_reverified),
      " total", sum(orbits_with_reverified.values()), "of", 8 * 287)
print("orbits resting only on LOCAL records:", len(only_local_orbits))
for x in only_local_orbits:
    print("   ", x)
print("orbits resting only on the C2C34 pilot table:", len(only_pilot_orbits))
lanes = sorted(lane_any)
zero = [s for s in lanes if lane_reverified[s] == 0]
print("\n== lanes: %d lanes with certified units; %d of them have no re-verified unit" % (len(lanes), len(zero)))
print("   load-bearing orbits (single-lane support) on lanes with no re-verified unit:",
      sum(lane_load[s] for s in zero), "of", sum(lane_load.values()))
print("   certified units on lanes with no re-verified unit:", sum(lane_any[s] for s in zero))
