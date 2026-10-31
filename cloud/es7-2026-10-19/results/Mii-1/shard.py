#!/usr/bin/env python3
"""Mii-1: solve shard 1 of 8 (cube lines i with i % 8 == 1) of march_cu -d 7 on m33k7int.sub.cnf.

usage: shard.py <cnf> <cubes.icnf> <bindir> <workdir> <leaves.jsonl> [nworkers=4] [shard=1] [nshards=8]

Every leaf = CNF + cube units, solved by `cadical --lrat -t 300`; every UNSAT is checked by
lrat-check.  A leaf that times out is split by `march_cu -d 6` on CNF + cube; its children are
the cube extended by each sub-cube (march_cu prints its refuted leaves as cubes too, so they
are solved like any other), and a "gap" instance (CNF + cube + the negation of every sub-cube
as a clause) is solved with LRAT too, as a checked proof that the sub-cubes cover the cube.
If march_cu refutes CNF + cube outright, the gap instance is CNF + cube itself.  leaves.jsonl is the resumable state: a restart
re-reads it and skips every finished node.
"""
import sys, os, json, time, subprocess, threading, hashlib
from concurrent.futures import ThreadPoolExecutor

cnf, cubes, bindir, wd, leaves = sys.argv[1:6]
nworkers = int(sys.argv[6]) if len(sys.argv) > 6 else 4
shard = int(sys.argv[7]) if len(sys.argv) > 7 else 1
nshards = int(sys.argv[8]) if len(sys.argv) > 8 else 8
TLIM = int(os.environ.get("MII_TLIM", "300"))
FORCE_SPLIT_DEPTH = int(os.environ.get("MII_FORCE_SPLIT_DEPTH", "-1"))  # testing only
os.makedirs(wd, exist_ok=True)
CAD, LRC, MARCH = (os.path.join(bindir, x) for x in ("cadical", "lrat-check", "march_cu"))

with open(cnf) as f:
    hdr = f.readline().split()
    assert hdr[:2] == ["p", "cnf"]
    NV, NC = int(hdr[2]), int(hdr[3])
    BODY = f.read()
if not BODY.endswith("\n"):
    BODY += "\n"

top = []
for i, ln in enumerate(open(cubes)):
    t = ln.split()
    assert t[0] == "a" and t[-1] == "0", ln
    if i % nshards == shard:
        top.append((i, [int(x) for x in t[1:-1]]))

lock = threading.Lock()
logf = open(leaves, "a")


def log(rec):
    with lock:
        logf.write(json.dumps(rec) + "\n")
        logf.flush()
        os.fsync(logf.fileno())


def key(lits):
    return " ".join(map(str, lits))


