#!/usr/bin/env python3
"""V1-2: re-check leaves i (0-based) with i % 4 == 2 of hull_leaves.icnf with cake_lpr and the
E2-patched lrat-check.  cubeCnf as in results/H3/scripts/check_cubes.sh (header count + |c|, units
appended).  Resumable: leaves already in OUT are skipped.
Usage: run_leaves.py CNF ICNF OUT TMPD  (env CADICAL, CAKE_LPR, LRAT_CHECK, JOBS)"""
import json, os, subprocess, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
CNF, ICNF, OUT, TMPD = sys.argv[1:5]
CAD, CAKE, LRAT = os.environ["CADICAL"], os.environ["CAKE_LPR"], os.environ["LRAT_CHECK"]
JOBS = int(os.environ.get("JOBS", "4"))
with open(CNF) as f:
    header = f.readline().split(); body = f.read()
nv, nc = int(header[2]), int(header[3])
leaves = []
for i, line in enumerate(open(ICNF)):
    if i % 4 != 2: continue
    t = line.split()
    if t and t[0] == "a": t = t[1:]
    lits = [int(x) for x in t]; assert lits[-1] == 0
    leaves.append((i, lits[:-1]))
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        r = json.loads(l)
        if r.get("cake_lpr") == "s VERIFIED UNSAT" and r.get("lrat_check") == "c VERIFIED":
            done.add(r["i"])
lock = threading.Lock()
def ex(cmd):
    """Run cmd; return (exit code, output, cpu seconds of the child)."""
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = pr.stdout.read(); _, st, ru = os.wait4(pr.pid, 0); pr.returncode = os.waitstatus_to_exitcode(st)
    return pr.returncode, out, ru.ru_utime + ru.ru_stime
def run(i, cube, attempt):
    f = os.path.join(TMPD, f"leaf{i}.cnf"); p = os.path.join(TMPD, f"leaf{i}.lrat")
    with open(f, "w") as o:
        o.write(f"p cnf {nv} {nc + len(cube)}\n"); o.write(body)
        for l in cube: o.write(f"{l} 0\n")
    t0 = time.time()
    se, sout, scpu = ex([CAD, "-q", "--elim=0", "--lrat", "--binary=false", f, p])
    t1 = time.time(); cpu = scpu
    rec = {"i": i, "cube": cube, "attempt": attempt, "solver_exit": se,
           "solve_s": round(t1 - t0, 2)}
    if se == 20:
        rec["proof_bytes"] = os.path.getsize(p)
        ce, cout, ccpu = ex([CAKE, f, p])
        t2 = time.time()
        rec["cake_lpr"] = cout.strip(); rec["cake_exit"] = ce; rec["cake_s"] = round(t2 - t1, 2)
        de, dout, dcpu = ex([LRAT, f, p])
        t3 = time.time(); cpu += ccpu + dcpu
        vs = [l for l in dout.splitlines() if "VERIFIED" in l]
        rec["lrat_check"] = vs[-1].strip() if vs else dout.strip()[-300:]
        rec["lrat_exit"] = de; rec["lrat_s"] = round(t3 - t2, 2)
    else:
        rec["proof_bytes"] = 0; rec["solver_out"] = sout[-20000:]
        if se == 10:
            with open(os.path.join(os.path.dirname(OUT), f"SAT_leaf{i}.txt"), "w") as o:
                o.write(json.dumps(cube) + "\n" + sout)
    rec["cpu_s"] = round(cpu, 2)
    for x in (f, p):
        try: os.remove(x)
        except FileNotFoundError: pass
    with lock:
        with open(OUT, "a") as o: o.write(json.dumps(rec) + "\n")
    return rec
def job(i, cube):
    r = run(i, cube, 1)
    ok = r.get("cake_lpr") == "s VERIFIED UNSAT" and r.get("lrat_check") == "c VERIFIED"
    if not ok and r["solver_exit"] != 10:
        r = run(i, cube, 2)
    return r
todo = [(i, c) for i, c in leaves if i not in done]
print(f"assigned {len(leaves)} done {len(done)} todo {len(todo)}", flush=True)
with ThreadPoolExecutor(JOBS) as pool:
    for r in pool.map(lambda a: job(*a), todo):
        print(r["i"], r["solver_exit"], r["solve_s"], r.get("cake_lpr"), r.get("lrat_check"), flush=True)
