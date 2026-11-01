#!/usr/bin/env python3
"""A6 audit: independently rebuild (by streaming, without loading the base into memory) the SHA-256 of the unit
CNFs behind the C2FINAL re-solves (pilot/out.jsonl, sample/out.jsonl, sample/extra_out.jsonl), following the unit
construction documented in C2P/tools/lane.py: base CNF with the header clause count raised by n, then n extra clauses
"l1 ... 0\n" appended (cube literals as units in cube-file order; <case>_cover = hull cube units, then one clause per
subcase line negating its non-hull literals, in cube-file order). Also hashes the base itself and reports whether it
ends with a newline (if it did not, the first appended clause would merge with the last base clause).
usage: unit_cnf_hash.py BASE_CNF RESULTS_DIR
"""
import hashlib, json, os, sys

BASE, RES = sys.argv[1:3]
C = os.path.join(RES, "C2FINAL")

hull = {}
for l in open(os.path.join(RES, "C2C34", "cubes.txt")):
    if l.strip():
        n, *lits = l.split(); hull[n] = [int(x) for x in lits]
cubes, order = {}, {}
for a in range(1, 9):
    order[f"P{a}"] = []
    for l in open(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt")):
        if l.strip():
            n, *lits = l.split(); cubes[n] = [int(x) for x in lits]; order[f"P{a}"].append(n)


def extra(unit):
    case = unit.split("_")[0]
    if unit.endswith("_cover"):
        hs = set(hull[case]); cls = [[x] for x in hull[case]]
        for n in order[case]:
            assert hs <= set(cubes[n])
            cls.append([-x for x in cubes[n] if x not in hs])
        return cls
    return [[x] for x in cubes[unit]]


targets = []  # (file, unit, recorded hash)
for rel in ("pilot/out.jsonl", "sample/out.jsonl", "sample/extra_out.jsonl"):
    for l in open(os.path.join(C, rel)):
        if l.strip():
            r = json.loads(l); targets.append((rel, r["unit"], r["cnf_sha256"]))
ext = {u: extra(u) for _, u, _ in targets}
ns = sorted({len(e) for e in ext.values()})

whole = hashlib.sha256()
with open(BASE, "rb") as f:
    prefix = b""
    while True:
        line = f.readline()
        whole.update(line)
        if line.startswith(b"p cnf"):
            break
        prefix += line
    _, _, NV, NC = line.split(); NV, NC = int(NV), int(NC)
    hs = {}
    for n in ns:
        h = hashlib.sha256(); h.update(prefix); h.update(f"p cnf {NV} {NC + n}\n".encode()); hs[n] = h
    last = line[-1:]
    while (b := f.read(1 << 24)):
        whole.update(b)
        for h in hs.values():
            h.update(b)
        last = b[-1:]
print(f"base: p cnf {NV} {NC}; sha256 {whole.hexdigest()}; ends with newline: {last == b'\n'}")
print(f"distinct extra-clause counts: {ns}")
bad = 0
for rel, u, rec in targets:
    h = hs[len(ext[u])].copy()
    h.update("".join(" ".join(map(str, c)) + " 0\n" for c in ext[u]).encode())
    ok = h.hexdigest() == rec
    bad += not ok
    print(f"{rel:24s} {u:12s} n={len(ext[u]):4d} rebuilt={h.hexdigest()[:16]} recorded={rec[:16]} {'MATCH' if ok else 'MISMATCH'}")
print(f"{len(targets)} units, {bad} mismatches")
