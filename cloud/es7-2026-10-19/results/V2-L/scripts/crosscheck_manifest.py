#!/usr/bin/env python3
"""Check that every leaf of leaves_asm (as a set of literals) is a leaf of the acceptance
manifest for its case. usage: crosscheck_manifest.py RESULTS_DIR LEAVES_ASM MANIFEST.jsonl"""
import json, os, sys
res, asm, man = sys.argv[1:4]
cases = [json.loads(l) for l in open(os.path.join(res, "Mii-S/cases.jsonl"))]
M = {}
for l in open(man):
    x = json.loads(l)
    M.setdefault(x["case"], set()).add(frozenset(x["lits"]))
tot_a = tot_m = extra_m = missing = 0
bad = []
print("case asm_leaves manifest_leaves manifest_not_in_asm asm_not_in_manifest")
for r in cases:
    n = r["case"]
    A = set()
    for line in open(os.path.join(asm, "leaves", n + ".icnf")):
        t = line.split()
        assert t[0] == "a" and t[-1] == "0", line
        A.add(frozenset(int(z) for z in t[1:-1]))
    m = M.get(n, set())
    if r["status"] == "UNSAT_VERIFIED":
        ok = A == {frozenset()} and not m
        nm = 0 if ok else len(A)
    else:
        nm = len(A - m)
    em = len(m - A) if r["status"] != "UNSAT_VERIFIED" else len(m)
    if nm: bad.append((n, sorted(sorted(c) for c in (A - m))[:20]))
    tot_a += len(A); tot_m += len(m); extra_m += em; missing += nm
    print(n, len(A), len(m), em, nm)
print(f"TOTAL asm_leaves {tot_a} manifest_leaves {tot_m} manifest_not_in_asm {extra_m} asm_not_in_manifest {missing}")
for b in bad: print("NOT IN MANIFEST", b)
sys.exit(1 if missing else 0)
