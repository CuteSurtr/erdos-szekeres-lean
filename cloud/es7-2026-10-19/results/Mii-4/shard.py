#!/usr/bin/env python3
"""Mii-4 shard driver: solve cubes i with i mod 8 == 4 of cubes.icnf, CNF + cube units with
cadical --lrat, check every UNSAT with lrat-check, split >300 s cubes with march_cu -d 6 and
recurse.  A split parent is closed by its sub-cubes plus a 'remainder' job
CNF + parent units + (negation of each sub-cube as a clause), which covers the branches that
march_cu refuted by look-ahead; that job is LRAT-checked like any leaf.

usage: shard.py <cnf> <cubes.icnf> <outdir> <workdir> [workers=4] [tlim=300]
State: <outdir>/state.json (pending jobs), <outdir>/leaves.jsonl (append-only, one per finished job).
"""
import sys, os, json, subprocess, time, threading, queue, hashlib
CNF, CUBES, OUT, WD = sys.argv[1:5]
NW = int(sys.argv[5]) if len(sys.argv) > 5 else 4
TLIM = int(sys.argv[6]) if len(sys.argv) > 6 else 300
SHARD, NSH = 4, 8
CAD = "/tmp/claude-0/tools/cadical/build/cadical"
LRC = "/tmp/claude-0/tools/drat-trim/lrat-check"
MARCH = "/tmp/claude-0/tools/CnC/march_cu/march_cu"
os.makedirs(OUT, exist_ok=True); os.makedirs(WD, exist_ok=True)
LEAVES = os.path.join(OUT, "leaves.jsonl"); STATE = os.path.join(OUT, "state.json")

with open(CNF) as f:
    hdr = f.readline().split(); assert hdr[:2] == ["p", "cnf"]
    NV, NC = int(hdr[2]), int(hdr[3]); BODY = f.read()
if not BODY.endswith("\n"): BODY += "\n"

lock = threading.Lock()


def jid(kind, cube, extra=()):
    return hashlib.sha1(json.dumps([kind, cube, list(extra)]).encode()).hexdigest()[:16]


def load():
    done = {}
    if os.path.exists(LEAVES):
        for line in open(LEAVES):
            if line.strip():
                r = json.loads(line); done[r["id"]] = r
    if os.path.exists(STATE):
        st = json.load(open(STATE))
    else:
        cubes = []
        for i, line in enumerate(open(CUBES)):
            t = line.split()
            assert t[0] == "a" and t[-1] == "0"
            if i % NSH == SHARD:
                cubes.append({"top": i, "cube": [int(x) for x in t[1:-1]], "kind": "cube", "neg": []})
        for c in cubes: c["id"] = jid(c["kind"], c["cube"])
        st = {"jobs": cubes}
    return st, done


st, done = load()


def save_state():
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f: json.dump(st, f)
    os.replace(tmp, STATE)


def record(rec):
    with lock:
        with open(LEAVES, "a") as f: f.write(json.dumps(rec) + "\n")
        done[rec["id"]] = rec


def write_cnf(path, cube, neg):
    extra = "".join(f"{l} 0\n" for l in cube) + "".join(" ".join(str(-l) for l in c) + " 0\n" for c in neg)
    with open(path, "w") as f:
        f.write(f"p cnf {NV} {NC + len(cube) + len(neg)}\n"); f.write(BODY); f.write(extra)


