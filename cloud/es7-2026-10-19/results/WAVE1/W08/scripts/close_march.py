#!/usr/bin/env python3
"""W08 copy of results/Mii-S/scripts/close_march.py with sharding and resume.

  close_march.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --jobs J --hours H
Top cubes come from TOP.icnf (`march_cu CASE -d 7`); this run takes the cubes with 0-based line
index i, i mod K == S.  Each cube c: CASE + units(c) is solved by `cadical --lrat -t TIMEOUT`;
an UNSAT answer is checked with cake_lpr (proof deleted afterwards).  A timeout splits c with
`march_cu CASE+units(c) -d SPLIT` and the children c+s are queued (recorded in the SPLIT record
under "subs", so a restart can rebuild the queue).  Records go to OUTDIR/leaves.jsonl.
At the end OUTDIR/leaves.icnf lists the cubes with cake_lpr `s VERIFIED UNSAT` and
OUTDIR/open.icnf the cubes still open.  Resume: rerun the same command.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w08/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--hours", type=float, default=1e9)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
VER = "s VERIFIED UNSAT"
lock = threading.Lock(); LOG = os.path.join(a.out, "leaves.jsonl")
top_all = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top_all) if i % a.nshards == a.shard]
# resume: rebuild the open set from the records
done, queued = set(), [tuple(c) for c in mine]
if os.path.exists(LOG):
    for l in open(LOG):
        r = json.loads(l)
        if "cube" not in r: continue
        c = tuple(r["cube"])
        if r["status"] == "UNSAT" and r.get("cake_lpr") == VER: done.add(c)
        elif r["status"] == "SPLIT":
            done.add(c); queued += [c + tuple(s) for s in r["subs"]]
        elif r["status"] == "SAT": done.add(c)
pending = [list(c) for c in dict.fromkeys(queued) if c not in done]
log = open(LOG, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag):
    w = os.path.join(a.out, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
openset = set(); stop = [False]
def solve(cube):
    with lock: n[0] += 1; k = f"{os.getpid()}_{n[0]}"
    if time.time() > deadline:
        with lock: openset.add(tuple(cube))
        return
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
        if r["cake_lpr"] != VER:
            with lock: openset.add(tuple(cube))
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        subprocess.run(["sh", "-c", f"{os.path.join(BIN, 'cadical')} -q {f} > {os.path.join(a.out, f'SAT_{k}.model')}"])
    elif time.time() > deadline:
        r["status"] = "OPEN"; r["reason"] = "timeout after deadline"
        with lock: openset.add(tuple(cube))
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
rec({"start": True, "time": time.time(), "shard": a.shard, "nshards": a.nshards, "ntop": len(top_all),
     "nmine": len(mine), "pending": len(pending), "timeout": a.timeout, "split_depth": a.split_depth,
     "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
     "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
for c in pending: submit(c)
with cv:
    while count[0] > 0: cv.wait()
leaves = [json.loads(l) for l in open(LOG)]
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    seen = set()
    for r in leaves:
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER and tuple(r["cube"]) not in seen:
            seen.add(tuple(r["cube"])); f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in sorted(openset, key=lambda c: (len(c), c)): f.write("a " + " ".join(map(str, c)) + " 0\n")
rec({"end": True, "time": time.time(), "leaves": len(seen), "open": len(openset)})
