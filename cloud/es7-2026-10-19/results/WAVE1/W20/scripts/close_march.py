#!/usr/bin/env python3
"""W20 copy of results/Mii-S/scripts/close_march.py (original kept as close_march.orig.py), changed for
sharded, resumable runs.

  close_march.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --jobs J --deadline EPOCH
  close_march.py CASE.cnf OUTDIR --top TOP.icnf --shard S --nshards K --finalize

Changes against the original:
- the top cubes come from a precomputed `march_cu CASE -d 7 -o TOP.icnf` (same file for every shard);
  only the cubes with 0-based line index i, i mod K == S are processed;
- resumable: OUTDIR/leaves.jsonl is read on start; a cube with a cake_lpr-verified UNSAT record is
  done, a cube with a SPLIT record (which now lists its children `subs`) is replaced by its children,
  every other cube (no record, timed out at the deadline, killed, cake_lpr failure) is run again;
- cadical's stdout is kept for SAT answers (model in SAT_k.out);
- no new cube is started after --deadline; leaves.icnf (only cake_lpr `s VERIFIED UNSAT` leaves)
  and open.icnf (cubes still open) are rewritten at the end and by --finalize.
Recipe unchanged: cadical --lrat -t TIMEOUT per cube, cake_lpr on every UNSAT, march_cu -d SPLIT on a
timeout.
"""
import argparse, hashlib, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--deadline", type=float, default=1e18); ap.add_argument("--finalize", action="store_true")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
LJ = os.path.join(a.out, "leaves.jsonl")
OK = "s VERIFIED UNSAT"
top_all = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top_all) if i % a.nshards == a.shard]

def load():
    done, split, sat = set(), {}, []
    if os.path.exists(LJ):
        for l in open(LJ):
            r = json.loads(l)
            if "cube" not in r: continue
            k = tuple(r["cube"])
            if r.get("status") == "UNSAT" and r.get("cake_lpr") == OK: done.add(k)
            elif r.get("status") == "SPLIT" and "subs" in r: split[k] = r["subs"]
            elif r.get("status") == "SAT": sat.append(k)
    return done, split, sat

def frontier():
    """Leaves reached from my top cubes: (verified leaves, open cubes)."""
    done, split, sat = load(); leaves, opn = [], []
    stack = list(reversed(mine))
    while stack:
        c = stack.pop(); k = tuple(c)
        if k in done: leaves.append(c)
        elif k in split: stack.extend(reversed([c + s for s in split[k]]))
        else: opn.append(c)
    return leaves, opn, sat

def finalize():
    leaves, opn, sat = frontier()
    with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
        for c in leaves: f.write("a " + " ".join(map(str, c)) + " 0\n")
    with open(os.path.join(a.out, "open.icnf"), "w") as f:
        for c in opn: f.write("a " + " ".join(map(str, c)) + " 0\n")
    print(json.dumps({"mine": len(mine), "leaves": len(leaves), "open": len(opn), "sat": len(sat)}))

if a.finalize: finalize(); sys.exit(0)

hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); log = open(LJ, "a")
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
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]
n = [int(time.time() * 1000) % 10**9]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() > a.deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); return
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    with open(os.path.join(w, "out"), "w") as so:
        rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                             os.path.join(w, "p.lrat")], stdout=so).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", os.path.join(w, "out"), os.path.join(a.out, f"SAT_{k}.out")])
        with open(os.path.join(a.out, f"SAT_{k}.cube"), "w") as g: g.write(" ".join(map(str, cube)) + "\n")
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
        if not subs or any(not s for s in subs): r["status"] = "OPEN"; r["reason"] = "degenerate split"
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
leaves, opn, sat = frontier()
rec({"start": True, "time": time.time(), "shard": a.shard, "nshards": a.nshards, "ntop": len(top_all),
     "mine": len(mine), "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
     "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(),
     "resume_leaves": len(leaves), "resume_open": len(opn)})
for c in opn: submit(c)
with cv:
    while count[0] > 0: cv.wait()
finalize()
