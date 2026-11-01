import json, os, subprocess, sys, time, hashlib, threading
REPO = "/home/user/erdos-szekeres-lean"; ROOT = "cloud/es7-2026-10-19"; S5 = f"{ROOT}/results/WAVE2/S5"
END = time.mktime(time.strptime("2026-10-20 13:20:00", "%Y-%m-%d %H:%M:%S")) - time.timezone  # driver deadline (UTC)
order = open("/opt/work/order.txt").read().split()
LOG = open("/opt/work/runner.log", "a")
def log(*x): LOG.write(time.strftime("%H:%M:%S ", time.gmtime()) + " ".join(map(str, x)) + "\n"); LOG.flush()
glock = threading.Lock()
def git(*args): return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
def push(msg):
    with glock:
        git("add", S5); r = git("commit", "-qm", msg)
        for i in range(5):
            git("pull", "-q", "--rebase", "--autostash", "origin", "es7-cloud")
            p = git("push", "-q", "origin", "es7-cloud")
            if p.returncode == 0: log("pushed", msg); return
            time.sleep(2 ** (i + 1))
        p = git("push", "-q", "origin", "HEAD:claude/es7-w2-s5"); log("PUSH FALLBACK claude/es7-w2-s5", p.returncode, p.stderr[-200:])
def status(c):
    with glock: git("pull", "-q", "--rebase", "--autostash", "origin", "es7-cloud")
    out = subprocess.run(["python3", "/opt/work/status.py", c], cwd=f"{REPO}/{ROOT}", capture_output=True, text=True).stdout
    return "CLOSED" if "'CLOSED'" in out else ("STARTED" if "'STARTED'" in out else "FREE"), out.strip()
def periodic():
    while True:
        time.sleep(25 * 60); push("S5: progress " + time.strftime("%H:%M", time.gmtime()))
threading.Thread(target=periodic, daemon=True).start()
cases_sha = {json.loads(l)["case"]: json.loads(l)["cnf_sha256"] for l in open(f"{REPO}/{ROOT}/results/Mii-S/cases.jsonl")}
deferred = set(sys.argv[1:])
i = 0
while i < len(order):
    c = order[i]; i += 1
    if time.time() > END - 600: log("not reached", c); continue
    st, det = status(c); log("status", c, st, det)
    if st == "CLOSED": log("SKIP closed elsewhere", c); continue
    if st == "STARTED" and c not in deferred: deferred.add(c); order.append(c); log("defer", c); continue
    f = f"/opt/work/cases/{c}.cnf"; h = hashlib.sha256(open(f, "rb").read()).hexdigest()
    assert h == cases_sha[c], c
    out = f"{REPO}/{S5}/{c}"
    # whole-case attempt (may already have been run by whole.sh)
    wl = [l for l in open("/opt/work/whole.log")] if os.path.exists("/opt/work/whole.log") else []
    mine = [l for l in wl if l.split()[0] == c]
    if not mine:
        subprocess.run(["bash", "/opt/work/whole.sh", c]); mine = [l for l in open("/opt/work/whole.log") if l.split()[0] == c]
    while not mine:
        time.sleep(10); mine = [l for l in open("/opt/work/whole.log") if l.split()[0] == c]
    line = mine[-1].strip(); log("whole", line)
    if "rc=10" in line: log("SAT whole case!", c)
    if "cake=[s VERIFIED UNSAT]" in line:
        os.makedirs(out, exist_ok=True)
        kv = dict(x.split("=", 1) for x in line.split()[1:4])
        with open(f"{out}/leaves.jsonl", "w") as g:
            g.write(json.dumps({"case": c, "case_sha256": h}) + "\n")
            g.write(json.dumps({"cube": [], "status": "UNSAT", "method": "whole", "cake_lpr": "s VERIFIED UNSAT",
                                "solve_s": float(kv["solve"]), "check_s": float(kv["check"])}) + "\n")
        open(f"{out}/leaves.icnf.tmp", "w").write("a 0\n"); os.replace(f"{out}/leaves.icnf.tmp", f"{out}/leaves.icnf")
        open(f"{out}/open.icnf", "w").close()
        push(f"S5: {c} closed (whole)"); continue
    hours = (END - time.time()) / 3600
    if hours < 0.2: log("not reached (time)", c); continue
    log("driver", c, round(hours, 2))
    r = subprocess.run(["python3", f"{REPO}/{S5}/close_march.py", f, out, "--name", c, "--depth", "7", "--timeout", "300",
                        "--split-depth", "6", "--jobs", "4", "--hours", str(hours)],
                       env={**os.environ, "BIN": "/opt/work/bin", "WORK": "/opt/work/tmp"}, capture_output=True, text=True)
    log("driver done", c, r.returncode, r.stdout[-200:], r.stderr[-500:])
    push(f"S5: {c} " + r.stdout.strip()[-40:])
log("RUNNER DONE"); push("S5: runner done")
