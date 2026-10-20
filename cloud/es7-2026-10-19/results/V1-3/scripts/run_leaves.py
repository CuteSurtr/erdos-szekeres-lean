#!/usr/bin/env python3
# Re-check the leaves of hull_leaves.icnf with line index i % MOD == RES using two sound checkers.
# cubeCnf as in results/H3/scripts/check_cubes.sh: header count + |c|, unit clauses appended.
# Usage: run_leaves.py CNF LEAVES OUT.jsonl WORKDIR [JOBS] [MOD] [RES]
# Env: CADICAL, CAKE_LPR, LRAT_CHECK. Resumable: line indices already in OUT are skipped.
import json, os, subprocess, sys, time, resource
from concurrent.futures import ThreadPoolExecutor, as_completed
CNF, LEAVES, OUT, WD = sys.argv[1:5]
JOBS = int(sys.argv[5]) if len(sys.argv) > 5 else 4
MOD = int(sys.argv[6]) if len(sys.argv) > 6 else 4
RES = int(sys.argv[7]) if len(sys.argv) > 7 else 3
CAD, CAKE, LRC = os.environ["CADICAL"], os.environ["CAKE_LPR"], os.environ["LRAT_CHECK"]
with open(CNF) as f:
    hdr = f.readline().split(); body = f.read()
NV, NC = int(hdr[2]), int(hdr[3])
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        if l.strip(): done.add(json.loads(l)["line"])
todo = []
for i, l in enumerate(open(LEAVES)):
    if i % MOD != RES or i in done: continue
    t = l.split()
    if t and t[0] == "a": t = t[1:]
    lits = []
    for x in t:
        if x == "0": break
        lits.append(int(x))
    todo.append((i, lits))

def run(cmd, out=None):
    t0 = time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE if out is None else out, stderr=subprocess.STDOUT, text=True)
    return p.returncode, (p.stdout or ""), time.time() - t0

def attempt(i, lits, k):
    f = f"{WD}/leaf{i}.cnf"; p = f"{WD}/leaf{i}.lrat"; m = f"{WD}/leaf{i}.model"
    with open(f, "w") as g:
        g.write(f"p cnf {NV} {NC + len(lits)}\n"); g.write(body)
        for x in lits: g.write(f"{x} 0\n")
    with open(m, "w") as mo:
        st, _, ts = run([CAD, "-q", "--elim=0", "--lrat", "--binary=false", f, p], out=mo)
    r = {"line": i, "cube": lits, "attempt": k, "solver_exit": st, "solve_s": round(ts, 2)}
    r["proof_bytes"] = os.path.getsize(p) if os.path.exists(p) else 0
    if st == 20:
        c1, o1, t1 = run([CAKE, f, p])
        c2, o2, t2 = run([LRC, f, p])
        r["cake_lpr"] = "s VERIFIED UNSAT" if (c1 == 0 and "s VERIFIED UNSAT" in o1.splitlines()) else ("FAIL exit %d: %s" % (c1, o1.strip()[-400:]))
        r["cake_lpr_s"] = round(t1, 2)
        r["lrat_check"] = "c VERIFIED" if (c2 == 0 and "c VERIFIED" in o2.splitlines()) else ("FAIL exit %d: %s" % (c2, o2.strip()[-400:]))
        r["lrat_check_s"] = round(t2, 2)
        os.remove(m)
    elif st == 10:
        r["model_file"] = m
    for x in (f, p):
        if os.path.exists(x): os.remove(x)
    return r

def job(i, lits):
    r = attempt(i, lits, 1)
    if r["solver_exit"] == 20 and (r["cake_lpr"] != "s VERIFIED UNSAT" or r["lrat_check"] != "c VERIFIED"):
        r2 = attempt(i, lits, 2); r2["first_attempt"] = r; r = r2
    return r

print(f"todo {len(todo)} (done {len(done)})", flush=True)
with ThreadPoolExecutor(JOBS) as ex, open(OUT, "a") as out:
    futs = [ex.submit(job, i, c) for i, c in todo]
    for fu in as_completed(futs):
        r = fu.result()
        out.write(json.dumps(r) + "\n"); out.flush()
        print(json.dumps({k: r.get(k) for k in ("line", "solver_exit", "solve_s", "proof_bytes", "cake_lpr", "lrat_check", "cake_lpr_s", "lrat_check_s")}), flush=True)
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print(f"children CPU user {ru.ru_utime:.1f} s sys {ru.ru_stime:.1f} s", flush=True)
