#!/usr/bin/env python3
"""W32 driver: close_march.py (results/Mii-S/scripts, copied as close_march.orig.py) for a list of
cases on one shared pool of workers, resumable.

  run_w32.py CASEDIR OUTDIR --cases a,b,... --jobs 4 --stop-at UNIX_TIME

Per case, in the listed order (lower case index = higher priority on the pool):
  1. direct: `cadical --lrat -t 60` on CASE.cnf; closed only if cake_lpr prints `s VERIFIED UNSAT`.
  2. top: `march_cu CASE.cnf -d 7 -o top.icnf` (kept in OUTDIR/<case>/top.icnf, sha256 recorded).
  3. each cube c: CASE + units(c) by `cadical --lrat -t 300`; UNSAT checked with cake_lpr; a timeout
     is split by `march_cu CASE+units(c) -d 6` and the children c+s are queued (recorded in "subs").
Changes from close_march.py: shared pool across cases, the direct 60 s attempt, resume from
leaves.jsonl, leaves.icnf lists only cake_lpr-verified leaves, open.icnf lists the cubes not yet
closed, CPU time per subprocess from wait4, SAT models kept, optional --shard/--nshards for top cubes.
"""
import argparse, hashlib, heapq, itertools, json, os, re, subprocess, threading, time
BIN = os.environ.get("BIN", "/home/user/w/bin")
TMP = os.environ.get("TMPW", "/home/user/w/tmp")
ap = argparse.ArgumentParser(); ap.add_argument("casedir"); ap.add_argument("out")
ap.add_argument("--cases", required=True); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--direct", type=int, default=60); ap.add_argument("--depth", type=int, default=7)
ap.add_argument("--timeout", type=int, default=300); ap.add_argument("--split-depth", type=int, default=6)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--stop-at", type=float, default=1e18)
a = ap.parse_args(); os.makedirs(TMP, exist_ok=True)
CASES = a.cases.split(",")
lock = threading.Lock(); cv = threading.Condition(lock)
heap = []; seq = itertools.count(); running = [0]; stop = [False]

def run(cmd, out=None):
    """Run cmd; return (returncode, stdout text, cpu seconds)."""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE if out is None else open(out, "w"), stderr=subprocess.DEVNULL, text=True)
    so = p.stdout.read() if out is None else ""
    _, status, ru = os.wait4(p.pid, 0); p.returncode = os.waitstatus_to_exitcode(status)
    return p.returncode, so, round(ru.ru_utime + ru.ru_stime, 2)

class Case:
    def __init__(self, i, name):
        self.i, self.name = i, name; self.cnf = os.path.join(a.casedir, name + ".cnf")
        self.dir = os.path.join(a.out, name); os.makedirs(self.dir, exist_ok=True)
        hdr, self.body = open(self.cnf).read().split("\n", 1)
        self.nv, self.nc = int(hdr.split()[2]), int(hdr.split()[3])
        self.sha = hashlib.sha256(open(self.cnf, "rb").read()).hexdigest()
        self.log = open(os.path.join(self.dir, "leaves.jsonl"), "a")
        self.closed_direct = False; self.top = None; self.pending = set(); self.verified = []; self.n = 0
        self.resume()
    def rec(self, r):
        with lock: self.log.write(json.dumps(r) + "\n"); self.log.flush()
    def resume(self):
        recs = [json.loads(l) for l in open(os.path.join(self.dir, "leaves.jsonl"))]
        direct = [r for r in recs if r.get("direct")]
        self.closed_direct = any(r.get("cake_lpr") == "s VERIFIED UNSAT" for r in direct)
        if any(r.get("status") == "SAT" for r in recs): stop[0] = True
        tf = os.path.join(self.dir, "top.icnf")
        if self.closed_direct or not os.path.exists(tf) or not any(r.get("top") for r in recs):
            self.state = "closed" if self.closed_direct else ("top" if direct else "direct"); return
        self.top = [tuple(map(int, l.split()[1:-1])) for l in open(tf) if l.startswith("a")]
        gen = [c for k, c in enumerate(self.top) if k % a.nshards == a.shard]
        done = set()
        for r in recs:
            if "cube" not in r: continue
            c = tuple(r["cube"])
            if r.get("status") == "SPLIT":
                done.add(c); gen += [c + tuple(s) for s in r["subs"]]
            elif r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                done.add(c); self.verified.append(c)
        self.pending = set(gen) - done; self.state = "cubes"
    def write(self, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {self.nv} {self.nc + len(cube)}\n"); f.write(self.body); f.write("".join(f"{l} 0\n" for l in cube))
    def snapshot(self):
        with lock:
            ver, pend, st = list(self.verified), sorted(self.pending, key=lambda c: (len(c), c)), self.state
        with open(os.path.join(self.dir, "leaves.icnf"), "w") as f:
            if self.closed_direct: f.write("a 0\n")
            for c in ver: f.write("a " + " ".join(map(str, c)) + " 0\n")
        with open(os.path.join(self.dir, "open.icnf"), "w") as f:
            if st in ("direct", "top"): f.write("a 0\n")
            for c in pend: f.write("a " + " ".join(map(str, c)) + " 0\n")

def submit(case, kind, cube=()):
    with cv:
        if kind == "cube": case.pending.add(cube)
        heapq.heappush(heap, (case.i, 0 if kind != "cube" else 1, next(seq), case, kind, cube)); cv.notify_all()

def solve(case, f, w, t_out, r):
    rc, _, cpu = run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(t_out), f,
                      os.path.join(w, "p.lrat")], out=os.path.join(w, "stdout"))
    r["solve_cpu"] = cpu
    if rc == 20:
        r["status"] = "UNSAT"; r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat"))
        _, o, cpu = run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")])
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_cpu"] = cpu
    elif rc == 10:
        r["status"] = "SAT"; model = [l for l in open(os.path.join(w, "stdout")) if l.startswith("v ")]
        with open(os.path.join(case.dir, f"SAT_{w.split('/')[-1]}.model"), "w") as g: g.write("".join(model))
        stop[0] = True
    else:
        r["status"] = "UNKNOWN"
    return r

