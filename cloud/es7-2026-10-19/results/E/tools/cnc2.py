#!/usr/bin/env python3
"""cnc2: cube-and-conquer driver with a global shallowest-first queue and exact weights.

Fixes the two scheduler bugs of tools/cnc/cnc.py (newest-first popping with per-worker
queues; float progress weights):
  * one global priority queue ordered by (depth, budget, sequence number): the shallowest open
    cube is always handed out first, FIFO within a depth;
  * weights are exact: a cube of depth d has weight 2^-d; the driver keeps integer counters of
    closed and open cubes per depth and reports the closed weight as an exact fraction
    (numerator / 2^maxdepth) and as a decimal string; the invariant
    closed + open + running = 1 is checked exactly at every log line.
Cubes are binary splits on orientation variables chosen by ccworker's restricted look-ahead:
a cube that exhausts its conflict budget is replaced by cube+[-l] and cube+[l].  Budgets grow:
child budget = parent budget * GROW (capped), and a cube that cannot be split is retried with
budget * GROW.  Every closed cube is recorded (literal list, solve time) in closed.jsonl so
the tree can be re-checked (coverage) and closed cubes can be re-proved with LRAT.
UNSAT answers are solver claims; see lratcube.sh for proofs of individual cubes.

usage: cnc2.py CNF NX OUTDIR NWORKERS [--base 20000] [--grow 1.25] [--cap 5000000]
               [--maxcand 400] [--log-every 1800] [--hours H]
State: OUTDIR/state.json (open cubes, counters; resumable), OUTDIR/closed.jsonl,
OUTDIR/progress.log (JSON line per log interval), OUTDIR/events.log.
"""
import argparse
import heapq
import json
import os
import subprocess
import sys
import threading
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("cnf")
ap.add_argument("nx", type=int)
ap.add_argument("outdir")
ap.add_argument("nworkers", type=int)
ap.add_argument("--worker", default=str(Path(__file__).with_name("ccworker")))
ap.add_argument("--base", type=int, default=20000)
ap.add_argument("--grow", type=float, default=1.25)
ap.add_argument("--cap", type=int, default=5_000_000)
ap.add_argument("--maxcand", type=int, default=400)
ap.add_argument("--log-every", type=int, default=1800)
ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--solver-opt", action="append", default=[], help="CaDiCaL option for the workers, e.g. --solver-opt=--elim=0")
args = ap.parse_args()

out = Path(args.outdir)
out.mkdir(parents=True, exist_ok=True)
state_path = out / "state.json"
lock = threading.Lock()
stop = threading.Event()
seq = [0]
heap = []          # (depth, budget, seq, cube)
running = {}       # seq -> (cube, budget)
closed_by_depth = Counter()
st = {"cnf": os.path.abspath(args.cnf), "nx": args.nx, "jobs": 0, "splits": 0, "retries": 0,
      "closed": 0, "sat": None, "started": time.time(), "elapsed_before": 0.0,
      "solve_ms_total": 0, "split_lits": Counter()}

if state_path.exists():
    old = json.loads(state_path.read_text())
    for k in ("jobs", "splits", "retries", "closed", "sat", "solve_ms_total"):
        st[k] = old[k]
    st["elapsed_before"] = old["elapsed_before"] + old.get("elapsed_this_run", 0.0)
    closed_by_depth.update({int(k): v for k, v in old["closed_by_depth"].items()})
    st["split_lits"] = Counter({int(k): v for k, v in old.get("split_lits", {}).items()})
    for cube, budget in old["open"]:
        heapq.heappush(heap, (len(cube), budget, seq[0], cube)); seq[0] += 1
else:
    heapq.heappush(heap, (0, args.base, seq[0], [])); seq[0] += 1

closed_f = open(out / "closed.jsonl", "a")
events = open(out / "events.log", "a")
progress = open(out / "progress.log", "a")
t_start = time.time()
procs = []


def ev(obj):
    obj["t"] = round(time.time() - t_start + st["elapsed_before"], 1)
    events.write(json.dumps(obj) + "\n"); events.flush()


def weights():
    """exact closed weight and open weight (open includes running cubes)"""
    opens = [len(c) for (_, _, _, c) in heap] + [len(c) for c, _ in running.values()]
    D = max([0] + list(closed_by_depth) + opens)
    num_closed = sum(cnt << (D - d) for d, cnt in closed_by_depth.items())
    num_open = sum(1 << (D - d) for d in opens)
    return Fraction(num_closed, 1 << D), Fraction(num_open, 1 << D), num_closed + num_open == (1 << D)


def save():
    tmp = state_path.with_suffix(".tmp")
    data = dict(st)
    data["split_lits"] = {str(k): v for k, v in st["split_lits"].items()}
    data["closed_by_depth"] = {str(k): v for k, v in closed_by_depth.items()}
    # running cubes go back to the open list on resume
    data["open"] = [[c, b] for (_, b, _, c) in heap] + [[c, b] for c, b in running.values()]
    data["elapsed_this_run"] = time.time() - t_start
    tmp.write_text(json.dumps(data)); tmp.replace(state_path)


