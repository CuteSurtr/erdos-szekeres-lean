#!/usr/bin/env python3
"""Mi-0 shard driver: solve cubes (index i with i % 4 == 0 of cubes.icnf) of hm33k7.sub.cnf.
Each node = list of cube literals.  cadical --lrat (text) streamed through a FIFO into
lrat-check against CNF+cube units.  Timeout (300 s) -> split with march_cu -d 6 on CNF+cube;
children = cube + subcube.  The split itself is certified by a coverage leaf:
CNF + cube + negations of all subcubes must be UNSAT (LRAT-checked); this covers the
sub-branches march_cu refuted.  Records go to leaves.jsonl (append-only, also the resume state).
"""
import sys, os, json, subprocess, time, threading, queue, hashlib
from concurrent.futures import ThreadPoolExecutor
sys.setrecursionlimit(100000)
CNF, CUBES, OUT, WD = sys.argv[1:5]
NW = int(sys.argv[5]) if len(sys.argv) > 5 else 4
TLIM = 300; COV_TLIM = 3000
BIN = "/opt/es7/bin"
os.makedirs(WD, exist_ok=True)
head, body = None, []
with open(CNF) as f:
    for l in f:
        if l.startswith('p'): head = l.split(); continue
        if l.startswith('c'): continue
        body.append(l)
NV, NC = int(head[2]), int(head[3]); BODY = "".join(body); del body
lock = threading.Lock()
LEAVES = os.path.join(OUT, "leaves.jsonl")
def rec(d):
    with lock:
        with open(LEAVES, "a") as f: f.write(json.dumps(d) + "\n"); f.flush(); os.fsync(f.fileno())
def key(kind, cube): return kind + ":" + " ".join(map(str, cube))
def write_cnf(path, cube, extra=()):
    with open(path, "w") as f:
        f.write(f"p cnf {NV} {NC + len(cube) + len(extra)}\n"); f.write(BODY)
        for l in cube: f.write(f"{l} 0\n")
        for c in extra: f.write(" ".join(map(str, c)) + " 0\n")
