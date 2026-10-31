#!/usr/bin/env python3
"""Rebuild node records lost from out.jsonl (see README) from the driver's stdout (run.log).
close_tree.py prints {"node","status","solve_s","certified"} only after it has written the full record,
and "certified": true there means dual() returned lrat_check == "c VERIFIED" and cake_lpr == "s VERIFIED UNSAT".
The CNF sha256 is recomputed from BASE + node units (as compose.py does). Split records: every UNKNOWN
node, plus the --split-singles presplit rule applied to the parents of tried nodes.
usage: reconstruct_from_runlog.py BASE run.log out.jsonl > out_reconstructed.jsonl (only records not in out.jsonl)"""
import json, sys
sys.path.insert(0, "../../C3a"); sys.path.insert(0, ".")
from compose import node_sha, M, K
from c3cnf import C3Enc
from hullcase import layer_clauses, parse_layers, layers_name, tree_children
base, log, outj = sys.argv[1:4]
have = [json.loads(l) for l in open(outj)]
hc = {r["node"] for r in have if r.get("certified")}; hs = {r["node"] for r in have if r.get("split")}
E = C3Enc(M, K)
with open(base, "rb") as f:
    header = f.readline().decode().split(); body = f.read()
seen = set()
for l in open(log):
    if not l.startswith('{"node"'): continue
    r = json.loads(l)
    n = r["node"]
    if r["certified"] and n not in hc and n not in seen:
        us = [c[0] for c in layer_clauses(M, parse_layers(n), E.ccw, E.sig)]
        print(json.dumps({"node": n, "units": len(us), "cnf_sha256": node_sha(body, header, us), "status": r["status"],
              "solve_s": r["solve_s"], "lrat_check": "c VERIFIED", "cake_lpr": "s VERIFIED UNSAT", "certified": True,
              "reconstructed_from_run_log": True}))
        seen.add(n)
    elif r["status"] == "UNKNOWN" and n not in hs:
        print(json.dumps({"node": n, "status": "UNKNOWN", "solve_s": r["solve_s"], "reconstructed_from_run_log": True}))
        print(json.dumps({"node": n, "split": True, "children": len(tree_children(M, K, parse_layers(n))), "reconstructed_from_run_log": True}))
        hs.add(n)
    # presplit parents: single-orbit newest layer directly below a two-orbit layer (or at depth 2)
    L = parse_layers(n)
    P = L[:-1]
    if len(P) >= 2 and len(P[-1]) == 1 and (len(P) == 2 or len(P[-2]) == 2):
        pn = layers_name(P)
        if pn not in hs:
            print(json.dumps({"node": pn, "split": True, "children": len(tree_children(M, K, P)), "presplit": True, "reconstructed_from_run_log": True}))
            hs.add(pn)
