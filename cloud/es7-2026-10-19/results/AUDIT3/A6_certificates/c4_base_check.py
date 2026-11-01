#!/usr/bin/env python3
"""A6 audit: check that the archived fourfold CNF (decompressed on stdin) is exactly the base CNF c4_n32L.cnf with the
header clause count raised by the number of cuts and the cut clauses of cuts.jsonl appended in order, as c4final.sh
says. Reconstructs the base by streaming (6-line delay), hashes it and compares with the recorded base hash.
usage: zstd -dc c4_n32L_cuts.cnf.zst | c4_base_check.py CUTS_JSONL EXPECTED_BASE_SHA EXPECTED_CNF_SHA
"""
import hashlib, json, sys
from collections import deque

CUTS, EXP_BASE, EXP_CNF = sys.argv[1:4]
cuts = [json.loads(l)["clause"] for l in open(CUTS) if l.strip()]
k = len(cuts)
whole, base = hashlib.sha256(), hashlib.sha256()
tail = deque()
pline = None
nclauses = 0
for line in sys.stdin.buffer:
    whole.update(line)
    if pline is None and line.startswith(b"p cnf"):
        pline = line
        _, _, nv, nc = line.split()
        line = f"p cnf {int(nv)} {int(nc) - k}\n".encode()
        while tail:  # flush the comment lines that precede the header, in order
            base.update(tail.popleft())
        base.update(line)
        continue
    if pline is not None and not line.startswith(b"c"):
        nclauses += 1
    tail.append(line)
    if len(tail) > k:
        base.update(tail.popleft())
want = [(" ".join(map(str, c)) + " 0\n").encode() for c in cuts]
print("header:", pline.decode().strip(), "| clause lines after header:", nclauses)
print("whole-file sha256:", whole.hexdigest(), "== recorded CNF hash:", whole.hexdigest() == EXP_CNF)
print("reconstructed base sha256:", base.hexdigest(), "== recorded base hash:", base.hexdigest() == EXP_BASE)
print("last", k, "lines equal the cuts.jsonl clauses in order:", list(tail) == want)
print("cut clause lengths:", [len(c) for c in cuts], "| all literals nonzero:", all(all(x != 0 for x in c) for c in cuts))
