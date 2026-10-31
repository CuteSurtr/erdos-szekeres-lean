#!/usr/bin/env python3
"""Brute-force check of a model of a symcnf.py (C3) or d3cnf.py (D3) CNF, independent of the
clause generator: rebuilds chi on all P points from the map and the model, then checks with
symcheck.full_check
  * rotation symmetry, Knuth A4 (interiority) on all 4-sets, 3-term Grassmann-Pluecker on all
    5-sets, centre facts, labelling normal form,
  * no K points in convex position (exact DFS over convex subsets, 4-point criterion),
and for D3 additionally the reflection rule chi(S a, S b, S c) = -chi(a, b, c) for every triple.
A passing model is an abstract (CC-system) configuration, not a point set.
usage: modelcheck.py map.json model.txt [--sig out.sig]
"""
import itertools
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "..", "tools", "symmetric"))
import symcheck  # noqa: E402

info = json.load(open(sys.argv[1]))
status, vals = symcheck.read_model(sys.argv[2])
sig = sys.argv[sys.argv.index("--sig") + 1] if "--sig" in sys.argv else None
res = symcheck.full_check(info, vals, info["K"], sig, True)
if info.get("group") == "D3":
    chi = symcheck.Chi(info, vals)
    S = info["sigma"]
    bad = 0
    for a, b, c in itertools.combinations(range(info["P"]), 3):
        if chi.O(S[a], S[b], S[c]) != -chi.O(a, b, c):
            bad += 1
    res["reflection_violations"] = bad
res["status_line"] = status
ok = all(res.get(k, 0) == 0 for k in ("symmetry_violations", "A4_violations", "GP_violations",
                                        "center_fact_violations", "sb_violations", "reflection_violations"))
res["abstract_model_ok"] = ok and res["max_convex"] < info["K"]
print(json.dumps(res))
sys.exit(0 if res["abstract_model_ok"] else 1)
