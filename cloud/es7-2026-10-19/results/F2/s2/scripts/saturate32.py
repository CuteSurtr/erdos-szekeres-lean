#!/usr/bin/env python3
"""Saturation tests for exact heptagon-free point sets (default N = 32):
 (a) geometric: tools/trackA/sat.c over every face of the line arrangement (exact; face count
     cross-checked with Euler's relation); bad_candidates > 0 means a face where a new point
     creates no convex 7-gon.
 (b) abstract: ext_solve (results/A/scripts/ext_solve.cpp, CaDiCaL) on the base CNF
     tools/trackB/gen_cnf.py N+1 7, one job per x-position p = 1..N+1, all old triples fixed by
     assumptions.
usage: saturate32.py SAT EXT_SOLVE BASE.cnf IN.jsonl OUT.jsonl [climit] [lucky=0 ...]
IN lines: {"id":..., "points": [[x,y],...]} (|coord| < 2^27)."""
import sys, os, json, subprocess, tempfile, itertools
sat, ext, base, inp, outp = sys.argv[1:6]
climit = sys.argv[6] if len(sys.argv) > 6 else "0"; opts = sys.argv[7:]
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
out = open(outp, "a")
for line in open(inp):
    rec = json.loads(line)
    if "points" not in rec: continue
    P = [tuple(p) for p in rec["points"]]; n = len(P)
    res = {"id": rec["id"], "N": n}
    with tempfile.TemporaryDirectory() as td:
        pf = os.path.join(td, "p.txt"); bf = os.path.join(td, "bad.txt")
        open(pf, "w").write("".join(f"{x} {y}\n" for x, y in P))
        r = subprocess.run([sat, "sat", pf, "7", bf], capture_output=True, text=True)
        js = [l for l in r.stdout.splitlines() if l.startswith("{")]
        g = json.loads(js[-1]) if js else {"error": (r.stdout + r.stderr)[-400:]}
        res["geom"] = g
        if js:
            res["geom_faces_covered"] = g["faces_euler"] == g["faces_hit_by_valid_candidates"]
            res["geom_saturated"] = g["bad_candidates"] == 0 and res["geom_faces_covered"]
            if g["bad_candidates"]: res["geom_bad_head"] = open(bf).read()[:3000]
        # abstract: x-sorted signotope (shear if x repeats)
        Q = P
        if len({p[0] for p in Q}) < n:
            L = 2 * max(abs(p[1]) for p in Q) + 1; Q = [(L * x + y, y) for x, y in Q]
        Q = sorted(Q)
        signs = "".join("+" if orient(Q[i], Q[j], Q[k]) > 0 else "-" for i, j, k in itertools.combinations(range(n), 3))
        jobs = f"S {rec['id']} {n} {signs}\n" + "".join(f"P {p}\n" for p in range(1, n + 2))
        r = subprocess.run([ext, base, str(n + 1), climit] + opts, input=jobs, capture_output=True, text=True)
        R = [l.split() for l in r.stdout.splitlines() if l.startswith("R ")]
        res["abs"] = {"jobs": len(R), "SAT": sum(x[3] == "SAT" for x in R), "UNSAT": sum(x[3] == "UNSAT" for x in R),
                      "UNKNOWN": sum(x[3] == "UNKNOWN" for x in R), "ms": round(sum(float(x[6]) for x in R), 1),
                      "sat_positions": [x[2] for x in R if x[3] == "SAT"]}
        res["abs_saturated"] = res["abs"]["UNSAT"] == n + 1
        if res["abs"]["SAT"]:
            res["abs_models"] = [l for l in r.stdout.splitlines() if l.startswith("W ")]
    out.write(json.dumps(res) + "\n"); out.flush()
    print(json.dumps({k: v for k, v in res.items() if k not in ("abs_models", "geom_bad_head")}), flush=True)
