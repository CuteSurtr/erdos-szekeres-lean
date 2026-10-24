#!/usr/bin/env python3
"""Close one case (or one shard of its top cubes) by cube-and-conquer with cake_lpr-checked leaves.

Copy of results/Mii-S/scripts/close_march.py (close_march_orig.py here) with:
  --top FILE        precomputed `march_cu CASE -d DEPTH -o FILE` (else computed into OUTDIR/top.icnf)
  --shard/--nshards process only the top cubes with 0-based line index i, i mod nshards == shard
  resumable         state is rebuilt from OUTDIR/leaves.jsonl: a cube is done if it has a record
                    with cake_lpr `s VERIFIED UNSAT`, split if it has a SPLIT record (children in
                    "subs"), otherwise pending.  A SPLIT with no children or an UNSAT that cake_lpr
                    did not verify is left open (never retried).
  output            OUTDIR/leaves.icnf: only cake_lpr-verified leaves; OUTDIR/open.icnf: open cubes.
  --hours           no new cadical runs after the deadline; unstarted cubes stay open.
  --cases-pre S     (optional) plain cadical -t S on the whole case first; accepted only if cake_lpr verifies.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--hours", type=float, default=1e9); ap.add_argument("--top")
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--cases-pre", type=int, default=0)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
deadline = time.time() + a.hours * 3600
hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
case_sha = hashlib.sha256(open(a.case, "rb").read()).hexdigest()
LOG = os.path.join(a.out, "leaves.jsonl")
lock = threading.Lock(); log = open(LOG, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def run_march(cnf, d, outf):
    t = time.time()
    o = subprocess.run([os.path.join(BIN, "march_cu"), cnf, "-d", str(d), "-o", outf], capture_output=True, text=True).stdout
    cs = [list(map(int, l.split()[1:-1])) for l in open(outf) if l.startswith("a")]
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    return cs, time.time() - t, m.group(0) if m else o[-200:]
def march(cube, d, tag):
    w = os.path.join(a.out, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube)
    cs, ms, line = run_march(os.path.join(w, "f.cnf"), d, os.path.join(w, "cubes"))
    subprocess.run(["rm", "-rf", w]); return cs, ms, line
def cadical_cake(f, w, timeout):
    """cadical --lrat on f; on UNSAT check with cake_lpr. Returns record fields."""
    t = time.time()
    rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(timeout), f,
                         os.path.join(w, "p.lrat")], stdout=subprocess.DEVNULL).returncode
    r = {"solve_s": round(time.time() - t, 2)}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        o = subprocess.run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], capture_output=True, text=True).stdout
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:]); r["check_s"] = round(time.time() - t, 2)
        r["status"] = "UNSAT"
    elif rc == 10: r["status"] = "SAT"
    else: r["status"] = "UNKNOWN"
    return r
OK = "s VERIFIED UNSAT"
def load():
    rs = [json.loads(l) for l in open(LOG)] if os.path.exists(LOG) else []
    ver, split, bad, sat = set(), {}, set(), []
    for r in rs:
        if "cube" not in r: continue
        c = tuple(r["cube"])
        if r.get("status") == "UNSAT":
            (ver.add(c) if r.get("cake_lpr") == OK else bad.add(c))
        elif r.get("status") == "SPLIT": split[c] = r.get("subs", [])
        elif r.get("status") == "SAT": sat.append(c)
    return rs, ver, split, bad, sat
def walk(roots, ver, split, bad):
    """Return (verified leaves, pending, open-for-good) under the given roots."""
    leaves, pend, stuck, st = [], [], [], [list(c) for c in reversed(roots)]
    while st:
        c = st.pop(); t = tuple(c)
        if t in ver: leaves.append(c)
        elif t in split:
            if not split[t]: stuck.append(c)
            else: st.extend(c + s for s in reversed(split[t]))
        elif t in bad: stuck.append(c)
        else: pend.append(c)
    return leaves, pend, stuck
rs, ver, split, bad, sat = load()
# optional whole-case attempt
if a.cases_pre and not any(r.get("whole_case") for r in rs):
    w = os.path.join(a.out, "s_whole"); os.makedirs(w, exist_ok=True)
    r = cadical_cake(a.case, w, a.cases_pre); subprocess.run(["rm", "-rf", w])
    r.update(whole_case=True, case_sha256=case_sha); rec(r); rs.append(r)
if any(r.get("whole_case") and r.get("cake_lpr") == OK for r in rs):
    open(os.path.join(a.out, "leaves.icnf"), "w").write("a 0\n"); open(os.path.join(a.out, "open.icnf"), "w").close()
    print("whole case closed"); raise SystemExit
# top cubes
topf = a.top or os.path.join(a.out, "top.icnf")
top_rec = next((r for r in rs if r.get("top")), None)
if not os.path.exists(topf):
    _, ms, line = run_march(a.case, a.depth, topf)
else: ms, line = None, top_rec["march"] if top_rec else None
top = [list(map(int, l.split()[1:-1])) for l in open(topf) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % a.nshards == a.shard]
if not top_rec:
    rec({"top": True, "ncubes": len(top), "march_s": ms and round(ms, 1), "march": line, "case_sha256": case_sha,
         "top_sha256": hashlib.sha256(open(topf, "rb").read()).hexdigest(), "depth": a.depth,
         "shard": a.shard, "nshards": a.nshards, "nmine": len(mine)})
_, pend, _ = walk(mine, ver, split, bad)
print(f"top {len(top)} mine {len(mine)} pending {len(pend)} verified {len(ver)}", flush=True)
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [0]
def solve(cube):
    if time.time() > deadline: return
    with lock: n[0] += 1; k = n[0]
    w = os.path.join(a.out, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); r = {"cube": cube}; r.update(cadical_cake(f, w, a.timeout))
    if r["status"] == "SAT": subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
    subs = []
    if r["status"] == "UNKNOWN":
        r["status"] = "SPLIT"; subs, ms, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), march=line, nsub=len(subs), subs=subs)
        if any(not s for s in subs):
            # march refuted the cube itself (it prints the empty cube): no split progress, so
            # retry cadical with 3x the limit; if that fails too, the cube stays open (subs = [])
            r2 = cadical_cake(f, w, 3 * a.timeout); r["retry"] = r2; subs = []
            if r2["status"] != "UNKNOWN": r.update({k: v for k, v in r2.items()}); r.pop("subs")
            else: r["subs"] = []
            if r2["status"] == "SAT": subprocess.run(["cp", f, os.path.join(a.out, f"SAT_{k}.cnf")])
    subprocess.run(["rm", "-rf", w]); rec(r)
    for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
for c in pend: submit(c)
with cv:
    while count[0] > 0: cv.wait()
log.close()
rs, ver, split, bad, sat = load()
leaves, pend, stuck = walk(mine, ver, split, bad)
with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
    for c in leaves: f.write("a " + " ".join(map(str, c)) + " 0\n")
with open(os.path.join(a.out, "open.icnf"), "w") as f:
    for c in pend + stuck: f.write("a " + " ".join(map(str, c)) + " 0\n")
print(f"leaves {len(leaves)} open {len(pend) + len(stuck)} sat {len(sat)}")
