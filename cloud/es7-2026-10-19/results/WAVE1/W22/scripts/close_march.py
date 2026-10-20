#!/usr/bin/env python3
"""Close one case CNF by cube-and-conquer (the Mi recipe) with cake_lpr-checked leaves.

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs J
march_cu CASE -d DEPTH gives the top cubes (refuted leaves included, so the file is a full
partition).  Each cube c: CASE + units(c) is solved by `cadical --lrat -t TIMEOUT` and an UNSAT
answer is checked with cake_lpr (proof deleted afterwards).  A cube that times out is split by
`march_cu CASE+units(c) -d SPLIT` and its children c+s are queued.  Records go to
OUTDIR/leaves.jsonl; OUTDIR/leaves.icnf (written at the end) lists every closed leaf as
`a lits 0` for `cover_check` (H3) relative to CASE.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--finalize", action="store_true")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); log = open(os.path.join(a.out, "leaves.jsonl"), "a")
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
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); subprocess.run(["rm", "-rf", w]); return
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if r["cake_lpr"].strip() == "s VERIFIED UNSAT" else "UNSAT_UNCHECKED"
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
# W22 changes: top cubes kept in OUTDIR/top.icnf (shared by all shards of the case), shard
# s of k takes the top cubes with 0-based line index i, i mod k == s; resumable from leaves.jsonl.
topf = os.path.join(a.out, "top.icnf")
if not os.path.exists(topf):
    w = os.path.join(a.out, "m_top"); os.makedirs(w, exist_ok=True); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), a.case, "-d", str(a.depth), "-o", os.path.join(w, "cubes")],
                       capture_output=True, text=True).stdout
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    rec({"top": True, "march_s": round(time.time() - t, 1), "march": m.group(0) if m else o[-200:],
         "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
    os.replace(os.path.join(w, "cubes"), topf); subprocess.run(["rm", "-rf", w])
top = [list(map(int, l.split()[1:-1])) for l in open(topf) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
def state():
    st = {}
    for l in open(os.path.join(a.out, "leaves.jsonl")):
        r = json.loads(l)
        if "cube" in r: st[tuple(r["cube"])] = r
    return st
def pending(st):
    out, todo = [], list(mine)
    while todo:
        c = todo.pop(); r = st.get(tuple(c))
        if r is None or r["status"] == "OPEN": out.append(c)
        elif r["status"] == "SPLIT": todo.extend(c + s for s in r["subs"])
    return out
st = state()
if not a.finalize:
    rec({"run_start": time.time(), "shard": a.shard, "nshards": a.nshards, "ntop": len(top), "nmine": len(mine),
         "top_sha256": hashlib.sha256(open(topf, "rb").read()).hexdigest()})
    for c in pending(st): submit(c)
    with cv:
        while count[0] > 0: cv.wait()
    st = state()
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for r in st.values():
        if r.get("status") == "UNSAT": f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
op = pending(st)
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in op: f.write("a " + " ".join(map(str, c)) + " 0\n")
print(json.dumps({"mine": len(mine), "leaves": sum(r.get("status") == "UNSAT" for r in st.values()), "open": len(op),
                  "sat": sum(r.get("status") == "SAT" for r in st.values())}))
