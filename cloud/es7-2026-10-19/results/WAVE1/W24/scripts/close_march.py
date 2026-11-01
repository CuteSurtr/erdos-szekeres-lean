#!/usr/bin/env python3
"""Close one case CNF (or one shard of its top cubes) by cube-and-conquer with cake_lpr-checked leaves.

Copy of results/Mii-S/scripts/close_march.py with these changes (W24, wave 1):
  --shard s --nshards k   process only the top cubes with 0-based line index i, i mod k == s;
  resumable               the top cube file is kept as OUTDIR/top.icnf and reused; SPLIT records
                          store their children ("subs"), so a restart re-queues every cube that has
                          no UNSAT/SAT/SPLIT record yet (OPEN records are retried);
  cake_lpr retry          on "heap space exhausted" the check is re-run once with a larger heap
                          (one such check at a time);
  open.icnf               written at the end: every queued cube without an UNSAT/SAT/SPLIT record,
                          plus UNSAT leaves whose cake_lpr line is not "s VERIFIED UNSAT".
  leaves.icnf             only leaves with cake_lpr "s VERIFIED UNSAT".

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs J [--shard s --nshards k]
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--work", default=None, help="scratch dir for CNFs/proofs (default OUTDIR)")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
W = a.work or a.out; os.makedirs(W, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); biglock = threading.Lock()
LJ = os.path.join(a.out, "leaves.jsonl")
old = [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
log = open(LJ, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, keep=None):
    w = os.path.join(W, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    if keep: subprocess.run(["cp", os.path.join(w, "cubes"), keep])
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
def cake(f, p):
    o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, p], capture_output=True, text=True)
    if "exhausted" in o.stderr:
        with biglock:
            o = subprocess.run([os.path.join(BIN, "cake_lpr"), "--CML_HEAP_SIZE=10000", "--CML_STACK_SIZE=2000", f, p],
                               capture_output=True, text=True)
    return next((l for l in o.stdout.splitlines() if l.startswith("s ")), (o.stdout + o.stderr)[-100:])
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(W, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); subprocess.run(["rm", "-rf", w]); return
    write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        r["cake_lpr"] = cake(f, os.path.join(w, "p.lrat")); r["check_s"] = round(time.time() - t, 2)
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
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
TOP = os.path.join(a.out, "top.icnf")
if not os.path.exists(TOP):
    top, ms, line = march([], a.depth, "top", keep=TOP)
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line,
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(),
         "top_icnf_sha256": hashlib.sha256(open(TOP, "rb").read()).hexdigest(),
         "shard": a.shard, "nshards": a.nshards})
top = [list(map(int, l.split()[1:-1])) for l in open(TOP) if l.startswith("a")]
roots = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
done = {}
for r in old + []:
    if "cube" in r and r["status"] in ("UNSAT", "SAT", "SPLIT"): done[tuple(r["cube"])] = r
def pending(c):
    r = done.get(tuple(c))
    if r is None: return [c]
    if r["status"] == "SPLIT": return [x for s in r["subs"] for x in pending(c + s)]
    return []
todo = [x for c in roots for x in pending(c)]
rec({"start": True, "time": time.time(), "nroots": len(roots), "queued": len(todo), "resumed_records": len(old)})
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
log.close()
leaves = [json.loads(l) for l in open(LJ)]
done = {tuple(r["cube"]): r for r in leaves if "cube" in r and r["status"] in ("UNSAT", "SAT", "SPLIT")}
def walk(c, ok, bad):
    r = done.get(tuple(c))
    if r is None: bad.append(c)
    elif r["status"] == "SPLIT":
        for s in r["subs"]: walk(c + s, ok, bad)
    elif r["status"] == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT": ok.append(c)
    else: bad.append(c)
ok, bad = [], []
for c in roots: walk(c, ok, bad)
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for c in ok: f.write("a " + " ".join(map(str, c)) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in bad: f.write("a " + " ".join(map(str, c)) + " 0\n")
print(json.dumps({"roots": len(roots), "verified_leaves": len(ok), "open": len(bad)}))
