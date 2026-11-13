#!/usr/bin/env python3
"""W34 driver: kind "cases" entry of verify/ii_wave1.json, adapted from results/Mii-S/scripts/close_march.py.

  run_w34.py ASSIGN.json CASEDIR OUTROOT --jobs 4 --stop-at EPOCH
For each case in the listed order (one global priority queue, earlier cases first):
  1. whole: `cadical --lrat -t 60 CASE.cnf`; UNSAT counts only with cake_lpr `s VERIFIED UNSAT`.
  2. top:   `march_cu CASE -d 7 -o top.icnf` (kept in OUTROOT/<case>/top.icnf).
  3. cube c: CASE+units(c) by `cadical --lrat -t 300`, UNSAT checked by cake_lpr (proof deleted);
     a timeout is split by `march_cu CASE+units(c) -d 6` and the children c+s are queued.
Records go to OUTROOT/<case>/leaves.jsonl.  leaves.icnf lists only cake_lpr-verified leaves
(`a lits 0`, relative to the case CNF; a whole-case closure is `a 0`), open.icnf the cubes
still open.  Resumable: on restart the state is rebuilt from leaves.jsonl and top.icnf.
"""
import argparse, hashlib, heapq, itertools, json, os, re, subprocess, threading, time
BIN = os.environ.get("BIN", "/home/user/tools/bin")
SCR = os.environ.get("SCR", "/home/user/work/scratch")
ap = argparse.ArgumentParser(); ap.add_argument("assign"); ap.add_argument("casedir"); ap.add_argument("outroot")
ap.add_argument("--jobs", type=int, default=4); ap.add_argument("--stop-at", type=float, default=1e18)
ap.add_argument("--whole-timeout", type=int, default=60); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--split-depth", type=int, default=6)
a = ap.parse_args()
VER = "s VERIFIED UNSAT"
cases = json.load(open(a.assign)); lock = threading.Lock(); seq = itertools.count()
heap = []; cv = threading.Condition(lock); running = [0]; uid = itertools.count()
st = {}  # case -> state

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def key(c): return " ".join(map(str, c))

class Case:
    def __init__(s, i, c):
        s.i, s.name = i, c["case"]; s.cnf = os.path.join(a.casedir, s.name + ".cnf")
        s.out = os.path.join(a.outroot, s.name); os.makedirs(s.out, exist_ok=True)
        s.log = os.path.join(s.out, "leaves.jsonl"); s.expected = c["expected"]
        hdr, s.body = open(s.cnf).read().split("\n", 1); s.nv, s.nc = int(hdr.split()[2]), int(hdr.split()[3])
        s.done = {}; s.whole = None; s.top = None; s.children = {}; s.bad = set()
        if os.path.exists(s.log):
            for l in open(s.log):
                r = json.loads(l)
                if r.get("whole"): s.whole = r
                elif r.get("top"): s.top = r
                elif r.get("status") in ("UNSAT", "SPLIT", "SAT"):
                    s.done[key(r["cube"])] = r
                    if r["status"] == "SPLIT": s.children[key(r["cube"])] = r["children"]
    def rec(s, r):
        with open(s.log, "a") as f: f.write(json.dumps(r) + "\n")
    def closed_whole(s): return s.whole is not None and s.whole.get("cake_lpr") == VER
    def top_cubes(s):
        return [list(map(int, l.split()[1:-1])) for l in open(os.path.join(s.out, "top.icnf")) if l.startswith("a")]
    def pending(s):
        """Cubes of the tree not yet decided (leaves to do)."""
        if s.closed_whole() or s.top is None: return []
        todo, out = list(s.top_cubes()), []
        while todo:
            c = todo.pop(); r = s.done.get(key(c))
            if r is None: out.append(c)
            elif r["status"] == "SPLIT": todo += [c + x for x in r["children"]]
        return out
    def leaves(s):
        if s.closed_whole(): return [[]]
        return [r["cube"] for r in s.done.values() if r["status"] == "UNSAT" and r.get("cake_lpr") == VER]
    def opens(s):
        if s.closed_whole(): return []
        if s.top is None: return [[]]
        bad = [r["cube"] for r in s.done.values() if r["status"] in ("UNSAT", "SAT") and r.get("cake_lpr") != VER]
        return s.pending() + bad
    def write_icnf(s):
        for fn, cs in (("leaves.icnf", s.leaves()), ("open.icnf", s.opens())):
            with open(os.path.join(s.out, fn + ".tmp"), "w") as f:
                f.writelines("a " + " ".join(map(str, c) if c else []) + (" 0\n" if c else "0\n") for c in cs)
            os.replace(os.path.join(s.out, fn + ".tmp"), os.path.join(s.out, fn))
    def write(s, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {s.nv} {s.nc + len(cube)}\n"); f.write(s.body); f.write("".join(f"{l} 0\n" for l in cube))

def push(pri, task):
    with cv: heapq.heappush(heap, (pri, next(seq), task)); cv.notify_all()

def cadical_cake(C, cube, timeout, w):
    f = os.path.join(w, "f.cnf"); p = os.path.join(w, "p.lrat")
    if cube is None: f = C.cnf
    else: C.write(f, cube)
    t = time.time(); pr = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(timeout), f, p],
                                         capture_output=True, text=True)
    r = {"solve_s": round(time.time() - t, 2), "rc": pr.returncode}
    if pr.returncode == 20:
        r["status"] = "UNSAT"; r["proof_bytes"] = os.path.getsize(p); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, p], capture_output=True, text=True)
        r["cake_lpr"] = next((l for l in o.stdout.splitlines() if l.startswith("s ")), (o.stdout + o.stderr)[-150:])
        r["check_s"] = round(time.time() - t, 2)
    elif pr.returncode == 10:
        r["status"] = "SAT"; n = next(uid)
        subprocess.run(["cp", f, os.path.join(C.out, f"SAT_{n}.cnf.tmp")])  # never committed (CNF)
        with open(os.path.join(C.out, f"SAT_{n}.model"), "w") as g: g.write(pr.stdout)
        r["sat_model"] = f"SAT_{n}.model"
    else: r["status"] = "TIMEOUT"
    return r

