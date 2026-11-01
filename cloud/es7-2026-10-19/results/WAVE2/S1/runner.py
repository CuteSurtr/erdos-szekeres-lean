#!/usr/bin/env python3
"""S1 runner: phase A whole-case attempts (4 parallel), phase B close_march.py in order."""
import hashlib, json, os, subprocess, sys, tempfile, time, threading, glob, calendar
from concurrent.futures import ThreadPoolExecutor
REPO = "/home/user/erdos-szekeres-lean"; ROOT = REPO + "/cloud/es7-2026-10-19"; R = ROOT + "/results"
S1 = R + "/WAVE2/S1"; BIN = "/opt/work/bin"; F = "/opt/work/F.cnf"; CASES = "/opt/work/cases"
os.makedirs(CASES, exist_ok=True); os.makedirs("/opt/work/tmp", exist_ok=True)
T_END = calendar.timegm(time.strptime("2026-10-20 13:20:00", "%Y-%m-%d %H:%M:%S"))
ORDER = "U9_L10 U3-16_L U16_L4 U8_L14 U8_L9 U9_L11 U_L2-15 U9_L5 U16_L8 U16_L2 U15_L7 U14_L11 U14_L7 U13_L10 U13_L6 U12_L16 U12_L6 U11_L15 U11_L10 U11_L5 U10_L15 U10_L11 U10_L5 U9_L15 U9_L8 U8_L15 U8_L10 U8_L2 U7_L12 U7_L8".split()
META = {json.loads(l)["case"]: json.loads(l) for l in open(R + "/Mii-S/cases.jsonl")}
glock = threading.Lock(); SUM = S1 + "/summary.jsonl"
def log(*x):
    print(time.strftime("%H:%M:%S", time.gmtime()), *x, flush=True)
def sh(cmd, **kw): return subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, **kw)
def summ(r):
    with glock:
        with open(SUM, "a") as f: f.write(json.dumps(r) + "\n")
def commit(msg, paths):
    with glock:
        for p in paths: sh(f"git add -- {p}")
        sh("git add -- results/WAVE2/S1/summary.jsonl")
        c = sh(f"git commit -q -m '{msg}'")
        for i in range(4):
            sh("git pull -q --rebase --autostash")
            p = sh("git push -q origin es7-cloud")
            if p.returncode == 0: log("pushed:", msg); return
            time.sleep(2 ** (i + 1))
        p = sh("git push -q origin HEAD:claude/es7-w2-s1"); log("PUSH REJECTED on es7-cloud; pushed to claude/es7-w2-s1:", p.returncode, p.stderr[-200:])
def other_status(case):
    with glock: sh("git pull -q --rebase --autostash")
    started, closed = [], []
    for d in glob.glob(f"{R}/WAVE1/*/{case}") + glob.glob(f"{R}/WAVE2/*/{case}") + glob.glob(f"{R}/WAVE1/*/{case}_s*") + glob.glob(f"{R}/WAVE2/*/{case}_s*"):
        if d.startswith(S1 + "/"): continue
        lv, op = d + "/leaves.icnf", d + "/open.icnf"
        nl = sum(1 for l in open(lv) if l.startswith("a")) if os.path.exists(lv) else 0
        no = sum(1 for l in open(op) if l.startswith("a")) if os.path.exists(op) else None
        if os.path.basename(d) == case and nl > 0 and no == 0: closed.append(d[len(R) + 1:])
        elif nl > 0 or os.path.exists(d + "/top.icnf"): started.append(d[len(R) + 1:])
    return closed, started
def build(case):
    m = META[case]; out = f"{CASES}/{case}.cnf"
    if not os.path.exists(out):
        sh(f"python3 results/Mii-S/scripts/hullsplit.py case {F} '{','.join(map(str, m['U']))}' '{','.join(map(str, m['L']))}' {out}")
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    assert h == m["cnf_sha256"], (case, h, m["cnf_sha256"])
    return out, h
