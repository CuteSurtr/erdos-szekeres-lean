#!/usr/bin/env python3
"""Simple cube-and-conquer with a shallowest-first global queue and exact progress weights.

Fixes the known bugs of tools/cnc/cnc.py: one global priority queue ordered by (depth, FIFO)
instead of newest-first per-worker deques, and exact rational weights (fractions.Fraction)
instead of floats.

* The root cube is empty. A cube that exhausts its conflict budget is split by the worker
  (cncw) on an ORIENTATION variable v into cube+[v] and cube+[-v], each with budget
  limit*GROW. Weight of a cube at depth d = 2^-d exactly. Open and closed cubes always
  partition the search space, so closed_weight + open_weight = 1 exactly (checked each log).
* Every finished job is appended to events.jsonl (id, parent cube, result, split literal), so
  the cube tree can be re-verified offline (cover.py).
* LRAT lane (optional): a sample of closed cubes is re-solved from scratch as CNF + unit
  clauses with `cadical --lrat` and checked with drat-trim's lrat-check; the same cube is
  also re-solved on a second CNF (Baek-Balko encoding) to cross-check UNSAT.
* Logs: progress.jsonl every 60 s, report30.jsonl every 30 min (open count, depth
  histogram of open cubes, exact closed weight).
UNSAT answers of the workers carry no proof; only LRAT-checked cubes are proof-checked.

usage: cnc2.py --cnf F --nx NX --out DIR [--workers W] [--base B] [--grow G]
               [--lrat-cnf F2 --xcheck-cnf F3 --lrat-rate R --cadical BIN --lratcheck BIN]
               [--deadline EPOCH] [--sigcheck BIN --params N,a,u,k]
"""
import argparse, heapq, json, os, random, subprocess, threading, time
from fractions import Fraction
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--cnf", required=True); ap.add_argument("--nx", type=int, required=True)
ap.add_argument("--out", required=True); ap.add_argument("--workers", type=int, default=4)
ap.add_argument("--base", type=int, default=10000); ap.add_argument("--grow", type=float, default=1.25)
ap.add_argument("--worker-bin", required=True)
ap.add_argument("--lrat-cnf", default=None, help="CNF re-solved with LRAT (normally = --cnf)")
ap.add_argument("--xcheck-cnf", default=None, help="second encoding for cube-level UNSAT cross-check")
ap.add_argument("--lrat-rate", type=float, default=0.0, help="probability a closed cube is sampled")
ap.add_argument("--lrat-timeout", type=int, default=900)
ap.add_argument("--cadical", default=None); ap.add_argument("--lratcheck", default=None)
ap.add_argument("--deadline", type=float, default=None, help="unix time at which to stop dispatching")
ap.add_argument("--sigcheck", default=None); ap.add_argument("--params", default=None, help="N,a,u,k for sigcheck")
ap.add_argument("--seed", type=int, default=1)
args = ap.parse_args()
random.seed(args.seed)
out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
(out / "models").mkdir(exist_ok=True)

lock = threading.Lock(); stop = threading.Event()
heap = []           # (depth, seq, id)
open_set = {}       # id -> (cube tuple, limit)
seq = [0]
st = {"cnf": args.cnf, "base": args.base, "grow": args.grow, "workers": args.workers,
      "started": time.time(), "closed": 0, "splits": 0, "jobs": 0, "sat": None,
      "closed_weight": Fraction(0), "busy_s": 0.0}
depth_stats = {}    # depth -> [processed, closed, split, sat, secs]
running = {}        # id -> (cube, start)
lrat_q = []         # sampled closed cubes for the LRAT lane
lrat_stats = {"sampled": 0, "lrat_verified": 0, "lrat_failed": 0, "lrat_timeout": 0, "xcheck_unsat": 0,
              "xcheck_other": 0}
ev = open(out / "events.jsonl", "a")
prog = open(out / "progress.jsonl", "a")
rep = open(out / "report30.jsonl", "a")
lratlog = open(out / "lrat.jsonl", "a")


def push(cube, limit):
    i = seq[0]; seq[0] += 1
    open_set[i] = (cube, limit)
    heapq.heappush(heap, (len(cube), i, i))