def march(C, cube, d, w, outp):
    f = os.path.join(w, "m.cnf"); C.write(f, cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), f, "-d", str(d), "-o", outp], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(outp) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    return cs, round(time.time() - t, 1), (m.group(0) if m else o[-200:]), m

def run(task):
    kind, name = task[0], task[1]; C = st[name]
    if time.time() > a.stop_at: return
    w = os.path.join(SCR, f"{name}_{next(uid)}"); os.makedirs(w, exist_ok=True)
    try:
        if kind == "whole":
            r = cadical_cake(C, None, a.whole_timeout, w); r.update(whole=True, cnf_sha256=sha(C.cnf))
            with lock: C.whole = r; C.rec(r)
            if r.get("cake_lpr") == VER:
                with lock: C.write_icnf()
            else: push((C.i, 1), ("top", name))
        elif kind == "top":
            tp = os.path.join(C.out, "top.icnf")
            cs, ms, line, m = march(C, [], a.depth, w, tp + ".tmp"); os.replace(tp + ".tmp", tp)
            r = {"top": True, "ncubes": len(cs), "refuted": int(m.group(2)) if m else None, "march_s": ms, "march": line,
                 "top_sha256": sha(tp), "case_sha256": sha(C.cnf)}
            with lock: C.top = r; C.rec(r); C.write_icnf()
            for c in cs: push((C.i, 2, len(c)), ("cube", name, c))
        else:
            cube = task[2]
            r = cadical_cake(C, cube, a.timeout, w); r["cube"] = cube
            if r["status"] == "TIMEOUT":
                if time.time() > a.stop_at: return
                subs, ms, line, _ = march(C, cube, a.split_depth, w, os.path.join(w, "sub.icnf"))
                r.update(status="SPLIT" if subs else "SPLIT_EMPTY", split_s=ms, march=line, nsub=len(subs), children=subs)
            with lock:
                C.rec(r)
                if r["status"] in ("UNSAT", "SPLIT", "SAT"): C.done[key(cube)] = r
            if r["status"] == "SPLIT":
                for s in subs: push((C.i, 2, len(cube) + len(s)), ("cube", name, cube + s))
    finally:
        subprocess.run(["rm", "-rf", w])

def worker():
    while True:
        with cv:
            while not heap and running[0] > 0: cv.wait()
            if not heap: cv.notify_all(); return
            _, _, task = heapq.heappop(heap); running[0] += 1
        try: run(task)
        except Exception as e:
            print("ERR", task[:2], repr(e), flush=True)
        finally:
            with cv: running[0] -= 1; cv.notify_all()

for i, c in enumerate(cases):
    C = Case(i, c); st[C.name] = C
    assert sha(C.cnf) == C.expected, C.name
    if C.closed_whole(): continue
    if C.whole is None: push((i, 0), ("whole", C.name))
    elif C.top is None: push((i, 1), ("top", C.name))
    else:
        for cb in C.pending(): push((i, 2, len(cb)), ("cube", C.name, cb))
def status():
    while True:
        time.sleep(300)
        with lock:
            for C in st.values(): C.write_icnf()
threading.Thread(target=status, daemon=True).start()
ths = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ths: t.start()
for t in ths: t.join()
with lock:
    for C in st.values(): C.write_icnf()
print("DRIVER DONE", time.strftime("%H:%M:%S"), flush=True)
