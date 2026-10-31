#!/usr/bin/env python3
"""W25 variant of results/Mii-S/scripts/close_march.py (original copied as close_march.orig.py).

  close_w25.py OUTROOT --deadline EPOCH --jobs 4 NAME=CASE.cnf ...
Changes: several cases share one pool of JOBS workers, served in the listed order (priority
by case index); each case first gets a plain `cadical -t 60` (UNSAT accepted only with cake_lpr
`s VERIFIED UNSAT`); then the close_march recipe (march_cu -d 7 top cubes, cadical --lrat -t 300,
march_cu -d 6 split on timeout, cake_lpr on every UNSAT).  Resumable: SPLIT records carry their
children, top cubes are kept in top.icnf, and a restart re-queues every cube without a terminal
record.  leaves.icnf lists only cake_lpr-verified leaves; open.icnf lists cubes still open.
"""
import argparse, hashlib, heapq, itertools, json, os, re, subprocess, threading, time
BIN = os.environ.get("BIN", "/home/user/work/bin")
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("cases", nargs="+")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--plain", type=int, default=60); ap.add_argument("--deadline", type=float, default=1e12)
ap.add_argument("--work", default="/home/user/work/tmp")
a = ap.parse_args()
lock = threading.Lock(); cv = threading.Condition(); heap = []; seq = itertools.count(); busy = [0]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
class Case:
    def __init__(s, idx, name, cnf):
        s.idx, s.name, s.cnf = idx, name, cnf; s.dir = os.path.join(a.out, name); os.makedirs(s.dir, exist_ok=True)
        hdr, s.body = open(cnf).read().split("\n", 1); s.nv, s.nc = int(hdr.split()[2]), int(hdr.split()[3])
        s.recs = [json.loads(l) for l in open(os.path.join(s.dir, "leaves.jsonl"))] if os.path.exists(os.path.join(s.dir, "leaves.jsonl")) else []
        s.log = open(os.path.join(s.dir, "leaves.jsonl"), "a")
    def rec(s, r):
        with lock: s.log.write(json.dumps(r) + "\n"); s.log.flush(); s.recs.append(r)
    def write(s, path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {s.nv} {s.nc + len(cube)}\n"); f.write(s.body); f.write("".join(f"{l} 0\n" for l in cube))
cases = [Case(i, *c.split("=", 1)) for i, c in enumerate(a.cases)]
def push(case, kind, cube=None):
    with cv: heapq.heappush(heap, (case.idx, next(seq), kind, case, cube)); cv.notify_all()
def wdir(case, tag):
    w = os.path.join(a.work, f"{case.name}_{tag}_{next(seq)}"); os.makedirs(w, exist_ok=True); return w
def cadical(case, cube, tlim, w, lrat=True):
    f = os.path.join(w, "f.cnf"); case.write(f, cube); p = os.path.join(w, "p.lrat"); t0 = time.time()
    args = [os.path.join(BIN, "cadical"), "-t", str(int(tlim)), f] + (["--lrat", "--binary=false", p] if lrat else [])
    with open(os.path.join(w, "out"), "w") as o: rc = subprocess.run(args, stdout=o).returncode
    r = {"cube": cube, "solve_s": round(time.time() - t0, 2), "rc": rc}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(p); t0 = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, p], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t0, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"; k = next(seq)
        subprocess.run(["cp", f, os.path.join(a.work, "..", f"SAT_{case.name}_{k}.cnf")]); subprocess.run(["cp", os.path.join(w, "out"), os.path.join(case.dir, f"SAT_{k}.model")])
        r["model_file"] = f"SAT_{k}.model"; open(os.path.join(a.out, "SAT_FOUND"), "a").write(f"{case.name} {k}\n")
    return r
def march(case, cube, d, tag):
    w = wdir(case, "m" + tag); case.write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(w, "cubes")) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    if tag == "top": subprocess.run(["cp", os.path.join(w, "cubes"), os.path.join(case.dir, "top.icnf")])
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
def do(kind, case, cube):
    if kind == "plain":
        w = wdir(case, "plain"); r = cadical(case, [], a.plain, w); subprocess.run(["rm", "-rf", w])
        r.update(plain=True, case_sha256=sha(case.cnf)); case.rec(r)
        if not (r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT") and r.get("status") != "SAT":
            push(case, "top")
    elif kind == "top":
        top, ms, line = march(case, [], a.depth, "top")
        case.rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line,
                  "case_sha256": sha(case.cnf), "top_icnf_sha256": sha(os.path.join(case.dir, "top.icnf"))})
        for c in top: push(case, "solve", c)
    else:
        left = a.deadline - time.time()
        if left < 30: case.rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); return
        tl = min(a.timeout, left); w = wdir(case, "s"); r = cadical(case, cube, tl, w); subprocess.run(["rm", "-rf", w])
        if r["rc"] not in (10, 20):
            if tl < a.timeout: r.update(status="OPEN", reason="deadline")
            else:
                subs, ms, line = march(case, cube, a.split_depth, "s")
                r.update(status="SPLIT", split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
                for s in subs: push(case, "solve", cube + s)
        case.rec(r)
# resume
for c in cases:
    plain = [r for r in c.recs if r.get("plain")]
    if not plain: push(c, "plain"); continue
    if plain[-1].get("status") == "SAT" or plain[-1].get("cake_lpr") == "s VERIFIED UNSAT": continue
    if not any(r.get("top") for r in c.recs) or not os.path.exists(os.path.join(c.dir, "top.icnf")): push(c, "top"); continue
    last = {}
    for r in c.recs:
        if "cube" in r and not r.get("plain"): last[tuple(r["cube"])] = r
    stack = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(c.dir, "top.icnf")) if l.startswith("a")]
    while stack:
        cu = stack.pop(); r = last.get(tuple(cu))
        if r is None or r.get("status") == "OPEN": push(c, "solve", cu)
        elif r.get("status") == "SPLIT": stack += [cu + s for s in r["subs"]]
def worker():
    while True:
        with cv:
            while not heap and busy[0] > 0: cv.wait()
            if not heap: cv.notify_all(); return
            _, _, kind, case, cube = heapq.heappop(heap); busy[0] += 1
        try: do(kind, case, cube)
        except Exception as e:
            case.rec({"cube": cube, "kind": kind, "status": "OPEN", "reason": "error " + repr(e)})
        finally:
            with cv: busy[0] -= 1; cv.notify_all()
ts = [threading.Thread(target=worker) for _ in range(a.jobs)]
for t in ts: t.start()
for t in ts: t.join()
# final files
for c in cases:
    last = {}
    for r in c.recs:
        if "cube" in r and not r.get("plain"): last[tuple(r["cube"])] = r
    ver = [k for k, r in last.items() if r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"]
    opn = []
    if os.path.exists(os.path.join(c.dir, "top.icnf")):
        stack = [list(map(int, l.split()[1:-1])) for l in open(os.path.join(c.dir, "top.icnf")) if l.startswith("a")]
        while stack:
            cu = stack.pop(); r = last.get(tuple(cu))
            if r is not None and r.get("status") == "SPLIT": stack += [cu + s for s in r["subs"]]
            elif not (r is not None and r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"): opn.append(cu)
    with open(os.path.join(c.dir, "leaves.icnf"), "w") as f:
        for k in sorted(ver, key=lambda k: (len(k), k)): f.write("a " + " ".join(map(str, k)) + " 0\n")
    with open(os.path.join(c.dir, "open.icnf"), "w") as f:
        for k in opn: f.write("a " + " ".join(map(str, k)) + " 0\n")
    print(c.name, "verified", len(ver), "open", len(opn))
