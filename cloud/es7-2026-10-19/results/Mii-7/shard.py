#!/usr/bin/env python3
"""Solve one shard of a march_cu cube file with CaDiCaL (LRAT) and lrat-check, splitting
cubes that time out with march_cu and recursing.

usage: shard.py <cnf> <cubes.icnf> <mod> <rem> <workdir> <leaves.jsonl> <state.json>
                [jobs=4] [tlim=300] [split_depth=6] [gap_tlim=3600]

Shard = cubes (lines starting with 'a') with 0-based index i, i % mod == rem.
Task kinds:
  cube  CNF + cube literals as units.
  gap   CNF + parent cube units + one clause (not c_j) per sub-cube c_j of a split.  Its UNSAT
        covers the branches march_cu refuted while splitting, so a parent is closed by LRAT
        exactly when every child cube and its gap are LRAT-verified UNSAT.
Every finished task is appended to leaves.jsonl (one JSON object per line); on restart, tasks
already in leaves.jsonl are not repeated and the children of recorded splits are re-queued.
state.json is a snapshot (pending ids, counts) rewritten after every task.
"""
import sys, os, json, subprocess, time, threading, socket, queue

cnf, icnf, mod, rem, wd, leaves_path, state_path = sys.argv[1:8]
mod, rem = int(mod), int(rem)
jobs = int(sys.argv[8]) if len(sys.argv) > 8 else 4
tlim = int(sys.argv[9]) if len(sys.argv) > 9 else 300
sdepth = int(sys.argv[10]) if len(sys.argv) > 10 else 6
gap_tlim = int(sys.argv[11]) if len(sys.argv) > 11 else 3600
BIN = os.environ.get("BIN", "/home/user/bin")
os.makedirs(wd, exist_ok=True)
host = socket.gethostname()

head, body = None, []
with open(cnf) as f:
    for line in f:
        if line.startswith('p'): head = line.split(); continue
        if line.startswith('c'): continue
        body.append(line)
nv, nc = int(head[2]), int(head[3])
body = ''.join(body)

def read_cubes(path):
    cs = []
    for line in open(path):
        t = line.split()
        if t and t[0] == 'a':
            assert t[-1] == '0'
            cs.append([int(x) for x in t[1:-1]])
    return cs

top = read_cubes(icnf)
tasks = {}          # id -> dict(kind, cube, extra)
order = []
for i, c in enumerate(top):
    if i % mod == rem:
        tid = "c%d" % i
        tasks[tid] = dict(id=tid, kind="cube", cube=c, extra=[])
        order.append(tid)

done = {}
if os.path.exists(leaves_path):
    for line in open(leaves_path):
        if not line.strip(): continue
        r = json.loads(line)
        if r["status"] == "ERROR": continue   # retried on restart
        done[r["id"]] = r
# replay splits so their children are known
changed = True
while changed:
    changed = False
    for r in list(done.values()):
        if r["status"] == "SPLIT":
            for ch in r["children"]:
                if ch["id"] not in tasks:
                    tasks[ch["id"]] = ch; order.append(ch["id"]); changed = True

lock = threading.Lock()
# scheduling only (does not change the shard): top cubes with the fewest pending tasks first,
# depth-first inside a top cube, so that whole top cubes close as early as possible
def top_of(tid): return tid.split('.')[0]
npend = {}
for tid in order:
    if tid not in done: npend[top_of(tid)] = npend.get(top_of(tid), 0) + 1
rank = {t: n for n, t in enumerate(sorted(npend, key=lambda t: (npend[t], int(t[1:]))))}
def prio(tid):
    path = tuple(int(x) if x.isdigit() else 10**6 for x in tid.split('.')[1:])
    return (rank.get(top_of(tid), 10**6), path)
class PQ(queue.PriorityQueue):
    def put(self, tid): super().put((prio(tid) if tid is not None else (10**9,), tid or ""))
    def get(self):
        _, tid = super().get(); return tid or None
q = PQ()
for tid in order:
    if tid not in done: q.put(tid)

def write_state():
    pend = [t for t in order if t not in done]
    st = {"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "shard": [mod, rem],
          "top_cubes_in_shard": sum(1 for t in order if t.count('.') == 0),
          "tasks": len(order), "done": len(done), "pending": pend,
          "counts": {}}
    for r in done.values():
        st["counts"][r["status"]] = st["counts"].get(r["status"], 0) + 1
    tmp = state_path + ".tmp"
    json.dump(st, open(tmp, "w"), indent=1); os.replace(tmp, state_path)

def record(r):
    with lock:
        done[r["id"]] = r
        with open(leaves_path, "a") as f:
            f.write(json.dumps(r) + "\n"); f.flush(); os.fsync(f.fileno())
        write_state()
    print(json.dumps({k: v for k, v in r.items() if k != "children"}), flush=True)

