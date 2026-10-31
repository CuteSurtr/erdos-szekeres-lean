#!/usr/bin/env python3
"""Experiment: write the node CNF (BASE + layer units, exactly as close_tree.py) and a reduced CNF
F' = { C minus the literals falsified by the units : C in BASE, C has no literal made true by the
units } + the units.  Every model of BASE + units satisfies F' (each clause of F' is a clause of
BASE with only false literals removed), so F' UNSAT implies the node CNF UNSAT.
usage: reduce_node.py BASE NODE FULL.cnf REDUCED.cnf   (run from results/C3-S/tools)"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), "..", "..", "C3a"))
sys.path.insert(0, os.getcwd())
from c3cnf import C3Enc  # noqa: E402
from hullcase import layer_clauses, parse_layers  # noqa: E402

E = C3Enc(11, 7)
base, node, full, red = sys.argv[1:5]
us = [c[0] for c in layer_clauses(11, parse_layers(node), E.ccw, E.sig)]
T = set(us)
F = {-u for u in us}
keep = []
with open(base) as f:
    h = f.readline().split()
    data = f.read()
with open(full, "w") as g:
    g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n")
    g.write(data)
    g.write("".join(f"{u} 0\n" for u in us))
for line in data.splitlines():
    c = [int(x) for x in line.split()[:-1]]
    if any(x in T for x in c):
        continue
    keep.append(" ".join(str(x) for x in c if x not in F) + " 0\n")
with open(red, "w") as g:
    g.write(f"p cnf {h[2]} {len(keep) + len(us)}\n")
    g.writelines(keep)
    g.write("".join(f"{u} 0\n" for u in us))
print(json.dumps({"node": node, "units": len(us), "base_clauses": int(h[3]), "reduced_clauses": len(keep) + len(us),
                  "empty_clause": any(k == " 0\n" or k == "0\n" for k in keep)}))
