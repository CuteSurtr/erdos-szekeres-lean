#!/usr/bin/env python3
"""Mi-1 shard solver: cubes with 0-based line index i % 4 == 1 of `march_cu <cnf> -d 7`.

usage: shard.py <cnf> <cubes.icnf> <bindir> <workdir> <leaves.jsonl> [nworkers=4] [tlim=300] [mod=4] [rem=1]

Every leaf: CNF + cube units solved with `cadical --lrat --binary=false -t <tlim>`; UNSAT proofs
are checked with drat-trim's lrat-check against that exact CNF and then deleted.
A cube that times out is split with `march_cu <CNF+cube> -d 6`; the children are parent + child
literals.  The split is also checked to be a cover: CNF + cube + one clause blocking each child
must be UNSAT (LRAT-checked), which certifies the leaves march_cu refuted by lookahead.
leaves.jsonl is the resumable state: on restart, cubes with a final record are skipped and the
children recorded by SPLIT entries are re-queued.
"""
import sys, os, json, time, subprocess, threading, queue, hashlib

cnf, cubef, bindir, wd, leavesf = sys.argv[1:6]
nworkers = int(sys.argv[6]) if len(sys.argv) > 6 else 4
tlim = int(sys.argv[7]) if len(sys.argv) > 7 else 300
mod = int(sys.argv[8]) if len(sys.argv) > 8 else 4
rem = int(sys.argv[9]) if len(sys.argv) > 9 else 1
os.makedirs(wd, exist_ok=True)
CAD, LC, MC = (os.path.join(bindir, b) for b in ("cadical", "lrat-check", "march_cu"))

head, body = None, []
with open(cnf) as f:
    for line in f:
        if line.startswith('p'): head = line.split(); continue
        if line.startswith('c') or not line.strip(): continue
        body.append(line)
NV, NC = int(head[2]), int(head[3])
BODY = ''.join(body).encode(); del body

def write_cnf(path, units=(), clauses=()):
    with open(path, 'wb') as f:
        f.write(f"p cnf {NV} {NC + len(units) + len(clauses)}\n".encode())
        f.write(BODY)
        f.write(''.join(f"{l} 0\n" for l in units).encode())
        f.write(''.join(' '.join(map(str, c)) + " 0\n" for c in clauses).encode())

def read_cubes(path):
    out = []
    for line in open(path):
        t = line.split()
        if t and t[0] == 'a': out.append([int(x) for x in t[1:-1]])
    return out

def key(c): return ' '.join(map(str, c))

