#!/usr/bin/env python3
"""W33 copy of results/Mii-S/scripts/close_march.py: same recipe, several cases on one shared
priority pool (earlier cases first).

  close_march_w33.py --cases NAME=CASE.cnf ... --root OUTROOT --jobs 4 --deadline EPOCH
                     [--plain 60] [--shard s --nshards k]
Per case (in the order given): plain `cadical --lrat -t PLAIN` on the whole case (accepted only on
cake_lpr `s VERIFIED UNSAT`); if not closed, `march_cu CASE -d DEPTH -o top.icnf` (kept in the case
dir), cubes with 0-based index i, i mod k == s are queued.  Each cube c: CASE + units(c) by
`cadical --lrat -t TIMEOUT`, UNSAT checked with cake_lpr; a timeout is split by `march_cu -d SPLIT`
and its children queued.  Changes from close_march.py: shared pool across cases, --shard/--nshards,
SPLIT records list their children (`subs`) so a rerun resumes from leaves.jsonl, leaves.icnf holds
only cake_lpr-verified leaves, open.icnf holds cubes not closed, SAT models are kept.
"""
import argparse, hashlib, heapq, json, os, re, subprocess, threading, time, sys
BIN = os.environ.get("BIN", "/opt/w33/bin")
ap = argparse.ArgumentParser(); ap.add_argument("--cases", nargs="+", required=True); ap.add_argument("--root", required=True)
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--plain", type=int, default=60); ap.add_argument("--deadline", type=float, default=1e18)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--work", default="/opt/w33/work"); ap.add_argument("--finish-only", action="store_true")
a = ap.parse_args()
VER = "s VERIFIED UNSAT"
lock = threading.Lock(); cv = threading.Condition(); count = [0]; nid = [0]
heap = []; seq = [0]  # (case index, seq): earlier cases first, so cases close in the listed order

class Case:
    def __init__(s, name, path):
        s.name, s.path = name, path; s.out = os.path.join(a.root, name); os.makedirs(s.out, exist_ok=True)
        hdr, s.body = open(path).read().split("\n", 1); s.nv, s.nc = int(hdr.split()[2]), int(hdr.split()[3])
        s.sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
        s.logp = os.path.join(s.out, "leaves.jsonl")
        s.recs = [json.loads(l) for l in open(s.logp)] if os.path.exists(s.logp) else []
        s.log = open(s.logp, "a"); s.pending = 0; s.finished = False
    def rec(s, r):
        with lock: s.log.write(json.dumps(r) + "\n"); s.log.flush(); s.recs.append(r)
    def write(s, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {s.nv} {s.nc + len(cube)}\n"); f.write(s.body); f.write("".join(f"{l} 0\n" for l in cube))

def wdir():
    with lock: nid[0] += 1; k = nid[0]
    w = os.path.join(a.work, f"w{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); return w

def march(C, cube, d, dest=None):
    w = wdir(); C.write(os.path.join(w, "f.cnf"), cube); t = time.time(); cf = dest or os.path.join(w, "cubes")
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o", cf],
                       capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]

def cadical(C, cube, tlim):
    """returns record dict with status UNSAT/SAT/UNKNOWN (UNSAT carries the cake_lpr line)."""
    w = wdir(); f = os.path.join(w, "f.cnf"); C.write(f, cube); t = time.time()
    with open(os.path.join(w, "out"), "w") as so:
        p = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(tlim), f,
                            os.path.join(w, "p.lrat")], stdout=so)
    rc = p.returncode; r = {"solve_s": round(time.time() - t, 2)}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True)
        r["cake_lpr"] = next((l for l in o.stdout.splitlines() if l.startswith("s ")), (o.stdout + o.stderr)[-200:])
        r["check_s"] = round(time.time() - t, 2); r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; k = len([x for x in os.listdir(C.out) if x.startswith("SAT_")])
        subprocess.run(["cp", os.path.join(w, "out"), os.path.join(C.out, f"SAT_{k}.model")])
        json.dump({"cube": cube}, open(os.path.join(C.out, f"SAT_{k}.cube.json"), "w"))
        print(f"!!! SAT in {C.name} cube {cube}", flush=True)
    else:
        r["status"] = "UNKNOWN"; r["rc"] = rc
    subprocess.run(["rm", "-rf", w]); return r

def submit(fn, *args):
    with cv:
        count[0] += 1; seq[0] += 1; heapq.heappush(heap, (args[0].idx, seq[0], fn, args)); cv.notify_all()

