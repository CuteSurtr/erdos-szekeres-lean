#!/usr/bin/env python3
"""W16 copy of results/Mii-S/scripts/close_march.py, changed for wave-1 shards.

  close_march_w16.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --jobs 4
Changes against the original:
- --top: the top cubes come from a fixed `march_cu CASE -d 7 -o top.icnf` file (the same file for
  every shard of a case); only lines with 0-based line index i, i mod K == S, are processed.
- resumable: every finished cube is a record in OUTDIR/leaves.jsonl; a SPLIT record stores its
  children ("subs"), so on restart the pending set is (shard top cubes + children of SPLIT
  records) minus cubes that already have an UNSAT/SAT/SPLIT record.  OPEN records are retried.
- CPU time (user+sys of the child processes, via wait4) per record.
- leaves.icnf lists only cubes whose cake_lpr verdict is `s VERIFIED UNSAT`; open.icnf lists
  every cube of the shard that is neither closed that way nor split (see summarize()).
Leaf solve: `cadical --lrat -t TIMEOUT` on CASE + units(cube), proof checked with cake_lpr and
deleted.  A cube that times out is split by `march_cu CASE+units(c) -d SPLIT`.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/opt/w16/bin")
VER = "s VERIFIED UNSAT"

def run(cmd, out=None):
    """Run cmd, return (returncode, cpu seconds of the child)."""
    f = open(out, "w") if out else subprocess.DEVNULL
    p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT if out else subprocess.DEVNULL)
    _, status, ru = os.wait4(p.pid, 0)
    p.returncode = os.waitstatus_to_exitcode(status)
    if out: f.close()
    return p.returncode, ru.ru_utime + ru.ru_stime

def shard_top(top, s, k):
    lines = open(top).read().splitlines()
    return [list(map(int, l.split()[1:-1])) for i, l in enumerate(lines) if i % k == s and l.startswith("a")]

def summarize(out, topcubes):
    """Write leaves.icnf (cake_lpr-verified leaves) and open.icnf; return counts."""
    recs = [json.loads(l) for l in open(os.path.join(out, "leaves.jsonl")) if l.strip()]
    done, ver, subs, sat, cpu = {}, [], [], 0, 0.0
    for r in recs:
        if "cube" not in r: continue
        cpu += r.get("cpu_s", 0.0)
        if r["status"] == "UNSAT" and r.get("cake_lpr") == VER: done[tuple(r["cube"])] = r; ver.append(r["cube"])
        elif r["status"] == "SPLIT": done[tuple(r["cube"])] = r; subs += [r["cube"] + c for c in r["subs"]]
        elif r["status"] == "SAT": sat += 1
    pend = [c for c in topcubes + subs if tuple(c) not in done]
    with open(os.path.join(out, "leaves.icnf"), "w") as f:
        for c in ver: f.write("a " + " ".join(map(str, c)) + " 0\n")
    with open(os.path.join(out, "open.icnf"), "w") as f:
        for c in pend: f.write("a " + " ".join(map(str, c)) + " 0\n")
    nsplit = sum(1 for r in done.values() if r["status"] == "SPLIT")
    return {"verified_leaves": len(ver), "splits": nsplit, "open": len(pend), "sat": sat, "cpu_s": round(cpu, 1)}, pend

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
    ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--hours", type=float, default=1e9)
    ap.add_argument("--summarize", action="store_true", help="only rewrite leaves.icnf/open.icnf")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    topcubes = shard_top(a.top, a.shard, a.nshards)
    lp = os.path.join(a.out, "leaves.jsonl")
    if not os.path.exists(lp): open(lp, "w").close()
    if a.summarize:
        print(json.dumps(summarize(a.out, topcubes)[0])); return
    deadline = time.time() + a.hours * 3600
    hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
    lock = threading.Lock(); log = open(lp, "a")
    def rec(r):
        with lock: log.write(json.dumps(r) + "\n"); log.flush()
    if not any('"top"' in l for l in open(lp)):
        rec({"top": True, "top_file": a.top, "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
             "shard": a.shard, "nshards": a.nshards, "shard_cubes": len(topcubes),
             "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest()})
    def write(path, cube):
        with open(path, "w") as f:
            f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
    def march(cube, d, w):
        t = time.time(); f = os.path.join(w, "f.cnf"); c = os.path.join(w, "cubes"); o = os.path.join(w, "m.out")
        _, cpu = run([os.path.join(BIN, "march_cu"), f, "-d", str(d), "-o", c], o)
        cs = [list(map(int, l.split()[1:-1])) for l in open(c) if l.startswith("a")]
        m = re.search(r"number of cubes (\d+), including (\d+) refuted", open(o).read())
        return cs, time.time() - t, cpu, m.group(0) if m else open(o).read()[-200:]
    pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
    def solve(cube):
        with lock: n[0] += 1; k = n[0]
        if time.time() > deadline:
            rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); return
        w = os.path.join(a.out, f"s_{os.getpid()}_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
        write(f, cube); t = time.time()
        rc, cpu = run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                       os.path.join(w, "p.lrat")])
        r = {"cube": cube, "solve_s": round(time.time() - t, 2)}
        if rc == 20:
            r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
            _, c2 = run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], os.path.join(w, "c.out"))
            o = open(os.path.join(w, "c.out")).read(); cpu += c2
            r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
            r["status"] = "UNSAT"
        elif rc == 10:
            r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
            out = subprocess.run([os.path.join(BIN, "cadical"), "-q", f], capture_output=True, text=True).stdout
            open(os.path.join(a.out, f"SAT_{k}.model"), "w").write(out)
        else:
            os.remove(os.path.join(w, "p.lrat")) if os.path.exists(os.path.join(w, "p.lrat")) else None
            subs, ms, c3, line = march(cube, a.split_depth, w); cpu += c3
            r.update(status="SPLIT", cadical_rc=rc, split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
        r["cpu_s"] = round(cpu, 2)
        subprocess.run(["rm", "-rf", w]); rec(r)
        if r["status"] == "SPLIT":
            for s in subs: submit(cube + s)
    def task(c):
        try: solve(c)
        except Exception as e: rec({"cube": c, "status": "ERROR", "error": repr(e)})
        finally:
            with cv: count[0] -= 1; cv.notify_all()
    def submit(c):
        with cv: count[0] += 1
        pool.submit(task, c)
    _, pend = summarize(a.out, topcubes)
    rec({"resume": True, "pending": len(pend), "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    for c in pend: submit(c)
    with cv:
        while count[0] > 0: cv.wait()
    print(json.dumps(summarize(a.out, topcubes)[0]))

if __name__ == "__main__":
    main()
