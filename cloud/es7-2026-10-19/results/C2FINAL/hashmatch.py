#!/usr/bin/env python3
"""Rebuild the CNF of every central-34 unit record and compare its SHA-256 with the recorded cnf_sha256.

All lanes (C2C34/hlane.sh, C2C34/p8/solver.sh, C2P/tools/lane.py) build a unit CNF as: the base CNF with the header
clause count raised by n, then n extra clauses appended ("l1 l2 ... 0\n"). So the SHA-256 state after header + base
body is computed once per n and copied per unit.
- hexagonal hull cases (C2C34/logs/hex_cases.tsv): extra = hull cube literals as units (C2C34/cubes.txt)
- subcase units: extra = subcase cube literals as units (C2P/cubes/<case>_cubes.txt)
- <case>_cover (lane.py): hull cube units + one clause per subcase negating its non-hull literals
usage: hashmatch.py BASE_CNF RESULTS_DIR [OUT_JSON]"""
import csv, glob, hashlib, json, os, sys

BASE, RES = sys.argv[1], sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else None
data = open(BASE, "rb").read()
h0 = data.index(b"p cnf")
assert h0 == 0 or data[h0 - 1:h0] == b"\n"
h1 = data.index(b"\n", h0) + 1
_, _, NV, NC = data[h0:h1].split()
NV, NC = int(NV), int(NC)
states = {}


def state(n):
    if n not in states:
        h = hashlib.sha256(); h.update(data[:h0]); h.update(f"p cnf {NV} {NC + n}\n".encode()); h.update(data[h1:])
        states[n] = h
    return states[n].copy()


def digest(clauses):
    h = state(len(clauses))
    h.update("".join(" ".join(map(str, c)) + " 0\n" for c in clauses).encode())
    return h.hexdigest()


hull = {l.split()[0]: [int(x) for x in l.split()[1:]] for l in open(os.path.join(RES, "C2C34", "cubes.txt")) if l.strip()}
cubes, order = {}, {}
for a in range(1, 9):
    order[f"P{a}"] = []
    for l in open(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt")):
        if l.strip():
            name, *lits = l.split(); cubes[name] = [int(x) for x in lits]; order[f"P{a}"].append(name)


def extra(unit, case):
    if unit in hull:
        return [[l] for l in hull[unit]]
    if unit.endswith("_cover"):
        hs = set(hull[case]); cls = [[l] for l in hull[case]]
        for n in order[case]:
            assert hs <= set(cubes[n]); cls.append([-x for x in cubes[n] if x not in hs])
        return cls
    return [[l] for l in cubes[unit]]


rows = []
with open(os.path.join(RES, "C2C34", "logs", "hex_cases.tsv")) as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        rows.append(("C2C34/hex", r["case"], r["case"], r["cnf_sha256"], r["status"]))
with open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")) as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        rows.append(("C2C34/pilot", r["unit"], "P8", r["cnf_sha256"], r["status"]))
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for line in open(f):
        if line.strip():
            r = json.loads(line); rows.append((src, r["unit"], r["case"], r.get("cnf_sha256", ""), r["status"]))

res = {"match": 0, "mismatch": [], "no_hash": [], "skipped_subunits": 0, "distinct_n": 0}
for src, unit, case, rec, st in rows:
    if "/" in unit:  # third-layer pieces (lane3.py): not used to close any orbit
        res["skipped_subunits"] += 1; continue
    if not rec:
        res["no_hash"].append(f"{src} {unit} {st}"); continue
    got = digest(extra(unit, case))
    if got == rec:
        res["match"] += 1
    else:
        res["mismatch"].append(f"{src} {unit} {st} rec={rec[:12]} got={got[:12]}")
res["distinct_n"] = len(states)
# hashes of the CNFs that have no recorded hash, for the record
res["computed_for_no_hash"] = {u.split()[1]: digest(extra(u.split()[1], "P8")) for u in res["no_hash"]}
print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 30 else v[:30] + [f"... {len(v)} total"])
                  for k, v in res.items()}, indent=1))
if OUT:
    json.dump(res, open(OUT, "w"), indent=1)
