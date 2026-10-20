#!/usr/bin/env python3
"""Append the literals of one cube (line ID, 0-based, of a march_cu .icnf) as unit clauses.
usage: subcnf.py in.cnf cubes.icnf ID out.cnf"""
import sys
inp, cub, cid, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
cubes = [l.split()[1:-1] for l in open(cub) if l.startswith("a ")]
c = cubes[cid]
with open(inp) as f:
    h = f.readline().split(); body = f.read()
with open(out, "w") as f:
    f.write(f"p cnf {h[2]} {int(h[3]) + len(c)}\n"); f.write(body)
    for l in c: f.write(f"{l} 0\n")
print(cid, " ".join(c))