def solve_lrat(tag, units, clauses=(), t=tlim):
    """Returns dict(status, solve_s, lrat, lrat_s, proof_bytes)."""
    p = os.path.join(wd, tag + ".cnf"); pr = os.path.join(wd, tag + ".lrat")
    write_cnf(p, units, clauses)
    t0 = time.time()
    r = subprocess.run([CAD, "-q", "--lrat", "--binary=false", "-t", str(t), p, pr],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0
    st = {10: "SAT", 20: "UNSAT"}.get(r.returncode, "UNKNOWN")
    res = {"status": st, "solve_s": round(dt, 2)}
    if st == "SAT":
        res["model"] = [int(x) for l in r.stdout.splitlines() if l.startswith('v')
                        for x in l.split()[1:] if x != '0']
    if st == "UNSAT":
        res["proof_bytes"] = os.path.getsize(pr)
        t1 = time.time()
        c = subprocess.run([LC, p, pr], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        res["lrat_s"] = round(time.time() - t1, 2)
        res["lrat"] = "VERIFIED" if "c VERIFIED" in c.stdout else ("FAILED: " + c.stdout[-300:])
    for q in (p, pr):
        if os.path.exists(q): os.remove(q)
    return res

lock = threading.Lock()
def record(rec):
    with lock:
        with open(leavesf, 'a') as f:
            f.write(json.dumps(rec) + "\n"); f.flush(); os.fsync(f.fileno())

# initial shard and resume
allc = read_cubes(cubef)
shard = [c for i, c in enumerate(allc) if i % mod == rem]
done, children = set(), {}
if os.path.exists(leavesf):
    for line in open(leavesf):
        r = json.loads(line)
        if r["kind"] == "leaf" and r["status"] in ("UNSAT", "SAT", "SPLIT") and \
                (r["status"] != "UNSAT" or r.get("lrat") == "VERIFIED"):
            done.add(key(r["cube"]))
            if r["status"] == "SPLIT": children[key(r["cube"])] = r["children"]
todo = []
def expand(c, origin):
    k = key(c)
    if k in done:
        for ch in children.get(k, []): expand(ch, origin)
    else: todo.append((c, origin))
for i, c in enumerate(allc):
    if i % mod == rem: expand(c, i)
print(json.dumps({"event": "start", "cubes_total": len(allc), "shard": len(shard),
                  "already_done": len(done), "todo": len(todo)}), flush=True)

Q = queue.Queue()
for it in todo: Q.put(it)
pending = [len(todo)]
cnt = {"UNSAT": 0, "SAT": 0, "SPLIT": 0, "FAIL": 0}
seq = [0]

def work(wid):
    while True:
        it = Q.get()
        if it is None: return
        cube, origin = it
        with lock: seq[0] += 1; tag = f"w{wid}_{seq[0]}"
        res = solve_lrat(tag, cube)
        rec = {"kind": "leaf", "origin_index": origin, "depth": len(cube), "cube": cube, **res}
        if res["status"] == "UNSAT" and res["lrat"] != "VERIFIED":
            with lock: cnt["FAIL"] += 1
        elif res["status"] == "UNKNOWN":
            p = os.path.join(wd, tag + ".split.cnf"); o = os.path.join(wd, tag + ".icnf")
            write_cnf(p, cube)
            t0 = time.time()
            m = subprocess.run([MC, p, "-d", "6", "-o", o], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True)
            subs = read_cubes(o) if os.path.exists(o) else []
            for q in (p, o):
                if os.path.exists(q): os.remove(q)
            refuted = [l for l in m.stdout.splitlines() if "refuted" in l]
            kids = [cube + s for s in subs]
            cov = solve_lrat(tag + "c", cube, [[-l for l in s] for s in subs], t=1800)
            rec.update({"status": "SPLIT", "timeout_s": res["solve_s"], "children": kids,
                        "march_s": round(time.time() - t0, 2), "march_info": refuted[-2:],
                        "cover_check": {k: v for k, v in cov.items() if k != "model"}})
            if cov["status"] == "SAT": rec["cover_check"]["note"] = "cover formula SAT: model outside children"
            for k_ in kids: Q.put((k_, origin));
            with lock: pending[0] += len(kids)
        if res["status"] == "SAT":
            with open(os.path.join(os.path.dirname(leavesf), f"SAT_model_{tag}.json"), 'w') as f:
                json.dump({"cube": cube, "model": res["model"]}, f)
            rec["model_file"] = f"SAT_model_{tag}.json"; del rec["model"]
            print(json.dumps({"event": "SAT", "cube": cube}), flush=True)
        record(rec)
        with lock:
            cnt[rec["status"] if rec["status"] in cnt else "FAIL"] += 1
            pending[0] -= 1
            print(json.dumps({"event": "leaf", "t": time.strftime("%H:%M:%S"), "cube": key(cube),
                              "status": rec["status"], "s": res["solve_s"], "lrat": res.get("lrat"),
                              "pending": pending[0], **cnt}), flush=True)
            if pending[0] == 0:
                for _ in range(nworkers): Q.put(None)

if pending[0] == 0:
    print(json.dumps({"event": "nothing to do"})); sys.exit(0)
ts = [threading.Thread(target=work, args=(w,)) for w in range(nworkers)]
for t in ts: t.start()
for t in ts: t.join()
print(json.dumps({"event": "done", **cnt}), flush=True)