def run_job(job):
    tag = job["id"]; cnf = os.path.join(WD, tag + ".cnf"); prf = os.path.join(WD, tag + ".lrat")
    write_cnf(cnf, job["cube"], job["neg"])
    t0 = time.time()
    try:
        p = subprocess.run([CAD, "-q", "--lrat", "--binary=false", "-t", str(TLIM), cnf, prf],
                           capture_output=True, text=True, timeout=TLIM + 60)
        out = p.stdout
    except subprocess.TimeoutExpired:
        out = ""
    dt = time.time() - t0
    status = "UNKNOWN"
    for line in out.splitlines():
        if line.startswith("s "): status = line[2:].strip()
    rec = {"id": tag, "top": job["top"], "kind": job["kind"], "cube": job["cube"],
           "nneg": len(job["neg"]), "status": status, "solve_s": round(dt, 2)}
    if status == "UNSATISFIABLE":
        psz = os.path.getsize(prf)
        t1 = time.time()
        c = subprocess.run([LRC, cnf, prf], capture_output=True, text=True)
        rec["lrat_bytes"] = psz; rec["lrat_check_s"] = round(time.time() - t1, 2)
        rec["lrat"] = "VERIFIED" if "c VERIFIED" in c.stdout else "FAILED: " + c.stdout[-300:]
        os.remove(prf); os.remove(cnf)
        record(rec); return []
    if os.path.exists(prf): os.remove(prf)
    if status == "SATISFIABLE":
        model = [int(x) for line in out.splitlines() if line.startswith("v ") for x in line[2:].split()]
        mp = os.path.join(OUT, f"SAT_{tag}.json")
        json.dump({"job": job, "model": model}, open(mp, "w"))
        rec["model_file"] = os.path.basename(mp); os.remove(cnf)
        record(rec)
        subprocess.run(["bash", "-c", f"cd {OUT} && git add -A . && git commit -qm 'Mii-4: SAT leaf {tag}' && /tmp/claude-0/push.sh"])
        return []
    # timeout: split with march_cu -d 6 on CNF + cube (+ remainder clauses, if any)
    if job["kind"] == "remainder":
        rec["status"] = "OPEN_REMAINDER_TIMEOUT"; os.remove(cnf); record(rec); return []
    icnf = os.path.join(WD, tag + ".icnf")
    t1 = time.time()
    m = subprocess.run([MARCH, cnf, "-d", "6", "-o", icnf], capture_output=True, text=True)
    os.remove(cnf)
    subs = []
    if os.path.exists(icnf):
        for line in open(icnf):
            t = line.split()
            if t and t[0] == "a": subs.append([int(x) for x in t[1:-1]])
        os.remove(icnf)
    rec["status"] = "SPLIT"; rec["march_s"] = round(time.time() - t1, 2); rec["nsub"] = len(subs)
    rec["march_tail"] = [l for l in m.stdout.splitlines() if l.startswith("c number of cubes") or l.startswith("s ")][-3:]
    new = []
    for s in subs:
        cube = job["cube"] + [l for l in s if l not in job["cube"]]
        new.append({"top": job["top"], "cube": cube, "kind": "cube", "neg": [], "id": jid("cube", cube)})
    rem = {"top": job["top"], "cube": job["cube"], "kind": "remainder", "neg": subs}
    rem["id"] = jid("remainder", job["cube"], [tuple(s) for s in subs])
    new.append(rem)
    rec["children"] = [n["id"] for n in new]
    with lock:
        st["jobs"].extend(new); save_state()
    record(rec)
    return new


q = queue.Queue()
pending = [j for j in st["jobs"] if j["id"] not in done]
for j in pending: q.put(j)
print(f"{len(st['jobs'])} jobs known, {len(pending)} pending", flush=True)


def worker():
    while True:
        j = q.get()
        if j is None: return
        try:
            new = run_job(j)
        except Exception as e:
            print("ERROR", j["id"], repr(e), flush=True); new = []
        for n in new: q.put(n)
        r = done.get(j["id"])
        print(time.strftime("%H:%M:%S"), j["top"], j["kind"], len(j["cube"]), r and r["status"], r and r.get("solve_s"), r and r.get("lrat"), flush=True)
        q.task_done()


save_state()
ths = [threading.Thread(target=worker, daemon=True) for _ in range(NW)]
for t in ths: t.start()
q.join()
for _ in ths: q.put(None)
print("ALL DONE", flush=True)
