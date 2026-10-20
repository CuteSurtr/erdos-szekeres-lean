#!/usr/bin/env python3
"""Close one case CNF by cube-and-conquer (the Mi recipe) with cake_lpr-checked leaves.

W04 version of results/Mii-S/scripts/close_march.py, with sharding, a scratch work dir and resume.

  close_march.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --work DIR --jobs J --hours H
TOP.icnf is the output of `march_cu CASE -d 7` (refuted leaves included, so the file is a full
partition); if it is missing it is made.  Only the top cubes with 0-based line index i,
i mod K == S, are processed.  Each cube c: CASE + units(c) is solved by `cadical --lrat -t TIMEOUT`
and an UNSAT answer is checked with cake_lpr (proof deleted afterwards).  A cube that times out is
split by `march_cu CASE+units(c) -d SPLIT` and its children c+s are queued (the children are stored
in the SPLIT record, so the run can be resumed from OUTDIR/leaves.jsonl).  A cube counts as closed
only when cake_lpr printed `s VERIFIED UNSAT`.  OUTDIR/leaves.icnf lists the closed leaves as
`a lits 0`, OUTDIR/open.icnf the cubes still open (see summarize.py).
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/home/user/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--work", required=True)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); os.makedirs(a.work, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
LOG = os.path.join(a.out, "leaves.jsonl")
lock = threading.Lock()
old = [json.loads(l) for l in open(LOG)] if os.path.exists(LOG) else []
log = open(LOG, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, outcubes=None):
    w = os.path.join(a.work, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    oc = outcubes or os.path.join(w, "cubes")
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o", oc],
                       capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(oc) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]
n = [max([r.get("k", 0) for r in old] + [0])]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline", "k": k}); return
    w = os.path.join(a.work, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st, "k": k}; subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.work, f"SAT_{k}.cnf")])
        with open(os.path.join(a.out, f"SAT_{k}.cube"), "w") as g: g.write(" ".join(map(str, cube)) + "\n")
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
if not os.path.exists(a.top):
    march([], a.depth, "top", outcubes=a.top)
top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
if not any(r.get("top") for r in old):
    rec({"top": True, "ncubes": len(top), "shard": a.shard, "nshards": a.nshards, "nmine": len(mine),
         "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
# resume: queue = my top cubes + children of SPLIT records, minus cubes with a final record
done, queue = set(), list(mine)
for r in old:
    if "cube" not in r: continue
    c = r["cube"]
    if r["status"] == "SPLIT": queue += [c + s for s in r["subs"]]; done.add(tuple(c))
    elif r["status"] == "SAT" or (r["status"] == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"): done.add(tuple(c))
for c in queue:
    if tuple(c) not in done: done.add(tuple(c)); submit(c)
with cv:
    while count[0] > 0: cv.wait()