push((), args.base)


def take():
    with lock:
        if stop.is_set() or (args.deadline and time.time() > args.deadline):
            return None
        while heap:
            d, _, i = heapq.heappop(heap)
            if i in open_set:
                running[i] = (open_set[i][0], time.time())
                return i
        return -1


def frac_str(x):
    return f"{x.numerator}/{x.denominator}"


def snapshot(full=False):
    ow = Fraction(0); hist = {}
    for cube, _ in open_set.values():
        ow += Fraction(1, 2 ** len(cube)); hist[len(cube)] = hist.get(len(cube), 0) + 1
    cw = st["closed_weight"]
    total = cw + ow + (Fraction(1, 2 ** len(st["sat"]["cube"])) if st["sat"] else 0)
    s = {"t": round(time.time() - st["started"]), "open": len(open_set), "running": len(running),
         "closed": st["closed"], "splits": st["splits"], "jobs": st["jobs"],
         "closed_weight": frac_str(cw), "closed_weight_float": float(cw), "open_weight_float": float(ow),
         "partition_exact": total == 1, "max_open_depth": max(hist) if hist else None,
         "min_open_depth": min(hist) if hist else None, "busy_s": round(st["busy_s"]),
         "sat": bool(st["sat"])}
    if full:
        s["open_depth_hist"] = {str(k): hist[k] for k in sorted(hist)}
        s["depth_stats"] = {str(k): v[:4] + [round(v[4], 1)] for k, v in sorted(depth_stats.items())}
        s["lrat"] = dict(lrat_stats)
    return s


def save_state():
    d = {"open": [[list(c), l] for c, l in open_set.values()], "closed_weight": frac_str(st["closed_weight"]),
         "closed": st["closed"], "splits": st["splits"], "jobs": st["jobs"], "sat": st["sat"],
         "depth_stats": depth_stats, "lrat": lrat_stats, "started": st["started"], "saved": time.time()}
    tmp = out / "state.tmp"; tmp.write_text(json.dumps(d)); tmp.replace(out / "state.json")


def worker(w):
    p = subprocess.Popen([args.worker_bin, args.cnf, str(args.nx), str(out / "models")], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, text=True, bufsize=1)
    assert p.stdout.readline().startswith("READY")
    while not stop.is_set():
        i = take()
        if i is None:
            break
        if i == -1:
            with lock:
                if not open_set and not running:
                    break
            time.sleep(0.5); continue
        cube, limit = open_set[i]
        p.stdin.write(f"{i} {limit} {' '.join(map(str, cube))} 0\n"); p.stdin.flush()
        r = p.stdout.readline().split()
        if not r:
            break
        with lock:
            running.pop(i, None)
            del open_set[i]
            d = len(cube); secs = float(r[2] if r[0] != "K" else r[3])
            ds = depth_stats.setdefault(d, [0, 0, 0, 0, 0.0]); ds[0] += 1; ds[4] += secs
            st["jobs"] += 1; st["busy_s"] += secs
            e = {"id": i, "d": d, "cube": list(cube), "limit": limit, "r": r[0], "s": secs, "w": w}
            if r[0] == "U":
                st["closed"] += 1; ds[1] += 1
                st["closed_weight"] += Fraction(1, 2 ** d)
                if args.lrat_rate > 0 and random.random() < args.lrat_rate:
                    lrat_q.append((i, cube)); lrat_stats["sampled"] += 1
            elif r[0] == "S":
                ds[3] += 1
                st["sat"] = {"id": i, "cube": list(cube), "model": f"models/model-{i}.txt", "time": time.time()}
                stop.set()
            else:
                lit = int(r[2]); e["lit"] = lit; e["ncand"] = int(r[4])
                nl = int(limit * args.grow)
                if lit == 0:
                    push(cube, nl)
                else:
                    st["splits"] += 1; ds[2] += 1
                    push(cube + (lit,), nl); push(cube + (-lit,), nl)
            ev.write(json.dumps(e) + "\n"); ev.flush()
    p.kill()


