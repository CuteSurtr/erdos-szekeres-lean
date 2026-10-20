#!/usr/bin/env python3
"""Close one case CNF by cube-and-conquer (the Mi recipe) with cake_lpr-checked leaves.

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs J
march_cu CASE -d DEPTH gives the top cubes (refuted leaves included, so the file is a full
partition).  Each cube c: CASE + units(c) is solved by `cadical --lrat -t TIMEOUT` and an UNSAT
answer is checked with cake_lpr (proof deleted afterwards).  A cube that times out is split by
`march_cu CASE+units(c) -d SPLIT` and its children c+s are queued.  Records go to
OUTDIR/leaves.jsonl; OUTDIR/leaves.icnf (written at the end) lists every closed leaf as
`a lits 0` for `cover_check` (H3) relative to CASE.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
WORK = os.environ.get("WORK", "/tmp/close_march_work"); os.makedirs(WORK, exist_ok=True)  # CNFs/proofs stay out of OUTDIR
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9)
# W01 additions: shard the top cubes (0-based line index i, i mod nshards == shard), reuse a fixed
# top-cube file, resume from leaves.jsonl, write open.icnf, and count only cake_lpr-verified leaves.
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--top", default=None, help="precomputed march_cu -d DEPTH cube file for CASE")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); log = open(os.path.join(a.out, "leaves.jsonl"), "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag):
    w = os.path.join(WORK, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(WORK, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); subprocess.run(["rm", "-rf", w]); return
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if r["cake_lpr"].strip() == "s VERIFIED UNSAT" else "UNCHECKED"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(WORK, f"SAT_{k}.cnf")])
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
    with cv: count[0] += 1
    pool.submit(task, c)
VER = "s VERIFIED UNSAT"
if a.top:
    lines = [l for l in open(a.top) if l.strip()]
    top = [list(map(int, l.split()[1:-1])) for l in lines]
    assert all(l.startswith("a ") for l in lines)
    mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
    prev = [json.loads(l) for l in open(os.path.join(a.out, "leaves.jsonl"))]
    if not any(r.get("top") for r in prev):
        rec({"top": True, "ncubes": len(top), "top_file": a.top, "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
             "shard": a.shard, "nshards": a.nshards, "nmine": len(mine),
             "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
else:
    top, ms, line = march([], a.depth, "top"); mine = top; prev = []
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line,
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
# resume: walk the recorded tree from my top cubes; closed leaves stay closed, recorded splits are
# expanded from their stored children, everything else (OPEN, UNCHECKED, unrecorded) is solved again.
done = {}
for r in prev:
    if "cube" in r and r.get("status") in ("UNSAT", "SPLIT"): done[tuple(r["cube"])] = r
def walk(c):
    r = done.get(tuple(c))
    if r is None or (r["status"] == "SPLIT" and "subs" not in r): submit(c)
    elif r["status"] == "SPLIT":
        for s in r["subs"]: walk(c + s)
if prev: rec({"resume": True, "time": time.time()})
for c in mine: walk(c)
with cv:
    while count[0] > 0: cv.wait()
leaves = [json.loads(l) for l in open(os.path.join(a.out, "leaves.jsonl"))]
final = {}
for r in leaves:
    if "cube" in r: final[tuple(r["cube"])] = r
closed, opened = [], []
def fin(c):
    r = final.get(tuple(c))
    if r and r.get("status") == "UNSAT" and r.get("cake_lpr", "").strip() == VER: closed.append(c)
    elif r and r.get("status") == "SPLIT" and "subs" in r:
        for s in r["subs"]: fin(c + s)
    else: opened.append(c)
for c in mine: fin(c)
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for c in closed: f.write("a " + " ".join(map(str, c)) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in opened: f.write("a " + " ".join(map(str, c)) + " 0\n")
rec({"final": True, "closed": len(closed), "open": len(opened)})
