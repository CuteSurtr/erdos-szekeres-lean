#!/usr/bin/env python3
"""Mi-3 shard solver.

usage: shard_solve.py <cnf> <cubes.icnf> <bindir> <workdir> <leaves.jsonl> [shard=3] [nshards=4] [workers=4] [tlim=300]

Shard = cube lines of cubes.icnf with 0-based index i, i % nshards == shard.
Each cube: CNF + cube units solved by `cadical --lrat` with a time limit; every UNSAT is
checked by `lrat-check`.  A cube that hits the time limit is split with `march_cu -d 6` on
CNF + cube; children are cube + subcube.  The branches march_cu refutes during splitting are
covered by a "residual" instance (CNF + cube + one clause per child negating its subcube),
which is solved and LRAT-checked like a leaf, so every closed node has an LRAT-checked
certificate.

leaves.jsonl is append-only and is also the resume state: a restart skips every node with
a final record (unsat/sat/split) and re-queues the rest.
"""
import json, os, subprocess, sys, time, threading, queue, hashlib

cnf, icnf, bindir, wd, out = sys.argv[1:6]
shard = int(sys.argv[6]) if len(sys.argv) > 6 else 3
nsh = int(sys.argv[7]) if len(sys.argv) > 7 else 4
nworkers = int(sys.argv[8]) if len(sys.argv) > 8 else 4
tlim = int(sys.argv[9]) if len(sys.argv) > 9 else 300
os.makedirs(wd, exist_ok=True)
FORCE = int(os.environ.get("FORCE_SPLIT_DEPTH", "0"))  # testing only: treat cubes shorter than this as timed out
CAD, LRC, MARCH = (os.path.join(bindir, x) for x in ("cadical", "lrat-check", "march_cu"))

hdr = None; body = []
with open(cnf) as f:
    for line in f:
        if line.startswith("p "): hdr = line.split()
        elif line.startswith("c"): continue
        else: body.append(line)
NV, NC = int(hdr[2]), int(hdr[3]); BODY = "".join(body); del body

def key(lits, kind="cube"): return kind + ":" + " ".join(map(str, lits))

def write_cnf(path, units, extra=()):
    with open(path, "w") as g:
        g.write(f"p cnf {NV} {NC + len(units) + len(extra)}\n"); g.write(BODY)
        for u in units: g.write(f"{u} 0\n")
        for c in extra: g.write(" ".join(map(str, c)) + " 0\n")

lock = threading.Lock()
def emit(rec):
    with lock:
        with open(out, "a") as g: g.write(json.dumps(rec) + "\n")
        print(json.dumps({k: v for k, v in rec.items() if k != "children"}), flush=True)

def solve(name, units, extra=()):
    path = os.path.join(wd, name + ".cnf"); proof = os.path.join(wd, name + ".lrat")
    write_cnf(path, units, extra)
    t0 = time.time()
    r = subprocess.run([CAD, "-q", "-t", str(tlim), "--lrat", "--binary=false", path, proof],
                       capture_output=True, text=True)
    dt = round(time.time() - t0, 2)
    st = "unknown"
    for l in r.stdout.splitlines():
        if l.startswith("s "):
            st = {"s UNSATISFIABLE": "unsat", "s SATISFIABLE": "sat"}.get(l.strip(), "unknown")
    rec = {"status": st, "solve_s": dt}
    if st == "unsat":
        rec["lrat_bytes"] = os.path.getsize(proof)
        t1 = time.time()
        c = subprocess.run([LRC, path, proof], capture_output=True, text=True)
        rec["lrat_check"] = "VERIFIED" if "c VERIFIED" in c.stdout + c.stderr else "NOT VERIFIED"
        rec["lrat_check_s"] = round(time.time() - t1, 2)
    elif st == "sat":
        model = [int(x) for l in r.stdout.splitlines() if l.startswith("v ") for x in l.split()[1:] if x != "0"]
        mp = os.path.join(os.path.dirname(out), f"SAT_{name}.model")
        with open(mp, "w") as g: g.write(" ".join(map(str, model)) + "\n")
        rec["model_file"] = os.path.basename(mp)
    for p in (path, proof):
        if os.path.exists(p) and not (st == "sat" and p == path): os.remove(p)
    return rec

def split(name, units):
    path = os.path.join(wd, name + ".split.cnf"); sub = os.path.join(wd, name + ".icnf")
    write_cnf(path, units)
    t0 = time.time()
    r = subprocess.run([MARCH, path, "-d", "6", "-o", sub], capture_output=True, text=True)
    kids = []
    if os.path.exists(sub):
        for l in open(sub):
            if l.startswith("a "):
                ch = [int(x) for x in l.split()[1:-1] if int(x) not in units]
                if ch: kids.append(ch)   # march_cu writes "a 0" when it refutes the root
        os.remove(sub)
    os.remove(path)
    summ = [l for l in r.stdout.splitlines() if "cubes" in l or "refuted" in l or l.startswith("s ")][-4:]
    return kids, round(time.time() - t0, 2), summ

# ---- state ----
done = {}
if os.path.exists(out):
    for l in open(out):
        r = json.loads(l); done[r["key"]] = r

cubes = [[int(x) for x in l.split()[1:-1]] for l in open(icnf) if l.startswith("a ")]
mine = [(i, c) for i, c in enumerate(cubes) if i % nsh == shard]
print(f"cubes {len(cubes)}, shard {shard}/{nsh}: {len(mine)}", flush=True)

q = queue.Queue(); pending = [0]; plock = threading.Lock()
def push(task):
    with plock: pending[0] += 1
    q.put(task)

def enqueue(task):
    """task = (kind, lits, extra, top_index, parent_key); resolves finished nodes from state."""
    kind, lits, extra, top, parent = task
    k = key(lits, kind)
    r = done.get(k)
    if r is None or r["status"] == "unknown":
        push(task); return
    if r["status"] == "split":
        for ch in r["children"]: enqueue(("cube", ch, (), top, k))
        enqueue(("residual", lits, [[-x for x in ch] for ch in r["children"]], top, k))

ctr = [0]
def worker():
    while True:
        task = q.get()
        if task is None: return
        kind, lits, extra, top, parent = task
        k = key(lits, kind)
        with plock: ctr[0] += 1; n = ctr[0]
        name = f"t{top}_{n}_{os.getpid()}"
        rec = {"key": k, "kind": kind, "top_index": top, "cube": lits, "parent": parent, "depth": len(lits)}
        if kind == "residual": rec["n_children"] = len(extra)
        if kind == "cube" and len(lits) < FORCE: rec.update({"status": "unknown", "solve_s": 0, "forced": True})
        else: rec.update(solve(name, lits, extra))
        if rec["status"] == "unknown" and kind == "cube":
            kids, sdt, summ = split(name, lits)
            rec["status"] = "split"; rec["split_s"] = sdt; rec["march"] = summ
            rec["children"] = [lits + ch for ch in kids]
            emit(rec)
            for ch in rec["children"]: push(("cube", ch, (), top, k))
            push(("residual", lits, [[-x for x in ch] for ch in kids], top, k))
        else:
            emit(rec)
        with plock: pending[0] -= 1; left = pending[0]
        if left == 0:
            for _ in range(nworkers): q.put(None)

for i, c in mine: enqueue(("cube", c, (), i, None))
if pending[0] == 0:
    print("nothing to do", flush=True); sys.exit(0)
ts = [threading.Thread(target=worker) for _ in range(nworkers)]
for t in ts: t.start()
for t in ts: t.join()
print("shard finished", flush=True)
