#!/usr/bin/env python3
"""W21 version of results/Mii-S/scripts/close_march.py (copied as close_march_orig.py).

  close_march.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --timeout 300
      --split-depth 6 --jobs 4 --stop-at UNIX_TIME
Changes from the original:
- the top cubes come from a given TOP.icnf (`march_cu CASE -d 7 -o TOP.icnf`, run once, so all
  shards share one file); only cubes with 0-based line index i, i mod K == S are processed;
- resumable: on restart OUTDIR/leaves.jsonl is read; a cube with a cake_lpr-verified UNSAT
  record or a SPLIT record (whose "subs" field lists its children) is not redone, every
  other cube of the shard tree is queued again;
- no new cube is started after --stop-at; at the end OUTDIR/leaves.icnf lists the leaves
  with cake_lpr `s VERIFIED UNSAT` and OUTDIR/open.icnf the cubes still open.
A cube is solved by `cadical --lrat -t TIMEOUT` on CASE + units(cube); an UNSAT answer counts
only with cake_lpr `s VERIFIED UNSAT` (the proof is deleted afterwards); a timeout is split by
`march_cu CASE+units(cube) -d SPLIT` into children cube + s.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--stop-at", type=float, default=1e18)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
VER = "s VERIFIED UNSAT"
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LP = os.path.join(a.out, "leaves.jsonl")
done = {}  # tuple(cube) -> record (verified UNSAT or SPLIT with subs)
if os.path.exists(LP):
    for l in open(LP):
        r = json.loads(l)
        if "cube" not in r: continue
        if (r.get("status") == "UNSAT" and r.get("cake_lpr") == VER) or (r.get("status") == "SPLIT" and "subs" in r):
            done[tuple(r["cube"])] = r
log = open(LP, "a")
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
openl = []
def solve(cube):
    if tuple(cube) in done:
        r = done[tuple(cube)]
        if r["status"] == "SPLIT":
            for s in r["subs"]: submit(cube + s)
        return
    if time.time() > a.stop_at:
        with lock: openl.append(cube)
        return
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(a.out, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time(); tc = time.process_time()
    p = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                        os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL)
    rc = p.returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
        if r["cake_lpr"] != VER:
            with lock: openl.append(cube)
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{os.getpid()}_{k}.cnf")])
        with lock: openl.append(cube)
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, f"{os.getpid()}_{k}")
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception as e:
        rec({"cube": c, "status": "ERROR", "err": repr(e)})
        with lock: openl.append(c)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
rec({"top": True, "resume": len(done), "ncubes_top": len(top), "ncubes_shard": len(mine), "shard": a.shard,
     "nshards": a.nshards, "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
     "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(), "start": time.time()})
for c in mine: submit(c)
with cv:
    while count[0] > 0: cv.wait()
pool.shutdown()
leaves = [json.loads(l) for l in open(LP)]
seen = set()
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for r in leaves:
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER and tuple(r["cube"]) not in seen:
            seen.add(tuple(r["cube"])); f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in openl: f.write("a " + " ".join(map(str, c)) + " 0\n")
rec({"end": True, "verified_leaves": len(seen), "open": len(openl), "time": time.time()})
