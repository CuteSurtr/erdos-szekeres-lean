#!/usr/bin/env python3
"""W18 copy of results/Mii-S/scripts/close_march.py (original kept as close_march_orig.py),
changed for wave 1 shards and resumable runs.

  close_march.py CASE.cnf OUTDIR --top top.icnf --shard S --nshards K --tmp DIR --jobs 4
                 [--depth 7 --timeout 300 --split-depth 6 --deadline EPOCH] [--summarize]

Changes against the original:
- the top cubes come from a fixed file (`march_cu CASE -d 7 -o top.icnf`, run once); only lines
  with 0-based index i, i mod K == S are processed;
- resumable: on start leaves.jsonl is replayed (UNSAT with cake_lpr `s VERIFIED UNSAT` and SPLIT
  records with their children are final; anything else is redone);
- leaves.icnf lists only leaves whose cake_lpr line is `s VERIFIED UNSAT`; open.icnf lists the
  cubes still open (not yet run, deadline, unverified UNSAT, SAT, or a split without children);
- solver work files go to --tmp and the live leaves.jsonl to --state (both outside the
  repository; --summarize copies it into OUTDIR); child CPU time is recorded;
- a SAT answer keeps the model (`v` lines) in OUTDIR/SAT_<k>.model.
"""
import argparse, hashlib, json, os, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
BIN = os.environ.get("BIN", "/home/user/w18/bin")
ap = argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("out")
ap.add_argument("--top", required=True); ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1); ap.add_argument("--tmp", required=True)
ap.add_argument("--depth", type=int, default=7); ap.add_argument("--timeout", type=int, default=300)
ap.add_argument("--split-depth", type=int, default=6); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--state", required=True)
ap.add_argument("--deadline", type=float, default=1e18); ap.add_argument("--summarize", action="store_true")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); os.makedirs(a.tmp, exist_ok=True)
os.makedirs(a.state, exist_ok=True)
VER = "s VERIFIED UNSAT"
# the live log is kept in --state (outside the repository): `git pull --rebase --autostash`
# replaces tracked files, which would leave an open log handle writing to an unlinked file
LJ = os.path.join(a.state, "leaves.jsonl")
top_all = [list(map(int, l.split()[1:-1])) for l in open(a.top) if l.startswith("a")]
mine = [c for i, c in enumerate(top_all) if i % a.nshards == a.shard]

def replay():
    final = {}
    if os.path.exists(LJ):
        for l in open(LJ):
            r = json.loads(l)
            if "cube" not in r: continue
            k = tuple(r["cube"])
            if r["status"] == "UNSAT" and r.get("cake_lpr") == VER: final[k] = r
            elif r["status"] == "SPLIT" and r.get("subs"): final[k] = r
            elif r["status"] == "SAT": final[k] = r
    return final
def walk(final):
    """Return (verified leaves, todo cubes, open-final cubes) for my part."""
    leaves, todo, bad, st = [], [], [], list(mine)
    while st:
        c = st.pop(); r = final.get(tuple(c))
        if r is None: todo.append(c)
        elif r["status"] == "UNSAT": leaves.append(c)
        elif r["status"] == "SPLIT": st.extend(c + s for s in r["subs"])
        else: bad.append(c)
    return leaves, todo, bad
def write_lists():
    leaves, todo, bad = walk(replay())
    if os.path.exists(LJ): subprocess.run(["cp", LJ, os.path.join(a.out, "leaves.jsonl")])
    subprocess.run(f"cp {a.state}/SAT_* {a.out}/ 2>/dev/null", shell=True)
    with open(os.path.join(a.out, "leaves.icnf"), "w") as f:
        for c in sorted(leaves, key=lambda c: (len(c), c)): f.write("a " + " ".join(map(str, c)) + " 0\n")
    with open(os.path.join(a.out, "open.icnf"), "w") as f:
        for c in sorted(todo + bad, key=lambda c: (len(c), c)): f.write("a " + " ".join(map(str, c)) + " 0\n")
    return len(leaves), len(todo), len(bad)
if a.summarize:
    print(json.dumps(dict(zip(["leaves", "todo", "bad"], write_lists())))); raise SystemExit

