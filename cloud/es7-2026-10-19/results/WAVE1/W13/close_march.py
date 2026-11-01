#!/usr/bin/env python3
"""W13 copy of results/Mii-S/scripts/close_march.py with sharding and resume.

  close_march.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --jobs J --hours H
Changes from the original:
- the top cubes are read from TOP.icnf (made once by `march_cu CASE -d 7 -o TOP.icnf`, so every
  shard uses the same file); only lines with 0-based index i, i mod K == S are processed;
- a SPLIT record stores its children ("subs"), so a restart rebuilds the pending set from
  leaves.jsonl: pending = my top cubes + children of SPLIT records - cubes already closed
  (UNSAT with cake_lpr `s VERIFIED UNSAT`), split or SAT;
- after the deadline a timed-out cube is not split but left open;
- leaves.icnf (cake_lpr-verified leaves only) and open.icnf are rewritten every few minutes and
  at the end.
Solver recipe unchanged: cadical --lrat -t TIMEOUT, cake_lpr on every UNSAT (proof deleted
afterwards), march_cu -d SPLIT on a timeout.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--work", default=None)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
work = a.work or a.out; os.makedirs(work, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LOG = os.path.join(a.out, "leaves.jsonl")
def key(c): return " ".join(map(str, c))
def load():
    return [json.loads(l) for l in open(LOG)] if os.path.exists(LOG) else []
def verified(r): return r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"
alltop = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(alltop) if i % a.nshards == a.shard]
old = load(); done = set(); queue = list(mine)
for r in old:
    if "cube" not in r: continue
    if verified(r) or r["status"] in ("SPLIT", "SAT"): done.add(key(r["cube"]))
    if r["status"] == "SPLIT": queue += [r["cube"] + s for s in r["subs"]]
pending = {key(c): c for c in queue if key(c) not in done}
log = open(LOG, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def dump():
    with lock:
        rs = load()
        with open(os.path.join(a.out, "leaves.icnf.tmp"), "w") as f:
            for r in rs:
                if "cube" in r and verified(r): f.write("a " + key(r["cube"]) + " 0\n")
        with open(os.path.join(a.out, "open.icnf.tmp"), "w") as f:
            for c in pending.values(): f.write("a " + key(c) + " 0\n")
    os.replace(os.path.join(a.out, "leaves.icnf.tmp"), os.path.join(a.out, "leaves.icnf"))
    os.replace(os.path.join(a.out, "open.icnf.tmp"), os.path.join(a.out, "open.icnf"))
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag):
    w = os.path.join(work, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() > deadline: return
    w = os.path.join(work, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
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
    elif rc == 10:
        r["status"] = "SAT"; os.makedirs(os.path.join(a.out, "SAT"), exist_ok=True)
        subprocess.run([os.path.join(BIN, "cadical"), "-q", "-w", os.path.join(a.out, "SAT", f"model_{k}.txt"), f],
                       stdout=subprocess.DEVNULL)
        with open(os.path.join(a.out, "SAT", f"cube_{k}.txt"), "w") as g: g.write(key(cube) + "\n")
    elif time.time() > deadline:
        r["status"] = "OPEN"; r["reason"] = "timeout after deadline"
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, f"{os.getpid()}_{k}")
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=[s for s in subs])
    subprocess.run(["rm", "-rf", w]); rec(r)
    with lock:
        if verified(r) or r["status"] in ("SPLIT", "SAT"): pending.pop(key(cube), None)
        for s in subs: pending[key(cube + s)] = cube + s
    for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
if not old:
    rec({"top": True, "top_file": a.top, "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
         "ntop": len(alltop), "shard": a.shard, "nshards": a.nshards, "nmine": len(mine),
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
rec({"resume": True, "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "npending": len(pending)})
for c in list(pending.values()): submit(c)
last = time.time()
with cv:
    while count[0] > 0:
        cv.wait(timeout=60)
        if time.time() - last > 300:
            cv.release()
            try: dump()
            finally: cv.acquire()
            last = time.time()
dump()
