#!/usr/bin/env python3
"""Mi-2 shard driver: solve every cube with 0-based line index i % 4 == SHARD of cubes.icnf.

usage: shard.py <cnf> <cubes.icnf> <bindir> <workdir> <leaves.jsonl> [shard=2] [nproc=4] [tlim=300]

Each node is a cube (list of literals).  A node is solved with `cadical --lrat` on CNF + cube
units (time limit tlim); UNSAT proofs are checked with lrat-check and deleted.  A node that
times out is split with `march_cu -d 6` on CNF + cube; its children (parent + child literals)
are queued.  For a split we also run a "gap check": CNF + parent units + one clause blocking each
child cube must be UNSAT (LRAT-checked), which certifies the branches march_cu refuted itself.
State is leaves.jsonl itself (append-only): on restart, nodes with a final record are skipped and
split nodes are re-expanded from their recorded children.
"""
import sys, os, json, subprocess, time, threading, queue, hashlib

cnf, cubesf, B, WD, LEAVES = sys.argv[1:6]
SHARD = int(sys.argv[6]) if len(sys.argv) > 6 else 2
NP = int(sys.argv[7]) if len(sys.argv) > 7 else 4
TLIM = int(sys.argv[8]) if len(sys.argv) > 8 else 300
os.makedirs(WD, exist_ok=True)

with open(cnf, "rb") as f:
    data = f.read()
nl = data.index(b"\n")
hdr = data[:nl].split()
NV, NC = int(hdr[2]), int(hdr[3])
BODY = data[nl + 1:]
if not BODY.endswith(b"\n"): BODY += b"\n"

def write_cnf(path, units, extra=()):
    with open(path, "wb") as f:
        f.write(b"p cnf %d %d\n" % (NV, NC + len(units) + len(extra)))
        f.write(BODY)
        f.write("".join(f"{l} 0\n" for l in units).encode())
        f.write("".join(" ".join(map(str, c)) + " 0\n" for c in extra).encode())

lock = threading.Lock()
def log(rec):
    with lock:
        with open(LEAVES, "a") as f:
            f.write(json.dumps(rec) + "\n"); f.flush(); os.fsync(f.fileno())

def nid(cube): return hashlib.sha1(" ".join(map(str, cube)).encode()).hexdigest()[:16]

def solve(cube, extra=(), tl=TLIM, tag="n"):
    """returns (status, seconds, lratcheck, model)"""
    h = nid(cube) + tag
    c, p, o = f"{WD}/{h}.cnf", f"{WD}/{h}.lrat", f"{WD}/{h}.out"
    write_cnf(c, cube, extra)
    t0 = time.time()
    with open(o, "w") as fo:
        try:
            subprocess.run([f"{B}/cadical", "--lrat", "--binary=false", "-t", str(tl), c, p],
                           stdout=fo, stderr=subprocess.STDOUT, timeout=tl + 60)
        except subprocess.TimeoutExpired:
            pass
    dt = time.time() - t0
    out = open(o).read()
    st = "UNKNOWN"
    for line in out.splitlines():
        if line.startswith("s "): st = line[2:].strip()
    chk, model = None, None
    if st == "UNSATISFIABLE":
        r = subprocess.run([f"{B}/lrat-check", c, p], capture_output=True, text=True)
        chk = "VERIFIED" if "VERIFIED" in r.stdout and "FAIL" not in r.stdout else "FAILED:" + r.stdout[-200:]
    elif st == "SATISFIABLE":
        model = [int(x) for line in out.splitlines() if line.startswith("v ") for x in line[2:].split()]
        model = [x for x in model if x != 0]
    for fn in (c, p, o):
        try: os.remove(fn)
        except FileNotFoundError: pass
    return st, dt, chk, model

