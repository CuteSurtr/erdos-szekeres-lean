#!/usr/bin/env python3
"""Mii-6 shard driver: solve every cube of one shard of a march_cu cube file, with LRAT checks.

usage: shard_driver.py <cnf> <cubes.icnf> <shard> <nshards> <bindir> <workdir> <outdir>
                       [--jobs 4] [--tlim 300] [--split-depth 6] [--gap-tlim 1800]

Shard = cubes whose 0-based line index i in cubes.icnf has i % nshards == shard.
Per cube C: write CNF + C as unit clauses, run `cadical --lrat --binary=false -t tlim`.
 * UNSAT -> lrat-check the proof against that CNF (proof deleted afterwards).
 * SAT   -> model saved to <outdir>/sat/ at once; driver flags it.
 * time limit -> logged, then a separate "split" job runs
   `march_cu <CNF+C> -d split_depth -o sub.icnf`; children are C + subcube.
   march_cu also emits its refuted leaves as cubes, but we do not trust its tree: we also solve
   the "gap" formula
   CNF + C + {not subcube_j for every j} with cadical --lrat and lrat-check it: its UNSAT
   certifies that the children cover every assignment extending C.
Every finished job appends one JSON line to <outdir>/leaves.jsonl; resume replays that file
(finished jobs are not repeated). <outdir>/state.json holds a snapshot of the open queue.
"""
import argparse, hashlib, json, os, subprocess, sys, time
from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait

ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("cubes"); ap.add_argument("shard", type=int)
ap.add_argument("nshards", type=int); ap.add_argument("bindir"); ap.add_argument("workdir")
ap.add_argument("outdir")
ap.add_argument("--jobs", type=int, default=4); ap.add_argument("--tlim", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6)
ap.add_argument("--gap-tlim", type=int, default=1800)
a = ap.parse_args()
os.makedirs(a.workdir, exist_ok=True); os.makedirs(a.outdir, exist_ok=True)
LEAVES = os.path.join(a.outdir, "leaves.jsonl"); STATE = os.path.join(a.outdir, "state.json")

head, body = None, []
with open(a.cnf) as f:
    for line in f:
        if line.startswith('p'): head = line.split(); continue
        if line.startswith('c') or not line.strip(): continue
        body.append(line)
NV, NC = int(head[2]), int(head[3])
BODY = "".join(body); del body


def key(kind, cube): return kind + ":" + " ".join(map(str, cube))


def write_cnf(path, cube, extra=()):
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (NV, NC + len(cube) + len(extra)))
        f.write(BODY)
        for l in cube: f.write("%d 0\n" % l)
        for c in extra: f.write(" ".join(map(str, c)) + " 0\n")


def solve(path, tlim, tag):
    """cadical --lrat; returns dict with status, times, lrat check."""
    proof = path + ".lrat"
    t0 = time.time()
    p = subprocess.run([os.path.join(a.bindir, "cadical"), "-q", "--lrat", "--binary=false",
                        "-t", str(tlim), path, proof], capture_output=True, text=True)
    dt = time.time() - t0
    st = "UNKNOWN"; model = []
    for line in p.stdout.splitlines():
        if line.startswith("s "): st = line[2:].strip()
        elif line.startswith("v "): model += [int(x) for x in line[2:].split()]
    r = {"status": st, "solve_s": round(dt, 2), "rc": p.returncode}
    if st == "UNSATISFIABLE":
        r["proof_bytes"] = os.path.getsize(proof)
        t1 = time.time()
        c = subprocess.run([os.path.join(a.bindir, "lrat-check"), path, proof],
                           capture_output=True, text=True)
        out = c.stdout + c.stderr
        r["lrat_check"] = "VERIFIED" if "c VERIFIED" in out else "FAILED"
        if r["lrat_check"] != "VERIFIED": r["lrat_out_tail"] = out[-500:]
        r["check_s"] = round(time.time() - t1, 2)
    elif st == "SATISFIABLE":
        sd = os.path.join(a.outdir, "sat"); os.makedirs(sd, exist_ok=True)
        fn = os.path.join(sd, "model_%s.txt" % tag)
        with open(fn, "w") as f: f.write(" ".join(map(str, model)) + "\n")
        r["model_file"] = os.path.relpath(fn, a.outdir)
    if os.path.exists(proof): os.remove(proof)
    return r


def job_cube(cube, tag):
    path = os.path.join(a.workdir, "c_%s.cnf" % tag)
    write_cnf(path, cube)
    r = solve(path, a.tlim, tag)
    r.update(kind="cube", cube=cube, depth=len(cube))
    os.remove(path)
    return r


