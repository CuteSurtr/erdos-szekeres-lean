#!/usr/bin/env python3
"""Check the saved symmetric models in inputs/enum/ against freshly generated CNFs.

For every inputs/enum/<tag>.models file (one projected model per line: the signed orientation
literals 1..X):
  * the line has exactly X literals, one per orientation variable;
  * CaDiCaL (assume_check) finds the CNF satisfiable under the line as assumptions, i.e. the
    projected model extends to a model of the regenerated CNF;
  * symcheck.py (independent checker) finds no symmetry/axiom violation and no convex K-gon;
  * where inputs/enum/<tag>.brute exists (brute-force list of all satisfying projections), the
    two files list the same set; and enum_models on the regenerated CNF reproduces the count
    (small instances only).
usage: check_saved.py ENUM_DIR CNF_DIR BIN_DIR [--enum-timeout S]
"""
import json
import os
import subprocess
import sys

enum_dir, cnf_dir, bin_dir = sys.argv[1:4]
etime = 120
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "..", "tools", "symmetric"))
import symcheck  # noqa: E402

results = []
tags = sorted({f.split(".")[0] for f in os.listdir(enum_dir) if f.endswith(".models")})
for tag in tags:
    base = tag.replace("_seeds", "")
    cnf = os.path.join(cnf_dir, base + ".cnf")
    mp = os.path.join(cnf_dir, base + ".json")
    info = json.load(open(mp))
    nX, K = info["X_vars"], info["K"]
    lines = [l.split() for l in open(os.path.join(enum_dir, tag + ".models")) if l.strip()]
    rec = {"file": tag + ".models", "cnf": base, "X_vars": nX, "models": len(lines)}
    rec["all_lines_complete"] = all(sorted(abs(int(x)) for x in l) == list(range(1, nX + 1)) for l in lines)
    if lines:
        r = subprocess.run([os.path.join(bin_dir, "assume_check"), cnf, os.path.join(enum_dir, tag + ".models")],
                           capture_output=True, text=True, check=True)
        last = r.stdout.strip().splitlines()[-1]
        rec["assume_check"] = last
        rec["all_extend_to_cnf_models"] = last == f"TOTAL lines={len(lines)} sat={len(lines)}"
        bad = 0
        maxconv = 0
        for l in lines:
            vals = {abs(int(x)): int(x) > 0 for x in l}
            res = symcheck.full_check(info, vals, K, None, True)
            maxconv = max(maxconv, res["max_convex"])
            if res["symmetry_violations"] or res["A4_violations"] or res["GP_violations"] or res["center_fact_violations"] \
                    or res["sb_violations"] or res["max_convex"] >= K:
                bad += 1
        rec["symcheck_bad"] = bad
        rec["max_convex_over_models"] = maxconv
    bf = os.path.join(enum_dir, tag + ".brute")
    if os.path.exists(bf):
        bl = [l.split() for l in open(bf) if l.strip()]
        rec["brute_count"] = len(bl)
        rec["brute_equals_models"] = {frozenset(map(int, l)) for l in bl} == {frozenset(map(int, l)) for l in lines}
        if nX <= 64:
            outp = os.path.join(cnf_dir, base + ".enum")
            r = subprocess.run([os.path.join(bin_dir, "enum_models"), cnf, str(nX), "100000", outp, str(etime)],
                               capture_output=True, text=True, check=True)
            rec["enum_models"] = r.stdout.strip()
            rec["enum_equals_brute"] = {frozenset(map(int, l.split())) for l in open(outp) if l.strip()} == {frozenset(map(int, l)) for l in bl}
    results.append(rec)
    print(json.dumps(rec), flush=True)