def split(cube):
    h = nid(cube)
    c, ic, o = f"{WD}/{h}.s.cnf", f"{WD}/{h}.icnf", f"{WD}/{h}.march"
    write_cnf(c, cube)
    t0 = time.time()
    with open(o, "w") as fo:
        subprocess.run([f"{B}/march_cu", c, "-d", "6", "-o", ic], stdout=fo, stderr=subprocess.STDOUT)
    dt = time.time() - t0
    kids = []
    if os.path.exists(ic):
        for line in open(ic):
            t = line.split()
            if t and t[0] == "a":
                k = [int(x) for x in t[1:-1]]
                if k: kids.append(k)
    mout = open(o).read()
    ref = None
    for line in mout.splitlines():
        if "refuted" in line: ref = line.strip()
    unsat_root = "UNSATISFIABLE" in mout
    for fn in (c, ic, o):
        try: os.remove(fn)
        except FileNotFoundError: pass
    return kids, dt, ref, unsat_root

# ---- load cubes and state
cubes = []
for line in open(cubesf):
    t = line.split()
    cubes.append([int(x) for x in t[1:-1]] if t and t[0] == "a" else None)
roots = [(i, cubes[i]) for i in range(len(cubes)) if i % 4 == SHARD]
assert all(c is not None for _, c in roots), "non-cube line in shard"
done, splits = {}, {}
if os.path.exists(LEAVES):
    for line in open(LEAVES):
        r = json.loads(line)
        if r["kind"] == "leaf": done[tuple(r["cube"])] = r
        elif r["kind"] == "split": splits[tuple(r["cube"])] = r
q = queue.Queue()
pending = [0]
plock = threading.Lock()
def enqueue(root, cube):
    with plock: pending[0] += 1
    q.put((root, cube))
def expand(root, cube):
    key = tuple(cube)
    if key in done: return
    if key in splits:
        for k in splits[key]["children"]: expand(root, cube + k)
        return
    enqueue(root, cube)
for i, c in roots: expand(i, c)
print(f"shard {SHARD}: {len(roots)} roots, {len(done)} leaves done, {len(splits)} splits, {pending[0]} queued", flush=True)

def worker():
    while True:
        item = q.get()
        if item is None: return
        root, cube = item
        if len(cube) < int(os.environ.get("FORCE_SPLIT_LEN", "0")): st, dt, chk, model = "UNKNOWN", 0.0, None, None
        else: st, dt, chk, model = solve(cube)
        if st == "UNKNOWN":
            kids, sdt, ref, ur = split(cube)
            gap = None
            if kids:
                gst, gdt, gchk, _ = solve(cube, extra=[[-l for l in k] for k in kids], tl=3600, tag="g")
                gap = {"status": gst, "time": round(gdt, 2), "lrat": gchk}
            rec = {"kind": "split", "root": root, "cube": cube, "solve_time": round(dt, 2),
                   "march_time": round(sdt, 2), "children": kids, "march_refuted": ref,
                   "march_unsat_root": ur, "gap_check": gap}
            log(rec)
            if not kids:
                # march_cu refuted the whole node: certify by a long cadical run
                st2, dt2, chk2, model2 = solve(cube, tl=36000, tag="L")
                log({"kind": "leaf", "root": root, "cube": cube, "status": st2, "time": round(dt2, 2),
                     "lrat": chk2, "note": "march refuted node; long solve"})
                if model2: save_sat(root, cube, model2)
            for k in kids: enqueue(root, cube + k)
        else:
            log({"kind": "leaf", "root": root, "cube": cube, "status": st, "time": round(dt, 2), "lrat": chk})
            if model: save_sat(root, cube, model)
        with plock: pending[0] -= 1
        q.task_done()

def save_sat(root, cube, model):
    fn = f"{os.path.dirname(os.path.abspath(LEAVES))}/sat_{root}_{nid(cube)}.json"
    with open(fn, "w") as f: json.dump({"root": root, "cube": cube, "model": model}, f)
    print("SAT FOUND", fn, flush=True)

ths = [threading.Thread(target=worker, daemon=True) for _ in range(NP)]
for t in ths: t.start()
q.join()
for _ in ths: q.put(None)
print("shard finished", flush=True)
