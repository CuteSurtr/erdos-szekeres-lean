#!/usr/bin/env python3
"""Close one case CNF (or one shard of its top cubes) by cube-and-conquer with cake_lpr-checked leaves.

  close_march.py CASE.cnf OUTDIR --depth 7 --timeout 300 --split-depth 6 --jobs J
                 [--top TOP.icnf] [--shard s --nshards k] [--hours H]
  close_march.py CASE.cnf OUTDIR --finalize [--top TOP.icnf] [--shard s --nshards k]
Changes from results/Mii-S/scripts/close_march.py (W12, wave 1):
- --top reuses a top-cube file made by `march_cu CASE -d DEPTH -o TOP.icnf` (all shards of a case
  must use the same file); without it the top cubes are made as before and kept in OUTDIR/top.icnf.
- --shard/--nshards: only top cubes with 0-based cube-line index i, i mod nshards == shard.
- resumable: OUTDIR/leaves.jsonl is re-read; a cube is done if it has an UNSAT record with
  cake_lpr `s VERIFIED UNSAT`, it is replaced by its children if it has a SPLIT record (children
  are now stored in `subs`); everything else is (re)queued.
- leaves.icnf lists only leaves with cake_lpr `s VERIFIED UNSAT`; an UNSAT answer that cake_lpr
  does not verify is recorded as UNSAT_UNVERIFIED and stays open.  open.icnf lists the open cubes.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/home/user/tools/bin")
VER = "s VERIFIED UNSAT"
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--top")
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--finalize", action="store_true")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
L = os.path.join(a.out, "leaves.jsonl")
def read_cubes(path): return [list(map(int, l.split()[1:-1])) for l in open(path) if l.startswith("a")]
def records(): return [json.loads(l) for l in open(L)] if os.path.exists(L) else []
def mine(top): return [c for i, c in enumerate(top) if i % a.nshards == a.shard]
def state(recs, roots):
    """Expand the roots through SPLIT records; return (verified leaves, open cubes)."""
    done = {tuple(r["cube"]) for r in recs if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER}
    split = {tuple(r["cube"]): r["subs"] for r in recs if r.get("status") == "SPLIT" and "subs" in r}
    leaves, opn, stack = [], [], list(reversed(roots))
    while stack:
        c = stack.pop(); t = tuple(c)
        if t in done: leaves.append(c)
        elif t in split: stack.extend(reversed([c + s for s in split[t]]))
        else: opn.append(c)
    return leaves, opn
def finalize(roots):
    leaves, opn = state(records(), roots)
    with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
        f.writelines("a " + " ".join(map(str, c)) + " 0\n" for c in leaves)
    with open(os.path.join(a.out, "open.icnf"), "w") as f:
        f.writelines("a " + " ".join(map(str, c)) + " 0\n" for c in opn)
    return leaves, opn
top_path = a.top or os.path.join(a.out, "top.icnf")
if a.finalize:
    l, o = finalize(mine(read_cubes(top_path))); print(f"verified leaves {len(l)} open {len(o)}"); raise SystemExit
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); log = open(L, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def march(cube, d, tag, keep=None):
    w = os.path.join(a.out, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                        os.path.join(w, "cubes")], capture_output=True, text=True).stdout
    cs = read_cubes(os.path.join(w, "cubes"))
    if keep: subprocess.run(["cp", os.path.join(w, "cubes"), keep])
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, m.group(0) if m else o[-200:]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    if time.time() > deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); subprocess.run(["rm", "-rf", w]); return
    write(f, cube); t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT" if r["cake_lpr"] == VER else "UNSAT_UNVERIFIED"
    elif rc == 10:
        r["status"] = "SAT"; subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
    else:
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
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
case_sha = hashlib.sha256(open(a.case, "rb").read()).hexdigest()
if not os.path.exists(top_path):
    top, ms, line = march([], a.depth, "top", keep=top_path)
    rec({"top": True, "ncubes": len(top), "march_s": round(ms, 1), "march": line, "case_sha256": case_sha})
top = read_cubes(top_path); roots = mine(top)
_, todo = state(records(), roots)
rec({"start": True, "case_sha256": case_sha, "top_sha256": hashlib.sha256(open(top_path, "rb").read()).hexdigest(),
     "ntop": len(top), "shard": a.shard, "nshards": a.nshards, "nroots": len(roots), "queued": len(todo),
     "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
l, o = finalize(roots); rec({"end": True, "verified_leaves": len(l), "open": len(o),
                            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
