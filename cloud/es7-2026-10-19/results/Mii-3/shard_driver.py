#!/usr/bin/env python3
"""Mii-3 shard driver: solve every cube of shard 3 (line index i with i % 8 == 3) of
`march_cu m33k7int.sub.cnf -d 7`, with LRAT checking and recursive splitting.

usage: shard_driver.py <cnf> <cubes.icnf> <bindir> <workdir> <leaves.jsonl> [jobs=4] [tlim=300]

bindir must contain cadical, lrat-check and march_cu.
Each leaf is CNF + cube literals as unit clauses, solved with `cadical --lrat --binary=false -t tlim`;
every UNSAT proof is checked with lrat-check against that exact CNF, then deleted.
A leaf that hits the time limit is split with `march_cu <CNF+cube> -d 6`; the children are
the cube extended by each emitted sub-cube, plus every branch march_cu refuted itself
("gap": the missing sibling of a node in the sub-cube prefix tree), so that the children
partition the parent and every child (gaps included) gets its own LRAT-checked solve.
leaves.jsonl is append-only and is the resumable state: on restart the pending set is
recomputed (shard cubes + children of SPLIT records - finished records).
"""
import sys, os, json, time, subprocess, hashlib
from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait

cnf, icnf, bindir, wd, leaves = sys.argv[1:6]
jobs = int(sys.argv[6]) if len(sys.argv) > 6 else 4
tlim = int(sys.argv[7]) if len(sys.argv) > 7 else 300
SHARD, NSHARDS = 3, 8
os.makedirs(wd, exist_ok=True)

HEAD = BODY = None
def load():
    global HEAD, BODY
    if BODY is None:
        lines = open(cnf).read().split("\n", 1)
        h = lines[0].split(); assert h[0] == "p"
        HEAD = (int(h[2]), int(h[3])); BODY = lines[1]
        if not BODY.endswith("\n"): BODY += "\n"

def key(cube): return hashlib.sha1(" ".join(map(str, cube)).encode()).hexdigest()[:16]

def write_cnf(cube, path):
    load()
    with open(path, "w") as f:
        f.write(f"p cnf {HEAD[0]} {HEAD[1] + len(cube)}\n"); f.write(BODY)
        for l in cube: f.write(f"{l} 0\n")

def read_icnf(path):
    out = []
    for line in open(path):
        t = line.split()
        if t and t[0] == "a": out.append([int(x) for x in t[1:-1]])
    return out

def gaps(cubes):
    """Sibling branches absent from the prefix tree of `cubes` (march_cu-refuted)."""
    pref = set()
    for c in cubes:
        for d in range(len(c) + 1): pref.add(tuple(c[:d]))
    g = []
    for p in pref:
        d = len(p)
        if d == 0: continue
        sib = p[:-1] + (-p[-1],)
        if sib not in pref: g.append(list(sib))
    return sorted(g, key=lambda c: (len(c), c))

def check_partition(cubes):
    """Verify the cube prefix tree branches on one variable per node (both signs after gaps)."""
    allc = [tuple(c) for c in cubes]
    def ok(cs, d):
        if any(len(c) == d for c in cs): return len(cs) == 1
        vs = set(abs(c[d]) for c in cs)
        if len(vs) != 1: return False
        pos = [c for c in cs if c[d] > 0]; neg = [c for c in cs if c[d] < 0]
        return bool(pos) and bool(neg) and ok(pos, d + 1) and ok(neg, d + 1)
    return ok(allc, 0) if allc else False

