#!/usr/bin/env python3
"""Checksum of each block as listed by the exe (data/exe_lists.txt), with the same arithmetic as Lrv.ck in
lean/LrvReview.lean (the kernel recomputes it from the olean definitions Res118.rowsP/Q/U/A). Prints JSON."""
import json, sys
M = 2305843009213693951  # 2^61 - 1
def ck(rows):
    a = 0
    for s in rows:
        b = (a * 1000033 + len(s) + 7) % M
        for x in s:
            b = (b * 1000003 + x + 1) % M
        a = b
    return a
blocks = {}
for line in open(sys.argv[1]):
    B, i, supp = line.split()
    blocks.setdefault(B, []).append([int(x) for x in supp.split(',')])
print(json.dumps({B: {'rows': len(r), 'ck': ck(r)} for B, r in blocks.items()}))
