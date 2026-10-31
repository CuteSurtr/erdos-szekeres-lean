#!/usr/bin/env python3
"""W35 driver: close_march.py (results/Mii-S/scripts, copied here unchanged) run over a list of
cases with one shared priority pool, resumable.

  close_march_w35.py ENTRY.json CASEDIR OUTROOT --jobs 4 --deadline UNIX_TIME [--work DIR]

Cases are taken in the listed order: lower case index runs first, later cases only backfill idle
cores.  Per case (CASEDIR/<case>.cnf, sha256 checked against the entry):
  1. whole: `cadical --lrat -t 60` on the case; UNSAT accepted only with cake_lpr `s VERIFIED UNSAT`.
  2. otherwise the close_march recipe: `march_cu CASE -d 7` top cubes (saved as top.icnf),
     each cube solved by `cadical --lrat -t 300`, UNSAT checked by cake_lpr, a timeout split by
     `march_cu CASE+cube -d 6` and the children queued.
Records go to OUTROOT/<case>/leaves.jsonl.  A SPLIT record lists its children ("subs"), so the
state can be rebuilt from leaves.jsonl + top.icnf: on restart only cubes without a final record
are re-queued.  Final records: whole/cube UNSAT with cake_lpr VERIFIED, SPLIT with subs, SAT,
UNSAT_UNCHECKED (cake_lpr did not verify; stays in open.icnf).
leaves.icnf = VERIFIED leaves (`a lits 0`, `a 0` for a whole-case closure); open.icnf = cubes
without a verified leaf below them.  After the deadline no new solver call starts.
"""
import argparse, hashlib, heapq, json, os, re, subprocess, threading, time
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("entry"); ap.add_argument("cases"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--whole-timeout", type=int, default=60)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--deadline", type=float, default=1e18); ap.add_argument("--work", default="/tmp/claude-0/w/work")
a = ap.parse_args()
entry = json.load(open(a.entry)); CASES = [c["case"] for c in entry["cases"]]
SHA = {c["case"]: c["cnf_sha256"] for c in entry["cases"]}
VER = "s VERIFIED UNSAT"
lock = threading.Lock(); cv = threading.Condition(lock); heap = []; seq = [0]; busy = [0]; stop = [False]
CNF = {}

def key(c): return " ".join(map(str, c))

class Case:
    def __init__(s, idx, name):
        s.idx, s.name = idx, name; s.dir = os.path.join(a.out, name); os.makedirs(s.dir, exist_ok=True)
        s.cnf = os.path.join(a.cases, name + ".cnf")
        h = hashlib.sha256(open(s.cnf, "rb").read()).hexdigest()
        assert h == SHA[name], (name, h)
        s.sha = h; s.log = open(os.path.join(s.dir, "leaves.jsonl"), "a")
        s.recs = [json.loads(l) for l in open(os.path.join(s.dir, "leaves.jsonl")) if l.strip()]
    def rec(s, r):
        with lock: s.log.write(json.dumps(r) + "\n"); s.log.flush(); s.recs.append(r)
    def body(s):
        if s.name not in CNF:
            hdr, b = open(s.cnf).read().split("\n", 1); CNF[s.name] = (int(hdr.split()[2]), int(hdr.split()[3]), b)
        return CNF[s.name]
    def write(s, path, cube):
        nv, nc, b = s.body()
        with open(path, "w") as f:
            f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(b); f.write("".join(f"{l} 0\n" for l in cube))
    def top(s):
        p = os.path.join(s.dir, "top.icnf")
        return [list(map(int, l.split()[1:-1])) for l in open(p) if l.startswith("a")] if os.path.exists(p) else None
    def state(s):
        """(closed_whole, top cubes or None, final records by cube key, pending cubes)"""
        whole = [r for r in s.recs if r.get("whole")]
        if any(r["status"] == "UNSAT" and r.get("cake_lpr") == VER for r in whole):
            return True, None, {}, []
        top = s.top(); final = {}
        for r in s.recs:
            if "cube" in r and r["status"] in ("UNSAT", "SPLIT", "SAT", "UNSAT_UNCHECKED"): final[key(r["cube"])] = r
        if top is None: return False, None, final, None
        pend, stack = [], list(top)
        while stack:
            c = stack.pop(); r = final.get(key(c))
            if r is None: pend.append(c)
            elif r["status"] == "SPLIT": stack.extend(c + x for x in r["subs"])
        return False, top, final, pend
    def finish_files(s):
        closed, top, final, pend = s.state()
        with open(os.path.join(s.dir, "leaves.icnf"), "w") as f:
            if closed: f.write("a 0\n")
            else:
                for r in s.recs:
                    if "cube" in r and r["status"] == "UNSAT" and r.get("cake_lpr") == VER:
                        f.write("a " + " ".join(map(str, r["cube"] + [0])) + "\n")
        op = []
        if not closed:
            if top is None: op = [[]]
            else:
                op = pend + [r["cube"] for r in final.values() if r["status"] in ("SAT", "UNSAT_UNCHECKED")]
        with open(os.path.join(s.dir, "open.icnf"), "w") as f:
            for c in op: f.write("a " + " ".join(map(str, c + [0])) + "\n")
        return closed, top, pend

