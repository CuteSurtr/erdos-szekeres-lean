#!/usr/bin/env python3
"""Compare the C3U close_tree re-runs at m = 11 (--sigma-split 3 --caps 1,300,300) with the
sigma_cubes.py records of results/C3SIG/G0/out.jsonl: for every cube both have, the same
cnf_sha256 and units; also: every cube certified, the sigma-split record names the same 3 bits
as G0's cubes.
usage: m11_vs_g0.py G0_OUT.jsonl TREE.jsonl [...]"""
import json, sys

g0 = {}
for l in open(sys.argv[1]):
    r = json.loads(l)
    if "cube" in r:
        C = sorted((int(x), v) for x, v in r["cube"].items())
        g0[r["node"] + "__" + "-".join(f"{a}s{b}" for a, b in C)] = r
fails = 0
for f in sys.argv[2:]:
    R = [json.loads(l) for l in open(f)]
    root = R[0]["node"]
    sp = [r for r in R if r.get("split")]
    cubes = [r for r in R if "__" in r["node"] and not r.get("split")]
    same = sum(1 for r in cubes if r["node"] in g0 and (g0[r["node"]]["cnf_sha256"], g0[r["node"]]["units"]) == (r["cnf_sha256"], r["units"]))
    g0bits = sorted({int(x) for r in g0.values() if r["node"] == root for x in r["cube"]})
    ok = (len(sp) == 1 and sp[0].get("sigma_bits") == g0bits and sp[0]["children"] == 8 and len(cubes) == 8
          and same == 8 and all(r.get("certified") for r in cubes))
    fails += not ok
    print(json.dumps({"root": root, "root_status": R[0]["status"], "root_cap": R[0]["cap"], "split": sp,
                      "cubes": len(cubes), "certified": sum(1 for r in cubes if r.get("certified")),
                      "caps": sorted({r["cap"] for r in cubes}), "cnf_sha256_and_units_equal_G0": same,
                      "solve_s": round(sum(r["solve_s"] for r in cubes), 1),
                      "check_s": round(sum(r.get("check_s", 0) for r in cubes), 1),
                      "proof_sha256_present": sum(1 for r in cubes if r.get("proof_sha256")),
                      "result": "OK" if ok else "FAIL"}))
print("FAILURES", fails)
