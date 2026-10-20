#!/usr/bin/env python3
"""Close one case CNF (or one shard of its top cubes) by cube-and-conquer with cake_lpr-checked leaves.

W14 copy of results/Mii-S/scripts/close_march.py (original kept as close_march.orig.py). Changes:
  --top FILE        use a precomputed `march_cu CASE -d DEPTH -o FILE` top-cube file
                    (otherwise march_cu is run and its output saved to OUTDIR/top.icnf)
  --shard S --nshards K   process only top cubes with 0-based line index i, i % K == S
  --work DIR        scratch dir for CNF/LRAT files (kept out of OUTDIR, deleted after use)
  resumable: on start, OUTDIR/leaves.jsonl is replayed; a cube with a cake_lpr-verified UNSAT
  record is a leaf, a SPLIT record (which now stores its children `subs`) expands into its
  children, anything else (no record, deadline OPEN, unverified UNSAT) is queued again.
  --report          only rewrite leaves.icnf / open.icnf from leaves.jsonl, solve nothing
  leaves.icnf: only leaves whose cake_lpr line is `s VERIFIED UNSAT`; open.icnf: the open frontier.
  On SAT the cadical model is saved to OUTDIR/SAT_k.model (CNF copy goes to WORK, not OUTDIR).
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--top"); ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--work", default="/tmp/claude-0/w/work"); ap.add_argument("--report", action="store_true")
ap.add_argument("--test-split-len", type=int, default=0)  # testing only: split cubes shorter than this unsolved
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); os.makedirs(a.work, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
LJ = os.path.join(a.out, "leaves.jsonl")
lock = threading.Lock()
def load():
    return [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
def verified(r):
    return r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"
def frontier(top, recs):
    """(leaves, open) of the subtree partition rooted at the shard's top cubes."""
    by = {}
    for r in recs:
        if "cube" in r: by[tuple(r["cube"])] = r
    leaves, opn, st = [], [], list(top)
    while st:
        c = st.pop(); r = by.get(tuple(c))
        if r and verified(r): leaves.append(c)
        elif r and r.get("status") == "SPLIT" and r.get("subs") and all(r["subs"]): st.extend(c + s for s in r["subs"])
        else: opn.append(c)
    return leaves, opn
def write_icnf(path, cubes):
    with open(path, "w") as f:
        for c in cubes: f.write("a " + " ".join(map(str, c)) + " 0\n")
def report(top):
    leaves, opn = frontier(top, load())
    write_icnf(os.path.join(a.out, "leaves.icnf"), leaves); write_icnf(os.path.join(a.out, "open.icnf"), opn)
    return leaves, opn
cpu = threading.local()
def run(cmd, outpath):
    """run cmd with stdout to outpath; returns exit code, adds its CPU seconds to cpu.s"""
    with open(outpath, "w") as so:
        p = subprocess.Popen(cmd, stdout=so, stderr=subprocess.DEVNULL)
        _, status, ru = os.wait4(p.pid, 0)
    cpu.s = getattr(cpu, "s", 0.0) + ru.ru_utime + ru.ru_stime
    return os.waitstatus_to_exitcode(status)
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, keep=None):
    w = os.path.join(a.work, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
         os.path.join(w, "cubes")], os.path.join(w, "mout")); o = open(os.path.join(w, "mout")).read()
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    if keep: subprocess.run(["cp", os.path.join(w, "cubes"), keep])
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
# ---- top cubes
recs = load()
if a.top:
    topall = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
    topsha = hashlib.sha256(open(a.top, "rb").read()).hexdigest()
else:
    tf = os.path.join(a.out, "top.icnf")
    if not os.path.exists(tf):
        _, ms, line = march([], a.depth, "top", keep=tf)
        with open(LJ, "a") as f: f.write(json.dumps({"top_march": True, "march_s": round(ms, 1), "march": line}) + "\n")
    topall = [list(map(int, l.split()[1:-1])) for l in open(tf) if l.startswith("a")]
    topsha = hashlib.sha256(open(tf, "rb").read()).hexdigest()
top = [c for i, c in enumerate(topall) if i % a.nshards == a.shard]
if a.report:
    l, o = report(top); print(json.dumps({"leaves": len(l), "open": len(o), "top_shard": len(top)})); raise SystemExit
log = open(LJ, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
rec({"top": True, "ncubes": len(topall), "shard": a.shard, "nshards": a.nshards, "shard_cubes": len(top),
     "top_sha256": topsha, "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(),
     "start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]
n = [max([0] + [r.get("k", 0) for r in recs])]
def solve(cube, tmul=1):
    with lock: n[0] += 1; k = n[0]
    if time.time() > deadline:
        rec({"cube": cube, "k": k, "status": "OPEN", "reason": "deadline"}); return
    w = os.path.join(a.work, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time(); cpu.s = 0.0
    rc = 0 if len(cube) < a.test_split_len else run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout * tmul), f,
              os.path.join(w, "p.lrat")], os.path.join(w, "out"))
    st = round(time.time() - t, 2); r = {"cube": cube, "k": k, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], os.path.join(w, "cout")); o = open(os.path.join(w, "cout")).read()
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.work, f"SAT_{k}.cnf")])
        subprocess.run(["cp", os.path.join(w, "out"), os.path.join(a.out, f"SAT_{k}.model")])
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
        # march refuted the cube itself (it prints one empty cube): its children would be the cube
        # again, so instead re-solve the cube once with a 4x timeout (march's refutation is unchecked)
        if not subs or not all(subs): r["status"] = "SPLIT_EMPTY"
    r["cpu_s"] = round(cpu.s, 2)
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
    elif r["status"] == "SPLIT_EMPTY" and tmul == 1: submit(cube, 4)
def task(c, tmul=1):
    try: solve(c, tmul)
    except Exception as e: rec({"cube": c, "status": "ERROR", "err": repr(e)})
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c, tmul=1):
    with cv: count[0] += 1
    pool.submit(task, c, tmul)
_, todo = frontier(top, recs)
rec({"resume": True, "queued": len(todo)})
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
l, o = report(top)
rec({"done": True, "leaves": len(l), "open": len(o), "end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
