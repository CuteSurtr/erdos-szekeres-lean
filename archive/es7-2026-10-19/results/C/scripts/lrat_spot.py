#!/usr/bin/env python3
"""LRAT spot checks of closed cubes from a cnc2 run.

usage: lrat_spot.py <cnf> <closed.txt> <bindir> <workdir> <count> [timeout_s=900] [seed=1] [min_cnc_seconds=0]

For each sampled closed cube: write <cnf> + the cube as unit clauses, solve it from scratch with
`cadical --lrat --binary=false` (time limit), and check the proof with drat-trim's `lrat-check`
against that CNF.  A VERIFIED line certifies "CNF + cube is UNSAT" for that cube only; the
proof files are deleted after checking.  Prints one JSON line per cube.
"""
import sys, os, random, subprocess, time, json
cnf, closed, bindir, wd, count = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
tlim = int(sys.argv[6]) if len(sys.argv) > 6 else 900
seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
min_dt = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0   # sample only cubes whose cnc solve took >= this
os.makedirs(wd, exist_ok=True)
cubes = []
for line in open(closed):
    t = line.split()
    if t and float(t[0]) >= min_dt: cubes.append((float(t[0]), [int(x) for x in t[1:-1]]))
random.Random(seed).shuffle(cubes)
cubes = cubes[:count]
head, body = None, []
with open(cnf) as f:
    for line in f:
        if line.startswith('p'): head = line.split(); continue
        if line.startswith('c'): continue
        body.append(line)
nv, nc = int(head[2]), int(head[3])
for n, (dt, cube) in enumerate(cubes):
    path = os.path.join(wd, f"cube{n}.cnf"); proof = os.path.join(wd, f"cube{n}.lrat")
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.writelines(body)
        for l in cube: f.write(f"{l} 0\n")
    t0 = time.time()
    r = subprocess.run([os.path.join(bindir, "cadical"), "-q", "-t", str(tlim), "--lrat", "--binary=false", path, proof],
                       capture_output=True, text=True)
    st = [l for l in r.stdout.split("\n") if l.startswith("s ")]
    rec = {"cube": cube, "depth": len(cube), "cnc_solve_s": dt, "status": st[0][2:] if st else "UNKNOWN",
           "solve_s": round(time.time() - t0, 1)}
    if rec["status"] == "UNSATISFIABLE":
        rec["proof_bytes"] = os.path.getsize(proof)
        t1 = time.time()
        c = subprocess.run([os.path.join(bindir, "lrat-check"), path, proof], capture_output=True, text=True)
        out = c.stdout + c.stderr
        rec["lrat_check"] = "VERIFIED" if "c VERIFIED" in out else "NOT VERIFIED"
        rec["check_s"] = round(time.time() - t1, 1)
    for p in (path, proof):
        if os.path.exists(p): os.unlink(p)
    print(json.dumps(rec), flush=True)