def push(prio, fn, *args):
    with cv: seq[0] += 1; heapq.heappush(heap, (prio, seq[0], fn, args)); cv.notify()

def cadical(case, cube, tmo, tag):
    w = os.path.join(a.work, f"{case.name}_{tag}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    case.write(f, cube); t = time.time()
    with open(os.path.join(w, "out.txt"), "w") as o:
        rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(tmo), f,
                             os.path.join(w, "p.lrat")], stdout=o).returncode
    r = {"cube": cube, "solve_s": round(time.time() - t, 2)}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat"))
        t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if r["cake_lpr"] == VER else "UNSAT_UNCHECKED"
    elif rc == 10:
        r["status"] = "SAT"; d = os.path.join(a.work, "SAT"); os.makedirs(d, exist_ok=True)
        subprocess.run(["cp", f, os.path.join(d, f"{case.name}_{tag}.cnf")])
        subprocess.run(["cp", os.path.join(w, "out.txt"), os.path.join(d, f"{case.name}_{tag}.model")])
        r["model_file"] = os.path.join(d, f"{case.name}_{tag}.model")
    else: r["status"] = "TIMEOUT"
    subprocess.run(["rm", "-rf", w]); return r

def march(case, cube, d, tag):
    w = os.path.join(a.work, f"{case.name}_m{tag}"); os.makedirs(w, exist_ok=True)
    case.write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    raw = open(os.path.join(w, "cubes"), "rb").read()
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m, raw

def t_whole(case):
    r = cadical(case, [], a.whole_timeout, "whole"); r["whole"] = True; r["case_sha256"] = case.sha
    case.rec(r)
    if r["status"] == "SAT": stop[0] = True
    elif r["status"] != "UNSAT": push((case.idx, 1), t_top, case)

def t_top(case):
    cs, ms, m, raw = march(case, [], a.depth, "top")
    open(os.path.join(case.dir, "top.icnf"), "wb").write(raw)
    case.rec({"top": True, "ncubes": len(cs), "refuted": int(m.group(2)) if m else None,
              "march": m.group(0) if m else None, "march_s": round(ms, 1),
              "top_sha256": hashlib.sha256(raw).hexdigest(), "case_sha256": case.sha})
    for c in cs: push((case.idx, 2), t_cube, case, c)

def t_cube(case, cube):
    seq_tag = hashlib.md5(key(cube).encode()).hexdigest()[:10]
    r = cadical(case, cube, a.timeout, seq_tag)
    if r["status"] == "TIMEOUT":
        subs, ms, m, _ = march(case, cube, a.split_depth, seq_tag)
        r.update(status="SPLIT", split_s=round(ms, 1), march=m.group(0) if m else None, nsub=len(subs), subs=subs)
    case.rec(r)
    if r["status"] == "SAT": stop[0] = True
    if r["status"] == "SPLIT":
        for s in subs: push((case.idx, 2), t_cube, case, cube + s)

def worker():
    while True:
        with cv:
            while not heap and busy[0] > 0: cv.wait()
            if not heap: cv.notify_all(); return
            _, _, fn, args = heapq.heappop(heap); busy[0] += 1
        try:
            if time.time() < a.deadline and not stop[0]: fn(*args)
        except Exception as e:
            print("ERROR", fn.__name__, args[0].name, repr(e), flush=True)
        finally:
            with cv: busy[0] -= 1; cv.notify_all()

os.makedirs(a.work, exist_ok=True)
cases = [Case(i, n) for i, n in enumerate(CASES)]
for c in cases:   # resume
    closed, top, final, pend = c.state()
    if closed: continue
    if any(r.get("whole") and r["status"] == "SAT" for r in c.recs) or any(r["status"] == "SAT" for r in final.values()):
        stop[0] = True
    if top is None:
        if any(r.get("whole") for r in c.recs): push((c.idx, 1), t_top, c)
        else: push((c.idx, 0), t_whole, c)
    else:
        for cube in pend: push((c.idx, 2), t_cube, c, cube)
def snapshot():
    while True:
        time.sleep(300)
        with lock: pass
        for c in cases:
            try: c.finish_files()
            except Exception as e: print("snap", c.name, e, flush=True)
threading.Thread(target=snapshot, daemon=True).start()
ts = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ts: t.start()
for t in ts: t.join()
for c in cases: c.finish_files()
print("DONE", "SAT_STOP" if stop[0] else "", flush=True)