def fmt_frac(fr, digits=30):
    # exact decimal expansion to `digits` places (truncated)
    n, d = fr.numerator, fr.denominator
    ip = n // d
    r = n % d
    s = []
    for _ in range(digits):
        r *= 10
        s.append(str(r // d)); r %= d
    return f"{ip}." + "".join(s)


def log_progress(tag="periodic"):
    cw, ow, ok = weights()
    depths = Counter(len(c) for (_, _, _, c) in heap)
    depths.update(len(c) for c, _ in running.values())
    rec = {"tag": tag, "t": round(time.time() - t_start + st["elapsed_before"], 1),
           "open": len(heap) + len(running), "running": len(running), "closed": st["closed"],
           "jobs": st["jobs"], "splits": st["splits"], "retries": st["retries"],
           "closed_weight_exact": f"{cw.numerator}/{cw.denominator}",
           "closed_weight_dec": fmt_frac(cw), "open_weight_dec": fmt_frac(ow),
           "weights_sum_to_one": ok,
           "open_depth_hist": {str(k): depths[k] for k in sorted(depths)},
           "closed_depth_hist": {str(k): closed_by_depth[k] for k in sorted(closed_by_depth)},
           "min_open_depth": min(depths) if depths else None, "max_open_depth": max(depths) if depths else None,
           "solve_hours_total": round(st["solve_ms_total"] / 3.6e6, 3), "sat": bool(st["sat"])}
    progress.write(json.dumps(rec) + "\n"); progress.flush()
    return rec


def worker(w):
    wdir = out / "models"
    wdir.mkdir(exist_ok=True)
    p = subprocess.Popen([args.worker, args.cnf, str(args.nx), str(wdir), str(args.maxcand)] + args.solver_opt,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    procs.append(p)
    line = p.stdout.readline()
    if not line.startswith("READY"):
        ev({"event": "worker_failed", "w": w, "line": line}); return
    ev({"event": "worker_ready", "w": w})
    while not stop.is_set():
        with lock:
            if not heap:
                item = None
            else:
                item = heapq.heappop(heap)
                running[item[2]] = (item[3], item[1])
        if item is None:
            with lock:
                if not running:
                    break
            time.sleep(0.5); continue
        depth, budget, sid, cube = item
        t0 = time.time()
        p.stdin.write(f"{sid} {budget} {' '.join(map(str, cube))} 0\n"); p.stdin.flush()
        r = p.stdout.readline().split()
        if not r:
            ev({"event": "worker_died", "w": w, "cube": cube})
            with lock:
                del running[sid]
                heapq.heappush(heap, (depth, budget, sid, cube))
            return
        wall = time.time() - t0
        with lock:
            del running[sid]
            st["jobs"] += 1
            st["solve_ms_total"] += int(r[2])
            if r[0] == "U":
                st["closed"] += 1
                closed_by_depth[depth] += 1
                closed_f.write(json.dumps({"cube": cube, "budget": budget, "solve_ms": int(r[2]), "wall": round(wall, 2)}) + "\n")
                closed_f.flush()
            elif r[0] == "S":
                st["sat"] = {"cube": cube, "model": f"models/model-{sid}.txt"}
                ev({"event": "SAT", "cube": cube, "model": f"models/model-{sid}.txt"})
                stop.set()
            else:
                lit = int(r[3])
                if lit == 0:
                    st["retries"] += 1
                    nb = min(args.cap, int(budget * args.grow))
                    heapq.heappush(heap, (depth, nb, seq[0], cube)); seq[0] += 1
                    ev({"event": "retry", "cube_depth": depth, "budget": nb})
                else:
                    st["splits"] += 1
                    st["split_lits"][abs(lit)] += 1
                    nb = min(args.cap, int(budget * args.grow))
                    for l in (-lit, lit):
                        heapq.heappush(heap, (depth + 1, nb, seq[0], cube + [l])); seq[0] += 1
    p.stdin.close()
    p.kill()


threads = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(args.nworkers)]
for t in threads:
    t.start()
ev({"event": "start", "solver_opts": args.solver_opt, "nworkers": args.nworkers, "base": args.base, "grow": args.grow, "cap": args.cap,
    "maxcand": args.maxcand, "open": len(heap)})
last_log = time.time()
last_save = time.time()
log_progress("start")
deadline = t_start + args.hours * 3600
while any(t.is_alive() for t in threads):
    time.sleep(2)
    now = time.time()
    if now > deadline and not stop.is_set():
        ev({"event": "deadline"}); stop.set()
    with lock:
        if now - last_save > 60:
            save(); last_save = now
        if now - last_log > args.log_every:
            log_progress(); last_log = now
    if os.path.exists(out / "STOP") and not stop.is_set():
        ev({"event": "stop_file"}); stop.set()
    if stop.is_set():
        for p in procs:
            try:
                p.kill()
            except Exception:
                pass
# kill workers still busy: their running cubes go back to the open queue (worker_died path)
for p in procs:
    try:
        p.kill()
    except Exception:
        pass
for t in threads:
    t.join(timeout=5)
with lock:
    save()
    rec = log_progress("final")
print(json.dumps(rec))
