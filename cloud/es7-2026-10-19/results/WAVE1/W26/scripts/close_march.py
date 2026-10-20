#!/usr/bin/env python3
"""W26 variant of results/Mii-S/scripts/close_march.py (original copied as close_march_orig.py).

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs J
                 [--shard s --nshards k] [--hours H] [--whole 60]
Changes from the original:
- resumable: OUTDIR/top.icnf is the march_cu -d DEPTH output, made once and reused; on restart
  leaves.jsonl is replayed: cubes with a cake_lpr "s VERIFIED UNSAT" record are done, SPLIT
  records (which now store their children in "subs") are expanded, everything else is re-queued;
- --shard/--nshards: only top cubes with 0-based line index i, i mod k == s;
- --whole T: first try plain cadical -t T on the whole case (accepted only with cake_lpr);
- leaves.icnf lists only leaves whose cake_lpr line is "s VERIFIED UNSAT";
  open.icnf lists the cubes still open at the end (deadline, failed check, or a split with 0 children);
- a split that yields no children re-solves the cube with timeout 10*TIMEOUT instead.
"""
import argparse, hashlib, json, os, re, signal, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/home/user/bin")
OK = "s VERIFIED UNSAT"
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1); ap.add_argument("--whole", type=int, default=0)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
case_sha = hashlib.sha256(open(a.case, "rb").read()).hexdigest()
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LJ = os.path.join(a.out, "leaves.jsonl")
old = [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
log = open(LJ, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def run(cmd, **kw):
    p = subprocess.Popen(cmd, start_new_session=True, **kw)
    out, _ = p.communicate(); return p.returncode, out
def march(cube, d, w, dest):
    os.makedirs(w, exist_ok=True); write(os.path.join(w, "f.cnf"), cube); t = time.time()
    _, o = run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o", dest],
               stdout=subprocess.PIPE, text=True)
    cs = [list(map(int, l.split()[1:-1])) for l in open(dest) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    return cs, time.time() - t, m.group(0) if m else o[-200:]
def solve_cnf(f, w, timeout):
    """cadical --lrat -t timeout, cake_lpr on UNSAT. Returns record fields."""
    t = time.time(); p = os.path.join(w, "p.lrat")
    rc, _ = run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(timeout), f, p],
                stdout=subprocess.DEVNULL)
    r = {"solve_s": round(time.time() - t, 2)}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(p); t = time.time()
        _, o = run([os.path.join(BIN, "cake_lpr"), f, p], stdout=subprocess.PIPE, text=True)
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:])
        r["check_s"] = round(time.time() - t, 2); r["status"] = "UNSAT"
    elif rc == 10: r["status"] = "SAT"
    else: r["status"] = "UNKNOWN"
    if os.path.exists(p): os.remove(p)
    return r
def finish(open_cubes):
    leaves = [json.loads(l) for l in open(LJ)]
    with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
        for r in leaves:
            if "cube" in r and r.get("status") == "UNSAT" and r.get("cake_lpr") == OK:
                f.write("a " + " ".join(map(str, r["cube"] + [0])) + "\n")
    with open(os.path.join(a.out, "open.icnf"), "w") as f:
        for c in open_cubes: f.write("a " + " ".join(map(str, c + [0])) + "\n")

# whole-case attempt
if a.whole and not any(r.get("whole") for r in old):
    w = os.path.join(a.out, "s_whole"); os.makedirs(w, exist_ok=True)
    r = solve_cnf(a.case, w, a.whole); subprocess.run(["rm", "-rf", w])
    r.update(whole=True, timeout=a.whole, case_sha256=case_sha); rec(r); old.append(r)
    if r["status"] == "SAT": subprocess.run(["cp", a.case, os.path.join(a.out, "SAT_whole.cnf")])
wh = next((r for r in old if r.get("whole") and r.get("status") == "UNSAT" and r.get("cake_lpr") == OK), None)
if wh:
    rec({"cube": [], "status": "UNSAT", "cake_lpr": OK, "from_whole": True, "case_sha256": case_sha})
    finish([]); print("CLOSED whole"); raise SystemExit(0)

# top cubes (made once)
TOP = os.path.join(a.out, "top.icnf")
if not os.path.exists(TOP):
    top, ms, line = march([], a.depth, os.path.join(a.out, "m_top"), TOP); subprocess.run(["rm", "-rf", os.path.join(a.out, "m_top")])
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line, "case_sha256": case_sha,
         "top_sha256": hashlib.sha256(open(TOP, "rb").read()).hexdigest(), "shard": a.shard, "nshards": a.nshards})
top = [list(map(int, l.split()[1:-1])) for l in open(TOP) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]

done = {tuple(r["cube"]) for r in old if "cube" in r and r.get("status") == "UNSAT" and r.get("cake_lpr") == OK}
splits = {tuple(r["cube"]): r["subs"] for r in old if r.get("status") == "SPLIT" and "subs" in r}
longt = {tuple(r["cube"]) for r in old if r.get("status") == "NOSPLIT"}
sat = [r for r in old if r.get("status") == "SAT"]
pending = set(); ctr = [len(old)]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]
def solve(cube, timeout):
    with lock: ctr[0] += 1; k = ctr[0]
    if time.time() > deadline: return
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); r = {"cube": cube, "timeout": timeout}; r.update(solve_cnf(f, w, timeout))
    if r["status"] == "SAT": subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")]); sat.append(r)
    subs = []
    if r["status"] == "UNKNOWN" and timeout == a.timeout:
        subs, ms, line = march(cube, a.split_depth, os.path.join(w, "m"), os.path.join(w, "cubes"))
        r.update(status="SPLIT" if subs else "NOSPLIT", split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    with lock:
        if r["status"] == "UNSAT" and r.get("cake_lpr") == OK: pending.discard(tuple(cube))
    if r["status"] == "SPLIT":
        with lock: pending.discard(tuple(cube))
        for s in subs: submit(cube + s, a.timeout)
    elif r["status"] == "NOSPLIT": submit(cube, 10 * a.timeout)
def task(c, t):
    try: solve(c, t)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c, t):
    with lock: pending.add(tuple(c))
    with cv: count[0] += 1
    pool.submit(task, c, t)
def expand(c):
    t = tuple(c)
    if t in done: return
    if t in splits:
        for s in splits[t]: expand(c + s)
    else: submit(c, 10 * a.timeout if t in longt else a.timeout)
for c in mine: expand(c)
with cv:
    while count[0] > 0: cv.wait()
finish(sorted(pending, key=len))
print("OPEN" if pending else "CLOSED", len(pending), "SAT" if sat else "")
