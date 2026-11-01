#!/usr/bin/env python3
"""Close one case CNF by cube-and-conquer (the Mi recipe) with cake_lpr-checked leaves.

W00 copy of results/Mii-S/scripts/close_march.py (original kept as close_march_orig.py).
Changes: --top FILE reuses a saved `march_cu CASE -d 7` cube file; --shard/--nshards keep only
top cubes with 0-based line index i, i mod nshards == shard; SPLIT records store their children
("subs") and a restart replays leaves.jsonl (resumable); leaves.icnf takes only leaves whose
cake_lpr line is `s VERIFIED UNSAT`; open.icnf lists the cubes still open; after the --hours
deadline no new solve or split starts (cubes are recorded OPEN instead).

  close_march.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --jobs 4 --hours H
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
VER = "s VERIFIED UNSAT"
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--top")
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LOG = os.path.join(a.out, "leaves.jsonl")
old = [json.loads(l) for l in open(LOG)] if os.path.exists(LOG) else []
log = open(LOG, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, cubes_out=None):
    w = os.path.join(a.out, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    if cubes_out: subprocess.run(["cp", os.path.join(w, "cubes"), cubes_out])
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
# state from earlier runs: last record per cube wins
done, splits = set(), {}
for r in old:
    if "cube" not in r: continue
    k = tuple(r["cube"])
    if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: done.add(k)
    elif r.get("status") == "SPLIT" and "subs" in r: splits[k] = r["subs"]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]
n = [max([int(r.get("k", 0)) for r in old] + [0])]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline", "k": k}); return
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st, "k": k}
    subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        subprocess.run(["cp", f, os.path.join("/tmp/claude-0/w", f"SAT_{k}.cnf")])
    elif time.time() > deadline:
        r["status"] = "OPEN"; r["reason"] = "timeout after deadline"
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    if tuple(c) in done: return
    if tuple(c) in splits:
        for s in splits[tuple(c)]: submit(c + s)
        return
    with cv: count[0] += 1
    pool.submit(task, c)
case_sha = hashlib.sha256(open(a.case, "rb").read()).hexdigest()
if a.top:
    top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
    line, ms = "from --top", 0.0
else:
    top, ms, line = march([], a.depth, "top", os.path.join(a.out, "top.icnf"))
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line, "case_sha256": case_sha,
     "top_sha256": hashlib.sha256(open(a.top or os.path.join(a.out, "top.icnf"), "rb").read()).hexdigest(),
     "shard": a.shard, "nshards": a.nshards, "nmine": len(mine), "resumed_done": len(done),
     "resumed_splits": len(splits), "start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
for c in mine: submit(c)
with cv:
    while count[0] > 0: cv.wait()
pool.shutdown()
# final files from the whole log
last = {}
for r in (json.loads(l) for l in open(LOG)):
    if "cube" in r: last[tuple(r["cube"])] = r
ver = sorted(k for k, r in last.items() if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER)
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for k in ver: f.write("a " + " ".join(map(str, k)) + " 0\n")
sp = {k: r["subs"] for k, r in last.items() if r.get("status") == "SPLIT" and "subs" in r}
vs, op = set(ver), []
def walk(c):
    if tuple(c) in vs: return
    if tuple(c) in sp:
        for s in sp[tuple(c)]: walk(c + s)
    else: op.append(c)
for c in mine: walk(c)
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in op: f.write("a " + " ".join(map(str, c)) + " 0\n")
rec({"final": True, "verified_leaves": len(ver), "open": len(op),
     "end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
