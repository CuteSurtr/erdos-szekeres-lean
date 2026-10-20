#!/usr/bin/env python3
"""cnc2: adaptive cube-and-conquer with persistent CaDiCaL workers (cncw).

Fixes the two scheduler bugs of tools/cnc/cnc.py noted in plan/es7_critique.md:
 * one global queue, shallowest cube first (ties: oldest first), no newest-first popping;
 * exact progress weights: closed weight is a Fraction sum of 2^-len(cube).
Splits are on orientation-orbit representatives only (cncw's restricted lookahead).

Every cube is closed (UNSAT claim), satisfiable (stop), or open; the open cubes always cover
exactly the not-yet-refuted part of the space, so closed_weight + sum(open weights) == 1.
UNSAT answers are solver claims; closed cubes are listed in closed.txt for LRAT spot checks.

usage: cnc2.py cnf cands outdir nworkers [--base 20000] [--grow 1.5] [--maxcand 0] [--hours H]
"""
import argparse, heapq, json, os, subprocess, sys, threading, time
from fractions import Fraction
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("cands"); ap.add_argument("outdir"); ap.add_argument("nworkers", type=int)
ap.add_argument("--base", type=int, default=20000); ap.add_argument("--grow", type=float, default=1.5)
ap.add_argument("--maxcand", type=int, default=0); ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--log-every", type=float, default=1800.0)
ap.add_argument("--worker", required=True, help="path to the cncw binary")
ap.add_argument("--resume", action="store_true", help="continue from outdir/state.json")
ap.add_argument("--reset-limits", action="store_true", help="on resume, give every open cube the --base limit")
a = ap.parse_args()
out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
worker_bin = a.worker
lock = threading.Lock(); stop = threading.Event()
heap = []; open_set = {}; nid = [0]
st = {"cnf": a.cnf, "closed": 0, "closed_weight": Fraction(0), "splits": 0, "failed_lit_splits": 0, "sat": None,
      "jobs": 0, "started": time.time(), "busy": 0}
closed_by_depth = {}
closed_f = open(out / "closed.txt", "a")
def push(cube, limit):
    i = nid[0]; nid[0] += 1; open_set[i] = (cube, limit)
    heapq.heappush(heap, (len(cube), i))
log = open(out / "cnc.log", "a")
if a.resume and (out / "state.json").exists():
    # Resume from the last checkpoint: its open cubes (including cubes that were in flight) plus
    # its closed weight.  Work done after the checkpoint is redone, so closed.txt may list a
    # cube twice; the weights stay exact.  --reset-limits gives every open cube the new base.
    old = json.loads((out / "state.json").read_text())
    for k in ("closed", "splits", "failed_lit_splits", "jobs", "started"):
        st[k] = old[k]
    st["closed_weight"] = Fraction(old["closed_weight"])
    lat = json.loads((out / "latest.json").read_text())
    closed_by_depth.update({int(k): v for k, v in lat.get("closed_by_depth", {}).items()})
    for c, l in old["open"]:
        push(c, a.base if a.reset_limits else l)
    log.write(json.dumps({"event": "resume", "wall": time.strftime("%H:%M:%S"), "open": len(open_set),
                          "base": a.base, "grow": a.grow, "nworkers": a.nworkers, "reset_limits": a.reset_limits}) + "\n")
    log.flush()
else:
    push([], a.base)
def snapshot(event="progress", to_log=True):
    depths = [len(c) for c, _ in open_set.values()]
    hist = {}
    for d in depths: hist[d] = hist.get(d, 0) + 1
    ow = sum((Fraction(1, 2 ** d) for d in depths), Fraction(0))
    cw = st["closed_weight"]
    assert cw + ow == 1, "weight invariant broken"
    rec = {"event": event, "t": round(time.time() - st["started"]), "wall": time.strftime("%H:%M:%S"),
           "open": len(open_set), "open_min_depth": min(depths, default=0), "open_max_depth": max(depths, default=0),
           "open_depth_hist": dict(sorted(hist.items())), "closed": st["closed"],
           "closed_weight": str(cw), "closed_weight_float": float(cw), "splits": st["splits"],
           "failed_lit_splits": st["failed_lit_splits"], "jobs": st["jobs"],
           "closed_by_depth": dict(sorted(closed_by_depth.items())), "sat": st["sat"]}
    if to_log:
        log.write(json.dumps(rec) + "\n"); log.flush()
    (out / "latest.json").write_text(json.dumps(rec))
    tmp = out / "state.tmp"
    tmp.write_text(json.dumps({"open": [[c, l] for c, l in open_set.values()], **{k: (str(v) if isinstance(v, Fraction) else v) for k, v in st.items()}}))
    tmp.replace(out / "state.json")
    return rec
