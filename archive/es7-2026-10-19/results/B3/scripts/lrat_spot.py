#!/usr/bin/env python3
"""LRAT spot check of second-level cubes: CNF + top cube units + sub-cube units, solved from
scratch by cadical --lrat, proof checked by drat-trim's lrat-check.
usage: lrat_spot.py ROOT TOPID SUBCUBES.icnf SUBID [SUBID ...]   (prints one JSON line each)"""
import json, os, subprocess, sys, time
root, top, subf, ids = sys.argv[1], int(sys.argv[2]), sys.argv[3], [int(x) for x in sys.argv[4:]]
cad = f"{root}/cadical/build/cadical"; chk = f"{root}/drat-trim/lrat-check"
topc = [l.split()[1:-1] for l in open(f"{root}/cubes_d14.icnf") if l.startswith("a ")][top]
subs = [l.split()[1:-1] for l in open(subf) if l.startswith("a ")]
h, body = None, None
with open(f"{root}/cnf/bbx.cnf") as f:
    h = f.readline().split(); body = f.read()
for sid in ids:
    units = topc + subs[sid]
    cnf = f"{root}/lrat_tmp_{top}_{sid}.cnf"; prf = cnf + ".lrat"
    with open(cnf, "w") as f:
        f.write(f"p cnf {h[2]} {int(h[3]) + len(units)}\n"); f.write(body)
        for l in units: f.write(f"{l} 0\n")
    t = time.time()
    p = subprocess.run([cad, "--lrat", "--binary=false", "-q", cnf, prf], capture_output=True, text=True)
    ts = time.time() - t
    t = time.time()
    q = subprocess.run([chk, cnf, prf], capture_output=True, text=True)
    tc = time.time() - t
    ok = "c VERIFIED" in q.stdout or "s VERIFIED" in q.stdout
    print(json.dumps({"top": top, "sub": sid, "solver_rc": p.returncode, "solve_s": round(ts, 2),
                      "proof_MB": round(os.path.getsize(prf) / 1e6, 2), "check_s": round(tc, 2),
                      "verified": ok, "checker_tail": q.stdout.strip().splitlines()[-1:] }), flush=True)
    os.unlink(cnf); os.unlink(prf)
