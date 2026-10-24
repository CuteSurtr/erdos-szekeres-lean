#!/usr/bin/env python3
"""Mii-5: solve shard 5 of 8 of m33k7int.sub.cnf (cubes with 0-based index i, i % 8 == 5).

usage: shard.py <cnf> <cubes.icnf> <bindir> <workdir> <outdir> [jobs=4] [tlim=300] [shard=5] [nshards=8]

Every task is a cube (list of literals). For each one: write CNF + cube as unit clauses, run
`cadical -t tlim --lrat --binary=false`, and check every UNSAT proof with drat-trim's
`lrat-check` against that CNF. A cube that hits the time limit is split with
`march_cu <CNF+cube> -d 6`; its children are parent + subcube. march_cu does not print the
sub-cubes it refutes, so every split also gets a coverage check: CNF + parent cube + the
negation of every printed sub-cube as a clause must be UNSAT (solved and LRAT-checked like a
leaf). Records: outdir/leaves.jsonl (one line per leaf), outdir/splits.jsonl (one line per
split, with its children and coverage result). Both files are the resumable state: finished
leaves and splits are not redone on restart.
"""
import sys, os, json, time, subprocess, threading, queue, hashlib

cnf, cubes_path, bindir, wd, outdir = sys.argv[1:6]
jobs = int(sys.argv[6]) if len(sys.argv) > 6 else 4
tlim = int(sys.argv[7]) if len(sys.argv) > 7 else 300
shard = int(sys.argv[8]) if len(sys.argv) > 8 else 5
nsh = int(sys.argv[9]) if len(sys.argv) > 9 else 8
os.makedirs(wd, exist_ok=True); os.makedirs(outdir, exist_ok=True)
LEAVES, SPLITS = os.path.join(outdir, "leaves.jsonl"), os.path.join(outdir, "splits.jsonl")

head, body = None, []
with open(cnf) as f:
    for line in f:
        if line.startswith('p'): head = line.split(); continue
        if line.startswith('c'): continue
        body.append(line)
NV, NC = int(head[2]), int(head[3])
BODY = "".join(body); del body

top = []
with open(cubes_path) as f:
    for i, line in enumerate(f):
        t = line.split()
        assert t[0] == 'a' and t[-1] == '0', line
        if i % nsh == shard: top.append((i, [int(x) for x in t[1:-1]]))

key = lambda c: " ".join(map(str, c))
done, splits = {}, {}
if os.path.exists(LEAVES):
    for line in open(LEAVES):
        r = json.loads(line); done[key(r["cube"])] = r
if os.path.exists(SPLITS):
    for line in open(SPLITS):
        r = json.loads(line); splits[key(r["cube"])] = r
lock = threading.Lock()


def emit(path, rec):
    with lock:
        with open(path, "a") as f: f.write(json.dumps(rec) + "\n"); f.flush(); os.fsync(f.fileno())


def write_cnf(path, units, clauses=()):
    with open(path, "w") as f:
        f.write(f"p cnf {NV} {NC + len(units) + len(clauses)}\n"); f.write(BODY)
        for l in units: f.write(f"{l} 0\n")
        for c in clauses: f.write(" ".join(map(str, c)) + " 0\n")


def solve(tag, units, clauses=(), limit=tlim):
    path, proof = os.path.join(wd, tag + ".cnf"), os.path.join(wd, tag + ".lrat")
    write_cnf(path, units, clauses)
    t0 = time.time()
    r = subprocess.run([os.path.join(bindir, "cadical"), "-q", "-t", str(limit), "--lrat", "--binary=false",
                        path, proof], capture_output=True, text=True)
    dt = round(time.time() - t0, 2)
    st = [l for l in r.stdout.split("\n") if l.startswith("s ")]
    status = st[0][2:] if st else "UNKNOWN"
    rec = {"status": status, "solve_s": dt}
    if status == "UNSATISFIABLE":
        rec["lrat_bytes"] = os.path.getsize(proof)
        t1 = time.time()
        c = subprocess.run([os.path.join(bindir, "lrat-check"), path, proof], capture_output=True, text=True)
        rec["lrat_check"] = "VERIFIED" if "c VERIFIED" in c.stdout else "FAILED: " + (c.stdout + c.stderr)[-300:]
        rec["lrat_check_s"] = round(time.time() - t1, 2)
    elif status == "SATISFIABLE":
        model = [int(x) for l in r.stdout.split("\n") if l.startswith("v ") for x in l.split()[1:]]
        rec["model"] = [x for x in model if x != 0]
    if os.path.exists(proof): os.remove(proof)
    os.remove(path)
    return rec


def split(tag, cube):
    path = os.path.join(wd, tag + ".split.cnf"); out = os.path.join(wd, tag + ".icnf")
    write_cnf(path, cube)
    t0 = time.time()
    r = subprocess.run([os.path.join(bindir, "march_cu"), path, "-d", "6", "-o", out], capture_output=True, text=True)
    subs = [[int(x) for x in l.split()[1:-1]] for l in open(out) if l.startswith('a')] if os.path.exists(out) else []
    ref = [l for l in r.stdout.split("\n") if "refuted" in l]
    os.remove(path)
    if os.path.exists(out): os.remove(out)
    return subs, round(time.time() - t0, 2), ref


Q = queue.Queue()
stats = {"pending": 0}


def push(item):
    with lock: stats["pending"] += 1
    Q.put(item)


def worker(wid):
    while True:
        item = Q.get()
        if item is None: return
        top_i, cube = item
        k = key(cube)
        try:
            if k in splits:
                for s in splits[k]["children"]: push((top_i, s))
            elif k in done:
                pass
            else:
                rec = solve(f"w{wid}", cube)
                if rec["status"] == "UNKNOWN":
                    subs, dt, ref = split(f"w{wid}", cube)
                    children = [cube + [l for l in s if l not in cube] for s in subs]
                    cov = solve(f"w{wid}cov", cube, [[-l for l in s] for s in subs], limit=3600)
                    srec = {"top_index": top_i, "cube": cube, "timeout_s": rec["solve_s"], "march_s": dt,
                            "march_out": ref, "n_children": len(children), "children": children,
                            "coverage": cov}
                    emit(SPLITS, srec); splits[k] = srec
                    for s in children: push((top_i, s))
                else:
                    rec = {"top_index": top_i, "cube": cube, **rec}
                    emit(LEAVES, rec); done[k] = rec
                    if rec["status"] == "SATISFIABLE":
                        emit(os.path.join(outdir, "SAT_FOUND.jsonl"), rec)
        finally:
            with lock: stats["pending"] -= 1
            Q.task_done()


ths = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(jobs)]
for t in ths: t.start()
for it in top: push(it)
print(json.dumps({"shard": shard, "nshards": nsh, "top_cubes": len(top), "resumed_leaves": len(done),
                  "resumed_splits": len(splits)}), flush=True)
Q.join()
for _ in ths: Q.put(None)
print("done", flush=True)
