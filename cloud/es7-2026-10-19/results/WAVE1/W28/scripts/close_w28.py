#!/usr/bin/env python3
"""W28 runner: results/Mii-S/scripts/close_march.py (copied unchanged next to this file),
extended to several cases sharing one pool of JOBS workers, cases taken in the listed order.

  close_w28.py OUTROOT WORKDIR --cases NAME=CASE.cnf ... [--jobs 4] [--hours H]

Per case, in OUTROOT/NAME/:
  0. plain `cadical --lrat -t PLAIN` on the whole case; UNSAT counts only with cake_lpr
     `s VERIFIED UNSAT` (record {"plain": true, ...}, leaves.icnf = `a 0`).
  1. otherwise `march_cu CASE -d 7 -o top.icnf` once (kept, sha256 recorded); each cube c:
     CASE+units(c) by `cadical --lrat -t 300`, UNSAT checked by cake_lpr, a timeout is split by
     `march_cu CASE+units(c) -d 6` and the children c+s are queued (recorded in "subs").
Changes from close_march.py: leaves.icnf holds only cake_lpr-verified leaves; a cube whose
cadical says UNSAT but cake_lpr does not verify is recorded and stays open; open.icnf lists
the cubes left; per-call CPU time from wait4; resumable from leaves.jsonl + top.icnf;
a SAT answer saves the CNF and the model and stops nothing else.
"""
import argparse, hashlib, heapq, json, os, re, subprocess, sys, threading, time
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("work")
ap.add_argument("--cases", nargs="+", required=True)
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--plain", type=int, default=60); ap.add_argument("--hours", type=float, default=1e9)
a = ap.parse_args()
deadline = time.time() + a.hours * 3600
lock = threading.Lock(); cv = threading.Condition(lock)
heap = []; seq = [0]; active = [0]; procs = set()

def run(cmd, stdout=subprocess.DEVNULL, timeout=None):
    """Run cmd, return (returncode, stdout text or None, user+sys CPU seconds)."""
    p = subprocess.Popen(cmd, stdout=stdout, stderr=subprocess.DEVNULL, text=True)
    with lock: procs.add(p)
    out = p.stdout.read() if stdout == subprocess.PIPE else None
    _, status, ru = os.wait4(p.pid, 0); p.returncode = os.waitstatus_to_exitcode(status)
    with lock: procs.discard(p)
    return p.returncode, out, ru.ru_utime + ru.ru_stime

class Case:
    def __init__(self, idx, name, path):
        self.idx, self.name, self.path = idx, name, path
        self.out = os.path.join(a.out, name); os.makedirs(self.out, exist_ok=True)
        self.work = os.path.join(a.work, name); os.makedirs(self.work, exist_ok=True)
        hdr, self.body = open(path).read().split("\n", 1)
        self.nv, self.nc = int(hdr.split()[2]), int(hdr.split()[3])
        self.sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
        self.logp = os.path.join(self.out, "leaves.jsonl"); self.n = 0
    def rec(self, r):
        with lock:
            with open(self.logp, "a") as f: f.write(json.dumps(r) + "\n")
    def records(self):
        return [json.loads(l) for l in open(self.logp)] if os.path.exists(self.logp) else []
    def write(self, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {self.nv} {self.nc + len(cube)}\n"); f.write(self.body)
            f.write("".join(f"{l} 0\n" for l in cube))
    def wdir(self, tag):
        with lock: self.n += 1; k = self.n
        w = os.path.join(self.work, f"{tag}_{k}_{os.getpid()}"); os.makedirs(w, exist_ok=True); return w, k
    def march(self, cube, d, out_path=None):
        w, k = self.wdir("m"); f = os.path.join(w, "f.cnf"); self.write(f, cube)
        cf = out_path or os.path.join(w, "cubes"); t = time.time()
        _, o, cpu = run([os.path.join(BIN, "march_cu"), f, "-d", str(d), "-o", cf], stdout=subprocess.PIPE)
        cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")]
        m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
        subprocess.run(["rm", "-rf", w])
        return cs, round(time.time() - t, 1), round(cpu, 1), (m.group(0) if m else o[-200:])
    def solve(self, cube, limit, tag="s"):
        """cadical + cake_lpr; returns record dict (status UNSAT/SAT/UNKNOWN)."""
        w, k = self.wdir(tag); f = os.path.join(w, "f.cnf"); p = os.path.join(w, "p.lrat")
        self.write(f, cube); t = time.time()
        rc, o, cpu = run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-t", str(limit), f, p],
                         stdout=subprocess.PIPE)
        r = {"cube": cube, "solve_s": round(time.time() - t, 2), "solve_cpu": round(cpu, 2)}
        if rc == 20:
            r["proof_bytes"] = os.path.getsize(p); t = time.time()
            _, o2, cpu2 = run([os.path.join(BIN, "cake_lpr"), f, p], stdout=subprocess.PIPE)
            r["cake_lpr"] = next((l for l in o2.splitlines() if l.startswith("s ")), o2[-100:])
            r["check_s"] = round(time.time() - t, 2); r["check_cpu"] = round(cpu2, 2); r["status"] = "UNSAT"
        elif rc == 10:
            r["status"] = "SAT"; sd = os.path.join(self.out, f"SAT_{k}")
            os.makedirs(sd, exist_ok=True)
            with open(os.path.join(sd, "model.txt"), "w") as g: g.write(o)
            with open(os.path.join(sd, "cube.txt"), "w") as g: g.write(" ".join(map(str, cube)) + "\n")
            print(f"SAT in {self.name} cube {cube}", file=sys.stderr, flush=True)
        else:
            r["status"] = "UNKNOWN"
        subprocess.run(["rm", "-rf", w]); return r

