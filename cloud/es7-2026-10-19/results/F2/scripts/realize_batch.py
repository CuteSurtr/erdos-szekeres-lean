#!/usr/bin/env python3
"""Run the validated realizer (tools/realizer/realize.py) on bit-string signotope models.
usage: realize_batch.py MODELS N OUTDIR --time T --jobs J [--start S --count C] [--methods M]
Each model line: C(N,3) chars, '1' = ccw for x-sorted triple (i<j<k, lexicographic).
Appends to OUTDIR/results.jsonl; realized sets go to OUTDIR/<tag>.pts after an independent exact
re-check (chiro.verify_exact, Fractions)."""
import argparse, itertools, json, multiprocessing as mp, os, sys, time, zlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
from chiro import verify_exact, largest_convex_subset  # noqa

def work(job):
    tag, bits, n, budget, methods = job
    from realize import realize
    tr = list(itertools.combinations(range(n), 3))
    chi = {t: (1 if bits[v] == '1' else -1) for v, t in enumerate(tr)}
    t0 = time.process_time()
    res = realize(chi, n, 1, False, budget=budget, seed=zlib.crc32(tag.encode()) % 100003, methods=methods)
    out = {"tag": tag, "realized": res["realized"], "method": res["method"],
           "best_violations": res["best_violations"], "cpu": round(time.process_time() - t0, 2)}
    for k in ("insertion_ff_max_points_placed", "lp_best_slack"):
        if k in res: out[k] = res[k]
    if res["realized"]:
        pts = [tuple(p) for p in res["points"]]
        ok, bad, zero = verify_exact(pts, chi)
        out["exact_check"] = [ok, bad, zero]
        out["largest_convex_subset"] = largest_convex_subset(pts)
        out["points"] = [list(p) for p in pts]
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("models"); ap.add_argument("N", type=int); ap.add_argument("out")
    ap.add_argument("--time", type=float, default=10); ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--start", type=int, default=0); ap.add_argument("--count", type=int, default=10**9)
    ap.add_argument("--methods", default="auto"); ap.add_argument("--prefix", default="")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    nx = a.N * (a.N - 1) * (a.N - 2) // 6
    # lines: bits, or 'id mode bits' (prep_queue.py)
    lines = []
    for i, l in enumerate(open(a.models)):
        t = l.split()
        if t and len(t[-1]) == nx:
            lines.append((f"{a.prefix}{i}" if len(t) == 1 else f"{t[0]}_m{t[1]}", t[-1]))
    resf = os.path.join(a.out, "results.jsonl")
    done = {json.loads(l)["tag"] for l in open(resf)} if os.path.exists(resf) else set()
    jobs = [(lines[i][0], lines[i][1], a.N, a.time, a.methods.split(",") if a.methods != "auto" else "auto")
            for i in range(a.start, min(len(lines), a.start + a.count)) if lines[i][0] not in done]
    with mp.Pool(a.jobs) as P, open(os.path.join(a.out, "results.jsonl"), "a") as f:
        for r in P.imap_unordered(work, jobs):
            if r["realized"]:
                with open(os.path.join(a.out, r["tag"] + ".pts"), "w") as g:
                    for x, y in r["points"]: g.write(f"{x} {y}\n")
                print("REALIZED", r["tag"], r["exact_check"], r["largest_convex_subset"], flush=True)
            f.write(json.dumps(r) + "\n"); f.flush()

if __name__ == "__main__":
    main()
