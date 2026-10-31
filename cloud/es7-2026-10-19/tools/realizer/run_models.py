#!/usr/bin/env python3
"""Batch driver: realize every model of a symcnf.py model file (or a list of .sig files), in parallel.

usage: run_models.py --models FILE --P P --m M [--center] --out DIR [--time T] [--jobs J]
       run_models.py --signotope FILE --P N --out DIR ...      (trackB gen_cnf.py signotope models)
                     [--methods sym,lp,free] [--dedup] [--K K] [--limit L] [--seeds S]
       run_models.py --sigs a.sig b.sig ... --m M [--center] --out DIR ...

--dedup: group the models into isomorphism classes (relabelling and reflection, chiro.canonical_form)
         and run one representative per class; realizability is a class invariant, so the verdict is
         copied to every member.
--K:     also compute the exact largest convex subset of every realized point set (must be < K for a
         K-gon-free model).
--seeds: number of independent attempts (different seeds) per model, each with the full budget,
         stopping at the first success.
Writes DIR/results.jsonl (one line per model), DIR/summary.json and DIR/<name>.pts (integer
coordinates, one point per line, in model label order) for every realized model.
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chiro import (canonical_form, largest_convex_subset, read_models, read_sig,  # noqa: E402
                   read_signotope_models, verify_exact)


def work(job):
    name, chi, n, m, hc, budget, methods, seeds, K, outdir, xpool = job
    import realize as R
    from realize import realize
    if xpool and not R.KNOWN_XGRIDS:
        R.set_known_xgrids(R.read_point_sets(xpool))
    t0 = time.process_time()
    w0 = time.time()
    res = None
    for s in range(seeds):
        res = realize(chi, n, m, hc, budget=budget, seed=1000 * s + zlib.crc32(name.encode()) % 997, methods=methods)
        if res["realized"]:
            break
    out = {"name": name, "realized": res["realized"], "method": res["method"],
           "best_violations": res["best_violations"], "cpu_seconds": round(time.process_time() - t0, 3),
           "wall_seconds": round(time.time() - w0, 3)}
    for k in ("insertion_max_orbits_placed", "insertion_max_points_placed", "insertion_ff_max_points_placed", "lp_best_slack"):
        if k in res:
            out[k] = res[k]
    if res["realized"]:
        pts = [tuple(p) for p in res["points"]]
        ok, bad, zero = verify_exact(pts, chi)          # independent exact re-check (Fractions)
        out["exact_check"] = {"ok": ok, "mismatches": bad, "collinear": zero}
        out["max_abs_coord"] = max(max(abs(x), abs(y)) for x, y in pts)
        if K:
            out["largest_convex_subset"] = largest_convex_subset(pts)
        with open(os.path.join(outdir, name + ".pts"), "w") as f:
            for x, y in pts:
                f.write(f"{x} {y}\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models")
    ap.add_argument("--sigs", nargs="*")
    ap.add_argument("--signotope", help="signotope models (tools/trackB/gen_cnf.py numbering, needs --P)")
    ap.add_argument("--P", type=int)
    ap.add_argument("--m", type=int, default=1)
    ap.add_argument("--center", action="store_true")
    ap.add_argument("--out", required=True)
    ap.add_argument("--time", type=float, default=20, help="CPU-second budget per attempt")
    ap.add_argument("--jobs", type=int, default=max(1, os.cpu_count() - 2))
    ap.add_argument("--methods", default="auto")
    ap.add_argument("--dedup", action="store_true")
    ap.add_argument("--K", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--xgrid-pool", help="known point sets whose x-coordinates seed the lp method")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.signotope:
        chis = read_signotope_models(a.signotope, a.P)
        names = [f"model{i + 1}" for i in range(len(chis))]
        n = a.P
    elif a.models:
        chis = read_models(a.models, a.P, a.m, a.center)
        names = [f"model{i + 1}" for i in range(len(chis))]
        n = a.P
    else:
        chis = [read_sig(p) for p in a.sigs]
        names = [os.path.splitext(os.path.basename(p))[0] for p in a.sigs]
        n = max(max(k) for k in chis[0]) + 1
    if a.limit:
        chis, names = chis[:a.limit], names[:a.limit]
    t0 = time.time()
    cls = list(range(len(chis)))
    reps = list(range(len(chis)))
    if a.dedup:
        forms = {}
        cls = []
        for i, chi in enumerate(chis):
            f = canonical_form(chi, n, mirror=True)
            if f not in forms:
                forms[f] = len(forms)
            cls.append(forms[f])
        first = {}
        for i, c in enumerate(cls):
            first.setdefault(c, i)
        reps = sorted(first.values())
        print(f"{len(chis)} models in {len(reps)} classes (relabelling + reflection), "
              f"{time.time() - t0:.1f}s", flush=True)
    methods = a.methods.split(",")
    if methods == ["auto"]:
        from realize import default_methods
        methods = default_methods(a.m, a.center)
    jobs = [(names[i], chis[i], n, a.m, a.center, a.time, methods, a.seeds, a.K, a.out, a.xgrid_pool) for i in reps]
    results = {}
    with open(os.path.join(a.out, "results.jsonl"), "w") as fo, mp.Pool(a.jobs) as pool:
        for r in pool.imap_unordered(work, jobs):
            results[r["name"]] = r
            fo.write(json.dumps(r) + "\n")
            fo.flush()
            print(json.dumps(r), flush=True)
    rep_of = {}
    for i, c in enumerate(cls):
        rep_of.setdefault(c, names[i])
    per_model = []
    for i, nm in enumerate(names):
        r = results[rep_of[cls[i]]]
        per_model.append({"name": nm, "class": cls[i], "representative": rep_of[cls[i]],
                          "realized": r["realized"] and r.get("exact_check", {}).get("ok", False)})
    real_cls = sorted({cls[i] for i, p in enumerate(per_model) if p["realized"]})
    times = [results[names[i]]["cpu_seconds"] for i in reps]
    st = sorted(results[names[i]]["cpu_seconds"] for i in reps if results[names[i]]["realized"])
    summary = {
        "input": a.models or a.signotope or "sigs", "P": n, "m": a.m, "center": a.center, "methods": methods,
        "cpu_budget_per_attempt_s": a.time, "seeds": a.seeds, "models": len(chis),
        "classes": len(reps), "realized_models": sum(p["realized"] for p in per_model),
        "realized_classes": len(real_cls),
        "median_cpu_seconds_realized": (st[len(st) // 2] if st else None),
        "max_cpu_seconds_realized": (st[-1] if st else None),
        "mean_cpu_seconds_all": (sum(times) / len(times) if times else None),
        "wall_seconds": round(time.time() - t0, 1),
        "per_model": per_model,
    }
    with open(os.path.join(a.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("SUMMARY " + json.dumps({k: v for k, v in summary.items() if k != "per_model"}), flush=True)


if __name__ == "__main__":
    main()
