#!/usr/bin/env python3
"""Solve hull case + C2 open cube (results/H3/logs/open_cubes_ii_interior.txt) for K random
open cubes consistent with the case.  probe_open.py CNF SPEC K TIMEOUT SEED WORK"""
import json, os, random, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hullsplit as H
cnf, sp, K, T, seed, W = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
U, L = sp.split("/"); U = tuple(int(x) for x in U.split(",") if x); L = tuple(int(x) for x in L.split(",") if x)
cube = H.cube(U, L); fx = {abs(l): l for l in cube}
opn = [list(map(int, l.split()[:-1])) for l in open(os.path.join(HERE, "../../H3/logs/open_cubes_ii_interior.txt"))]
cons = [c for c in opn if not any(abs(l) in fx and fx[abs(l)] != l for l in c)]
nv, nc, body = H.read_cnf(cnf); rng = random.Random(seed); res = []
for c in rng.sample(cons, K):
    lits = list(dict.fromkeys(cube + c)); f = os.path.join(W, f"po_{os.getpid()}.cnf")
    with open(f, "w") as o:
        o.write(f"p cnf {nv} {nc + len(lits)}\n"); o.writelines(body); o.writelines(f"{l} 0\n" for l in lits)
    t = time.time(); rc = subprocess.run([os.path.join(os.environ.get("BIN", "/tmp/claude-0/w/bin"), "cadical"), "-q", "-t", str(T), f],
                                         stdout=subprocess.DEVNULL).returncode
    res.append({"open_cube": c, "rc": rc, "s": round(time.time() - t, 2)}); os.remove(f)
print(json.dumps({"case": sp, "open_cubes_total": len(opn), "consistent": len(cons), "timeout": T, "samples": res}))
