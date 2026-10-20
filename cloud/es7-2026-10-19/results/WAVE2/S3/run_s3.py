#!/usr/bin/env python3
"""S3 runner: hull cases of sub-case (ii) from the back of W34's list.

Phase 1 (4 workers): per case, skip check (git pull), build the case CNF with hullsplit.py, check its
sha256 against cases.jsonl, whole-case CaDiCaL 120 s with LRAT, cake_lpr. A case counts as closed
only with the exact line `s VERIFIED UNSAT`.
Phase 2 (sequential): close_march.py --depth 7 --timeout 300 --split-depth 6 --jobs 4 on the
remaining cases, the next case's top cubes (march_cu -d 7) made one case ahead.
Every finished case is committed and pushed; the running case every 20 minutes.
Usage: run_s3.py END_EPOCH   (driver deadline; nothing new starts after it)
"""
import glob, hashlib, json, os, subprocess, sys, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor
ROOT = "/home/user/erdos-szekeres-lean"; BASE = "cloud/es7-2026-10-19"; os.chdir(os.path.join(ROOT, BASE))
S = "results/WAVE2/S3"; BIN = "/opt/work/bin"; WORK = "/opt/work/tmp"; CN = "/opt/work/cases"; F = "/opt/work/F.cnf"
os.makedirs(WORK, exist_ok=True); os.makedirs(CN, exist_ok=True)
END = float(sys.argv[1]); VER = "s VERIFIED UNSAT"
ORDER = "U16_L11 U13_L11 U15_L9 U_L4-10 U3-15_L U12_L9 U8_L6 U12_L2 U4_L10 U5_L15 U16_L9 U16_L5 U15_L8 U15_L2 U14_L8 U14_L2 U13_L7 U13_L2 U12_L8 U11_L16 U11_L12 U11_L7 U10_L16 U10_L12 U10_L6 U9_L16 U9_L12 U9_L2 U8_L11 U8_L4".split()
CASES = {r["case"]: r for r in map(json.loads, open("results/Mii-S/cases.jsonl"))}
glock = threading.Lock(); LOG = open(os.path.join(S, "run.log"), "a")
def log(*m):
    with glock: LOG.write(time.strftime("%H:%M:%S ") + " ".join(map(str, m)) + "\n"); LOG.flush()
