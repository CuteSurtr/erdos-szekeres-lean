#!/usr/bin/env python3
"""C3W3S S0 driver: roots of /opt/work/roots.tsv in order, in batches of 3; per root: skip check (after git pull),
direct close_node.py (cap 300, the 3 roots of a batch in parallel), then sigma_cubes.py K=3 (cap 300, 3 jobs), then
refine.py (level 2, 3 at a time). Commits progress every 25 min. Stops on SAT or an unconfirmed proof rejection."""
import glob, json, os, signal, subprocess, sys, threading, time
REPO = "/home/user/erdos-szekeres-lean"
RES = REPO + "/cloud/es7-2026-10-19/results"
MY = RES + "/C3W3S/S0"
T = "/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools"
W = "/opt/work"
BASE = W + "/base.cnf"
OD, OS, RC = W + "/out_direct.jsonl", W + "/out_sigma.jsonl", W + "/recheck.jsonl"
LOG, SKIP = W + "/driver.log", W + "/skips.log"
START = int(open("/tmp/claude-0/start").read())
END = START + 4 * 3600 - 15 * 60
os.environ["PATH"] = "/opt/bin:" + os.environ["PATH"]
gitlock = threading.Lock()
stop = threading.Event()


def log(m):
    with open(LOG, "a") as f:
        f.write(time.strftime("%H:%M:%S", time.gmtime()) + " " + m + "\n")


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True)


def commit(msg):
    with gitlock:
        for src, dst in [(OD, "out_direct.jsonl"), (OS, "out_sigma.jsonl"), (RC, "recheck.jsonl"), (SKIP, "skips.log")]:
            if os.path.exists(src):
                subprocess.run(["cp", src, MY + "/" + dst])
        subprocess.run(f"tail -n 200 {LOG} > {MY}/driver.log.tail", shell=True)
        subprocess.run(["cp", W + "/drv/driver.py", W + "/drv/refine.py", MY + "/"])
        git("add", MY)
        git("commit", "-q", "-m", msg)
        for i in range(10):
            git("pull", "-q", "--rebase", "--autostash", "origin", "es7-cloud")
            if git("push", "-q", "origin", "HEAD:es7-cloud").returncode == 0:
                log("pushed: " + msg); return True
            time.sleep(2 * (i + 1))
        r = git("push", "-q", "origin", "HEAD:es7-fallback-c3w3s-s0")
        log("PUSH FAILED 10x; fallback push rc=%d" % r.returncode)


def committer():
    while not stop.wait(20 * 60):
        commit("C3W3S S0: progress")


def reached(R):
    with gitlock:
        git("pull", "-q", "--rebase", "--autostash", "origin", "es7-cloud")
    for f in glob.glob(RES + "/C3W3/C*/out.jsonl"):
        for l in open(f):
            try: n = json.loads(l).get("node", "")
            except Exception: continue
            if n == R or n.startswith(R + "_"):
                return f"record {n} in {f[len(RES)+1:]}"
    for f in glob.glob(RES + "/C3W3/C*/driver*.log*"):
        st = en = 0
        for l in open(f, errors="replace"):
            if l.startswith(f"=== ROOT {R} start"): st += 1
            if l.startswith(f"=== ROOT {R} end"): en += 1
        if st > en:
            return f"started without end in {f[len(RES)+1:]}"
    return None


def run_procs(cmds, tag):
    """run commands (each its own process group) from TOOLS, wait; kill all at END. returns True if killed."""
    ps = [subprocess.Popen(c, cwd=T, stdout=open(LOG, "a"), stderr=subprocess.STDOUT, start_new_session=True) for c in cmds]
    killed = False
    while any(p.poll() is None for p in ps):
        if time.time() >= END:
            for p in ps:
                try: os.killpg(p.pid, signal.SIGKILL)
                except Exception: pass
            subprocess.run("pkill -KILL cadical; pkill -KILL cake_lpr; pkill -KILL lrat-check", shell=True)
            killed = True; log(f"KILLED at END during {tag}"); break
        if sat_seen():
            break
        time.sleep(5)
    for p in ps: p.wait()
    return killed


def recs(path):
    if not os.path.exists(path): return []
    return [json.loads(l) for l in open(path) if l.strip()]


def sat_seen():
    return any(r.get("status") == "SATISFIABLE" for p in (OD, OS, RC) for r in recs(p))


