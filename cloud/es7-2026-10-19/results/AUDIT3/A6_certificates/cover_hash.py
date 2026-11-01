#!/usr/bin/env python3
"""A6 audit: rebuild, by streaming, the SHA-256 of the central-34 hull cover CNF as results/SYMZ/hullcubes.py writes
it: header 'p cnf NV NC+136' (lines before the base header are dropped), every non-empty base line after the header,
then for each cube of cubes.txt (file order) the clause of its negated literals (cube order).
usage: cover_hash.py BASE_CNF CUBES_TXT EXPECTED_SHA
"""
import hashlib, sys

BASE, CUBES, EXP = sys.argv[1:4]
cubes = [l.split()[1:] for l in open(CUBES) if l.strip()]
h = hashlib.sha256()
with open(BASE, "rb") as f:
    for line in f:
        if line.startswith(b"p cnf"):
            _, _, nv, nc = line.split()
            h.update(f"p cnf {int(nv)} {int(nc) + len(cubes)}\n".encode())
            break
    for line in f:
        if line.strip(b"\n"):
            h.update(line if line.endswith(b"\n") else line + b"\n")
for lits in cubes:
    h.update((" ".join(str(-int(x)) for x in lits) + " 0\n").encode())
print("cubes:", len(cubes), "| rebuilt cover sha256:", h.hexdigest(), "| equals recorded:", h.hexdigest() == EXP)