def write_cnf(path, units, clauses=()):
    with open(path, "w") as f:
        f.write(f"p cnf {NV} {NC + len(units) + len(clauses)}\n")
        f.write(BODY)
        for l in units:
            f.write(f"{l} 0\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def cadical_lrat(tag, path, tlim):
    proof = path + ".lrat"
    t0 = time.time()
    args = [CAD, "-q", "--lrat", "--binary=false"] + (["-t", str(tlim)] if tlim else []) + [path, proof]
    r = subprocess.run(args, capture_output=True, text=True)
    dt = round(time.time() - t0, 2)
    st = {10: "SAT", 20: "UNSAT"}.get(r.returncode, "UNKNOWN")
    out = {"status": st, "solve_s": dt}
    if st == "SAT":
        model = [int(x) for ln in r.stdout.split("\n") if ln.startswith("v ") for x in ln.split()[1:]]
        out["model"] = [x for x in model if x != 0]
    if st == "UNSAT":
        out["proof_bytes"] = os.path.getsize(proof)
        t1 = time.time()
        c = subprocess.run([LRC, path, proof], capture_output=True, text=True)
        txt = c.stdout + c.stderr
        out["lrat"] = "VERIFIED" if "c VERIFIED" in txt else "FAILED: " + txt[-300:].replace("\n", " | ")
        out["lrat_s"] = round(time.time() - t1, 2)
    for p in (proof,):
        if os.path.exists(p):
            os.remove(p)
    return out


def march_split(path, out):
    t0 = time.time()
    r = subprocess.run([MARCH, path, "-d", "6", "-o", out], capture_output=True, text=True)
    txt = r.stdout + r.stderr
    subs = []
    if os.path.exists(out):
        for ln in open(out):
            t = ln.split()
            if t and t[0] == "a":
                subs.append([int(x) for x in t[1:-1]])
        os.remove(out)
    info = {"march_s": round(time.time() - t0, 2), "n_sub": len(subs)}
    for ln in txt.split("\n"):
        if "refuted" in ln or ln.startswith("s ") or "number of cubes" in ln:
            info.setdefault("march_lines", []).append(ln.strip())
    return subs, info


# ---- resume ----
done = {}
for ln in open(leaves):
    if ln.strip():
        r = json.loads(ln)
        if r.get("kind") in ("leaf", "split", "gap"):
            done[(r["kind"], key(r["cube"]))] = r

sat_found = threading.Event()


def run_node(root, lits):
    """Solve node lits (a list); returns list of child nodes to schedule."""
    k = key(lits)
    if ("split", k) in done:
        sp = done[("split", k)]
        kids = [lits + s for s in sp["subs"]]
        if ("gap", k) not in done:
            run_gap(root, lits, sp["subs"])
        return kids
    if ("leaf", k) in done and done[("leaf", k)]["status"] in ("UNSAT", "SAT"):
        return []
    tag = hashlib.md5(k.encode()).hexdigest()[:12]
    path = os.path.join(wd, f"n{tag}.cnf")
    write_cnf(path, lits)
    res = cadical_lrat(tag, path, TLIM) if len(lits) > FORCE_SPLIT_DEPTH else {"status": "UNKNOWN", "solve_s": 0, "forced": True}
    rec = {"kind": "leaf", "root": root, "cube": lits, "depth": len(lits), **res}
    if res["status"] == "SAT":
        sat_found.set()
        rec["unsat_core_note"] = "SAT leaf: see sat/"
        os.makedirs(os.path.join(os.path.dirname(leaves), "sat"), exist_ok=True)
        with open(os.path.join(os.path.dirname(leaves), "sat", f"model_{tag}.json"), "w") as f:
            json.dump({"root": root, "cube": lits, "model": res["model"]}, f)
        rec.pop("model")
        log(rec)
        os.remove(path)
        return []
    if res["status"] == "UNSAT":
        log(rec)
        os.remove(path)
        return []
    # timeout: split
    rec["status"] = "TIMEOUT"
    log(rec)
    subs, info = march_split(path, path + ".icnf")
    os.remove(path)
    if [] in subs:
        # march_cu refuted CNF + cube outright (it prints "a 0"); no children, and the gap
        # instance below is CNF + cube itself, solved with LRAT.
        assert subs == [[]], subs
        subs = []
        info["march_refuted_whole_cube"] = True
        info["n_sub"] = 0
    log({"kind": "split", "root": root, "cube": lits, "subs": subs, **info})
    run_gap(root, lits, subs)
    return [lits + s for s in subs]


def run_gap(root, lits, subs):
    k = key(lits)
    tag = "g" + hashlib.md5(k.encode()).hexdigest()[:12]
    path = os.path.join(wd, f"{tag}.cnf")
    write_cnf(path, lits, [[-x for x in s] for s in subs])
    res = cadical_lrat(tag, path, 3600)
    os.remove(path)
    res.pop("model", None)
    log({"kind": "gap", "root": root, "cube": lits, "n_sub": len(subs), **res})


def main():
    pending = [(i, c) for i, c in top]
    log({"kind": "start", "t": time.time(), "shard": shard, "nshards": nshards, "n_top": len(top),
         "resumed_records": len(done), "nworkers": nworkers})
    with ThreadPoolExecutor(nworkers) as ex:
        futs = {}
        while pending or futs:
            while pending and len(futs) < nworkers:
                root, lits = pending.pop(0)
                futs[ex.submit(run_node, root, lits)] = (root, lits)
            time.sleep(0.5)
            for f in [f for f in futs if f.done()]:
                root, _ = futs.pop(f)
                kids = f.result()
                pending = [(root, c) for c in kids] + pending
    log({"kind": "end", "t": time.time()})


main()
