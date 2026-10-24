#!/usr/bin/env python3
"""W11 copy of results/Mii-S/scripts/close_march.py, changed for wave 1.

  close_march.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --jobs J [--hours H]
  close_march.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --summarize

Changes against the original:
- --top: the top cubes come from a fixed `march_cu CASE -d 7 -o top.icnf` file shared by all
  shards; only the cubes with 0-based line index i, i mod K == S are processed.
- A leaf is closed only when cake_lpr prints `s VERIFIED UNSAT`.  An UNSAT answer that
  cake_lpr does not verify is recorded as UNSAT_UNVERIFIED and stays open.
- SPLIT records keep their children ("subs"), so the run is resumable: on start the tree is
  replayed from leaves.jsonl, verified leaves are skipped, split nodes are expanded and every
  other cube is queued again.
- leaves.icnf (verified leaves only) and open.icnf (the cubes not closed) are rebuilt from the
  replay by --summarize and at the end of a run.
"""
import argparse, hashlib, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--summarize", action="store_true")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
OK = "s VERIFIED UNSAT"
LOG = os.path.join(a.out, "leaves.jsonl")
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
top_all = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top_all) if i % a.nshards == a.shard]

def replay():
    """Walk the tree from my top cubes.  Returns (verified leaves, open cubes, SAT cubes)."""
    recs = {}
    if os.path.exists(LOG):
        for l in open(LOG):
            r = json.loads(l)
            if "cube" in r: recs.setdefault(tuple(r["cube"]), []).append(r)
    closed, opn, sat = [], [], []
    stack = list(reversed(mine))
    while stack:
        c = stack.pop(); rs = recs.get(tuple(c), [])
        if any(r["status"] == "UNSAT" and r.get("cake_lpr") == OK for r in rs): closed.append(c)
        elif any(r["status"] == "SAT" for r in rs): sat.append(c); opn.append(c)
        else:
            sp = [r for r in rs if r["status"] == "SPLIT" and "subs" in r]
            if sp: stack.extend(reversed([c + s for s in sp[-1]["subs"]]))
            else: opn.append(c)
    return closed, opn, sat

def summarize():
    closed, opn, sat = replay()
    with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
        for c in closed: f.write("a " + " ".join(map(str, c)) + " 0\n")
    with open(os.path.join(a.out, "open.icnf"), "w") as f:
        for c in opn: f.write("a " + " ".join(map(str, c)) + " 0\n")
    return closed, opn, sat

if a.summarize:
    c, o, s = summarize(); print(f"closed {len(c)} open {len(o)} sat {len(s)} mine {len(mine)}"); sys.exit()

lock = threading.Lock(); log = open(LOG, "a")
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
def run(cmd, out=subprocess.DEVNULL):
    """Run cmd; return (returncode, stdout text, child cpu seconds)."""
    p = subprocess.Popen(cmd, stdout=out, text=True); so = p.stdout.read() if out == subprocess.PIPE else ""
    _, status, ru = os.wait4(p.pid, 0); p.returncode = os.waitstatus_to_exitcode(status)
    return p.returncode, so, ru.ru_utime + ru.ru_stime
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() > deadline: return
    w = os.path.join(a.out, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    rc, _, cpu = run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                      os.path.join(w, "p.lrat")])
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st, "solve_cpu_s": round(cpu, 2)}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        _, o, cpu = run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], subprocess.PIPE)
        r["check_cpu_s"] = round(cpu, 2)
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if r["cake_lpr"] == OK else "UNSAT_UNVERIFIED"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
        so = subprocess.run([os.path.join(BIN, "cadical"), "-q", f], capture_output=True, text=True).stdout
        open(os.path.join(a.out, f"SAT_{k}.model"), "w").write(so)
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
_, todo, _ = replay()
rec({"start": True, "shard": a.shard, "nshards": a.nshards, "mine": len(mine), "todo": len(todo),
     "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(),
     "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(), "time": time.time()})
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
c, o, s = summarize(); rec({"end": True, "closed": len(c), "open": len(o), "sat": len(s), "time": time.time()})
print(f"closed {len(c)} open {len(o)} sat {len(s)}")
