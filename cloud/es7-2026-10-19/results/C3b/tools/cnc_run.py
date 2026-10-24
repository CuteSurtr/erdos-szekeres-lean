#!/usr/bin/env python3
"""Solve march_cu cubes with CaDiCaL + LRAT and check each UNSAT with lrat-check (patched).

For cube c (line "a l1 ... 0" of the icnf): writes CNF + units (header adjusted), runs
`cadical --lrat --binary=false -t TLIM`, then `lrat-check cube.cnf proof` (drat-trim lrat-check with the E2 empty-clause patch) and
`cake_lpr cube.cnf proof` (CakeML-verified); the leaf counts as closed only if CaDiCaL says
UNSATISFIABLE and both checkers accept ("certified": true).  Proof and
cube CNF are deleted afterwards.  Results appended to OUT (JSONL), one line per cube;
cubes already in OUT are skipped (resumable).  Order: cube index; workers take cubes
round-robin by index.
usage: cnc_run.py CNF CUBES OUT --workers 4 --tlim 600 [--only i,j,...] [--limit N]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

CAD = os.environ.get("CAD", "/tmp/claude-0/build/cadical/build/cadical")
LRAT = os.environ.get("LRATCHECK", "/tmp/claude-0/build/drat-trim/lrat-check")
CAKE = os.environ.get("CAKE_LPR", "/tmp/claude-0/build/cake_lpr/cake_lpr")
WORK = os.environ.get("CNC_WORK", "/tmp/claude-0/cncwork")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf"); ap.add_argument("cubes"); ap.add_argument("out")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tlim", type=int, default=600)
    ap.add_argument("--only")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    os.makedirs(WORK, exist_ok=True)
    with open(a.cnf) as f:
        lines = f.readlines()
    hdr = [i for i, l in enumerate(lines) if l.startswith("p cnf")][0]
    nv, nc = map(int, lines[hdr].split()[2:4])
    body = "".join(lines[hdr + 1:])
    del lines
    cubes = [list(map(int, l.split()[1:-1])) for l in open(a.cubes) if l.startswith("a ")]
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            done.add(json.loads(l)["cube"])
    idx = [i for i in range(len(cubes)) if i not in done]
    if a.only:
        want = set(int(x) for x in a.only.split(","))
        idx = [i for i in idx if i in want]
    if a.limit:
        idx = idx[:a.limit]
    outf = open(a.out, "a")

    def run(i):
        cube = cubes[i]
        cp = os.path.join(WORK, f"cube{i}.cnf")
        pp = os.path.join(WORK, f"cube{i}.lrat")
        with open(cp, "w") as f:
            f.write(f"p cnf {nv} {nc + len(cube)}\n")
            f.write(body)
            for l in cube:
                f.write(f"{l} 0\n")
        t0 = time.time()
        r = subprocess.run([CAD, "-q", "--lrat", "--binary=false", "-t", str(a.tlim), cp, pp],
                           capture_output=True, text=True)
        t1 = time.time()
        st = "UNKNOWN"
        for l in r.stdout.splitlines():
            if l.startswith("s "):
                st = l[2:].strip()
        rec = {"cube": i, "depth": len(cube), "lits": cube, "status": st, "solve_s": round(t1 - t0, 1)}
        if st == "UNSATISFIABLE":
            rec["proof_bytes"] = os.path.getsize(pp)
            c = subprocess.run([LRAT, cp, pp], capture_output=True, text=True)
            ver = [l for l in c.stdout.splitlines() if l.startswith("c VERIFIED") or l.startswith("c NOT VERIFIED") or "FAILED" in l]
            rec["lrat"] = "VERIFIED" if any(l.strip() == "c VERIFIED" for l in ver) else ("NOT VERIFIED " + " | ".join(ver[:2]))
            rec["check_s"] = round(time.time() - t1, 1)
            t2 = time.time()
            c2 = subprocess.run([CAKE, cp, pp], capture_output=True, text=True)
            rec["cake_lpr"] = c2.stdout.strip().splitlines()[0] if c2.stdout.strip() else "no output"
            rec["cake_s"] = round(time.time() - t2, 1)
            rec["certified"] = rec["lrat"] == "VERIFIED" and rec["cake_lpr"] == "s VERIFIED UNSAT"
        elif st == "SATISFIABLE":
            mpath = a.out + f".model{i}"
            open(mpath, "w").write(r.stdout)
            rec["model_file"] = mpath
        for p in (cp, pp):
            if os.path.exists(p):
                os.remove(p)
        outf.write(json.dumps(rec) + "\n"); outf.flush()
        print(json.dumps({k: v for k, v in rec.items() if k != "lits"}), flush=True)
        return rec

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(run, idx))


if __name__ == "__main__":
    main()
