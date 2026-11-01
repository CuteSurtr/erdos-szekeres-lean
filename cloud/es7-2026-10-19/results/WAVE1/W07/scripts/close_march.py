#!/usr/bin/env python3
"""W07 version of results/Mii-S/scripts/close_march.py (original copied as close_march_orig.py).

  close_march.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --jobs J --until EPOCH
Changes from the original:
- the top cubes are read from TOP.icnf (made once by `march_cu CASE -d 7 -o TOP.icnf`), and only
  those with 0-based line index i, i mod K == S are processed;
- resumable: OUTDIR/leaves.jsonl is replayed at start (a cube counts as done if it has an UNSAT
  record with cake_lpr `s VERIFIED UNSAT`, or a SPLIT record, whose children are now stored in `subs`);
- leaves.icnf lists only leaves with cake_lpr `s VERIFIED UNSAT`; an UNSAT whose check fails is
  recorded as UNSAT_UNCHECKED and stays open;
- after --until (unix time) no new solve starts; cubes left are written to OUTDIR/open.icnf.
"""
import argparse, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--until", type=float, default=1e18)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
VER = "s VERIFIED UNSAT"
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LOG = os.path.join(a.out, "leaves.jsonl")
top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
# replay
pending = {tuple(c): None for c in mine}; done = set()
if os.path.exists(LOG):
    for l in open(LOG):
        r = json.loads(l)
        if "cube" not in r: continue
        c = tuple(r["cube"])
        if c in done: continue
        if r["status"] == "UNSAT" and r.get("cake_lpr") == VER or r["status"] == "SPLIT" and "subs" in r:
            pending.pop(c, None); done.add(c)
            for s in r.get("subs", []): pending.setdefault(c + tuple(s), None)
log = open(LOG, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
rec({"start": True, "time": time.time(), "shard": a.shard, "nshards": a.nshards, "ntop": len(top),
     "nmine": len(mine), "pending": len(pending), "done": len(done)})
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
left = set()
def solve(cube):
    if time.time() > a.until:
        with lock: left.add(tuple(cube))
        return
    with lock: n[0] += 1; k = f"{os.getpid()}_{n[0]}"
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        p = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True)
        o = p.stdout + p.stderr
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if r["cake_lpr"] == VER else "UNSAT_UNCHECKED"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        subprocess.run([os.path.join(BIN, "cadical"), "-q", f, "-w", os.path.join(a.out, f"SAT_{k}.model")])
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
    elif r["status"] != "UNSAT":
        with lock: left.add(tuple(cube))
def task(c):
    try: solve(c)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
for c in pending: submit(list(c))
with cv:
    while count[0] > 0: cv.wait()
leaves = [json.loads(l) for l in open(LOG)]
seen = set()
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for r in leaves:
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER and tuple(r["cube"]) not in seen:
            seen.add(tuple(r["cube"])); f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in sorted(left, key=lambda c: (len(c), c)): f.write("a " + " ".join(map(str, c)) + " 0\n")
rec({"end": True, "time": time.time(), "verified_leaves": len(seen), "open": len(left)})
