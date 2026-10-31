#!/usr/bin/env python3
"""C3W3S S4 driver: keeps 3 solver processes busy over the roots of /opt/work/roots.tsv, in order.
Per root R: (a) close_node.py BASE out 300 R (direct, cap 300); if not certified,
(b) the 8 sigma cubes on the 3 smallest free residues (sigma_cubes.run, cap 300, same records as sigma_cubes.py BASE OUT R 3 300 3);
(c) for every open level-1 cube, the 8 cubes on the 6 smallest free residues extending it (sigma_cubes.run, cap 300);
(d) whatever stays open is recorded.  Before starting R: fetch origin/es7-cloud and skip R if a C3W3 C machine reached it.
sigma_cubes and close_node are used unmodified."""
import concurrent.futures as cf
import itertools
import json
import os
import subprocess
import sys
import time

TOOLS = "/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools"
os.chdir(TOOLS)
os.environ["PATH"] = "/opt/bin:" + os.environ["PATH"]
sys.path.insert(0, TOOLS)
import sigma_cubes  # noqa: E402
from hullcase import parse_layers  # noqa: E402

W = "/opt/work"
BASE = W + "/base.cnf"
OUT_D, OUT_S, RECHK, SKIP, LOG = (W + "/out_direct.jsonl", W + "/out_sigma.jsonl", W + "/recheck.jsonl",
                                  W + "/skip.log", W + "/driver.log")
REPO = "/home/user/erdos-szekeres-lean"
C3W3 = "cloud/es7-2026-10-19/results/C3W3"
END = int(open(W + "/END").read())
LAST_START = END - 8 * 60
CAP = 300


def log(s):
    with open(LOG, "a") as f:
        f.write(time.strftime("%H:%M:%S ", time.gmtime()) + s + "\n")


def append(path, rec):
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True)


def reached(R):
    for i in range(6):
        if git("fetch", "-q", "origin", "es7-cloud").returncode == 0:
            break
        time.sleep(5 * (i + 1))
    else:
        log(f"WARN fetch failed before {R}; using the last fetched origin/es7-cloud")
    ref = "origin/es7-cloud"
    r = git("grep", "-l", "-F", "-e", f'"node": "{R}"', "-e", f'"node": "{R}_', ref, "--", f"{C3W3}/C*/out.jsonl")
    if r.stdout.strip():
        return "record in " + ", ".join(x.split(":", 1)[1] for x in r.stdout.split())
    r = git("grep", "-c", "-F", f"=== ROOT {R} start", ref, "--", f"{C3W3}/C*/driver*.log*")
    for line in r.stdout.split():
        f = line.split(":")[1]
        ends = git("grep", "-c", "-F", f"=== ROOT {R} end", ref, "--", f).stdout.split()
        e = int(ends[0].rsplit(":", 1)[1]) if ends else 0
        if int(line.rsplit(":", 1)[1]) > e:
            return f"start without end in {f}"
    return None


def direct(R):
    tmp = f"{W}/direct_{R}.jsonl"
    if os.path.exists(tmp):
        os.remove(tmp)
    subprocess.run([sys.executable, "close_node.py", BASE, tmp, str(CAP), R], capture_output=True, text=True)
    recs = [json.loads(l) for l in open(tmp)] if os.path.exists(tmp) else []
    os.remove(tmp) if os.path.exists(tmp) else None
    return recs[-1] if recs else {"node": R, "status": "NO_RECORD"}


def cube(R, bits, vals):
    return sigma_cubes.run((BASE, R, list(bits), list(vals), CAP))


def free(R):
    used = {r for L in parse_layers(R) for r, _ in L}
    return [r for r in range(1, 11) if r not in used]


