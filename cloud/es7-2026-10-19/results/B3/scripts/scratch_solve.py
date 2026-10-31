#!/usr/bin/env python3
"""Solve one second-level cube from scratch (fresh CaDiCaL or Kissat, no proof).
usage: scratch_solve.py ROOT TOPID SUBCUBES.icnf SUBID SOLVER TLIM"""
import json, os, subprocess, sys, time
root, top, subf, sid, solver, tl = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
topc = [l.split()[1:-1] for l in open(f"{root}/cubes_d14.icnf") if l.startswith("a ")][top]
sub = [l.split()[1:-1] for l in open(subf) if l.startswith("a ")][sid]
with open(f"{root}/cnf/bbx.cnf") as f:
    h = f.readline().split(); body = f.read()
cnf = f"{root}/scr_{top}_{sid}_{solver}.cnf"
with open(cnf, "w") as f:
    f.write(f"p cnf {h[2]} {int(h[3]) + len(topc) + len(sub)}\n"); f.write(body)
    for l in topc + sub: f.write(f"{l} 0\n")
exe = f"{root}/{solver}/build/{solver}"
args = [exe, "-q", f"-t", str(tl), cnf] if solver == "cadical" else [exe, "-q", f"--time={tl}", cnf]
t = time.time(); p = subprocess.run(args, capture_output=True, text=True); dt = time.time() - t
os.unlink(cnf)
print(json.dumps({"top": top, "sub": sid, "solver": solver, "rc": p.returncode, "secs": round(dt, 2)}), flush=True)
