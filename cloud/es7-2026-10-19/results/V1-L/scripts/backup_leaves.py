#!/usr/bin/env python3
"""Backup re-check of the V1-1 leaves (0-based line i of hull_leaves.icnf with i % 4 == 1),
run because V1-1 had pushed only 9 of its 300 leaves by 06:07 UTC. Leaves are taken in
reverse order, so the work overlaps V1-1's own (front-to-back) order as late as possible.
Before each leaf the current V1-1/leaves_cake.jsonl is re-read and leaves it has already
verified are skipped.

For each leaf c: cubeCnf as results/H3/scripts/check_cubes.sh (header clause count + |c|,
unit clauses appended), `cadical -q --elim=0 --lrat --binary=false`, then cake_lpr, which
must exit 0 and print the line `s VERIFIED UNSAT`. CNF and proof are deleted afterwards.

Usage: backup_leaves.py CNF ICNF V1-1_JSONL OUT TMPD  (env CADICAL, CAKE_LPR, JOBS)"""
import json, os, subprocess, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
CNF, ICNF, SIB, OUT, TMPD = sys.argv[1:6]
CAD, CAKE = os.environ["CADICAL"], os.environ["CAKE_LPR"]
JOBS = int(os.environ.get("JOBS", "4"))
with open(CNF) as f:
    header = f.readline().split(); body = f.read()
nv, nc = int(header[2]), int(header[3])
leaves = [(i, [int(x) for x in l.split()[1:-1]]) for i, l in enumerate(open(ICNF)) if i % 4 == 1]
leaves.reverse()
lock = threading.Lock()
def sibling_done():
    d = set()
    try:
        for l in open(SIB):
            r = json.loads(l)
            if r.get("solver_exit") == 20 and r.get("cake_lpr") in ("VERIFIED UNSAT", "s VERIFIED UNSAT"):
                d.add(r.get("line", r.get("i")))
    except Exception:
        pass
    return d
mine = set()
if os.path.exists(OUT):
    mine = {json.loads(l)["i"] for l in open(OUT) if l.strip()}
def run(item):
    i, cube = item
    if i in mine or i in sibling_done():
        return
    f = os.path.join(TMPD, f"leaf{i}.cnf"); p = os.path.join(TMPD, f"leaf{i}.lrat")
    with open(f, "w") as o:
        o.write(f"p cnf {nv} {nc + len(cube)}\n"); o.write(body)
        for z in cube: o.write(f"{z} 0\n")
    t0 = time.time()
    se = subprocess.run([CAD, "-q", "--elim=0", "--lrat", "--binary=false", f, p],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    t1 = time.time()
    rec = {"i": i, "cube": cube, "solver_exit": se, "solve_s": round(t1 - t0, 2)}
    if se == 20:
        rec["proof_bytes"] = os.path.getsize(p)
        c = subprocess.run([CAKE, f, p], capture_output=True, text=True)
        rec["cake_lpr"] = "s VERIFIED UNSAT" if (c.returncode == 0 and "s VERIFIED UNSAT" in c.stdout.splitlines()) \
            else "FAIL exit %d: %s" % (c.returncode, (c.stdout + c.stderr).strip()[-300:])
        rec["cake_exit"] = c.returncode; rec["cake_s"] = round(time.time() - t1, 2)
    for x in (f, p):
        try: os.remove(x)
        except FileNotFoundError: pass
    with lock:
        with open(OUT, "a") as o: o.write(json.dumps(rec) + "\n")
with ThreadPoolExecutor(JOBS) as ex:
    list(ex.map(run, leaves))