def solve_units(cnf, cube, proof=None, timeout=900):
    """Write cnf + unit clauses of the cube; run cadical (with LRAT proof if requested)."""
    tmp = out / f"lrat_tmp_{os.getpid()}_{abs(hash(cube)) % 10**9}.cnf"
    with open(cnf) as f:
        h = f.readline().split(); body = f.read()
    with open(tmp, "w") as g:
        g.write(f"p cnf {h[2]} {int(h[3]) + len(cube)}\n"); g.write(body)
        for l in cube:
            g.write(f"{l} 0\n")
    cmd = [args.cadical, "-q", "-n", "-t", str(timeout), str(tmp)]
    if proof:
        cmd[1:1] = ["--lrat=true", "--binary=false"]
        cmd.append(str(proof))
    t = time.time(); pr = subprocess.run(cmd, capture_output=True, text=True); dt = time.time() - t
    return tmp, pr.returncode, dt


def lrat_lane():
    while not stop.is_set():
        with lock:
            item = lrat_q.pop(0) if lrat_q else None
        if item is None:
            if all(not t.is_alive() for t in threads):
                return
            time.sleep(2); continue
        i, cube = item
        rec = {"id": i, "d": len(cube), "cube": list(cube)}
        if args.lrat_cnf:
            proof = out / f"lrat_{i}.lrat"
            tmp, rc, dt = solve_units(args.lrat_cnf, cube, proof, args.lrat_timeout)
            rec["solve_rc"] = rc; rec["solve_s"] = round(dt, 2)
            if rc == 20:
                rec["proof_bytes"] = proof.stat().st_size
                t = time.time()
                pc = subprocess.run([args.lratcheck, str(tmp), str(proof)], capture_output=True, text=True)
                rec["check_s"] = round(time.time() - t, 2)
                ok = any(ln.strip() == "c VERIFIED" for ln in pc.stdout.splitlines())
                rec["lrat"] = "VERIFIED" if ok else "FAILED"
                rec["check_tail"] = pc.stdout.strip().splitlines()[-1:] if not ok else None
                lrat_stats["lrat_verified" if ok else "lrat_failed"] += 1
            else:
                rec["lrat"] = "TIMEOUT" if rc == 0 else f"rc{rc}"
                lrat_stats["lrat_timeout"] += 1
            tmp.unlink(missing_ok=True); proof.unlink(missing_ok=True)
        if args.xcheck_cnf:
            tmp, rc, dt = solve_units(args.xcheck_cnf, cube, None, args.lrat_timeout)
            rec["xcheck_rc"] = rc; rec["xcheck_s"] = round(dt, 2)
            lrat_stats["xcheck_unsat" if rc == 20 else "xcheck_other"] += 1
            tmp.unlink(missing_ok=True)
        lratlog.write(json.dumps(rec) + "\n"); lratlog.flush()


threads = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(args.workers)]
for t in threads:
    t.start()
lt = None
if args.lrat_rate > 0:
    lt = threading.Thread(target=lrat_lane, daemon=True); lt.start()
last60 = last1800 = 0.0
while any(t.is_alive() for t in threads):
    time.sleep(2)
    now = time.time()
    if now - last60 >= 60:
        with lock:
            prog.write(json.dumps(snapshot()) + "\n"); prog.flush(); save_state()
        last60 = now
    if now - last1800 >= 1800:
        with lock:
            rep.write(json.dumps(snapshot(full=True)) + "\n"); rep.flush()
        last1800 = now
with lock:
    final = snapshot(full=True); save_state()
if st["sat"] and args.sigcheck and args.params:
    N, a, u, k = args.params.split(",")
    pc = subprocess.run([args.sigcheck, N, a, u, k, str(out / st["sat"]["model"])], capture_output=True, text=True)
    final["sat_check"] = pc.stdout.strip()
final["finished"] = "SAT" if st["sat"] else ("UNSAT (all cubes closed)" if not open_set else "stopped (deadline)")
rep.write(json.dumps(final) + "\n"); rep.flush()
(out / "final.json").write_text(json.dumps(final, indent=1))
print(json.dumps({k: final[k] for k in ("finished", "open", "closed", "closed_weight_float", "partition_exact")}))
if lt:
    lt.join(timeout=5)
