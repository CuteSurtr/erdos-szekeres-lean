#!/usr/bin/env python3
"""Layer-and-conquer over layers.py specs.

  lnc.py solve CNF SPECFILE OUT.jsonl --timeout T --jobs J [--maxlayers 3] [--lrat]
      Every spec is tried with `cadical -t T` (run_spec.sh; with --lrat, an UNSAT answer is
      checked by cake_lpr).  A spec that times out is replaced by all its next-layer specs
      (layers.py next) until it has --maxlayers layers; deeper ones are recorded OPEN.
      One JSON record per attempt (fields of run_spec.sh plus "expanded"/"children").
  lnc.py estimate CNF SPECFILE OUT.jsonl --timeout T --jobs J --k K [--maxlayers 3] [--seed S]
      Knuth-type estimate: a spec costs its own attempt; if it times out, K children chosen at
      random (seeded; K may be a per-layer list) are estimated recursively and scaled by nchildren / K.  Prints and writes
      per-spec estimates (core seconds; censored at T in the last layer).
"""
import argparse, json, os, random, subprocess, sys, threading
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("mode"); ap.add_argument("cnf"); ap.add_argument("specs"); ap.add_argument("out")
ap.add_argument("--timeout", type=int, default=20); ap.add_argument("--jobs", type=int, default=3)
ap.add_argument("--maxlayers", type=int, default=3); ap.add_argument("--lrat", action="store_true")
ap.add_argument("--k", default="4,2", help="children sampled per layer, e.g. 4,2"); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--work", default="/tmp/claude-0/w/runs")
a = ap.parse_args()
lock = threading.Lock(); outf = open(a.out, "a")

def attempt(spec):
    cmd = [os.path.join(HERE, "run_spec.sh"), a.cnf, spec, str(a.timeout), a.work] + (["lrat"] if a.lrat else [])
    r = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    return r

def children(spec):
    return subprocess.run([sys.executable, os.path.join(HERE, "layers.py"), "next", spec],
                          capture_output=True, text=True, check=True).stdout.split()

def log(r):
    with lock:
        outf.write(json.dumps(r) + "\n"); outf.flush()

specs = [l.strip() for l in open(a.specs) if l.strip()]
if a.mode == "solve":
    pool = ThreadPoolExecutor(a.jobs); pending = []; cv = threading.Condition()
    count = [0]
    def task(spec):
        r = attempt(spec)
        if r["result"] == "UNKNOWN" and spec.count(";") + 1 < a.maxlayers:
            ch = children(spec); r["expanded"] = True; r["children"] = len(ch)
            log(r)
            for c in ch: submit(c)
        else:
            if r["result"] == "UNKNOWN": r["open"] = True
            log(r)
            if r["result"] == "SAT": print("SAT", spec, flush=True)
        with cv:
            count[0] -= 1; cv.notify_all()
    def submit(spec):
        with cv: count[0] += 1
        pool.submit(task, spec)
    for s in specs: submit(s)
    with cv:
        while count[0] > 0: cv.wait()
    pool.shutdown()
else:
    rng = random.Random(a.seed); pool = ThreadPoolExecutor(a.jobs)
    def est(spec):
        r = attempt(spec); cost = r["solve_s"] + (r["check_s"] or 0)
        rec = {"spec": spec, "result": r["result"], "own_s": cost}
        if r["result"] == "SAT": print("SAT", spec, flush=True)
        if r["result"] == "UNKNOWN" and spec.count(";") + 1 < a.maxlayers:
            ch = children(spec)
            ks = [int(x) for x in a.k.split(",")]; k = ks[min(spec.count(";"), len(ks) - 1)]
            with lock: pick = rng.sample(ch, min(k, len(ch)))
            subs = [est(c) for c in pick]
            rec.update(nchildren=len(ch), sampled=len(pick), child_est=[s["est_s"] for s in subs],
                       child_results=[s["result"] for s in subs])
            rec["censored"] = any(s["censored"] for s in subs)
            cost += len(ch) / len(pick) * sum(s["est_s"] for s in subs)
        rec["est_s"] = round(cost, 1)
        rec.setdefault("censored", r["result"] == "UNKNOWN")
        log(rec); return rec
    res = list(pool.map(est, specs))
    print(json.dumps({"total_est_core_s": round(sum(r["est_s"] for r in res), 1), "n": len(res)}))