hdr, body = open(a.case).read().split("\n", 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
lock = threading.Lock(); log = open(LJ, "a")
def rec(r):
    with lock: log.write(json.dumps(r) + "\n"); log.flush()
def write(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))
def run(cmd, stdout=subprocess.DEVNULL):
    """Run cmd; return (returncode, stdout text or None, child cpu seconds)."""
    p = subprocess.Popen(cmd, stdout=stdout, stderr=subprocess.DEVNULL, text=True)
    out = p.stdout.read() if stdout == subprocess.PIPE else None
    _, status, ru = os.wait4(p.pid, 0); p.returncode = os.waitstatus_to_exitcode(status)
    return p.returncode, out, ru.ru_utime + ru.ru_stime
def march(cube, d, tag):
    w = os.path.join(a.tmp, f"m_{tag}"); os.makedirs(w, exist_ok=True)
    write(os.path.join(w, "f.cnf"), cube); t = time.time()
    _, o, cpu = run([os.path.join(BIN, "march_cu"), os.path.join(w, "f.cnf"), "-d", str(d), "-o",
                     os.path.join(w, "cubes")], subprocess.PIPE)
    cf = os.path.join(w, "cubes")
    cs = [list(map(int, l.split()[1:-1])) for l in open(cf) if l.startswith("a")] if os.path.exists(cf) else []
    m = re.search(r"number of cubes (\d+), including (\d+) refuted", o)
    subprocess.run(["rm", "-rf", w]); return cs, time.time() - t, cpu, m.group(0) if m else o[-200:]
pool = ThreadPoolExecutor(a.jobs); cv = threading.Condition(); count = [0]; n = [int(time.time()) % 100000 * 1000]
def solve(cube):
    with lock: n[0] += 1; k = n[0]
    if time.time() > a.deadline:
        rec({"cube": cube, "status": "OPEN", "reason": "deadline"}); return
    w = os.path.join(a.tmp, f"s_{k}"); os.makedirs(w, exist_ok=True); f = os.path.join(w, "f.cnf")
    write(f, cube); t = time.time()
    rc, o, cpu = run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", str(a.timeout), f,
                      os.path.join(w, "p.lrat")], subprocess.PIPE)
    st = round(time.time() - t, 2); r = {"cube": cube, "solve_s": st, "solve_cpu": round(cpu, 2)}
    subs = []
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(os.path.join(w, "p.lrat")); t = time.time()
        _, o, cpu = run([os.path.join(BIN, "cake_lpr"), f, os.path.join(w, "p.lrat")], subprocess.PIPE)
        r["cake_lpr"] = next((l for l in o.splitlines() if l.startswith("s ")), o[-100:])
        r["check_s"] = round(time.time() - t, 2); r["check_cpu"] = round(cpu, 2)
        r["status"] = "UNSAT"
    elif rc == 10:
        r["status"] = "SAT"
        with open(os.path.join(a.state, f"SAT_{k}.model"), "w") as g: g.write(o)
        subprocess.run(["cp", f, os.path.join(a.tmp, f"SAT_{k}.cnf")])
    else:
        r["status"] = "SPLIT"; subs, ms, mcpu, line = march(cube, a.split_depth, k)
        r.update(split_s=round(ms, 1), split_cpu=round(mcpu, 2), march=line, nsub=len(subs), subs=subs)
    subprocess.run(["rm", "-rf", w]); rec(r)
    for s in subs: submit(cube + s)
def task(c):
    try: solve(c)
    except Exception:
        import traceback; rec({"cube": c, "status": "ERROR", "error": traceback.format_exc()[-1500:]})
    finally:
        with cv: count[0] -= 1; cv.notify_all()
def submit(c):
    with cv: count[0] += 1
    pool.submit(task, c)
final = replay(); leaves, todo, bad = walk(final)
rec({"start": True, "shard": a.shard, "nshards": a.nshards, "ntop": len(top_all), "nmine": len(mine),
     "top_sha256": hashlib.sha256(open(a.top, "rb").read()).hexdigest(),
     "case_sha256": hashlib.sha256(open(a.case, "rb").read()).hexdigest(),
     "resume_leaves": len(leaves), "resume_todo": len(todo), "resume_bad": len(bad), "time": time.time()})
for c in todo: submit(c)
with cv:
    while count[0] > 0: cv.wait()
print(json.dumps(dict(zip(["leaves", "todo", "bad"], write_lists()))))