def solve(tag, cube, extra, tlim):
    h = hashlib.sha1(tag.encode()).hexdigest()[:16]
    cnf = os.path.join(WD, h + ".cnf"); fifo = os.path.join(WD, h + ".fifo")
    write_cnf(cnf, cube, extra)
    if os.path.exists(fifo): os.remove(fifo)
    os.mkfifo(fifo)
    t0 = time.time()
    chk = subprocess.Popen([BIN + "/lrat-check", cnf, fifo], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    cad = subprocess.run([BIN + "/cadical", "-q", "--lrat", "--binary=false", "-t", str(tlim), cnf, fifo],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0
    try: cout, _ = chk.communicate(timeout=3600)
    except subprocess.TimeoutExpired: chk.kill(); cout = "lrat-check timeout"
    dtc = time.time() - t0
    st = [l for l in cad.stdout.splitlines() if l.startswith("s ")]
    st = st[0][2:] if st else "UNKNOWN"
    model = None
    if st == "SATISFIABLE":
        model = [int(x) for l in cad.stdout.splitlines() if l.startswith("v ") for x in l.split()[1:] if x != "0"]
    lr = "VERIFIED" if "c VERIFIED" in cout else ("NOT VERIFIED" if "NOT VERIFIED" in cout else "?")
    os.remove(cnf); os.remove(fifo)
    return st, dt, dtc, lr, model
def split(cube):
    h = hashlib.sha1(key("split", cube).encode()).hexdigest()[:16]
    cnf = os.path.join(WD, h + ".s.cnf"); icnf = os.path.join(WD, h + ".icnf")
    write_cnf(cnf, cube); t0 = time.time()
    r = subprocess.run([BIN + "/march_cu", cnf, "-d", "6", "-o", icnf], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0
    subs = []
    if os.path.exists(icnf):
        for l in open(icnf):
            t = l.split()
            if t and t[0] == "a": subs.append([int(x) for x in t[1:-1]])
    info = [l for l in r.stdout.splitlines() if "refuted" in l or "cubes" in l or l.startswith("s ")]
    os.remove(cnf)
    if os.path.exists(icnf): os.remove(icnf)
    return subs, dt, info
done = {}
if os.path.exists(LEAVES):
    for l in open(LEAVES):
        d = json.loads(l); done[d["key"]] = d
def covers(cubes, d):
    """exact: the cubes (literal sequences in split order) form a complete binary partition."""
    if any(len(c) == d for c in cubes): return len(cubes) == 1
    vs = set(abs(c[d]) for c in cubes)
    if len(vs) != 1: return False
    pos = [c for c in cubes if c[d] > 0]; neg = [c for c in cubes if c[d] < 0]
    return bool(pos) and bool(neg) and covers(pos, d + 1) and covers(neg, d + 1)
def node(cube, origin):
    """Process one node; return list of child cubes to schedule."""
    k = key("cube", cube)
    if k in done and done[k]["status"] in ("UNSAT", "SAT", "SPLIT"):
        d = done[k]
    else:
        st, dt, dtc, lr, model = solve(k, cube, (), TLIM)
        d = {"key": k, "kind": "cube", "origin": origin, "cube": cube, "status": st if st != "UNKNOWN" else "TIMEOUT",
             "solve_s": round(dt, 2), "total_s": round(dtc, 2), "lrat": lr if st == "UNSATISFIABLE" else None}
        if st == "UNSATISFIABLE": d["status"] = "UNSAT"
        if st == "SATISFIABLE":
            d["status"] = "SAT"; d["model"] = model
            with open(os.path.join(OUT, "SAT_" + hashlib.sha1(k.encode()).hexdigest()[:12] + ".json"), "w") as f: json.dump(d, f)
        if os.environ.get("FORCESPLIT") and origin is not None and len(cube) < 4 and d["status"] == "UNSAT": d["status"] = "TIMEOUT"
        if d["status"] == "TIMEOUT":
            rec(d)
            subs, sdt, info = split(cube)
            if subs == [[]]: subs = []
            d = {"key": k, "kind": "cube", "origin": origin, "cube": cube, "status": "SPLIT", "split_s": round(sdt, 2),
                 "children": [cube + s for s in subs], "march_info": info}
        rec(d); done[k] = d
    if d["status"] == "UNSAT" and d.get("lrat") != "VERIFIED":
        print("WARNING lrat not verified", k, flush=True)
    if d["status"] != "SPLIT": return []
    ch = d["children"]
    if not ch:  # march_cu refuted the whole node ("a 0"): certify with a long CDCL run
        kc = key("long", cube)
        if not (kc in done and done[kc]["status"] == "UNSAT"):
            st, dt, dtc, lr, model = solve(kc, cube, (), COV_TLIM)
            dc = {"key": kc, "kind": "long", "cube": cube, "status": {"UNSATISFIABLE": "UNSAT", "SATISFIABLE": "SAT"}.get(st, "TIMEOUT"),
                  "solve_s": round(dt, 2), "total_s": round(dtc, 2), "lrat": lr if st == "UNSATISFIABLE" else None}
            if st == "SATISFIABLE": dc["model"] = model
            rec(dc); done[kc] = dc
        return []
    if not done.get(key("partition", cube)):
        ok = covers([c[len(cube):] for c in ch], 0)
        dp = {"key": key("partition", cube), "kind": "partition", "cube": cube, "n_children": len(ch), "status": "OK" if ok else "FAIL"}
        rec(dp); done[dp["key"]] = dp
        if not ok: print("PARTITION FAIL", cube, flush=True); return []
    return ch
def main():
    cubes = [l for l in open(CUBES) if l.strip()]
    mine = [(i, [int(x) for x in cubes[i].split()[1:-1]]) for i in range(len(cubes)) if i % 4 == 0]
    print(f"{len(cubes)} cubes, shard has {len(mine)}", flush=True)
    q = queue.Queue(); pending = [0]; cv = threading.Condition()
    ex = ThreadPoolExecutor(NW)
    def submit(c, o):
        with cv: pending[0] += 1
        ex.submit(run, c, o)
    def run(c, o):
        try:
            for ch in node(c, o): submit(ch, o)
        except Exception as e:
            print("ERROR", c, repr(e), flush=True)
        with cv:
            pending[0] -= 1; cv.notify_all()
    for i, c in mine: submit(c, i)
    with cv:
        while pending[0] > 0: cv.wait(30)
    ex.shutdown()
    print("all done", flush=True)
main()
