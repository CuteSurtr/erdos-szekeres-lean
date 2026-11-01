#!/usr/bin/env python3
"""Reviewer's own recomputation of every recorded CNF hash.
Builders reproduced (from reading the lane code):
  lane.py / resolve.py : bytes before 'p cnf' line verbatim; header 'p cnf NV NC+n\n'; rest verbatim; then n clauses.
  hlane.sh / solver.sh : awk prints every line, header rewritten as '$1 $2 $3 $4+n'; then 'l 0' per cube literal.
  hullcubes.py cover   : header 'p cnf NV NC+136\n' (comment line dropped), non-empty body lines, negated cubes.
usage: myhash.py BASE RESULTS OUT_JSON"""
import csv, glob, hashlib, json, os, sys
from collections import Counter

BASE, RES, OUTJ = sys.argv[1:4]
raw = open(BASE, "rb").read()
lines_end = raw.split(b"\n")
assert raw.endswith(b"\n")
hi = next(i for i, l in enumerate(lines_end) if l.startswith(b"p cnf"))
pre = b"".join(l + b"\n" for l in lines_end[:hi])
hdr = lines_end[hi].split()
NV, NC = int(hdr[2]), int(hdr[3])
body_off = len(pre) + len(lines_end[hi]) + 1
body = memoryview(raw)[body_off:]
print("pre-header bytes", len(pre), "header", lines_end[hi], "body bytes", len(body))

cache = {}
def prefix(n, keep_pre=True):
    k = (n, keep_pre)
    if k not in cache:
        h = hashlib.sha256()
        if keep_pre: h.update(pre)
        h.update(b"p cnf %d %d\n" % (NV, NC + n)); h.update(body)
        cache[k] = h
    return cache[k].copy()

def H(clauses, keep_pre=True):
    h = prefix(len(clauses), keep_pre)
    for c in clauses:
        h.update((" ".join(str(x) for x in c) + " 0\n").encode())
    return h.hexdigest()

def readcubes(path):
    out = []
    for l in open(path):
        p = l.split()
        if p: out.append((p[0], [int(x) for x in p[1:]]))
    return out

hull_list = readcubes(os.path.join(RES, "C2C34", "cubes.txt"))
hull = dict(hull_list)
sub = {}; sub_order = {}
for a in range(1, 9):
    L = readcubes(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt"))
    sub_order[a] = [n for n, _ in L]
    sub.update(L)

def expected(unit, kind_hint=None):
    if unit in hull:                       # hexagonal hull case (hlane.sh)
        return H([[l] for l in hull[unit]])
    if unit.endswith("_cover"):            # lane.py cover
        a = int(unit[1:].split("_")[0]); hs = set(hull[f"P{a}"])
        cls = [[l] for l in hull[f"P{a}"]]
        for n in sub_order[a]:
            cls.append([-x for x in sub[n] if x not in hs])
        return H(cls)
    return H([[l] for l in sub[unit]])

rows = []
with open(os.path.join(RES, "C2C34", "logs", "hex_cases.tsv")) as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        rows.append(("hex", r["case"], r["cnf_sha256"], r["status"], r))
with open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")) as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        rows.append(("pilot", r["unit"], r["cnf_sha256"], r["status"], r))
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "**", "out.jsonl"), recursive=True)):
    for l in open(f):
        if l.strip():
            r = json.loads(l); rows.append((os.path.relpath(f, RES), r["unit"], r.get("cnf_sha256", ""), r["status"], r))
for l in open(os.path.join(RES, "C2FINAL", "pilot", "out.jsonl")):
    if l.strip():
        r = json.loads(l); rows.append(("C2FINAL/pilot", r["unit"], r["cnf_sha256"], r["status"], r))

res = Counter(); bad = []; nohash = []; skipped = []
extra_mismatch = []
for src, unit, rec, st, r in rows:
    if "/" in unit:
        skipped.append(unit); continue
    if not rec:
        nohash.append((src, unit)); continue
    e = expected(unit)
    if e == rec: res[src.split("/")[0] if src not in ("hex", "pilot") else src] += 1
    else: bad.append((src, unit, rec[:12], e[:12]))
    # extra_clauses field consistency
    if "extra_clauses" in r:
        n = (len(hull[f"P{int(unit[1:].split('_')[0])}"]) + len(sub_order[int(unit[1:].split('_')[0])])) if unit.endswith("_cover") else len(sub[unit])
        if int(r["extra_clauses"]) != n: extra_mismatch.append((src, unit, r["extra_clauses"], n))
    if "cnf_sha256_expected" in r and r["cnf_sha256_expected"] != e:
        bad.append((src, unit, "expected-field", r["cnf_sha256_expected"][:12], e[:12]))

# hash of the pilot cover as mkunits.py wrote it (sorted names), for information
a = 8; hs = set(hull["P8"])
names_sorted = sorted(sub_order[8])
pilot_cover = H([[l] for l in hull["P8"]] + [[-x for x in sub[n] if x not in hs] for n in names_sorted])
# hull cover (hullcubes.py): no comment line, header +136
hullcover = H([[-l for l in lits] for _, lits in hull_list], keep_pre=False)
out = {"matches_by_source": dict(res), "total_match": sum(res.values()), "mismatches": bad, "no_hash": nohash,
       "skipped_third_layer": len(skipped), "extra_clauses_mismatch": extra_mismatch,
       "pilot_cover_mkunits_order": pilot_cover, "hull_cover_cnf": hullcover,
       "hull_cover_expected": "bb60facb223788fb57291c73abfacd6deaa1eccd82ad2be9f50d36292959a60f",
       "hull_cover_bytes": len(b"p cnf %d %d\n" % (NV, NC + 136)) + len(body) + sum(len((" ".join(str(-x) for x in lits) + " 0\n").encode()) for _, lits in hull_list),
       "distinct_n": len(cache)}
print(json.dumps({k: v for k, v in out.items()}, indent=1)[:4000])
json.dump(out, open(OUTJ, "w"), indent=1)
