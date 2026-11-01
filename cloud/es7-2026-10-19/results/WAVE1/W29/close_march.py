#!/usr/bin/env python3
"""Close case CNFs by cube-and-conquer (the Mi recipe) with cake_lpr-checked leaves.

W29 version of results/Mii-S/scripts/close_march.py, changed to (a) take several cases that share
one worker pool, served in the listed order (a lower case index always goes first), (b) be
resumable, and (c) take --shard/--nshards.

  close_march.py OUTROOT NAME=CASE.cnf [NAME=CASE.cnf ...] --depth 7 --timeout 300 --split-depth 6
                 --jobs J [--shard s --nshards k] [--stop-at EPOCH]
For each case, OUTROOT/NAME/top.icnf is `march_cu CASE -d DEPTH` (made once, then reused).
Each cube c: CASE + units(c) is solved by `cadical --lrat -t TIMEOUT`; an UNSAT answer is checked
with cake_lpr (proof deleted afterwards).  A cube that times out is split by
`march_cu CASE+units(c) -d SPLIT` and its children c+s are queued (stored in the SPLIT record).
Records go to OUTROOT/NAME/leaves.jsonl.  On restart the queue is rebuilt from top.icnf and the
SPLIT records minus the cubes that already have a final record.  At the end (or at --stop-at,
after which no new cube is started) OUTROOT/NAME/leaves.icnf lists every leaf whose cake_lpr
line is `s VERIFIED UNSAT` as `a lits 0`, and OUTROOT/NAME/open.icnf every cube still open.
"""
import argparse, hashlib, heapq, json, os, re, subprocess, threading, time
BIN = os.environ.get("BIN", "/home/user/tools/bin")
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("cases", nargs="+")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--stop-at", type=float, default=1e18)
ap.add_argument("--scratch", default="/home/user/work/scratch")
a = ap.parse_args()
lock = threading.Lock()

class Case:
    def __init__(s, idx, spec):
        s.idx = idx; s.name, s.cnf = spec.split("=", 1)
        s.dir = os.path.join(a.out, s.name); os.makedirs(s.dir, exist_ok=True)
        s.hdr, s.body = open(s.cnf).read().split("\n", 1)
        s.nv, s.nc = int(s.hdr.split()[2]), int(s.hdr.split()[3])
        s.log = open(os.path.join(s.dir, "leaves.jsonl"), "a")
    def rec(s, r):
        with lock: s.log.write(json.dumps(r) + "\n"); s.log.flush()
    def write(s, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {s.nv} {s.nc + len(cube)}\n"); f.write(s.body)
            f.write("".join(f"{l} 0\n" for l in cube))
    def records(s):
        p = os.path.join(s.dir, "leaves.jsonl")
        return [json.loads(l) for l in open(p) if l.strip()]

def march(case, cube, d, tag, outfile=None):
    w = os.path.join(a.scratch, f"m_{case.name}_{tag}"); os.makedirs(w, exist_ok=True)
    case.write(os.path.join(w, "f.cnf"), cube); t = time.time()
    cf = outfile or os.path.join(w, "cubes")
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o", cf],
                       capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]

heap = []; cv = threading.Condition(); active = [0]; seq = [0]; stop = [False]
def push(case, cube):
    with cv:
        seq[0] += 1; heapq.heappush(heap, (case.idx, seq[0], case.name, cube)); cv.notify()

def solve(case, cube, k):
    w = os.path.join(a.scratch, f"s_{case.name}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    case.write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st, "rc": rc}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(case.dir, f"SAT_{k}.cnf")])
        subprocess.run([os.path.join(BIN, "cadical"), "-q", f], stdout=open(os.path.join(case.dir, f"SAT_{k}.model"), "w"))
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(case, cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); case.rec(r)
    if r["status"] == "SPLIT":
        for s in subs: push(case, cube + s)

def worker():
    while True:
        with cv:
            while not heap and active[0] > 0 and not stop[0]: cv.wait()
            if stop[0] or not heap or time.time() > a.stop_at:
                stop[0] = stop[0] or time.time() > a.stop_at or not heap; cv.notify_all(); return
            _, k, name, cube = heapq.heappop(heap); active[0] += 1
        try: solve(byname[name], cube, k)
        finally:
            with cv: active[0] -= 1; cv.notify_all()

def pending(case, top):
    done = set(); known = [list(c) for c in top]
    for r in case.records():
        if "cube" not in r: continue
        if r["status"] == "SPLIT": known += [r["cube"] + s for s in r["subs"]]
        if r["status"] in ("SPLIT", "SAT") or (r["status"] == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"):
            done.add(tuple(r["cube"]))
    return [c for c in known if tuple(c) not in done]

cases = [Case(i, s) for i, s in enumerate(a.cases)]; byname = {c.name: c for c in cases}
tops = {}
def get_top(case):
    tf = os.path.join(case.dir, "top.icnf")
    if not os.path.exists(tf):
        full, ms, line = march(case, [], a.depth, "top", outfile=tf + ".tmp"); os.rename(tf + ".tmp", tf)
        m = re.search(r"number of cubes (\d+), including (\d+) refuted", line)
        case.rec({"top": True, "ncubes": len(full), "march_s": round(ms, 1), "march": line,
                  "march_ncubes": int(m.group(1)) if m else None, "march_refuted": int(m.group(2)) if m else None,
                  "top_icnf_sha256": hashlib.sha256(open(tf, "rb").read()).hexdigest(),
                  "case_sha256": hashlib.sha256(open(case.cnf, "rb").read()).hexdigest(),
                  "shard": a.shard, "nshards": a.nshards})
    full = [list(map(int, l.split()[1:-1])) for l in open(tf) if l.startswith("a")]
    tops[case.name] = [c for i, c in enumerate(full) if i % a.nshards == a.shard]
ts = [threading.Thread(target=get_top, args=(c,)) for c in cases]
for t in ts: t.start()
for t in ts: t.join()
for c in cases:
    for cube in pending(c, tops[c.name]): push(c, cube)
ws = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ws: t.start()
for t in ws: t.join()
for c in cases:
    recs = c.records()
    with open(os.path.join(c.dir, "leaves.icnf"), "w") as f:
        for r in recs:
            if r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
    with open(os.path.join(c.dir, "open.icnf"), "w") as f:
        for cube in pending(c, tops[c.name]): f.write("a " + " ".join(map(str, cube)) + " 0\n")
