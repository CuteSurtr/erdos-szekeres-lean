#!/usr/bin/env python3
"""Run the validated realizer (results/F/realizer/realize.py, m = 1, default portfolio ins-ff,lp)
on '+/-' model lines; every success is re-checked exactly (chiro.verify_exact, Fractions).
Appends one JSON line per model to OUT.jsonl; successes also to OUT.pts.jsonl."""
import sys, os, json, argparse, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../F/realizer"))
from multiprocessing import Pool
import chiro, realize as R
ap = argparse.ArgumentParser()
ap.add_argument("models"); ap.add_argument("--n", type=int, default=26)
ap.add_argument("--time", type=float, default=5.0); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--methods", default="auto"); ap.add_argument("--start", type=int, default=0)
ap.add_argument("--limit", type=int, default=0); ap.add_argument("-o", required=True)
a = ap.parse_args()
TR = list(itertools.combinations(range(a.n), 3))
def work(job):
    idx, line = job
    chi = {t: (1 if c == "+" else -1) for t, c in zip(TR, line)}
    r = R.realize(chi, a.n, budget=a.time, seed=1000 + idx, methods=a.methods)
    out = {"model": idx, "realized": r["realized"], "method": r["method"], "cpu": r["seconds"],
           "ins_ff_placed": r.get("insertion_ff_max_points_placed"), "lp_slack": r.get("lp_best_slack")}
    if r["realized"]:
        ok, bad, zero = chiro.verify_exact(r["points"], chi)
        out["exact_check"] = bool(ok); out["points"] = r["points"]
    return out
if __name__ == "__main__":
    lines = open(a.models).read().split()
    jobs = list(enumerate(lines))[a.start:]
    if a.limit: jobs = jobs[:a.limit]
    with Pool(a.jobs) as p, open(a.o, "a") as f:
        for o in p.imap_unordered(work, jobs):
            f.write(json.dumps(o) + "\n"); f.flush()
            if o["realized"]:
                print("REALIZED", o["model"], o.get("exact_check"), flush=True)