def solve(task):
    cube, origin = task
    k = key(cube); path = os.path.join(wd, k + ".cnf"); proof = os.path.join(wd, k + ".lrat")
    write_cnf(cube, path)
    t0 = time.time()
    r = subprocess.run([os.path.join(bindir, "cadical"), "-t", str(tlim), "--lrat", "--binary=false",
                        path, proof], capture_output=True, text=True)
    dt = time.time() - t0
    st = [l[2:] for l in r.stdout.split("\n") if l.startswith("s ")]
    st = st[0] if st else "UNKNOWN"
    rec = {"cube": cube, "depth": len(cube), "origin": origin, "solve_s": round(dt, 2)}
    if st == "UNSATISFIABLE":
        psz = os.path.getsize(proof)
        t1 = time.time()
        c = subprocess.run([os.path.join(bindir, "lrat-check"), path, proof], capture_output=True, text=True)
        out = c.stdout + c.stderr
        ver = "VERIFIED" if "c VERIFIED" in out else ("FAILED: " + " ".join(l for l in out.split("\n") if l.strip())[-300:])
        rec.update(status="UNSAT", lrat=ver, lrat_bytes=psz, lrat_check_s=round(time.time() - t1, 2))
    elif st == "SATISFIABLE":
        model = [int(x) for l in r.stdout.split("\n") if l.startswith("v ") for x in l[2:].split()]
        mpath = os.path.join(os.path.dirname(leaves), "sat_" + k + ".model")
        with open(mpath, "w") as f: f.write(" ".join(map(str, model)) + "\n")
        rec.update(status="SAT", model_file=os.path.basename(mpath))
    else:
        # time limit: split with march_cu -d 6 on CNF + cube
        if os.path.exists(proof): os.remove(proof)
        sub = os.path.join(wd, k + ".icnf"); t1 = time.time()
        m = subprocess.run([os.path.join(bindir, "march_cu"), path, "-d", "6", "-o", sub],
                           capture_output=True, text=True)
        subs = read_icnf(sub) if os.path.exists(sub) else []
        mout = m.stdout
        if any(l.startswith("s UNSAT") for l in mout.split("\n")) and not subs:
            subs = []
        g = gaps(subs)
        allc = subs + g
        part = check_partition(allc) if allc else None
        if len(allc) < 2:
            rec.update(status="UNKNOWN", note="split produced <2 children", march_tail=mout[-500:])
        else:
            assert part, "children do not form a partition"
            rec.update(status="SPLIT", children=[cube + s for s in subs], gap_children=[cube + s for s in g],
                       split_s=round(time.time() - t1, 2))
        for p in (sub,):
            if os.path.exists(p): os.remove(p)
    for p in (path, proof):
        if os.path.exists(p): os.remove(p)
    rec["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return rec

def main():
    top = read_icnf(icnf)
    shard = [c for i, c in enumerate(top) if i % NSHARDS == SHARD]
    pending, done = {}, set()
    for c in shard: pending[key(c)] = (c, "shard")
    if os.path.exists(leaves):
        for line in open(leaves):
            if not line.strip(): continue
            r = json.loads(line)
            done.add(key(r["cube"]))
            if r["status"] == "SPLIT":
                for ch in r["children"]: pending.setdefault(key(ch), (ch, "split"))
                for ch in r["gap_children"]: pending.setdefault(key(ch), (ch, "gap"))
    todo = [v for k, v in pending.items() if k not in done]
    print(f"shard cubes {len(shard)}, done {len(done)}, todo {len(todo)}", flush=True)
    with ProcessPoolExecutor(jobs) as ex, open(leaves, "a") as out:
        futs = {ex.submit(solve, t) for t in todo}
        while futs:
            fin, futs = wait(futs, return_when=FIRST_COMPLETED)
            for f in fin:
                r = f.result()
                out.write(json.dumps(r) + "\n"); out.flush()
                print(r["status"], r["depth"], r["solve_s"], r.get("lrat", ""), flush=True)
                if r["status"] == "SPLIT":
                    for ch in r["children"]: futs.add(ex.submit(solve, (ch, "split")))
                    for ch in r["gap_children"]: futs.add(ex.submit(solve, (ch, "gap")))
                if r["status"] == "SAT":
                    print("SAT LEAF", r["model_file"], flush=True)

if __name__ == "__main__":
    main()