def worker(w):
    p = subprocess.Popen([worker_bin, a.cnf, a.cands, str(out)] + ([str(a.maxcand)] if a.maxcand else []),
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    assert p.stdout.readline().startswith("READY")
    while not stop.is_set():
        with lock:
            if heap:
                _, i = heapq.heappop(heap); cube, limit = open_set[i]; st["busy"] += 1
            else:
                i = None
                if st["busy"] == 0: break
        if i is None:
            time.sleep(0.5); continue
        t0 = time.time()
        p.stdin.write(f"{i} {limit} {' '.join(map(str, cube))} 0\n"); p.stdin.flush()
        r = p.stdout.readline().split()
        dt = time.time() - t0
        if not r:  # worker died: put the cube back and end this thread
            with lock:
                st["busy"] -= 1; heapq.heappush(heap, (len(cube), i))
            break
        with lock:
            st["jobs"] += 1; st["busy"] -= 1
            del open_set[i]
            if r[0] == "U":
                st["closed"] += 1; st["closed_weight"] += Fraction(1, 2 ** len(cube))
                closed_by_depth[len(cube)] = closed_by_depth.get(len(cube), 0) + 1
                closed_f.write(f"{round(dt, 2)} {' '.join(map(str, cube))} 0\n"); closed_f.flush()
            elif r[0] == "S":
                st["sat"] = {"cube": cube, "model": f"model-{i}.txt"}
                open_set[i] = (cube, limit)  # keep it listed; the run stops here
                snapshot("SAT"); stop.set()
            else:
                lit, np_, nn_ = int(r[2]), int(r[3]), int(r[4])
                nl = int(limit * a.grow)
                if len(r) > 5:
                    # protocol 2: failed literals chained by the worker.  Each one is a binary
                    # node whose child cube+[f] is refuted by unit propagation (logged with dt -1).
                    nf = int(r[5]); fl = [int(x) for x in r[6:6 + nf]]
                    c = list(cube)
                    for f in fl:
                        cc = c + [f]
                        st["closed"] += 1; st["closed_weight"] += Fraction(1, 2 ** len(cc))
                        closed_by_depth[len(cc)] = closed_by_depth.get(len(cc), 0) + 1
                        closed_f.write(f"-1 {' '.join(map(str, cc))} 0\n")
                        st["splits"] += 1; st["failed_lit_splits"] += 1
                        c = c + [-f]
                    closed_f.flush()
                    if lit == 0 and np_ == -2:
                        st["closed"] += 1; st["closed_weight"] += Fraction(1, 2 ** len(c))
                        closed_by_depth[len(c)] = closed_by_depth.get(len(c), 0) + 1
                        closed_f.write(f"-1 {' '.join(map(str, c))} 0\n"); closed_f.flush()
                    elif lit == 0:
                        push(c, nl)
                    else:
                        st["splits"] += 1
                        push(c + [lit], nl); push(c + [-lit], nl)
                elif lit == 0:
                    push(cube, nl)
                else:
                    st["splits"] += 1
                    if np_ < 0 or nn_ < 0: st["failed_lit_splits"] += 1
                    push(cube + [lit], nl); push(cube + [-lit], nl)
    p.kill()
threads = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(a.nworkers)]
for t in threads: t.start()
with lock: snapshot("start")
last_log = time.time(); last_ckpt = time.time()
deadline = time.time() + a.hours * 3600
while any(t.is_alive() for t in threads):
    time.sleep(2)
    now = time.time()
    if now > deadline: stop.set()
    if now - last_ckpt > 60 or now - last_log > a.log_every:
        with lock:
            snapshot("progress", to_log=(now - last_log > a.log_every))
        if now - last_log > a.log_every: last_log = now
        last_ckpt = now
with lock: rec = snapshot("end")
print(json.dumps(rec))
