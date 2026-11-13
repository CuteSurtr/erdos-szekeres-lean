#!/usr/bin/env python3
"""W17 copy of results/Mii-S/scripts/close_march.py with --shard/--nshards, a shared top-cube
file (--top), a separate scratch dir (--work, CNF/LRAT never land in OUT), resume from
OUT/leaves.jsonl, and OUT/leaves.icnf (cake_lpr-verified leaves only) + OUT/open.icnf rewritten
every --flush seconds and at the end.

  close_march.py CASE.cnf OUT --top top.icnf --shard s --nshards k --work W --jobs 4 --hours H
Top cubes with 0-based line index i (over the `a` lines of top.icnf), i mod k == s, are this
shard's part.  Each cube c: CASE + units(c) is solved by `cadical --lrat -t TIMEOUT`; UNSAT is
checked by cake_lpr (retried once with an 8 GB heap); only `s VERIFIED UNSAT` closes a leaf.
A timeout splits c with `march_cu CASE+units(c) -d SPLIT` (children c+s, kept in the record as
"subs").  On resume the frontier is: shard cubes and recorded children with no VERIFIED or SPLIT
record.  SAT: the CNF and cadical's model are kept in WORK and OUT/SAT_<k>.model.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/opt/es7/work/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--work", required=True)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--timeout", type=int, default=300); ap.add_argument("--split-depth", type=int, default=6)
ap.add_argument("--jobs", type=int, default=4); ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--flush", type=int, default=300)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); os.makedirs(a.work, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
VER = "s VERIFIED UNSAT"
lock = threading.Lock(); LJ = os.path.join(a.out, "leaves.jsonl")
top = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
# resume state
done, known, n = {}, [tuple(c) for c in mine], [0]
if os.path.exists(LJ):
    for l in open(LJ):
        r = json.loads(l)
        if "cube" not in r: continue
        n[0] = max(n[0], r.get("k", 0)); c = tuple(r["cube"])
        if r["status"] == "SPLIT":
            done[c] = "SPLIT"; known += [c + tuple(s) for s in r["subs"]]
        elif r["status"] == "UNSAT" and r.get("cake_lpr") == VER: done[c] = "UNSAT"
        elif r["status"] == "SAT": done[c] = "SAT"
log = open(LJ, "a")
def rec(r):
    with lock:
        log.write(json.dumps(r) + "\n"); log.flush()
        if "cube" in r:
            c = tuple(r["cube"])
            if r["status"] == "SPLIT": done[c] = "SPLIT"; known.extend(c + tuple(s) for s in r["subs"])
            elif r["status"] == "UNSAT" and r.get("cake_lpr") == VER: done[c] = "UNSAT"
            elif r["status"] == "SAT": done[c] = "SAT"
def flush():
    with lock:
        lv = [c for c in known if done.get(c) == "UNSAT"]; op = [c for c in known if c not in done or done[c] == "SAT"]
    for name, cs in (("leaves.icnf", lv), ("open.icnf", op)):
        with open(os.path.join(a.out, name + ".tmp"), "w") as f:
            f.writelines("a " + " ".join(map(str, c)) + " 0\n" for c in cs)
        os.replace(os.path.join(a.out, name + ".tmp"), os.path.join(a.out, name))
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag):
    w = os.path.join(a.work, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
def cake(f, p, heap=None):
    cmd = [os.path.join(BIN, "cake_lpr")] + ([f"--CML_HEAP_SIZE={heap}"] if heap else []) + [f, p]
    o = subprocess.run(cmd, capture_output=True, text=True)
    return next((l for l in o.stdout.splitlines() if l.startswith("s ")), (o.stdout + o.stderr)[-150:])
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]
def solve(cube):
    if time.time() > deadline: return
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(a.work, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    with open(os.path.join(w, "out"), "w") as so:
        rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                             os.path.join(w, "p.lrat")], stdout=so).returncode
    st = round(time.time() - t, 2); r = {"k": k, "cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        v = cake(f, os.path.join(w, "p.lrat"))
        if v != VER: r["cake_lpr_first"] = v; v = cake(f, os.path.join(w, "p.lrat"), 8192)
        r["cake_lpr"] = v; r["check_s"] = round(time.time() - t, 2); r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.work, f"SAT_{k}.cnf")])
        subprocess.run(["cp", os.path.join(w, "out"), os.path.join(a.out, f"SAT_{k}.model")])
    else:
        r["status"] = "SPLIT"; r["rc"] = rc; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception as e: rec({"error": repr(e), "cube_err": c})
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
rec({"start": True, "time": time.time(), "shard": a.shard, "nshards": a.nshards, "ntop": len(top), "nmine": len(mine),
     "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
     "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(), "resumed_done": len(done)})
for c in list(known):
    if c not in done: submit(list(c))
with cv:
    while count[0] > 0:
        cv.wait(a.flush); flush()
flush(); rec({"end": True, "time": time.time()})
