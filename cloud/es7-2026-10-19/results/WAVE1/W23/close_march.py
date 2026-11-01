#!/usr/bin/env python3
"""Close one case CNF (or one shard of its top cubes) by cube-and-conquer with cake_lpr-checked leaves.

Copy of results/Mii-S/scripts/close_march.py with these W23 changes:
  --top FILE        use a precomputed `march_cu CASE -d DEPTH -o FILE` top-cube file
  --shard/--nshards process only top cubes with 0-based index i (over the `a` lines), i mod k == s
  resumable         records already in OUTDIR/leaves.jsonl are reused: a cube with cake_lpr
                    `s VERIFIED UNSAT` is done, a SPLIT record (which now stores its `subs`) is expanded
                    into its children, anything else (OPEN, unchecked UNSAT, in flight) is redone
  open.icnf         written at the end: every cube of the shard not closed by a verified leaf
  leaves.icnf       only leaves whose cake_lpr verdict is `s VERIFIED UNSAT`

  close_march.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --timeout 300 --split-depth 6 --jobs J
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w23/bin")
VER = "s VERIFIED UNSAT"
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--top")
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lp = os.path.join(a.out, "leaves.jsonl")
old = {}
if os.path.exists(lp):
    for l in open(lp):
        try: r = json.loads(l)
        except ValueError: continue
        if "cube" in r: old[tuple(r["cube"])] = r
lock = threading.Lock(); log = open(lp, "a")
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
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); return
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
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        subprocess.run(["touch", os.path.join(a.out, "SAT_FOUND")])
    else:
        subprocess.run(["rm", "-f", os.path.join(w, "p.lrat")])
        if time.time() > deadline:
            r.update(status="OPEN", reason="timeout_after_deadline")
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
    r = old.get(tuple(c))
    if r is not None and r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: return
    if r is not None and r.get("status") == "SPLIT" and "subs" in r:
        for s in r["subs"]: submit(c + s)
        return
    with cv: count[0] += 1
    pool.submit(task, c)
if a.top:
    top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
    line = "precomputed " + a.top; ms = 0.0
else:
    top, ms, line = march([], a.depth, "top")
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
rec({"top": True, "ncubes": len(top), "nmine": len(mine), "shard": a.shard, "nshards": a.nshards,
     "march_s": round(ms, 1), "march": line, "resumed_records": len(old),
     "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest() if a.top else None,
     "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
for c in mine: submit(c)
with cv:
    while count[0] > 0: cv.wait()
log.close()
recs = {}
for l in open(lp):
    r = json.loads(l)
    if "cube" in r: recs[tuple(r["cube"])] = r
closed, opn = [], []
def walk(c):
    r = recs.get(tuple(c))
    if r is not None and r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: closed.append(c)
    elif r is not None and r.get("status") == "SPLIT" and "subs" in r:
        for s in r["subs"]: walk(c + s)
    else: opn.append(c)
for c in mine: walk(c)
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for c in closed: f.write("a " + " ".join(map(str, c)) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in opn: f.write("a " + " ".join(map(str, c)) + " 0\n")
print(json.dumps({"closed_leaves": len(closed), "open": len(opn)}))
