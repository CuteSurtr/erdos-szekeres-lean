#!/usr/bin/env python3
"""W10 copy of results/Mii-S/scripts/close_march.py, with shards, resume and a sound leaf list.

  close_march.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --work DIR --jobs J
Changes from the Mii-S script:
- --top: a precomputed `march_cu CASE -d DEPTH -o top.icnf` file (computed by march here if
  absent); --shard/--nshards keep only the top cubes with 0-based line index i, i mod K == S.
- resume: OUTDIR/leaves.jsonl is re-read; cubes with a final record (cake_lpr VERIFIED UNSAT,
  SAT) are skipped, SPLIT records store their children so they are not re-split.
- leaves.icnf holds only leaves whose cake_lpr line is `s VERIFIED UNSAT`; it and open.icnf
  (the cubes still pending) are rewritten after every record.
- temporary CNFs and LRAT proofs live in --work, never in OUTDIR; a SAT model goes to OUTDIR.
- --hours: no new cube is started after the deadline.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/home/user/tools/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--top")
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--work", default="/home/user/work/tmp")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); os.makedirs(a.work, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LJ = os.path.join(a.out, "leaves.jsonl")
VER = "s VERIFIED UNSAT"
def key(c): return " ".join(map(str, c))
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, out=None):
    w = os.path.join(a.work, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time(); cf = out or os.path.join(w, "cubes")
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o", cf],
                       capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]

# state: pending cubes (in order), finished keys
old = [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
done, splits, verified = set(), {}, []
for r in old:
    if "cube" not in r: continue
    k = key(r["cube"])
    if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: done.add(k); verified.append(r["cube"])
    elif r.get("status") == "SAT": done.add(k)
    elif r.get("status") == "SPLIT" and "subs" in r: splits[k] = r["subs"]; done.add(k)
log = open(LJ, "a")
if a.top and os.path.exists(a.top):
    top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]; line = "given"; ms = 0
else:
    top, ms, line = march([], a.depth, "top", a.top)
tsha = hashlib.sha256(open(a.top, "rb").read()).hexdigest() if a.top else None
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
if not any(r.get("top") for r in old):
    log.write(json.dumps({"top": True, "ncubes": len(top), "shard": a.shard, "nshards": a.nshards,
              "nmine": len(mine), "march_s": round(ms, 1), "march": line, "top_sha256": tsha,
              "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()}) + "\n"); log.flush()
pending = {}   # key -> cube, cubes queued or running and not finished
def expand(c):   # cubes reachable from c through recorded splits that are not done
    k = key(c)
    if k in splits:
        for s in splits[k]: expand(c + s)
    elif k not in done: pending[k] = c
for c in mine: expand(c)
def flush():
    with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
        for c in verified: f.write("a " + key(c) + " 0\n")
    with open(os.path.join(a.out, "open.icnf"), "w") as f:
        for c in pending.values(): f.write("a " + key(c) + " 0\n")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush(); flush()
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
def solve(cube):
    if time.time() > deadline: return
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(a.work, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    p = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                        os.path.join(w, "p.lrat")], capture_output=True, text=True)
    rc = p.returncode; st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}; subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"
        with open(os.path.join(a.out, f"SAT_{k}.model"), "w") as g: g.write(p.stdout)
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w])
    with lock:
        kk = key(cube)
        if r["status"] == "SPLIT":
            for s in subs: pending[key(cube + s)] = cube + s
        if r["status"] != "UNSAT" or r["cake_lpr"] == VER: pending.pop(kk, None)
        if r["status"] == "UNSAT" and r["cake_lpr"] == VER: verified.append(cube)
    rec(r)
    for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
flush()
for c in list(pending.values()): submit(c)
with cv:
    while count[0] > 0: cv.wait()
flush()
print("verified", len(verified), "open", len(pending))
