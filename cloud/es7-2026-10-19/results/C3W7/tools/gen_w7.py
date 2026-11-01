#!/usr/bin/env python3
"""Planning only: from lists/H3one.tsv (the 319 open six-bit cubes of the H3/one roots, made by gen_h3one.py, the
H3/one-only variant of results/C3W6/tools/gen_w6.py), take the first 239 cubes, write their nine-bit cubes (sigma
children on the 3 smallest free residues, which are 8, 9, 10 for every H3/one six-bit cube) to lists/W7.tsv and their
sigma-split records to presplit.jsonl.  The last 80 cubes are done locally (results/C3H1/LOCAL).
usage: gen_w7.py H3one.tsv OUTDIR   (run with results/C3U2/tools on sys.path for hullcase)"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3U2", "tools"))
from hullcase import free_residues, node_name, parse_node, sigma_children  # noqa: E402

M = 11
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1])][1:]
cubes = [r[1] for r in rows][:239]
meta = {r[1]: (r[2], r[3]) for r in rows}
tag = "C3W7 planning: sigma split written without a solve (results/C3W7/TASK.md)"
units, pre = [], []
for c in cubes:
    L, C = parse_node(c)
    assert len(C) == 6 and len(L) == 2
    bits, ch = sigma_children(M, L, C, 3)
    assert bits == free_residues(M, L, C)[:3] == [8, 9, 10], (c, bits)
    pre.append({"node": c, "split": True, "sigma_bits": bits, "children": 8, "planned": tag})
    for cl, cc in ch:
        units.append((node_name(cl, cc), c) + meta[c])
assert len(set(u[0] for u in units)) == len(units) == 8 * 239
out = sys.argv[2]
with open(os.path.join(out, "W7.tsv"), "w") as f:
    f.write("row\tnode\tparent\troot\tstratum\n")
    for i, u in enumerate(units):
        f.write(f"{i}\t" + "\t".join(u) + "\n")
with open(os.path.join(out, "presplit.jsonl"), "w") as f:
    for r in pre:
        f.write(json.dumps(r) + "\n")
print(len(units), "units;", len(pre), "presplit records;", dict(collections.Counter(u[2] for u in units)))
