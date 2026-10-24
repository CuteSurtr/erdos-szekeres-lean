#!/usr/bin/env python3
"""W15 version of results/Mii-S/scripts/close_march.py (original copied as close_march.orig.py).

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs 4 [--shard s --nshards k] [--hours H]
Changes against the original:
  * top cubes go to OUTDIR/top.icnf (sha256, cube count and refuted count recorded); an existing
    top.icnf is reused, so all runs of a case use the same file;
  * --shard/--nshards: only top cubes with 0-based line index i, i mod k == s are processed;
  * resumable: leaves.jsonl is replayed on start (verified leaves are done, SPLIT records list
    their children, everything else is redone);
  * a leaf counts as closed only if cake_lpr printed `s VERIFIED UNSAT`; leaves.icnf lists only
    those; open.icnf lists every cube of the part not yet closed (rewritten periodically);
  * on SAT the CNF and cadical's model are kept as SAT_<k>.cnf / SAT_<k>.out.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w15/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--work", default=None)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
WORK = a.work or a.out; os.makedirs(WORK, exist_ok=True)
deadline = time.time() + a.hours * 3600
VER = "s VERIFIED UNSAT"
raw = open(a.case, "rb").read(); case_sha = hashlib.sha256(raw).hexdigest()
hdr, body = raw.decode().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LP = os.path.join(a.out, "leaves.jsonl")
def rec(r):
    with lock:
        with open(LP, "a") as f: f.write(json.dumps(r) + "\n")
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, keep=None):
    w = os.path.join(WORK, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time(); cf = keep or os.path.join(w, "cubes")
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o", cf],
                       capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-300:]
# ---- top cubes
TOP = os.path.join(a.out, "top.icnf")
if not os.path.exists(TOP):
    top, ms, line = march([], a.depth, "top", keep=TOP + ".tmp"); os.rename(TOP + ".tmp", TOP)
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line, "case_sha256": case_sha,
         "top_sha256": hashlib.sha256(open(TOP, "rb").read()).hexdigest(), "depth": a.depth})
top = [list(map(int, l.split()[1:-1])) for l in open(TOP) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
# ---- replay
done = {}  # tuple(cube) -> record (VERIFIED UNSAT or SPLIT with subs)
if os.path.exists(LP):
    for l in open(LP):
        r = json.loads(l)
        if "cube" not in r: continue
        k = tuple(r["cube"])
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: done[k] = r
        elif r.get("status") == "SPLIT" and "subs" in r: done[k] = r
        elif r.get("status") == "SAT": done[k] = r
pending = []
def expand(c):
    r = done.get(tuple(c))
    if r is None: pending.append(c)
    elif r["status"] == "SPLIT":
        for s in r["subs"]: expand(c + s)
for c in mine: expand(c)
rec({"start": True, "shard": a.shard, "nshards": a.nshards, "mine": len(mine), "pending": len(pending),
     "case_sha256": case_sha, "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
openset = {tuple(c) for c in pending}
def dump_open():
    with lock: cs = sorted(openset, key=lambda c: (len(c), c))
    with open(os.path.join(a.out, "open.icnf.tmp"), "w") as f:
        for c in cs: f.write("a " + " ".join(map(str, c)) + " 0\n")
    os.rename(os.path.join(a.out, "open.icnf.tmp"), os.path.join(a.out, "open.icnf"))
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [int(time.time())]
def solve(cube):
    if time.time() > deadline: return
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(WORK, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time(); t0 = os.times()
    with open(os.path.join(w, "out"), "w") as so:
        rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                             os.path.join(w, "p.lrat")], stdout=so).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        subprocess.run(["cp", os.path.join(w, "out"), os.path.join(a.out, f"SAT_{k}.out")])
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    with lock:
        if r["status"] == "SPLIT" or (r["status"] == "UNSAT" and r["cake_lpr"] == VER): openset.discard(tuple(cube))
        for s in subs: openset.add(tuple(cube + s))
    for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception as e: rec({"cube": c, "status": "ERROR", "err": repr(e)})
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
# biggest work first is unknown; keep file order
for c in pending: submit(c)
last = 0
with cv:
    while count[0] > 0:
        cv.wait(60)
        if time.time() - last > 120: cv.release(); dump_open(); cv.acquire(); last = time.time()
dump_open()
leaves = [json.loads(l) for l in open(LP)]
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    seen = set()
    for r in leaves:
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER and tuple(r["cube"]) not in seen:
            seen.add(tuple(r["cube"])); f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
rec({"end": True, "open": len(openset), "verified_leaves": len(seen), "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
