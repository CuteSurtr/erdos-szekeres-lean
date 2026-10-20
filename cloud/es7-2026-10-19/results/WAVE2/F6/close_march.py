#!/usr/bin/env python3
"""W19 copy of results/Mii-S/scripts/close_march.py with sharding, resume and a deadline.

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs 4 \
      [--shard s --nshards k] [--top TOP.icnf] [--hours H]
Changes against the original:
- top cubes come from `march_cu CASE -d DEPTH -o OUTDIR/top.icnf` (run once, reused if present);
  with --nshards k only the cubes with 0-based line index i, i mod k == s are processed;
- a leaf counts as closed only when cake_lpr prints `s VERIFIED UNSAT` (other verdicts are kept
  as status UNSAT_UNCHECKED and stay open); leaves.icnf lists only the verified leaves;
- SPLIT records carry the sub-cubes ("subs"), so a restart rebuilds the frontier from
  leaves.jsonl and continues (resumable); open.icnf lists the frontier still open;
- no cube is started when less than TIMEOUT seconds remain before the deadline;
- the solver stdout is kept for SAT answers (SAT_k.cnf, SAT_k.out).
"""
import argparse, hashlib, json, os, re, subprocess, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
WORK = os.environ.get("WORK", "/opt/work/tmp"); os.makedirs(WORK, exist_ok=True)  # F2: scratch root for mkdtemp
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--top")
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--name")  # F2: case name for the first leaves.jsonl record (default: CNF basename)
ap.add_argument("--skip")  # F2: file of cubes closed elsewhere (step d); re-read when it changes
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
LJ = os.path.join(a.out, "leaves.jsonl")
lock = threading.Lock()
def rec(r):
    with lock:
        with open(LJ, "a") as log: log.write(json.dumps(r) + "\n")
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, outfile=None):
    w = tempfile.mkdtemp(prefix=f"m_{tag}_", dir=WORK)  # F2 (a): fresh directory per job
    write(os.path.join(w, "f.cnf"), cube); t = time.time(); cf = outfile or os.path.join(w, "cubes")
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o", cf],
                       capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
VER = "s VERIFIED UNSAT"
def load():
    rs = [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
    closed, split = set(), {}
    for r in rs:
        if "cube" not in r: continue
        c = tuple(r["cube"])
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: closed.add(c)
        elif r.get("status") == "SKIP": closed.add(c)   # F2 (d): closed elsewhere; not in leaves.icnf
        elif r.get("status") == "SPLIT" and "subs" in r: split[c] = r["subs"]
    return rs, closed, split
def frontier(roots, closed, split):
    out, st = [], list(reversed(roots))
    while st:
        c = st.pop()
        if tuple(c) in closed: continue
        if tuple(c) in split: st.extend(reversed([c + s for s in split[tuple(c)]])); continue
        out.append(c)
    return out
def cake(f, p, extra=()):
    r = subprocess.run([os.path.join(BIN, "cake_lpr"), *extra, f, p], capture_output=True, text=True)
    return next((l for l in r.stdout.splitlines() if l.startswith("s ")), (r.stdout + r.stderr)[-120:])
skipset, skipm = set(), [None]
def skipped(cube):  # F2 (d): exact cubes listed in --skip (computed outside from others' verified leaves)
    if not a.skip or not os.path.exists(a.skip): return False
    with lock:
        m = os.path.getmtime(a.skip)
        if m != skipm[0]:
            skipset.clear(); skipm[0] = m
            for l in open(a.skip):
                if l.startswith("a ") and l.endswith(" 0\n"): skipset.add(tuple(map(int, l.split()[1:-1])))
        return tuple(cube) in skipset
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]; inflight = {}
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() + a.timeout > deadline: return   # left open, rebuilt on resume
    if skipped(cube): rec({"cube": cube, "status": "SKIP", "why": "closed elsewhere"}); return  # F2 (d)
    w = tempfile.mkdtemp(prefix=f"s_{k}_", dir=WORK); f = os.path.join(w, "f.cnf")  # F2 (a): fresh directory per job
    write(f, cube); t = time.time(); c0 = os.times()
    with open(os.path.join(w, "out"), "w") as so:
        rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                             os.path.join(w, "p.lrat")], stdout=so).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        v = cake(f, os.path.join(w, "p.lrat"))
        if v != VER and "heap" in v.lower():
            v = cake(f, os.path.join(w, "p.lrat"), ["--CML_HEAP_SIZE=10000", "--CML_STACK_SIZE=4000"]); r["cake_retry"] = True
        r["cake_lpr"] = v; r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if v == VER else "UNSAT_UNCHECKED"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        subprocess.run(["cp", os.path.join(w, "out"), os.path.join(a.out, f"SAT_{k}.out")])
    elif time.time() > deadline:
        r["status"] = "TIMEOUT"   # no split after the deadline; stays open
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
        if not subs or any(not x for x in subs):  # F6: march refuted it or gave no cubes; child == parent would loop
            r["status"] = "SPLIT_FAIL"; del r["subs"]
    c1 = os.times(); r["cpu_s"] = round(c1.children_user + c1.children_system - c0.children_user - c0.children_system, 1)
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
topf = os.path.join(a.out, "top.icnf")
if a.top and not os.path.exists(topf): subprocess.run(["cp", a.top, topf])
if not os.path.exists(LJ):  # F2 (c): first record names the case
    rec({"case": a.name or os.path.basename(a.case).rsplit(".", 1)[0],
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
rs, closed, split = load()
if not os.path.exists(topf):
    _, ms, line = march([], a.depth, "top", topf)
    rec({"top": True, "march_s": round(ms, 1), "march": line})
lines = open(topf).read().splitlines()
alltop = [list(map(int, l.split()[1:-1])) for l in lines]
assert all(l.startswith("a ") for l in lines)
mine = [c for i, c in enumerate(alltop) if i % a.nshards == a.shard]
if not any(r.get("top") and "top_sha256" in r for r in rs):
    rec({"top": True, "ncubes": len(alltop), "shard": a.shard, "nshards": a.nshards, "nmine": len(mine),
         "top_sha256": hashlib.sha256(open(topf, "rb").read()).hexdigest(),
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
todo = frontier(mine, closed, split)
rec({"resume": True, "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "frontier": len(todo)})
def finalize():
    rs, closed, split = load()
    def atomic(name, cubes):  # F2 (b): write a temporary file, then rename into place
        fd, tmp = tempfile.mkstemp(prefix="." + name + ".", dir=a.out)
        with os.fdopen(fd, "w") as f:
            for c in cubes: f.write("a " + " ".join(map(str, c)) + " 0\n")
        os.chmod(tmp, 0o644); os.replace(tmp, os.path.join(a.out, name))
    atomic("leaves.icnf", [r["cube"] for r in rs if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER])
    op = frontier(mine, closed, split)
    atomic("open.icnf", op)
    return len(op)
for c in todo: submit(c)
with cv:
    while count[0] > 0:
        cv.wait(600)
        with lock: finalize()
with lock: print("open", finalize())
