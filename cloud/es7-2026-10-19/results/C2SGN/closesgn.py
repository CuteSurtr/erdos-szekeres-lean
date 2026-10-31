#!/usr/bin/env python3
"""Adaptive closer for the compact encoding (check and delete).

Each node is a cube of the base formula, named by its layers (see l3sgn.py). A node is solved with CaDiCaL --lrat
under a time cap. On UNSAT the proof is checked by lrat-check and cake_lpr and then deleted. On a timeout the node is
split at its next convex layer (l3sgn.py). Children refuted by unit propagation are dropped. The split is certified by
a cover proof: base + node cube as units + one clause per remaining child, also checked by both checkers and deleted.
The children are then queued. A satisfiable node stops the run.

One JSON line per node and per cover goes to OUT/results.jsonl. A rerun skips nodes already recorded as closed. All
files are written under OUT; only proofs and per-node CNFs under OUT/work are deleted.
usage: closesgn.py BASE.cnf MAP.json n CUBES ROOT_NAME... --out OUT [--cap S] [--jobs J] [--heap MB] [--hours H]"""
import argparse, hashlib, json, os, queue, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "..", "local", "bin")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base"); ap.add_argument("map"); ap.add_argument("n", type=int); ap.add_argument("cubes")
    ap.add_argument("roots", nargs="+"); ap.add_argument("--out", required=True)
    ap.add_argument("--cap", type=int, default=120); ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--heap", type=int, default=3000); ap.add_argument("--hours", type=float, default=1.0)
    a = ap.parse_args()
    out = os.path.abspath(a.out); work = os.path.join(out, "work"); os.makedirs(work, exist_ok=True)
    deadline = time.time() + 3600 * a.hours
    base_lines = open(a.base).read().split("\n")
    hdr_i = next(i for i, l in enumerate(base_lines) if l.startswith("p cnf"))
    _, _, nv, nc = base_lines[hdr_i].split(); nv, nc = int(nv), int(nc)
    body = "\n".join(l for i, l in enumerate(base_lines) if i != hdr_i and l and not l.startswith("c")) + "\n"
    tree = os.path.join(out, "tree.cubes")
    if not os.path.exists(tree):
        with open(a.cubes) as f, open(tree, "w") as g:
            roots = set(a.roots)
            for l in f:
                if l.split()[0] in roots: g.write(l)
    cubes = {l.split()[0]: [int(x) for x in l.split()[1:]] for l in open(tree)}
    done = set()
    res = os.path.join(out, "results.jsonl")
    if os.path.exists(res):
        for l in open(res):
            r = json.loads(l)
            if r.get("closed"): done.add(r["node"])
    lock = threading.Lock(); cake = threading.Semaphore(1); q = queue.Queue(); stop = threading.Event()
    for r in a.roots:
        if r not in done: q.put(r)

    def record(r):
        r["finished"] = time.strftime("%H:%M:%SZ", time.gmtime())
        with lock, open(res, "a") as f: f.write(json.dumps(r) + "\n")

    def write_cnf(path, units, clauses=()):
        with open(path, "w") as f:
            f.write(f"p cnf {nv} {nc + len(units) + len(clauses)}\n"); f.write(body)
            for u in units: f.write(f"{u} 0\n")
            for c in clauses: f.write(" ".join(map(str, c)) + " 0\n")

    def prove(cnf, cap, tag):
        """CaDiCaL --lrat, then both checkers; returns a record dict (proof deleted when both accept)."""
        proof = os.path.join(work, tag + ".lrat"); log = os.path.join(work, tag + ".out")
        t0 = time.time()
        with open(log, "w") as f:
            subprocess.run(["nice", "-n", "5", os.path.join(BIN, "cadical"), "-t", str(cap), "--lrat", "--binary=false",
                            cnf, proof], stdout=f, stderr=subprocess.STDOUT)
        txt = open(log).read(); st = "UNKNOWN"
        for l in txt.splitlines():
            if l.startswith("s "): st = l[2:].strip(); break
        r = {"status": st, "solve_wall_s": round(time.time() - t0, 1), "cnf_sha256": sha(cnf)}
        if st == "UNSATISFIABLE":
            r["proof_bytes"] = os.path.getsize(proof); r["proof_sha256"] = sha(proof)
            t = time.time()
            lc = subprocess.run([os.path.join(BIN, "lrat-check"), cnf, proof], capture_output=True, text=True).stdout
            r["lrat_check"] = next((l for l in lc.splitlines() if "VERIFIED" in l or "FAIL" in l or "rror" in l), "no verdict")
            r["lrat_check_s"] = round(time.time() - t, 1)
            lockdir = os.path.join(HERE, "camp", "cakelock")     # shared with camp/lane.sh: one cake_lpr at a time
            while True:
                try:
                    os.mkdir(lockdir); break
                except FileExistsError:
                    time.sleep(3)
            try:
                t = time.time()
                ck = subprocess.run([os.path.join(BIN, "cake_lpr"), f"--CML_HEAP_SIZE={a.heap}", "--CML_STACK_SIZE=1000",
                                     cnf, proof], capture_output=True, text=True)
                o = ck.stdout + ck.stderr
                r["cake_lpr"] = next((l for l in o.splitlines() if "s VERIFIED" in l or "exhausted" in l or "rror" in l or "FAIL" in l), "no verdict")
                r["cake_s"] = round(time.time() - t, 1)
            finally:
                os.rmdir(lockdir)
            r["checked"] = r["lrat_check"] == "c VERIFIED" and r["cake_lpr"] == "s VERIFIED UNSAT"
            if r["checked"]:
                os.unlink(proof)
            else:
                os.rename(proof, os.path.join(out, tag + ".lrat.kept"))
        elif os.path.exists(proof):
            os.unlink(proof)
        if st == "SATISFIABLE":
            os.rename(log, os.path.join(out, "SAT_" + tag + ".out")); stop.set()
        elif os.path.exists(log):
            os.unlink(log)
        return r

    def children(name):
        p = subprocess.run([sys.executable, os.path.join(HERE, "l3sgn.py"), a.map, str(a.n), tree, name],
                           capture_output=True, text=True, check=True).stdout
        up = subprocess.run([os.path.join(HERE, "upfilter"), a.base], input=p, capture_output=True, text=True, check=True).stdout
        ok = {l.split()[0] for l in up.splitlines() if l.split()[1] == "OK"}
        kids = [l for l in p.splitlines() if l.split()[0] in ok]
        return kids, len(p.splitlines())

    def worker():
        while not stop.is_set():
            try:
                name = q.get(timeout=5)
            except queue.Empty:
                if q.unfinished_tasks == 0: return
                continue
            try:
                if time.time() > deadline: continue
                tag = name.replace("/", "_"); cnf = os.path.join(work, tag + ".cnf")
                write_cnf(cnf, cubes[name])
                r = prove(cnf, a.cap, tag); os.unlink(cnf)
                r.update({"node": name, "kind": "node", "cap_s": a.cap, "closed": r.get("checked", False)})
                record(r)
                if r["status"] == "UNKNOWN" and time.time() < deadline:
                    kids, total = children(name)
                    pre = set(cubes[name])
                    with lock, open(tree, "a") as f:
                        for l in kids:
                            cubes[l.split()[0]] = [int(x) for x in l.split()[1:]]; f.write(l + "\n")
                    ccnf = os.path.join(work, tag + "_cover.cnf")
                    write_cnf(ccnf, cubes[name], [[-x for x in cubes[k.split()[0]] if x not in pre] for k in kids])
                    rc = prove(ccnf, 7200, tag + "_cover"); os.unlink(ccnf)
                    rc.update({"node": name, "kind": "cover", "children": len(kids), "children_before_up": total})
                    record(rc)
                    if rc.get("checked"):
                        for k in kids:
                            if k.split()[0] not in done: q.put(k.split()[0])
            finally:
                q.task_done()

    ts = [threading.Thread(target=worker) for _ in range(a.jobs)]
    for t in ts: t.start()
    for t in ts: t.join()
    print("stopped:", "SAT found" if stop.is_set() else ("deadline" if time.time() > deadline else "queue empty"))


if __name__ == "__main__":
    main()
