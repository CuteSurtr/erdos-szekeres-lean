#!/usr/bin/env python3
"""Re-prove closed cubes from scratch with an LRAT proof and check the proof with lrat-check.

For a cube (l1..lk) the formula F + {l1} + ... + {lk} (the CNF with the cube literals appended
as unit clauses) is solved by a fresh CaDiCaL with --lrat; lrat-check then verifies the proof
against exactly that file.  A verified proof certifies that F has no model extending the cube.
Proof files are deleted after checking (they can be large); sizes and times are logged.

usage: lratcube.py CNF CLOSED_JSONL OUT_JSONL --cadical BIN --lratcheck BIN --tmp DIR
                   [--n N] [--seed S] [--max-solve-ms MS] [--timeout SEC]
Selects N closed cubes at random among those whose recorded solve time <= MS (the incremental
solve time is only a rough guide to the from-scratch time), plus always the first one.
"""
import argparse
import json
import os
import random
import subprocess
import time

ap = argparse.ArgumentParser()
ap.add_argument("cnf")
ap.add_argument("closed")
ap.add_argument("out")
ap.add_argument("--cadical", required=True)
ap.add_argument("--lratcheck", required=True)
ap.add_argument("--tmp", required=True)
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--max-solve-ms", type=int, default=10 ** 12)
ap.add_argument("--timeout", type=int, default=1800)
ap.add_argument("--solver-opt", action="append", default=[], help="extra CaDiCaL option, e.g. --solver-opt=--elim=0")
a = ap.parse_args()

cubes = [json.loads(l) for l in open(a.closed) if l.strip()]
done = set()
if os.path.exists(a.out):
    for l in open(a.out):
        try:
            done.add(tuple(json.loads(l)["cube"]))
        except Exception:
            pass
pool = [c for c in cubes if c["solve_ms"] <= a.max_solve_ms and tuple(c["cube"]) not in done]
rng = random.Random(a.seed)
pick = rng.sample(pool, min(a.n, len(pool)))
os.makedirs(a.tmp, exist_ok=True)
with open(a.cnf) as f:
    header = None
    pos = 0
    while True:
        line = f.readline()
        if line.startswith("p "):
            header = line.split()
            pos = f.tell()
            break
nv, nc = int(header[2]), int(header[3])
for c in pick:
    cube = c["cube"]
    tag = f"cube{abs(hash(tuple(cube))) % 10**10}"
    cnfp = os.path.join(a.tmp, tag + ".cnf")
    prf = os.path.join(a.tmp, tag + ".lrat")
    with open(cnfp, "w") as g, open(a.cnf) as f:
        f.seek(pos)
        g.write(f"p cnf {nv} {nc + len(cube)}\n")
        while True:
            buf = f.read(1 << 24)
            if not buf:
                break
            g.write(buf)
        for l in cube:
            g.write(f"{l} 0\n")
    t0 = time.time()
    try:
        r = subprocess.run([a.cadical, "-q", "--lrat=1", "--binary=0"] + a.solver_opt + [cnfp, prf], capture_output=True, text=True, timeout=a.timeout)
        solve_out = r.stdout
    except subprocess.TimeoutExpired:
        solve_out = "TIMEOUT"
    t1 = time.time()
    status = "s UNSATISFIABLE" if "s UNSATISFIABLE" in solve_out else ("TIMEOUT" if solve_out == "TIMEOUT" else solve_out.strip()[-60:])
    size = os.path.getsize(prf) if os.path.exists(prf) else 0
    chk = None
    t2 = t1
    if status == "s UNSATISFIABLE":
        try:
            rc = subprocess.run([a.lratcheck, cnfp, prf], capture_output=True, text=True, timeout=a.timeout)
            outl = (rc.stdout + rc.stderr).strip().splitlines()
            chk = [l for l in outl if "VERIFIED" in l or "FAILED" in l or "WARNING" in l or "parsed" in l or "time" in l]
            chk.append(f"exit={rc.returncode}")
        except subprocess.TimeoutExpired:
            chk = ["TIMEOUT"]
        t2 = time.time()
    # lrat-check prints "c VERIFIED" and exits 0 on success, "c NOT VERIFIED" / exit 1 otherwise
    verified = bool(chk) and "c VERIFIED" in chk and "exit=0" in chk
    rec = {"cube": cube, "depth": len(cube), "incremental_solve_ms": c["solve_ms"], "solve_status": status,
           "solve_s": round(t1 - t0, 1), "proof_bytes": size, "check": chk, "check_s": round(t2 - t1, 1),
           "lrat_verified": verified}
    with open(a.out, "a") as o:
        o.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)
    for p in (cnfp, prf):
        if os.path.exists(p):
            os.remove(p)