def task(case, kind, cube):
    with lock: case.n += 1; k = case.n
    w = os.path.join(TMP, f"{case.name}_{kind}_{k}_{time.time_ns()}"); os.makedirs(w); f = os.path.join(w, "f.cnf")
    case.write(f, cube); t = time.time()
    if kind == "direct":
        r = solve(case, f, w, a.direct, {"direct": True, "case_sha256": case.sha})
        r["wall_s"] = round(time.time() - t, 2); case.rec(r)
        if r.get("cake_lpr") == "s VERIFIED UNSAT":
            with lock: case.closed_direct = True; case.state = "closed"
        elif r["status"] != "SAT":
            with lock: case.state = "top"
            submit(case, "top")
    elif kind == "top":
        _, o, cpu = run([os.path.join(BIN, "march_cu"), case.cnf, "-d", str(a.depth), "-o", os.path.join(case.dir, "top.icnf")])
        top = [tuple(map(int, l.split()[1:-1])) for l in open(os.path.join(case.dir, "top.icnf")) if l.startswith("a")]
        m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
        case.top = top
        mine = [c for j, c in enumerate(top) if j % a.nshards == a.shard]
        case.rec({"top": True, "ncubes": len(top), "nrefuted": int(m.group(2)) if m else None, "march": m.group(0) if m else o[-200:],
                  "march_cpu": cpu, "top_sha256": hashlib.sha256(open(os.path.join(case.dir, "top.icnf"), "rb").read()).hexdigest(),
                  "case_sha256": case.sha, "shard": a.shard, "nshards": a.nshards, "nmine": len(mine)})
        with lock: case.state = "cubes"
        for c in mine: submit(case, "cube", c)
    else:
        r = solve(case, f, w, a.timeout, {"cube": list(cube)})
        if r["status"] == "UNKNOWN":
            _, o, cpu = run([os.path.join(BIN, "march_cu"), f, "-d", str(a.split_depth), "-o", os.path.join(w, "cubes")])
            subs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
            m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
            r.update(status="SPLIT", split_cpu=cpu, march=m.group(0) if m else o[-200:], nsub=len(subs), subs=subs)
        r["wall_s"] = round(time.time() - t, 2); case.rec(r)
        with lock:
            if r["status"] == "SPLIT": case.pending.discard(cube)
            elif r.get("cake_lpr") == "s VERIFIED UNSAT": case.pending.discard(cube); case.verified.append(cube)
            else: case.unresolved = True   # UNSAT not verified, or SAT: stays in open.icnf
        if r["status"] == "SPLIT":
            for s in r["subs"]: submit(case, "cube", cube + tuple(s))
    subprocess.run(["rm", "-rf", w])

def worker():
    while True:
        with cv:
            while not heap and running[0] > 0 and not stop[0]: cv.wait(5)
            if stop[0] or time.time() > a.stop_at or not heap: cv.notify_all(); return
            _, _, _, case, kind, cube = heapq.heappop(heap); running[0] += 1
        try: task(case, kind, cube)
        except Exception as e:
            print("ERROR", case.name, kind, cube, repr(e), flush=True)
        finally:
            with cv: running[0] -= 1; cv.notify_all()

cases = [Case(i, n) for i, n in enumerate(CASES)]
for c in cases:
    if c.state in ("direct", "top"): submit(c, c.state)
    elif c.state == "cubes":
        for cube in c.pending: heapq.heappush(heap, (c.i, 1, next(seq), c, "cube", cube))
def snapper():
    while True:
        for c in cases: c.snapshot()
        time.sleep(60)
threading.Thread(target=snapper, daemon=True).start()
ths = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ths: t.start()
for t in ths: t.join()
for c in cases: c.snapshot()
print("SAT" if stop[0] else "END", time.strftime("%H:%M:%S"), flush=True)