def write_cnf(path, cube, extra):
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nv, nc + len(cube) + len(extra)))
        f.write(body)
        for l in cube: f.write("%d 0\n" % l)
        for cl in extra: f.write(" ".join(map(str, cl)) + " 0\n")

def run(t):
    tid, cube, extra = t["id"], t["cube"], t["extra"]
    base = os.path.join(wd, tid)
    fcnf, fproof, fout = base + ".cnf", base + ".lrat", base + ".out"
    write_cnf(fcnf, cube, extra)
    lim = tlim if t["kind"] == "cube" else gap_tlim
    t0 = time.time()
    with open(fout, "w") as o:
        subprocess.run([BIN + "/cadical", "-q", "--lrat", "--binary=false", "-t", str(lim), fcnf, fproof],
                       stdout=o, stderr=subprocess.STDOUT)
    dt = time.time() - t0
    out = open(fout).read()
    st = [l for l in out.splitlines() if l.startswith("s ")]
    if st: st = st[0][2:]
    elif "c UNKNOWN" in out: st = "UNKNOWN"     # cadical -q prints the timeout as a comment
    else: st = "ERROR"
    if os.environ.get("TEST_FORCE_SPLIT") and t["kind"] == "cube" and tid.count('.') == 0:
        st = "UNKNOWN"   # testing only: exercise the split path
    r = dict(id=tid, kind=t["kind"], cube=cube, n_extra=len(extra), host=host,
             solve_s=round(dt, 2), status=None, lrat=None)
    if st == "UNSATISFIABLE":
        r["status"] = "UNSAT"
        r["proof_bytes"] = os.path.getsize(fproof)
        t1 = time.time()
        c = subprocess.run([BIN + "/lrat-check", fcnf, fproof], capture_output=True, text=True)
        lo = c.stdout + c.stderr
        r["lrat_s"] = round(time.time() - t1, 2)
        r["lrat"] = "VERIFIED" if "c VERIFIED" in lo else "FAILED"
        if r["lrat"] == "FAILED":
            r["lrat_tail"] = lo[-500:]
    elif st == "SATISFIABLE":
        r["status"] = "SAT"
        model = [int(x) for l in out.splitlines() if l.startswith("v ") for x in l[2:].split()]
        mp = os.path.join(os.path.dirname(leaves_path), "sat_model_%s.txt" % tid)
        with open(mp, "w") as f: f.write(" ".join(map(str, model)) + "\n")
        r["model_file"] = os.path.basename(mp)
    elif st == "UNKNOWN" and t["kind"] == "cube":
        # split with march_cu on CNF + cube
        sub = base + ".sub.icnf"
        t1 = time.time()
        m = subprocess.run([BIN + "/march_cu", fcnf, "-d", str(sdepth), "-o", sub],
                           capture_output=True, text=True)
        r["split_s"] = round(time.time() - t1, 2)
        mo = m.stdout
        if "s UNSATISFIABLE" in mo and not os.path.exists(sub):
            r["status"] = "OPEN"; r["note"] = "march_cu reports UNSAT on split; re-queue as gap"
            # fall back: a single gap task with no sub-cubes = the cube itself with long limit
            ch = [dict(id=tid + ".g", kind="gap", cube=cube, extra=[])]
            r["status"] = "SPLIT"; r["children"] = ch; r["n_sub"] = 0
        else:
            subs = [s for s in read_cubes(sub) if s]
            refl = [l for l in mo.splitlines() if "refuted" in l.lower()]
            r["march_refuted_line"] = refl[-1] if refl else None
            # an empty sub-cube means march_cu made no split; then the cube itself is
            # re-solved once as a gap task with the long limit
            ch = [dict(id="%s.%d" % (tid, j), kind="cube", cube=cube + s, extra=[])
                  for j, s in enumerate(subs)]
            ch.append(dict(id=tid + ".g", kind="gap", cube=cube, extra=[[-l for l in s] for s in subs]))
            r["status"] = "SPLIT"; r["children"] = ch; r["n_sub"] = len(subs)
            os.replace(sub, os.path.join(wd, tid + ".sub.icnf.done"))
    else:
        r["status"] = "OPEN" if st == "UNKNOWN" else "ERROR"
        r["note"] = out[-300:]
    for p in (fcnf, fproof):
        try: os.remove(p)
        except FileNotFoundError: pass
    return r

def worker():
    while True:
        tid = q.get()
        if tid is None: return
        r = run(tasks[tid])
        if r["status"] == "SPLIT":
            with lock:
                for ch in r["children"]:
                    tasks[ch["id"]] = ch; order.append(ch["id"])
        record(r)
        if r["status"] == "SPLIT":
            for ch in r["children"]: q.put(ch["id"])
        q.task_done()

write_state()
ths = [threading.Thread(target=worker, daemon=True) for _ in range(jobs)]
for th in ths: th.start()
q.join()
for _ in ths: q.put(None)
write_state()
print("ALL DONE", flush=True)