def job_split(cube, tag):
    """march_cu -d split_depth on CNF + C (logged separately so a restart keeps the timeout)."""
    path = os.path.join(a.workdir, "s_%s.cnf" % tag)
    write_cnf(path, cube)
    sub = path + ".icnf"; t0 = time.time()
    p = subprocess.run([os.path.join(a.bindir, "march_cu"), path, "-d", str(a.split_depth),
                        "-o", sub], capture_output=True, text=True)
    subs = []
    if os.path.exists(sub):
        for line in open(sub):
            t = line.split()
            if t and t[0] == "a": subs.append([int(x) for x in t[1:-1]])
        os.remove(sub)
    info = None
    for line in p.stdout.splitlines():
        if "number of cubes" in line: info = line.strip()
    children = [cube + [l for l in s if l not in cube] for s in subs]
    # march_cu prints "a 0" when it refutes CNF+C outright: no children, and the gap
    # job (CNF + C with no extra clauses) then carries the whole cube.
    children = [c for c in children if len(c) > len(cube)]
    os.remove(path)
    return {"kind": "split", "cube": cube, "status": "SPLIT", "solve_s": 0.0,
            "march_s": round(time.time() - t0, 2), "nsub": len(subs), "march_info": info,
            "march_rc": p.returncode, "children": children}


def job_gap(cube, children, tag):
    path = os.path.join(a.workdir, "g_%s.cnf" % tag)
    extra = [[-l for l in ch[len(cube):]] for ch in children]
    write_cnf(path, cube, extra)
    r = solve(path, a.gap_tlim, "gap_" + tag)
    r.update(kind="gap", cube=cube, nchildren=len(children))
    os.remove(path)
    return r


# ---- build queue (FIFO) from shard + replay of leaves.jsonl
shard = []
with open(a.cubes) as f:
    for i, line in enumerate(f):
        if i % a.nshards == a.shard:
            t = line.split(); assert t[0] == "a" and t[-1] == "0"
            shard.append([int(x) for x in t[1:-1]])
done = {}
if os.path.exists(LEAVES):
    for line in open(LEAVES):
        if line.strip():
            r = json.loads(line); done[key(r["kind"], r["cube"])] = r
queue = []
def expand(cube):
    k = key("cube", cube)
    if k not in done: queue.append(("cube", cube, None)); return
    r = done[k]
    if r["status"] == "UNKNOWN":
        sp = done.get(key("split", cube))
        if sp is None: queue.append(("split", cube, None)); return
        ch = sp["children"]
        if key("gap", cube) not in done: queue.append(("gap", cube, ch))
        for c in ch: expand(c)
for c in shard: expand(c)
print("shard size %d, already done %d, queued %d" % (len(shard), len(done), len(queue)), flush=True)


def snapshot():
    with open(STATE + ".tmp", "w") as f:
        json.dump({"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "shard": a.shard, "nshards": a.nshards, "shard_cubes": len(shard),
                   "finished_jobs": len(done),
                   "open": [{"kind": k, "cube": c} for k, c, _ in queue] +
                           [{"kind": k, "cube": c, "running": True} for k, c, _ in running.values()]},
                  f)
    os.replace(STATE + ".tmp", STATE)


running = {}
with ProcessPoolExecutor(a.jobs) as ex, open(LEAVES, "a") as log:
    while queue or running:
        while queue and len(running) < a.jobs:
            kind, cube, ch = queue.pop(0)
            tag = hashlib.sha1(key(kind, cube).encode()).hexdigest()[:12]
            fn = {"cube": job_cube, "split": job_split}.get(kind)
            fut = ex.submit(fn, cube, tag) if fn else ex.submit(job_gap, cube, ch, tag)
            running[fut] = (kind, cube, ch)
        snapshot()
        fin, _ = wait(list(running), return_when=FIRST_COMPLETED)
        for fut in fin:
            kind, cube, ch = running.pop(fut)
            r = fut.result()
            r["t"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            log.write(json.dumps(r) + "\n"); log.flush()
            done[key(kind, cube)] = r
            print(json.dumps({k: v for k, v in r.items() if k != "children"})[:300], flush=True)
            if r["status"] == "SATISFIABLE":
                print("!!! SAT", r.get("model_file"), flush=True)
                open(os.path.join(a.outdir, "SAT_FOUND"), "a").write(json.dumps(r) + "\n")
            if kind == "cube" and r["status"] == "UNKNOWN":
                queue.insert(0, ("split", cube, None))
            if kind == "split":
                queue.append(("gap", cube, r["children"]))
                for c in r["children"]: queue.append(("cube", c, None))
    snapshot()
print("queue empty", flush=True)
