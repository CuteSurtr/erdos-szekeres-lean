#!/usr/bin/env python3
"""Shard manifest: every node of the layer tree at depth <= 2 (H3 mirror reduction on), with its
number of unit clauses and the sha256 of its CNF (BASE + units, exactly as close_node.py /
close_tree.py write it).  usage: manifest.py BASE OUT.tsv"""
import hashlib
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from hullcase import layer_clauses, layers_name, tree_children  # noqa: E402
from compose import node_sha  # noqa: E402

base, out = sys.argv[1:3]
E = C3Enc(11, 7)
with open(base, "rb") as f:
    header = f.readline().decode().split()
    body = f.read()
rows = []
for c1 in tree_children(11, 7, []):
    for node in [c1] + tree_children(11, 7, c1):
        us = [c[0] for c in layer_clauses(11, node, E.ccw, E.sig)]
        rows.append((len(node), layers_name(node), len(us), node_sha(body, header, us)))
rows.sort()
with open(out, "w") as f:
    f.write("depth\tnode\tunits\tcnf_sha256\n")
    for r in rows:
        f.write("\t".join(map(str, r)) + "\n")
print(len(rows))