def push(case, kind, cube):
    with cv:
        heapq.heappush(heap, (case.idx, seq[0], kind, case, cube)); seq[0] += 1; cv.notify_all()

def do(kind, case, cube):
    if kind == "plain":
        r = case.solve([], a.plain, "plain"); r["plain"] = True; r["case_sha256"] = case.sha; case.rec(r)
        if not (r["status"] == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"):
            push(case, "top", None)
        return
    if kind == "top":
        tp = os.path.join(case.out, "top.icnf")
        cs, ms, cpu, line = case.march([], a.depth, tp)
        case.rec({"top": True, "ncubes": len(cs), "march_s": ms, "march_cpu": cpu, "march": line,
                  "top_sha256": hashlib.sha256(open(tp, "rb").read()).hexdigest(), "case_sha256": case.sha})
        for c in cs: push(case, "cube", c)
        return
    left = deadline - time.time()
    if left < 30: return                      # stays open
    lim = min(a.timeout, int(left))
    r = case.solve(cube, lim)
    if r["status"] == "UNKNOWN":
        if lim < a.timeout or time.time() > deadline: return   # cut by deadline: stays open, no record
        subs, ms, cpu, line = case.march(cube, a.split_depth)
        r.update(status="SPLIT", split_s=ms, split_cpu=cpu, march=line, nsub=len(subs), subs=subs)
        case.rec(r)
        for s in subs: push(case, "cube", cube + s)
        return
    case.rec(r)

def worker():
    while True:
        with cv:
            while not heap and active[0] > 0: cv.wait()
            if not heap: cv.notify_all(); return
            _, _, kind, case, cube = heapq.heappop(heap); active[0] += 1
        try: do(kind, case, cube)
        except Exception as e: print("ERR", case.name, cube, repr(e), file=sys.stderr, flush=True)
        finally:
            with cv: active[0] -= 1; cv.notify_all()

def pending(case):
    """Resume: the cubes of case not yet decided, from leaves.jsonl and top.icnf."""
    rs = case.records()
    if any(r.get("plain") and r.get("cake_lpr") == "s VERIFIED UNSAT" for r in rs): return None, []
    if not any(r.get("plain") for r in rs): return "plain", []
    if not any(r.get("top") for r in rs): return "top", []
    todo = {tuple(map(int, l.split()[1:-1])) for l in open(os.path.join(case.out, "top.icnf")) if l.startswith("a")}
    for r in rs:
        if r.get("top") or r.get("plain"): continue
        c = tuple(r["cube"])
        if r["status"] == "SPLIT":
            todo |= {c + tuple(s) for s in r["subs"]}
        if r["status"] in ("SPLIT", "SAT") or (r["status"] == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"):
            todo.discard(c)
    # children whose own record came before nothing: recompute until fixpoint
    done = {tuple(r["cube"]) for r in rs if "cube" in r and not r.get("plain") and
            (r["status"] in ("SPLIT", "SAT") or r.get("cake_lpr") == "s VERIFIED UNSAT")}
    return "cube", sorted(todo - done, key=lambda c: (len(c), c))

def finish(case):
    rs = case.records(); _, todo = pending(case)
    with open(os.path.join(case.out, "leaves.icnf"), "w") as f:
        for r in rs:
            if r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
    kind, _ = pending(case)
    with open(os.path.join(case.out, "open.icnf"), "w") as f:
        if kind in ("plain", "top"): f.write("a 0\n")
        for c in todo: f.write("a " + " ".join(map(str, c)) + " 0\n")

cases = []
for i, s in enumerate(a.cases):
    name, path = s.split("=", 1); cases.append(Case(i, name, path))
for c in cases:
    kind, todo = pending(c)
    if kind in ("plain", "top"): push(c, kind, None)
    for cube in todo: push(c, "cube", list(cube))
ths = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ths: t.start()
for t in ths: t.join()
for c in cases: finish(c)