def worker():
    while True:
        with cv:
            while not heap:
                if count[0] == 0: return
                cv.wait(timeout=60)
            _, _, fn, args = heapq.heappop(heap)
        try: fn(*args)
        except Exception as e: print("ERR", e, file=sys.stderr, flush=True)
        finally:
            with cv: count[0] -= 1; cv.notify_all()

def cube_task(C, cube):
    if time.time() > a.deadline: return
    r = {"cube": cube}; r.update(cadical(C, cube, a.timeout))
    if r["status"] == "UNKNOWN":
        if time.time() > a.deadline: r["status"] = "OPEN"; C.rec(r); return
        subs, ms, line = march(C, cube, a.split_depth)
        r.update(status="SPLIT", split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
    C.rec(r)
    if r["status"] == "SPLIT":
        for s in subs: submit(cube_task, C, cube + s)

def top_task(C):
    if time.time() > a.deadline: return
    tp = os.path.join(C.out, "top.icnf")
    top, ms, line = march(C, [], a.depth, dest=tp)
    C.rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line, "case_sha256": C.sha,
           "top_sha256": hashlib.sha256(open(tp, "rb").read()).hexdigest(), "shard": a.shard, "nshards": a.nshards})
    for i, c in enumerate(top):
        if i % a.nshards == a.shard: submit(cube_task, C, c)

def whole_task(C):
    if time.time() > a.deadline: return
    r = {"whole": True, "case_sha256": C.sha, "plain_s": a.plain}; r.update(cadical(C, [], a.plain)); C.rec(r)
    if not (r["status"] == "UNSAT" and r["cake_lpr"] == VER) and r["status"] != "SAT":
        submit(top_task, C)

def resume(C):
    R = C.recs
    if any(r.get("whole") and r.get("cake_lpr") == VER for r in R): return
    if not any(r.get("whole") for r in R): submit(whole_task, C); return
    top = [r for r in R if r.get("top")]
    if not top: submit(top_task, C); return
    cubes = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(C.out, "top.icnf")) if l.startswith("a")]
    want = [c for i, c in enumerate(cubes) if i % a.nshards == a.shard]
    for r in R:
        if r.get("status") == "SPLIT": want += [r["cube"] + s for s in r["subs"]]
    done = {tuple(r["cube"]) for r in R if "cube" in r and r["status"] in ("UNSAT", "SPLIT", "SAT")}
    for c in want:
        if tuple(c) not in done: submit(cube_task, C, c)

def finish(C):
    """leaves.icnf (cake_lpr-verified leaves) and open.icnf (everything not closed) from leaves.jsonl."""
    R = C.recs
    if any(r.get("whole") and r.get("cake_lpr") == VER for r in R):
        open(os.path.join(C.out, "leaves.icnf"), "w").write("a 0\n")
        open(os.path.join(C.out, "open.icnf"), "w").write(""); return
    ok = [r["cube"] for r in R if "cube" in r and r["status"] == "UNSAT" and r.get("cake_lpr") == VER]
    with open(os.path.join(C.out, "leaves.icnf"), "w") as f:
        for c in ok: f.write("a " + " ".join(map(str, c)) + " 0\n")
    tp = os.path.join(C.out, "top.icnf"); want = []
    if os.path.exists(tp):
        cubes = [list(map(int, l.split()[1:-1])) for l in open(tp) if l.startswith("a")]
        want = [c for i, c in enumerate(cubes) if i % a.nshards == a.shard]
    else: want = [[]]
    for r in R:
        if r.get("status") == "SPLIT": want += [r["cube"] + s for s in r["subs"]]
    closed = {tuple(r["cube"]) for r in R if "cube" in r and r["status"] in ("SPLIT",) or
              ("cube" in r and r["status"] == "UNSAT" and r.get("cake_lpr") == VER)}
    with open(os.path.join(C.out, "open.icnf"), "w") as f:
        for c in want:
            if tuple(c) not in closed: f.write("a " + " ".join(map(str, c)) + " 0\n")

os.makedirs(a.work, exist_ok=True)
cases = [Case(*x.split("=", 1)) for x in a.cases]
for i, C in enumerate(cases): C.idx = i
if a.finish_only:
    for C in cases: finish(C)
    sys.exit(0)
for C in cases: resume(C)
ws = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ws: t.start()
for t in ws: t.join()
for C in cases: finish(C)
print("ALL DONE", flush=True)
