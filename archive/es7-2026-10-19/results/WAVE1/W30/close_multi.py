#!/usr/bin/env python3
"""W30 variant of results/Mii-S/scripts/close_march.py (copied here unchanged as close_march.py).

  close_multi.py OUTROOT --case NAME CASE.cnf [--case NAME CASE.cnf ...] --jobs 4 --deadline EPOCH

Same recipe per case: plain `cadical --lrat -t DIRECT` on the whole case first (accepted only with
cake_lpr `s VERIFIED UNSAT`); otherwise `march_cu CASE -d 7` top cubes (OUTROOT/NAME/top.icnf),
each cube solved by `cadical --lrat -t 300` and checked by cake_lpr, a timeout split by
`march_cu CASE+cube -d 6`.  Changes: one shared worker pool over all cases, cases served in the
listed order (priority = case index, then queue order); resumable from leaves.jsonl (a cube is
final when it has an UNSAT record verified by cake_lpr, or a SPLIT record, which stores its
children); no new solve starts after --deadline, and the cubes still pending are written to
open.icnf.  An UNSAT that cake_lpr does not verify is not a leaf and stays open.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time, queue, itertools
BIN = os.environ.get("BIN", "/home/user/bin")
ap = argparse.ArgumentParser(); ap.add_argument("out")
ap.add_argument("--case", nargs=2, action="append", required=True)
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--direct", type=int, default=60); ap.add_argument("--snapshot", action="store_true"); ap.add_argument("--deadline", type=float, default=1e12)
a = ap.parse_args()
lock = threading.Lock(); seq = itertools.count(); q = queue.PriorityQueue()
pending = {}  # case index -> number of unfinished cubes
cases = []
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
class Case:
    def __init__(s, i, name, cnf):
        s.i, s.name, s.cnf = i, name, cnf; s.dir = os.path.join(a.out, name); os.makedirs(s.dir, exist_ok=True)
        hdr, s.body = open(cnf).read().split("\n", 1); s.nv, s.nc = int(hdr.split()[2]), int(hdr.split()[3])
        s.logp = os.path.join(s.dir, "leaves.jsonl"); s.n = itertools.count(1); s.sha = sha(cnf)
    def rec(s, r):
        with lock:
            with open(s.logp, "a") as f: f.write(json.dumps(r) + "\n")
    def records(s):
        return [json.loads(l) for l in open(s.logp)] if os.path.exists(s.logp) else []
    def write(s, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {s.nv} {s.nc + len(cube)}\n"); f.write(s.body); f.write("".join(f"{l} 0\n" for l in cube))
def verified(r): return r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"
def run_cadical(C, cube, tmo, tag):
    w = os.path.join(C.dir, f"s_{tag}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    C.write(f, cube); t = time.time()
    with open(os.path.join(w, "out"), "w") as so:
        rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-t", str(tmo), f,
                             os.path.join(w, "p.lrat")], stdout=so).returncode
    r = {"cube": cube, "solve_s": round(time.time() - t, 2)}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(C.dir, f"SAT_{tag}.cnf")])
        subprocess.run(["cp", os.path.join(w, "out"), os.path.join(C.dir, f"SAT_{tag}.out")])
        open(os.path.join(a.out, "SAT_FOUND"), "a").write(f"{C.name} {tag}\n")
    else: r["status"] = "TIMEOUT"
    subprocess.run(["rm", "-rf", w]); return r
def march(C, cube, d, tag):
    w = os.path.join(C.dir, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    C.write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cp = os.path.join(w, "cubes"); txt = open(cp).read() if os.path.exists(cp) else ""
    cs = [list(map(int, l.split()[1:-1])) for l in txt.splitlines() if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, (m.group(0) if m else o[-200:]), txt
def submit(C, cube):
    with lock: pending[C.i] = pending.get(C.i, 0) + 1
    q.put((C.i, next(seq), cube))
def solve(C, cube):
    if time.time() > a.deadline:
        C.rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); return
    k = next(C.n); r = run_cadical(C, cube, a.timeout, f"{os.getpid()}_{k}")
    if r["status"] == "TIMEOUT":
        subs, ms, line, _ = march(C, cube, a.split_depth, f"{os.getpid()}_{k}")
        r.update(status="SPLIT", split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
        if not subs: r["status"] = "OPEN"; r["reason"] = "march gave no cubes"
    C.rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(C, cube + s)
def worker():
    while True:
        i, _, cube = q.get()
        try: solve(cases[i], cube)
        except Exception as e: cases[i].rec({"cube": cube, "status": "OPEN", "reason": f"error {e!r}"})
        finally:
            with lock: pending[i] -= 1
            q.task_done()
for i, (name, cnf) in enumerate(a.case): cases.append(Case(i, name, cnf))
def setup(C):
    """Direct attempt and top cubes, or resume from leaves.jsonl.  Returns cubes to queue, or None if closed."""
    R = C.records()
    if any(r.get("whole_case") and verified(r) for r in R): return None
    if not any(r.get("whole_case") for r in R) and time.time() < a.deadline:
        r = run_cadical(C, [], a.direct, "direct"); r.update(whole_case=True, case_sha256=C.sha); C.rec(r)
        if verified(r): return None
    tp = os.path.join(C.dir, "top.icnf")
    if not any(r.get("top") for r in R):
        top, ms, line, txt = march(C, [], a.depth, "top"); open(tp, "w").write(txt)
        m = re.search(r"number of cubes (\d+), including (\d+) refuted", line)
        C.rec({"top": True, "ncubes": len(top), "march_cubes": int(m.group(1)) if m else None,
               "refuted": int(m.group(2)) if m else None, "march_s": round(ms, 1), "march": line,
               "top_icnf_sha256": sha(tp), "case_sha256": C.sha})
        R = C.records()
    return frontier(C)
def frontier(C):
    R = C.records(); tp = os.path.join(C.dir, "top.icnf")
    if any(r.get("whole_case") and verified(r) for r in R): return []
    if not os.path.exists(tp): return None
    todo = [list(map(int, l.split()[1:-1])) for l in open(tp) if l.startswith("a")]
    final = {}
    for r in R:
        if "cube" in r and not r.get("whole_case") and (verified(r) or r.get("status") in ("SPLIT", "SAT")):
            final[tuple(r["cube"])] = r
    out, stack = [], list(todo)
    while stack:
        c = stack.pop(); r = final.get(tuple(c))
        if r is None: out.append(c)
        elif r["status"] == "SPLIT": stack.extend(c + s for s in r["subs"])
    return out
def snapshot():
    for C in cases:
        R = C.records(); whole = any(r.get("whole_case") and verified(r) for r in R)
        with open(os.path.join(C.dir, "leaves.icnf"), "w") as f:
            if whole: f.write("a 0\n")
            else:
                for r in R:
                    if not r.get("whole_case") and "cube" in r and verified(r): f.write("a " + " ".join(map(str, r["cube"])) + " 0\n")
        op = frontier(C)
        with open(os.path.join(C.dir, "open.icnf"), "w") as f:
            if op is None: f.write("a 0\n")
            else:
                for c in op: f.write("a " + " ".join(map(str, c)) + " 0\n")
if a.snapshot: snapshot(); raise SystemExit
ths = [threading.Thread(target=worker, daemon=True) for _ in range(a.jobs)]
for t in ths: t.start()
# set up cases in order; the direct and march-top steps of case i+1 run while case i's cubes are in the pool
for C in cases:
    todo = setup(C)
    if todo is not None:
        for c in todo: submit(C, c)
q.join()
snapshot()
