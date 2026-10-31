#!/usr/bin/env python3
"""Third-level test: does cubing a heavy second-level cube deeper reduce its cost?
CNF + top-cube units + sub-cube units -> march_cu -d D -> incremental CaDiCaL (iworker) on all
third-level cubes. Prints march seconds, cube count, summed solve seconds, max, time-outs.
usage: lvl3.py ROOT TOPID SUBCUBES.icnf SUBID D TLIM OUTDIR"""
import json, os, subprocess, sys, time
root, top, subf, sid, D, tl, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7]
os.makedirs(out, exist_ok=True)
topc = [l.split()[1:-1] for l in open(f"{root}/cubes_d14.icnf") if l.startswith("a ")][top]
sub = [l.split()[1:-1] for l in open(subf) if l.startswith("a ")][sid]
with open(f"{root}/cnf/bbx.cnf") as f:
    h = f.readline().split(); body = f.read()
cnf = f"{out}/l3.cnf"; cub = f"{out}/l3.icnf"
with open(cnf, "w") as f:
    f.write(f"p cnf {h[2]} {int(h[3]) + len(topc) + len(sub)}\n"); f.write(body)
    for l in topc + sub: f.write(f"{l} 0\n")
t = time.time()
p = subprocess.run([f"{root}/CnC/march_cu/march_cu", cnf, "-d", D, "-o", cub], capture_output=True, text=True)
ms = time.time() - t
n = sum(1 for l in open(cub) if l.startswith("a ")) if os.path.exists(cub) else 0
rows = []
if n:
    subprocess.run([f"{root}/iworker", cnf, cub, "0", "1", tl, "2925", out, "7"], capture_output=True)
    rows = [l.split() for l in open(f"{out}/w0.log") if not l.startswith("#")]
ts = [float(r[2]) for r in rows]
os.unlink(cnf)
print(json.dumps({"top": top, "sub": sid, "depth": int(D), "march_s": round(ms, 1), "n_cubes": n,
                  "solve_s": round(sum(ts), 1), "max_s": round(max(ts), 1) if ts else 0,
                  "n_T": sum(r[1] == "T" for r in rows), "n_U": sum(r[1] == "U" for r in rows),
                  "total_s": round(ms + sum(ts), 1)}), flush=True)
