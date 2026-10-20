#!/usr/bin/env python3
"""Close one case CNF by cube-and-conquer (the Mi recipe) with cake_lpr-checked leaves.

Copy of results/Mii-S/scripts/close_march.py with W03 changes:
  --top FILE         reuse a precomputed `march_cu CASE -d DEPTH` top-cube file (same for all shards)
  --shard/--nshards  process only top cubes with 0-based line index i, i mod nshards == shard
  --work DIR         scratch dir for CNF/proof files (kept out of the results dir)
  --deadline EPOCH   no new cadical call is started after this time
  resumable: on start, leaves.jsonl is replayed; cubes with a final record (UNSAT verified, SPLIT,
  SAT) are skipped, children of SPLIT records are re-queued, everything else is re-solved.
  SPLIT records carry their children ("subs").  An UNSAT whose cake_lpr line is not
  `s VERIFIED UNSAT` is not a leaf.
At the end: leaves.icnf = cake_lpr-verified UNSAT leaves, open.icnf = cubes still open.

  close_march.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --timeout 300 --split-depth 6 --jobs J
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--deadline", type=float, default=0)
ap.add_argument("--top"); ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--work")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
WORK = a.work or a.out; os.makedirs(WORK, exist_ok=True)
deadline = a.deadline or time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
VER = "s VERIFIED UNSAT"
LJ = os.path.join(a.out, "leaves.jsonl")
lock = threading.Lock()
old = [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
log = open(LJ, "a")
def rec(r):
    r["t"] = round(time.time(), 1)
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
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); return
    w = os.path.join(WORK, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time(); c0 = os.times()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(WORK, f"SAT_{k}.cnf")])
        subprocess.run([os.path.join(BIN, "cadical"), "-q", f], stdout=open(os.path.join(a.out, f"SAT_{k}.model"), "w"))
    else:
        r["status"] = "SPLIT"; r["rc"] = rc; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    c1 = os.times(); r["cpu_s"] = round(c1.children_user + c1.children_system - c0.children_user - c0.children_system, 1)
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception:
        import traceback; traceback.print_exc(); rec({"cube": c, "status": "ERROR", "err": traceback.format_exc()[-300:]})
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
case_sha = hashlib.sha256(open(a.case, "rb").read()).hexdigest()
if a.top:
    top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
    line = "precomputed " + hashlib.sha256(open(a.top, "rb").read()).hexdigest(); ms = 0
else:
    top, ms, line = march([], a.depth, "top")
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
if not old:
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line, "case_sha256": case_sha,
         "shard": a.shard, "nshards": a.nshards, "nmine": len(mine)})
else:
    rec({"resume": True, "case_sha256": case_sha, "nold": len(old)})
# replay: final records close their cube (SPLIT children re-queued); anything else is re-solved
done, splits = set(), {}
for r in old:
    if "cube" not in r: continue
    k = tuple(r["cube"])
    if r["status"] == "SPLIT": done.add(k); splits[k] = r["subs"]
    elif r["status"] == "SAT" or (r["status"] == "UNSAT" and r.get("cake_lpr") == VER): done.add(k)
def pending(c):
    k = tuple(c)
    if k not in done: return [c]
    return [x for s in splits.get(k, []) for x in pending(c + s)]
todo = [x for c in mine for x in pending(c)]
print(f"top {len(top)} mine {len(mine)} todo {len(todo)}", flush=True)
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
recs = [json.loads(l) for l in open(LJ)]
final = {}
for r in recs:
    if "cube" in r: final[tuple(r["cube"])] = r
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for r in recs:
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
done, splits = set(), {}
for r in recs:
    if "cube" not in r: continue
    k = tuple(r["cube"])
    if r["status"] == "SPLIT": done.add(k); splits[k] = r["subs"]
    elif r["status"] == "UNSAT" and r.get("cake_lpr") == VER: done.add(k)
openc = [x for c in mine for x in pending(c)]
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in openc: f.write("a " + " ".join(map(str, c)) + " 0\n")
print(f"done: open {len(openc)}", flush=True)