def main():
    roots = [l.split("\t")[2] for l in open(W + "/roots.tsv").read().splitlines()[1:]]
    os.makedirs(sigma_cubes.WORK, exist_ok=True)
    state = {}  # R -> dict
    pending = []  # (rootidx, level, order, kind, args)
    nxt = 0
    running = {}
    stop = None
    ex = cf.ProcessPoolExecutor(3)
    seq = itertools.count()

    def activate():
        nonlocal nxt
        while nxt < len(roots):
            R = roots[nxt]; i = nxt; nxt += 1
            why = reached(R)
            if why:
                log(f"=== ROOT {R} skipped: {why}")
                with open(SKIP, "a") as f:
                    f.write(f"{time.strftime('%H:%M:%SZ', time.gmtime())}\t{R}\tskipped\t{why}\n")
                state[R] = {"result": "skipped", "why": why}
                continue
            log(f"=== ROOT {R} start")
            state[R] = {"i": i, "t0": time.time(), "result": None, "open1": [], "open2": [], "todo": 1}
            pending.append((i, 0, next(seq), "direct", (R,)))
            return True
        return False

    def finish(R, result):
        s = state[R]
        s["result"] = result
        log(f"=== ROOT {R} end {result} open1={len(s['open1'])} open2={len(s['open2'])} wall={time.time() - s['t0']:.0f}s")

    def is_rejection(rec):
        return rec.get("status") == "UNSATISFIABLE" and not rec.get("certified")

    while True:
        now = time.time()
        if stop is None and now < LAST_START:
            while len(running) < 3:
                if not pending and not activate():
                    break
                if not pending:
                    continue
                pending.sort()
                t = pending.pop(0)
                fn = direct if t[3] == "direct" else cube
                running[ex.submit(fn, *t[4])] = t
        if not running:
            break
        done, _ = cf.wait(list(running), timeout=10, return_when=cf.FIRST_COMPLETED)
        if time.time() >= END and running:
            log("END reached: killing running solvers/checkers")
            subprocess.run(["pkill", "-KILL", "-f", "cadical|lrat-check|cake_lpr"])
            done, _ = cf.wait(list(running), timeout=60)
        for fu in done:
            t = running.pop(fu)
            R = t[4][0]
            s = state[R]
            try:
                rec = fu.result()
            except Exception as e:  # noqa: BLE001
                rec = {"node": R, "status": "ERROR", "error": repr(e)}
            killed = time.time() >= END - 5
            if t[3] == "direct":
                append(OUT_D, rec)
            else:
                append(OUT_S, rec)
            short = {k: rec.get(k) for k in ("node", "cube", "status", "solve_s", "check_s", "certified", "lrat_check", "cake_lpr")}
            log(f"{t[3]} {json.dumps(short)}")
            if stop:
                continue
            if rec.get("status") == "SATISFIABLE":
                stop = "SAT"
                log(f"SAT FOUND {t[3]} {json.dumps(t[4])}")
                with open(W + "/SAT_TASK.json", "w") as f:
                    json.dump({"kind": t[3], "args": t[4]}, f)
                subprocess.run(["pkill", "-KILL", "-f", "cadical|lrat-check|cake_lpr"])
                continue
            if is_rejection(rec) and not killed:
                log(f"PROOF NOT ACCEPTED {t[3]} {json.dumps(t[4])}: re-checking alone")
                r2 = direct(R) if t[3] == "direct" else cube(*t[4])
                append(RECHK, dict(r2, recheck_of=t[3]))
                log(f"recheck {json.dumps({k: r2.get(k) for k in ('node', 'cube', 'status', 'certified', 'lrat_check', 'cake_lpr')})}")
                if r2.get("status") == "SATISFIABLE":
                    stop = "SAT"; log("SAT FOUND (recheck)"); continue
                if not r2.get("certified"):
                    stop = "REJECT"; log("STOP: proof rejected again"); continue
                rec = r2
            ok = bool(rec.get("certified"))
            s["todo"] -= 1
            if t[3] == "direct":
                if ok:
                    finish(R, "closed directly")
                else:
                    fr = free(R)
                    s["bits1"] = fr[:3]; s["bits2"] = fr[:6]
                    for v in itertools.product((0, 1), repeat=3):
                        pending.append((s["i"], 1, next(seq), "cube", (R, tuple(fr[:3]), v)))
                    s["todo"] += 8
            elif len(t[4][1]) == 3:
                if not ok:
                    s["open1"].append(t[4][2])
                    for v in itertools.product((0, 1), repeat=3):
                        pending.append((s["i"], 2, next(seq), "cube", (R, tuple(s["bits2"]), tuple(t[4][2]) + v)))
                    s["todo"] += 8
            else:
                if not ok:
                    s["open2"].append(t[4][2])
            if s["todo"] == 0 and s["result"] is None:
                if t[3] != "direct":
                    finish(R, "closed at sigma level 1" if not s["open1"] else
                           ("closed at sigma level 2" if not s["open2"] else "open"))
        if stop and not running:
            break
    ex.shutdown(wait=True, cancel_futures=True)
    for R, s in state.items():
        if s.get("result") is None:
            log(f"=== ROOT {R} unfinished at END: open1={s['open1']} open2={s['open2']} todo={s['todo']}")
    json.dump(state, open(W + "/state.json", "w"), default=list, indent=1)
    log(f"=== DRIVER DONE stop={stop} next_root_index={nxt}")


if __name__ == "__main__":
    main()