def whole(case):
    cl, st = other_status(case)
    if cl: summ({"case": case, "phase": "A", "result": "SKIP_CLOSED_ELSEWHERE", "where": cl}); log(case, "closed elsewhere", cl); return "skip"
    if st: log(case, "started elsewhere", st); return "defer"
    cnf, h = build(case)
    w = tempfile.mkdtemp(prefix=f"w_{case}_", dir="/opt/work/tmp"); t = time.time()
    with open(w + "/out", "w") as so:
        rc = subprocess.run([BIN + "/cadical", "--lrat", "--binary=false", "-q", "-t", "120", cnf, w + "/p.lrat"], stdout=so).returncode
    st = round(time.time() - t, 2); r = {"case": case, "phase": "A", "rc": rc, "solve_s": st}
    if rc == 20:
        r["proof_bytes"] = os.path.getsize(w + "/p.lrat"); t = time.time()
        o = subprocess.run([BIN + "/cake_lpr", cnf, w + "/p.lrat"], capture_output=True, text=True)
        v = next((l for l in o.stdout.splitlines() if l.startswith("s ")), (o.stdout + o.stderr)[-120:])
        if v != "s VERIFIED UNSAT" and "heap" in v.lower():
            o = subprocess.run([BIN + "/cake_lpr", "--CML_HEAP_SIZE=10000", "--CML_STACK_SIZE=4000", cnf, w + "/p.lrat"], capture_output=True, text=True)
            v = next((l for l in o.stdout.splitlines() if l.startswith("s ")), (o.stdout + o.stderr)[-120:]); r["cake_retry"] = True
        r["cake_lpr"] = v; r["check_s"] = round(time.time() - t, 2)
        if v == "s VERIFIED UNSAT":
            d = f"{S1}/{case}"; os.makedirs(d, exist_ok=True)
            with open(d + "/leaves.jsonl", "w") as f:
                f.write(json.dumps({"case": case, "case_sha256": h}) + "\n")
                f.write(json.dumps({"cube": [], "status": "UNSAT", "method": "direct", "timeout": 120, "solve_s": st,
                                    "proof_bytes": r["proof_bytes"], "cake_lpr": v, "check_s": r["check_s"]}) + "\n")
            with open(d + "/leaves.icnf", "w") as f: f.write("a 0\n")
            open(d + "/open.icnf", "w").close()
            r["result"] = "CLOSED_DIRECT"
        else: r["result"] = "CAKE_REJECTED"
    elif rc == 10:
        d = f"{S1}/{case}"; os.makedirs(d, exist_ok=True); subprocess.run(["cp", w + "/out", d + "/SAT_whole.out"]); r["result"] = "SAT"
    else: r["result"] = "UNKNOWN_120s"
    subprocess.run(["rm", "-rf", w]); summ(r); log(case, r)
    if r["result"] in ("CLOSED_DIRECT", "SAT"):
        commit(f"WAVE2 S1: {case} {r['result']}", [f"results/WAVE2/S1/{case}"])
    return r["result"]
def drive(case):
    cl, st = other_status(case)
    if cl: summ({"case": case, "phase": "B", "result": "SKIP_CLOSED_ELSEWHERE", "where": cl}); log(case, "closed elsewhere", cl); return
    cnf, h = build(case); hours = (T_END - time.time()) / 3600
    if hours * 3600 < 900: return "noreach"
    d = f"{S1}/{case}"; assert not os.path.exists(d + "/leaves.jsonl")
    log(case, "driver start, hours", round(hours, 3))
    p = subprocess.Popen(["python3", S1 + "/close_march.py", cnf, d, "--name", case, "--depth", "7", "--timeout", "300",
                          "--split-depth", "6", "--jobs", "4", "--hours", f"{hours:.4f}"], env=dict(os.environ, BIN=BIN, WORK="/opt/work/tmp"),
                         stdout=open(f"/opt/work/s1/{case}.out", "w"), stderr=subprocess.STDOUT)
    last = time.time(); t0 = time.time()
    paths = [f"results/WAVE2/S1/{case}/{x}" for x in ("leaves.icnf", "leaves.jsonl", "open.icnf", "top.icnf")]
    while p.poll() is None:
        time.sleep(15)
        if time.time() - last > 1500:
            last = time.time(); commit(f"WAVE2 S1: {case} progress", [x for x in paths if os.path.exists(ROOT + "/" + x)] + [f"results/WAVE2/S1/{case}/SAT_*"])
    out = open(f"/opt/work/s1/{case}.out").read().strip().splitlines()
    nopen = sum(1 for l in open(d + "/open.icnf") if l.startswith("a")); nleaf = sum(1 for l in open(d + "/leaves.icnf") if l.startswith("a"))
    summ({"case": case, "phase": "B", "rc": p.returncode, "last": out[-1:] , "leaves": nleaf, "open": nopen, "wall_s": round(time.time() - t0)})
    commit(f"WAVE2 S1: {case} driver {'closed' if nopen == 0 and nleaf else 'stopped'}: {nleaf} leaves, {nopen} open",
           [x for x in paths if os.path.exists(ROOT + "/" + x)] + [f"results/WAVE2/S1/{case}/SAT_*"])
    return nopen
if __name__ == "__main__":
    order = sys.argv[1:] or ORDER
    with ThreadPoolExecutor(4) as ex: resA = dict(zip(order, ex.map(whole, order)))
    commit("WAVE2 S1: phase A whole-case attempts", [])
    rest = [c for c in order if resA[c] in ("UNKNOWN_120s", "CAKE_REJECTED")] + [c for c in order if resA[c] == "defer"]
    log("phase B order", rest)
    for c in rest:
        if drive(c) == "noreach": log("time up; not reached:", c); break
    log("RUNNER_DONE")
