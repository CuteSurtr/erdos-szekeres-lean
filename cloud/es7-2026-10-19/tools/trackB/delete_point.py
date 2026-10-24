#!/usr/bin/env python3
"""Delete point q (1-based) from a signotope file; relabel. usage: delete_point.py in.sig N q out.sig"""
import sys
inp, N, q, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
m = lambda a: a if a < q else a - 1
with open(out, "w") as f:
    for line in open(inp):
        i, j, k, s = map(int, line.split())
        if q in (i, j, k):
            continue
        f.write(f"{m(i)} {m(j)} {m(k)} {s}\n")
