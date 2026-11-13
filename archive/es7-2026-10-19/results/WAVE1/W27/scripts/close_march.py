#!/usr/bin/env python3
"""W27 copy of results/Mii-S/scripts/close_march.py (original: close_march_orig.py, sha256
5215f5f1...d609), changed to be resumable and shardable.

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs J
                 [--shard s --nshards k] [--deadline UNIX_TIME]
Same recipe as the original: march_cu CASE -d DEPTH gives the top cubes (refuted leaves
included, so the file is a full partition); each cube c: CASE + units(c) is solved by
`cadical --lrat -t TIMEOUT` and an UNSAT answer is checked with cake_lpr (proof deleted
afterwards); a cube that times out is split by `march_cu CASE+units(c) -d SPLIT` and its
children c+s are queued.

Changes:
- the top cube file is kept as OUTDIR/top.icnf (sha256, cube count and refuted count recorded
  in the top record) and reused on restart;
- --shard/--nshards: only top cubes with 0-based line index i, i mod k == s are processed;
- SPLIT records carry their children ("subs"), so a restart rebuilds the tree from
  leaves.jsonl and only re-solves cubes that have no final record;
- a leaf counts as closed only if cake_lpr printed `s VERIFIED UNSAT`; anything else stays open;
- --deadline: no new cube is started after it;
- at the end leaves.icnf (closed leaves only) and open.icnf (cubes still open) are written.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/opt/es7tools/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--deadline", type=float, default=1e18)
ap.add_argument("--work", default=None)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
WORK = a.work or a.out; os.makedirs(WORK, exist_ok=True)
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); LJ = os.path.join(a.out, "leaves.jsonl")
VER = "s VERIFIED UNSAT"
def rec(r):
    with lock:
        with open(LJ, "a") as log: log.write(json.dumps(r) + "\n")
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, keep=None):
    w = os.path.join(WORK, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    if keep: subprocess.run(["cp", os.path.join(w, "cubes"), keep])
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]

# ---- top cubes (reused on restart)
TOP = os.path.join(a.out, "top.icnf")
recs = [json.loads(l) for l in open(LJ)] if os.path.exists(LJ) else []
if not os.path.exists(TOP):
    top, ms, line = march([], a.depth, "top", keep=TOP)
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", line)
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line,
         "refuted": int(m.group(2)) if m else None,
         "top_icnf_sha256": hashlib.sha256(open(TOP, "rb").read()).hexdigest(),
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(),
         "shard": a.shard, "nshards": a.nshards})
top = [list(map(int, l.split()[1:-1])) for l in open(TOP) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]

# ---- tree state from earlier records
closed, split = set(), {}
for r in recs:
    if "cube" not in r: continue
    k = tuple(r["cube"])
    if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: closed.add(k)
    elif r.get("status") == "SPLIT" and "subs" in r: split[k] = r["subs"]
def walk():
    """Leaves of the current tree below my top cubes: (closed leaves, open cubes)."""
    cl, op, st = [], [], list(reversed(mine))
    while st:
        c = st.pop(); k = tuple(c)
        if k in closed: cl.append(c)
        elif k in split: st.extend(reversed([c + s for s in split[k]]))
        else: op.append(c)
    return cl, op

pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
def solve(cube):
    if time.time() > a.deadline: return
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(WORK, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st, "rc": rc}
    subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True)
        out = o.stdout + o.stderr
        r["cake_lpr"] = next((l for l in o.stdout.splitlines() if l.startswith("s ")), out[-200:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        subprocess.run(["sh", "-c", f"{os.path.join(BIN, 'cadical')} -q {f} > {os.path.join(a.out, f'SAT_{k}.model')}"])
    elif rc == 0:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, f"{os.getpid()}_{k}")
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    else:
        r["status"] = "ERROR"
    subprocess.run(["rm", "-rf", w]); rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception as e: rec({"cube": c, "status": "ERROR", "exc": repr(e)})
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
_, todo = walk()
rec({"start": time.time(), "todo": len(todo), "closed_before": len(closed), "shard": a.shard, "nshards": a.nshards})
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
pool.shutdown()

# ---- final files from all records
closed, split = set(), {}
for r in [json.loads(l) for l in open(LJ)]:
    if "cube" not in r: continue
    k = tuple(r["cube"])
    if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: closed.add(k)
    elif r.get("status") == "SPLIT" and "subs" in r: split[k] = r["subs"]
cl, op = walk()
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for c in cl: f.write("a " + " ".join(map(str, c)) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in op: f.write("a " + " ".join(map(str, c)) + " 0\n")
rec({"end": time.time(), "closed_leaves": len(cl), "open": len(op)})
print(json.dumps({"closed_leaves": len(cl), "open": len(op)}))
