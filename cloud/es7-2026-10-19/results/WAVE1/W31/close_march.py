#!/usr/bin/env python3
"""W31 copy of results/Mii-S/scripts/close_march.py, changed for wave 1:

  close_march.py OUTROOT CASE1.cnf [CASE2.cnf ...] --depth 7 --timeout 300 --split-depth 6 --jobs 4
                 [--shard s --nshards k] [--until EPOCH]

- Several cases share one pool of JOBS workers; cubes of earlier cases run first (priority).
- Per case, OUTROOT/<name>/: top.icnf (march_cu CASE -d DEPTH, kept and reused on resume),
  leaves.jsonl (all records, appended), leaves.icnf (only leaves whose cake_lpr line is
  `s VERIFIED UNSAT`), open.icnf (cubes not closed when the run stops).
- Resumable: on start the tree is rebuilt from leaves.jsonl; a cube is final if it has a verified
  UNSAT, a SAT, or a SPLIT record (SPLIT records now store their children `subs`).
- --shard/--nshards: only top cubes with 0-based line index i, i mod k == s.
- A split whose march_cu output is empty is never treated as closed (recorded EMPTYSPLIT, open).
- cake_lpr runs with a 3000 MB heap; if it gives no `s ` verdict it is retried once with 11000 MB
  (one such retry at a time).
"""
import argparse, hashlib, heapq, json, os, re, subprocess, sys, threading, time
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("cases", nargs="+")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--until", type=float, default=1e18, help="epoch seconds; no new cube starts after it")
a = ap.parse_args()
VER = "s VERIFIED UNSAT"
biglock = threading.Lock(); qcv = threading.Condition(); heap = []; seq = [0]; busy = [0]; stop = [False]

class Case:
    def __init__(self, idx, path):
        self.idx, self.path = idx, path
        self.name = os.path.basename(path).rsplit(".cnf", 1)[0]
        self.out = os.path.join(a.out, self.name); os.makedirs(self.out, exist_ok=True)
        hdr, self.body = open(path).read().split("\n", 1)
        self.nv, self.nc = int(hdr.split()[2]), int(hdr.split()[3])
        self.sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
        subprocess.run(f"rm -rf {self.out}/s_* {self.out}/m_*", shell=True)  # scratch left by a killed run
        self.lock = threading.Lock(); self.log = open(os.path.join(self.out, "leaves.jsonl"), "a"); self.n = 0
    def rec(self, r):
        with self.lock: self.log.write(json.dumps(r) + "\n"); self.log.flush()
    def write(self, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {self.nv} {self.nc + len(cube)}\n"); f.write(self.body)
            f.write("".join(f"{l} 0\n" for l in cube))
    def records(self):
        p = os.path.join(self.out, "leaves.jsonl")
        return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []

def march(case, cube, d, tag, keep=None):
    w = os.path.join(case.out, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    case.write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cf = os.path.join(w, "cubes")
    cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")] if os.path.exists(cf) else []
    if keep and os.path.exists(cf): subprocess.run(["cp", cf, keep])
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]

def cake(f, p, heapmb):
    t = time.time()
    o = subprocess.run([os.path.join(BIN, "cake_lpr"), f"--CML_HEAP_SIZE={heapmb}", "--CML_STACK_SIZE=2000", f, p],
                       capture_output=True, text=True)
    line = next((l for l in o.stdout.splitlines() if l.startswith("s ")), None)
    return line, (o.stdout + o.stderr)[-200:], time.time() - t

def solve(case, cube):
    with case.lock: case.n += 1; k = case.n
    w = os.path.join(case.out, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    case.write(f, cube); t = time.time(); p = os.path.join(w, "p.lrat")
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f, p],
                        stdout=subprocess.DEVNULL).returncode
    r = {"cube": cube, "solve_s": round(time.time() - t, 2)}; subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(p)
        line, tail, ct = cake(f, p, 3000)
        if line is None:
            with biglock: line, tail, ct2 = cake(f, p, 11000)
            ct += ct2; r["cake_retry"] = True
        r["cake_lpr"] = line if line else tail; r["check_s"] = round(ct, 2); r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(case.out, f"SAT_{k}.cnf")])
        subprocess.run([os.path.join(BIN, "cadical"), "-q", f], stdout=open(os.path.join(case.out, f"SAT_{k}.model"), "w"))
    else:
        subs, ms, line = march(case, cube, a.split_depth, k)
        r.update(rc=rc, split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
        r["status"] = "SPLIT" if subs else "EMPTYSPLIT"
    subprocess.run(["rm", "-rf", w]); case.rec(r)
    if r["status"] == "SPLIT":
        for s in subs: push(case, cube + s)
    if r["status"] == "SAT":
        print(f"SAT in {case.name}: {cube}", flush=True)

def push(case, cube):
    with qcv:
        seq[0] += 1; heapq.heappush(heap, (case.idx, seq[0], case, cube)); qcv.notify_all()

def worker():
    while True:
        with qcv:
            while not heap and busy[0] > 0: qcv.wait()
            if not heap: qcv.notify_all(); return
            if time.time() > a.until: stop[0] = True; qcv.notify_all(); return
            _, _, case, cube = heapq.heappop(heap); busy[0] += 1
        try: solve(case, cube)
        finally:
            with qcv: busy[0] -= 1; qcv.notify_all()

def final(r): return r.get("status") in ("SAT", "SPLIT") or (r.get("status") == "UNSAT" and r.get("cake_lpr") == VER)

cases = [Case(i, p) for i, p in enumerate(a.cases)]
for case in cases:
    top_f = os.path.join(case.out, "top.icnf")
    if not os.path.exists(top_f):
        top, ms, line = march(case, [], a.depth, "top", keep=top_f)
        case.rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line, "case_sha256": case.sha,
                  "top_sha256": hashlib.sha256(open(top_f, "rb").read()).hexdigest(),
                  "shard": a.shard, "nshards": a.nshards})
    top = [list(map(int, l.split()[1:-1])) for l in open(top_f) if l.startswith("a")]
    done = {}
    for r in case.records():
        if "cube" in r and final(r): done[tuple(r["cube"])] = r
    def expand(c):
        r = done.get(tuple(c))
        if r is None: push(case, c)
        elif r["status"] == "SPLIT":
            for s in r["subs"]: expand(c + s)
    for i, c in enumerate(top):
        if i % a.nshards == a.shard: expand(c)
print(f"queued {len(heap)} cubes", flush=True)
ths = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ths: t.start()
for t in ths: t.join()
left = {}
for _, _, case, cube in heap: left.setdefault(case.name, []).append(cube)
for case in cases:
    rs = case.records()
    with open(os.path.join(case.out, "leaves.icnf"), "w") as f:
        for r in rs:
            if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
    fin = {tuple(r["cube"]) for r in rs if "cube" in r and final(r)}
    op = left.get(case.name, []) + [r["cube"] for r in rs if "cube" in r and not final(r) and tuple(r["cube"]) not in fin]
    op = [list(c) for c in dict.fromkeys(tuple(c) for c in op)]
    with open(os.path.join(case.out, "open.icnf"), "w") as f:
        for c in op: f.write("a " + " ".join(map(str, c)) + " 0\n")
    print(case.name, "open", len(op), flush=True)