def handle_rejects(seen):
    """re-check, alone, every UNSAT record not certified; returns False to stop."""
    for path in (OD, OS):
        for r in recs(path):
            if r.get("status") == "UNSATISFIABLE" and not r.get("certified"):
                key = (r["node"], json.dumps(r.get("cube")))
                if key in seen: continue
                seen.add(key)
                log(f"PROOF NOT ACCEPTED {key} lrat={r.get('lrat_check')} cake={r.get('cake_lpr')}; rechecking alone")
                if "cube" in r:
                    bits = [int(k) for k in r["cube"]]; vals = [r["cube"][k] for k in r["cube"]]
                    code = (f"import sys,json,os;sys.path.insert(0,os.getcwd());import sigma_cubes as s;os.makedirs(s.WORK,exist_ok=True);"
                            f"r=s.run(({BASE!r},{r['node']!r},{bits},{vals},300));open({RC!r},'a').write(json.dumps(r)+'\\n')")
                    run_procs([["python3", "-c", code]], "recheck")
                else:
                    run_procs([["python3", "close_node.py", BASE, RC, "300", r["node"]]], "recheck")
                rr = recs(RC)[-1] if recs(RC) else {}
                if rr.get("cnf_sha256") == r.get("cnf_sha256") and rr.get("certified"):
                    log(f"recheck OK {key}: {rr.get('lrat_check')} / {rr.get('cake_lpr')}")
                else:
                    log(f"RECHECK FAILED {key}: {rr}"); return False
    return True


def cert_direct(R):
    return any(r["node"] == R and r.get("certified") for r in recs(OD) + recs(RC) if "cube" not in r)


def cert_cube(R, cube):
    return any(r["node"] == R and r.get("cube") == cube and r.get("certified") for r in recs(OS) + recs(RC))


def main():
    roots = [l.split("\t")[1] for l in open(W + "/roots.tsv").read().splitlines()[1:]]
    th = threading.Thread(target=committer, daemon=True); th.start()
    seen = set(); i = 0
    from itertools import product
    while i < len(roots) and time.time() < END - 120:
        batch = []
        while len(batch) < 3 and i < len(roots):
            R = roots[i]; i += 1
            why = reached(R)
            if why:
                log(f"SKIP {R}: {why}")
                open(SKIP, "a").write(f"{time.strftime('%FT%TZ', time.gmtime())}\t{R}\t{why}\n")
            else:
                batch.append(R)
        if not batch: continue
        for R in batch: log(f"=== ROOT {R} start direct")
        run_procs([["python3", "close_node.py", BASE, OD, "300", R] for R in batch], "direct " + " ".join(batch))
        if sat_seen(): log("SAT FOUND"); break
        if not handle_rejects(seen): break
        for R in batch:
            if cert_direct(R):
                log(f"=== ROOT {R} end closed directly"); continue
            if time.time() >= END: break
            log(f"=== ROOT {R} sigma level 1")
            run_procs([["python3", "sigma_cubes.py", BASE, OS, R, "3", "300", "3"]], "sigma1 " + R)
            if sat_seen(): log("SAT FOUND"); stop.set(); return
            if not handle_rejects(seen): stop.set(); return
            used = {int(x.split("s")[0]) for L in R.split("_") for x in L.split("-")}
            free = [r for r in range(1, 11) if r not in used]
            b3 = free[:3]
            open1 = ["".join(map(str, v)) for v in product((0, 1), repeat=3) if not cert_cube(R, dict(zip(map(str, b3), v)))]
            if not open1:
                log(f"=== ROOT {R} end closed at sigma level 1"); continue
            if time.time() >= END: break
            log(f"=== ROOT {R} sigma level 2 on open cubes {open1}")
            run_procs([["python3", W + "/drv/refine.py", BASE, OS, R] + open1], "sigma2 " + R)
            if sat_seen(): log("SAT FOUND"); stop.set(); return
            if not handle_rejects(seen): stop.set(); return
            b6 = free[:6]
            open2 = ["".join(map(str, v)) for v in product((0, 1), repeat=6) if "".join(map(str, v[:3])) in open1
                     and not cert_cube(R, dict(zip(map(str, b6), v)))]
            log(f"=== ROOT {R} end " + ("closed at sigma level 2" if not open2 else f"open level-2 cubes ({''.join(map(str,b6))}): {open2}"))
    stop.set()
    log("=== DRIVER DONE")
    commit("C3W3S S0: driver done")


if __name__ == "__main__":
    main()
