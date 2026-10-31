#!/usr/bin/env python3
"""Time F + open cube o + cube(case) for a random sample of the (o, case) products that
hybrid_grid.py left unknown.  product_probe.py CNF GRID.jsonl K TIMEOUT SEED WORK"""
import json, os, random, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hullsplit as H
cnf, gj, K, T, seed, W = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
pairs = [(r["open_cube"], nm) for r in map(json.loads, open(gj)) for nm in r["unknown"]]
byname = {H.name(U, L): (U, L) for U, L in H.cases()}
nv, nc, body = H.read_cnf(cnf); rng = random.Random(seed)
for o, nm in rng.sample(pairs, min(K, len(pairs))):
    lits = list(dict.fromkeys(H.cube(*byname[nm]) + o)); f = os.path.join(W, f"pp_{os.getpid()}.cnf")
    with open(f, "w") as out:
        out.write(f"p cnf {nv} {nc + len(lits)}\n"); out.writelines(body); out.writelines(f"{l} 0\n" for l in lits)
    t = time.time(); rc = subprocess.run([os.path.join(os.environ.get("BIN", "/tmp/claude-0/w/bin"), "cadical"), "-q", "-t", str(T), f],
                                         stdout=subprocess.DEVNULL).returncode
    os.remove(f)
    print(json.dumps({"case": nm, "open_cube": o, "rc": rc, "s": round(time.time() - t, 2), "timeout": T}), flush=True)