def sh(*c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
def git_sync(msg, paths):
    with glock:
        fs = []
        for p in paths:
            for dp, _, fn in (os.walk(p) if os.path.isdir(p) else [(os.path.dirname(p), None, [os.path.basename(p)])]):
                fs += [os.path.join(dp, x) for x in fn if not x.startswith(".") and not x.endswith((".cnf", ".lrat"))
                       and os.path.getsize(os.path.join(dp, x)) <= 50e6]
        if fs: sh("git", "add", "--", *fs)
        sh("git", "commit", "-q", "-m", msg)
        sh("git", "pull", "-q", "--rebase", "--autostash", "origin", "es7-cloud")
        for i in range(5):
            r = sh("git", "push", "-q", "origin", "HEAD:es7-cloud")
            if r.returncode == 0: return "es7-cloud"
            if "rejected" in r.stderr or "non-fast-forward" in r.stderr:
                sh("git", "pull", "-q", "--rebase", "--autostash", "origin", "es7-cloud"); continue
            time.sleep(2 ** (i + 1))
        r = sh("git", "push", "-q", "origin", "HEAD:claude/es7-w2-s3")
        LOG.write(f"push to es7-cloud failed; pushed to claude/es7-w2-s3 rc={r.returncode} {r.stderr[-200:]}\n"); LOG.flush()
        return "claude/es7-w2-s3"
def pull():
    with glock: sh("git", "pull", "-q", "--rebase", "--autostash", "origin", "es7-cloud")
def others(case):
    """('closed', dir) | ('started', dir) | (None, None) from other machines' directories."""
    st = (None, None)
    for d in glob.glob(f"results/WAVE1/*/{case}") + glob.glob(f"results/WAVE2/*/{case}"):
        if d.startswith(S): continue
        lv, op = os.path.join(d, "leaves.icnf"), os.path.join(d, "open.icnf")
        nl = os.path.exists(lv) and any(l.startswith("a") for l in open(lv))
        if nl and os.path.exists(op) and not any(l.startswith("a") for l in open(op)): return ("closed", d)
        if nl or os.path.exists(os.path.join(d, "top.icnf")): st = ("started", d)
    return st
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def build(case):
    r = CASES[case]; out = os.path.join(CN, case + ".cnf")
    if not (os.path.exists(out) and sha(out) == r["cnf_sha256"]):
        sh("python3", "results/Mii-S/scripts/hullsplit.py", "case", F, ",".join(map(str, r["U"])), ",".join(map(str, r["L"])), out)
    h = sha(out); assert h == r["cnf_sha256"], (case, h); return out, h
def cake(f, p, extra=()):
    r = sh(os.path.join(BIN, "cake_lpr"), *extra, f, p)
    return next((l for l in r.stdout.splitlines() if l.startswith("s ")), (r.stdout + r.stderr)[-120:])
status = {}  # case -> dict for README
def whole(case):
    try: whole1(case)
    except Exception as e: log(case, "whole failed", repr(e)); status.setdefault(case, {})["error"] = repr(e)
PRIOR = {}
for l in (open(os.path.join(S, "run.log")) if os.path.exists(os.path.join(S, "run.log")) else []):
    t = l.split(" ", 3)
    if len(t) == 4 and t[2] == "whole" and t[3].startswith("{"): PRIOR[t[1]] = json.loads(t[3])
def whole1(case):
    st, d = others(case)
    if case in PRIOR and PRIOR[case]["status"] == "UNKNOWN" and st != "closed":   # restart: reuse phase-1 result
        f, h = build(case); status[case] = {"whole": PRIOR[case], "sha": h}; return
    if os.path.exists(os.path.join(S, case, "leaves.icnf")) and open(os.path.join(S, case, "leaves.icnf")).read() == "a 0\n":
        status[case] = {"whole": PRIOR.get(case), "sha": build(case)[1], "state": "closed_whole"}; return
    if st == "closed": status[case] = {"state": "skipped", "closed_in": d}; log(case, "closed elsewhere", d); return
    f, h = build(case); w = tempfile.mkdtemp(prefix="w_", dir=WORK); p = os.path.join(w, "p.lrat")
    t = time.time()
    with open(os.path.join(w, "out"), "w") as so:
        rc = subprocess.run([os.path.join(BIN, "cadical"), "--lrat", "--binary=false", "-q", "-t", "120", f, p], stdout=so).returncode
    r = {"whole": True, "cube": [], "timeout": 120, "rc": rc, "solve_s": round(time.time() - t, 2)}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(p); t = time.time(); v = cake(f, p)
        if v != VER and "heap" in v.lower(): v = cake(f, p, ["--CML_HEAP_SIZE=10000", "--CML_STACK_SIZE=4000"]); r["cake_retry"] = True
        r["cake_lpr"] = v; r["check_s"] = round(time.time() - t, 2); r["status"] = "UNSAT" if v == VER else "UNSAT_UNCHECKED"
    elif rc == 10:
        r["status"] = "SAT"; os.makedirs(os.path.join(S, case), exist_ok=True)
        subprocess.run(["cp", os.path.join(w, "out"), os.path.join(S, case, "SAT_whole.out")])
    else: r["status"] = "UNKNOWN"
    subprocess.run(["rm", "-rf", w]); log(case, "whole", json.dumps(r))
    status[case] = {"whole": r, "sha": h}
    if r["status"] in ("UNSAT", "SAT", "UNSAT_UNCHECKED"):
        od = os.path.join(S, case); os.makedirs(od, exist_ok=True)
        with open(os.path.join(od, "leaves.jsonl"), "w") as g:
            g.write(json.dumps({"case": case, "case_sha256": h}) + "\n"); g.write(json.dumps(r) + "\n")
        if r["status"] == "UNSAT":
            open(os.path.join(od, "leaves.icnf"), "w").write("a 0\n"); open(os.path.join(od, "open.icnf"), "w").write("")
            status[case]["state"] = "closed_whole"
        else:
            open(os.path.join(od, "leaves.icnf"), "w").write(""); open(os.path.join(od, "open.icnf"), "w").write("a 0\n")
            status[case]["state"] = r["status"]
        git_sync(f"WAVE2 S3: {case} whole-case {r['status']}", [od])
def top(case):
    tp = os.path.join(CN, case + ".top.icnf")
    if os.path.exists(tp): return tp
    f = os.path.join(CN, case + ".cnf"); t = time.time()
    o = sh(os.path.join(BIN, "march_cu"), f, "-d", "7", "-o", tp + ".tmp").stdout
    os.replace(tp + ".tmp", tp); log(case, "top", round(time.time() - t, 1), [l for l in o.splitlines() if "number of cubes" in l])
    return tp
def drive(case, tp):
    od = os.path.join(S, case); H = (END - time.time()) / 3600
    env = dict(os.environ, BIN=BIN, WORK=WORK)
    p = subprocess.Popen(["python3", os.path.join(S, "close_march.py"), os.path.join(CN, case + ".cnf"), od, "--name", case,
                          "--depth", "7", "--timeout", "300", "--split-depth", "6", "--jobs", "4", "--hours", f"{H:.4f}",
                          "--top", tp], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    t0 = time.time(); last = t0
    while p.poll() is None:
        time.sleep(15)
        if time.time() - last > 1200: git_sync(f"WAVE2 S3: {case} progress", [od]); last = time.time()
    out = p.stdout.read(); log(case, "driver exit", p.returncode, out[-300:])
    return time.time() - t0
if __name__ == "__main__":
    pull(); log("start END", time.strftime("%H:%M:%S", time.gmtime(END)))
    with ThreadPoolExecutor(4) as ex: list(ex.map(whole, ORDER))
    git_sync("WAVE2 S3: phase 1 log", [os.path.join(S, "run.log")])
    todo = [c for c in ORDER if status.get(c, {}).get("state") is None]
    moved = set(); i = 0; pre = None
    while i < len(todo):
        case = todo[i]; i += 1
        if time.time() > END - 400: log("out of time; not reached:", todo[i - 1:]); break
        pull(); st, d = others(case)
        if st == "closed": status.setdefault(case, {}).update(state="skipped", closed_in=d); log(case, "closed elsewhere", d); continue
        if st == "started" and case not in moved: moved.add(case); todo.append(case); log(case, "started elsewhere, moved to end", d); continue
        status.setdefault(case, {})
        if "sha" not in status[case]: log(case, "no checked CNF; not run"); continue
        tp = pre.result() if pre and pre.case == case else top(case)
        nxt = next((c for c in todo[i:] if others(c)[0] is None), None)
        if nxt:
            pre = ThreadPoolExecutor(1).submit(top, nxt); pre.case = nxt
        dt = drive(case, tp)
        od = os.path.join(S, case); nopen = sum(1 for l in open(os.path.join(od, "open.icnf")) if l.startswith("a"))
        status[case]["state"] = "closed" if nopen == 0 else "open"; status[case]["wall_s"] = round(dt)
        git_sync(f"WAVE2 S3: {case} {'closed' if nopen == 0 else f'{nopen} open'}", [od, os.path.join(S, "run.log")])
    json.dump(status, open(os.path.join(S, "status.json"), "w"), indent=1)
    git_sync("WAVE2 S3: runner done", [os.path.join(S, "status.json"), os.path.join(S, "run.log")]); log("done")
