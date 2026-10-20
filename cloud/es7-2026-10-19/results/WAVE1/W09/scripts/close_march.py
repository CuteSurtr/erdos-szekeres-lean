#!/usr/bin/env python3
"""W09 copy of results/Mii-S/scripts/close_march.py (original kept as close_march_orig.py).

Changes:
  --top FILE        use a precomputed `march_cu CASE -d DEPTH` top-cube file (not re-run)
  --shard/--nshards process only the top cubes with 0-based line index i, i % nshards == shard
  resumable         records already in OUTDIR/leaves.jsonl are replayed: a cube with a
                    cake_lpr `s VERIFIED UNSAT` record is closed, a SPLIT record (which now
                    stores its children in "subs") is expanded, anything else is re-queued
  leaves.icnf       only leaves whose cake_lpr line is exactly `s VERIFIED UNSAT`
  open.icnf         cubes not closed when the run stops (deadline or unverified UNSAT)
  --jobs 4 default; all cubes are absolute (CASE + cube units).
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--top")
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
VER = "s VERIFIED UNSAT"
LJ = os.path.join(a.out, "leaves.jsonl")
lock = threading.Lock()
old = [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
log = open(LJ, "a")
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
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception as e: rec({"cube": c, "status": "ERROR", "err": repr(e)})
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
if a.top:
    top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
    if not any(r.get("top") for r in old):
        rec({"top": True, "ncubes": len(top), "top_file": a.top,
             "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
             "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(),
             "shard": a.shard, "nshards": a.nshards})
else:
    top, ms, line = march([], a.depth, "top")
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line,
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
# replay earlier records
byc = {}
for r in old:
    if "cube" in r and r.get("status") in ("UNSAT", "SPLIT", "SAT"): byc.setdefault(tuple(r["cube"]), r)
    if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: byc[tuple(r["cube"])] = r
def frontier(c, out, final=False):
    r = byc.get(tuple(c))
    if r and r["status"] == "UNSAT" and r.get("cake_lpr") == VER: return
    if r and r["status"] == "SPLIT" and "subs" in r:
        for s in r["subs"]: frontier(c + s, out, final)
        return
    if r and r["status"] == "SAT" and not final: return
    out.append(c)
todo = []
for c in mine: frontier(c, todo)
rec({"resume": True, "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "nmine": len(mine), "todo": len(todo)})
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
log.close()
recs = [json.loads(l) for l in open(LJ)]
byc = {}
for r in recs:
    if "cube" in r and r.get("status") in ("UNSAT", "SPLIT", "SAT"): byc.setdefault(tuple(r["cube"]), r)
    if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: byc[tuple(r["cube"])] = r
openc = []
for c in mine: frontier(c, openc, True)
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    seen = set()
    for r in recs:
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER and tuple(r["cube"]) not in seen:
            seen.add(tuple(r["cube"])); f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in openc: f.write("a " + " ".join(map(str, c)) + " 0\n")
print("mine", len(mine), "open", len(openc))
