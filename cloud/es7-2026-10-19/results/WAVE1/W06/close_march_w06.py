#!/usr/bin/env python3
"""W06 copy of results/Mii-S/scripts/close_march.py, changed for sharded, resumable runs.

  close_march_w06.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --jobs 4 --hours H
Changes from the original:
- the top cubes come from TOP.icnf (`march_cu CASE -d 7 -o TOP.icnf`, run once, kept); only the
  cubes with 0-based line index i, i mod K == S are processed;
- resumable: on start, OUTDIR/leaves.jsonl is replayed.  A cube with an UNSAT record whose
  cake_lpr line is `s VERIFIED UNSAT` is done; a SPLIT record stores its sub-cubes ("subs"), which
  are followed; every other cube is queued again;
- an UNSAT answer counts only with cake_lpr `s VERIFIED UNSAT` (otherwise status UNSAT_UNCHECKED,
  left open);
- at the deadline no new cube is started; OUTDIR/open.icnf lists the frontier cubes still open;
- leaves.icnf lists only cake_lpr-verified leaves.
Solver settings are unchanged: cadical --lrat -t TIMEOUT, cake_lpr on each UNSAT, march_cu -d SPLIT.
"""
import argparse, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/home/user/tools/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--work", default=None)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
WK = a.work or a.out; os.makedirs(WK, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LJ = os.path.join(a.out, "leaves.jsonl")
VER = "s VERIFIED UNSAT"
# replay
done, splits = set(), {}
if os.path.exists(LJ):
    for l in open(LJ):
        r = json.loads(l)
        if "cube" not in r: continue
        k = tuple(r["cube"])
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: done.add(k)
        elif r.get("status") == "SPLIT" and "subs" in r: splits[k] = r["subs"]
        elif r.get("status") == "SAT": print("SAT record present:", r, flush=True)
log = open(LJ, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag):
    w = os.path.join(WK, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
openset = []
def solve(cube):
    if time.time() > deadline:
        with lock: openset.append(cube)
        return
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(WK, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time(); t0 = os.times()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}; subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if r["cake_lpr"] == VER else "UNSAT_UNCHECKED"
        if r["status"] != "UNSAT":
            with lock: openset.append(cube)
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        with lock: openset.append(cube)
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    t1 = os.times(); r["cpu_s"] = round(t1.children_user + t1.children_system - t0.children_user - t0.children_system, 2)
    subprocess.run(["rm", "-rf", w]); rec(r)
    for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception as e:
        with lock: openset.append(c)
        print("error", c, e, flush=True)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    k = tuple(c)
    if k in done: return
    if k in splits:
        for s in splits[k]: submit(c + s)
        return
    with cv: count[0] += 1
    pool.submit(task, c)
top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
rec({"start": True, "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ntop": len(top),
     "nmine": len(mine), "shard": a.shard, "nshards": a.nshards, "resumed_done": len(done), "resumed_splits": len(splits)})
for c in mine: submit(c)
with cv:
    while count[0] > 0: cv.wait()
pool.shutdown()
leaves = [json.loads(l) for l in open(LJ)]
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    seen = set()
    for r in leaves:
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER and tuple(r["cube"]) not in seen:
            seen.add(tuple(r["cube"])); f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in openset: f.write("a " + " ".join(map(str, c)) + " 0\n")
rec({"end": True, "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "nleaves": len(seen), "nopen": len(openset)})
print("done", len(seen), "leaves,", len(openset), "open", flush=True)
