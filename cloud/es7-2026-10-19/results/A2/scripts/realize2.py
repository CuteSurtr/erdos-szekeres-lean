#!/usr/bin/env python3
"""Realize SAT models (from summ2.py MODELS.jsonl) and re-check exactly.

usage: realize2.py WORKDIR MODELS.jsonl OUT.jsonl [--time T] [--workers W] [--sample N --seed S]
Per model: (1) task A's near-original realizer (realize_models.realize: alternating fixed-x/fixed-y
LPs from the original coordinates, then a nonlinear search); (2) if that fails,
tools/realizer/realize.py (portfolio; --xgrid-pool = the base set's coordinates) with T CPU s.
Any candidate is re-checked here independently: integer points, to_sig recomputed from the points
alone must equal the model, brute_kgon must report 0 axiom violations and its convex 7-subset count.
"""
import argparse
import json
import os
import random
import subprocess
import sys
import tempfile
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'A', 'scripts'))
import realize_models as RM  # noqa: E402
from sigutil import to_sig, brute, triples  # noqa: E402

A = None


def exact(M, model, P):
    spts, sg, _ = to_sig([tuple(p) for p in P])
    bk = brute(os.path.join(A.wd, 'brute_kgon'), M, 7, sg, os.path.join(A.wd, 'tmp'), f"r2_{os.getpid()}")
    return {"recomputed_equals_model": sg == model, "brute_violations": bk["violations"],
            "brute_convex7": bk["convex"], "realized": sg == model and bk["violations"] == 0}


def work(job):
    RM.WD = os.path.abspath(A.wd)
    M, model = job["M"], job["model"]
    out = {"label": job["label"], "tag": job["tag"], "realized": False}
    r = RM.realize(job)
    out["stage1"] = {k: v for k, v in r.items() if k != 'attempts'}
    if r["realized"]:
        P = next(a["points"] for a in r["attempts"] if a.get("realized"))
        out.update({"realized": True, "method": "A:" + r["method"], "points": P, "exact": exact(M, model, P)})
        out["realized"] = out["exact"]["realized"]
        return out
    with tempfile.TemporaryDirectory(dir=os.path.join(A.wd, 'tmp')) as td:
        sigf, ptsf, poolf = (os.path.join(td, n) for n in ('m.sig', 'm.pts', 'pool.txt'))
        with open(sigf, 'w') as f:
            for (i, j, k), c in zip(triples(M), model):
                f.write(f"{i - 1} {j - 1} {k - 1} {1 if c == '+' else -1}\n")
        with open(poolf, 'w') as f:
            f.write(f"x {len(job['old_pts'])} " + " ".join(f"{x} {y}" for x, y in job["old_pts"]) + "\n")
        p = subprocess.run([sys.executable, os.path.join(B, 'tools', 'realizer', 'realize.py'), sigf, '--time',
                            str(A.time), '--xgrid-pool', poolf, '--out', ptsf], capture_output=True, text=True)
        line = (p.stdout.strip().splitlines() or ['{}'])[-1]
        try:
            info = json.loads(line)
        except ValueError:
            info = {"raw": line[:200]}
        out["stage2"] = {k: v for k, v in info.items() if k in ("realized", "method", "seconds")}
        if p.returncode == 0 and os.path.exists(ptsf):
            P = [list(map(int, l.split()[:2])) for l in open(ptsf) if l.strip() and not l.startswith('#')]
            if len(P) == M:
                out.update({"method": "realizer:" + str(info.get("method")), "points": P, "exact": exact(M, model, P)})
                out["realized"] = out["exact"]["realized"]
    return out


def main():
    global A
    ap = argparse.ArgumentParser()
    ap.add_argument('wd')
    ap.add_argument('models')
    ap.add_argument('out')
    ap.add_argument('--time', type=float, default=120)
    ap.add_argument('--workers', type=int, default=os.cpu_count())
    ap.add_argument('--sample', type=int, default=0)
    ap.add_argument('--seed', type=int, default=1)
    A = ap.parse_args()
    jobs = [json.loads(l) for l in open(A.models) if l.strip()]
    jobs = [j for j in jobs if j.get("verified")]
    if A.sample and len(jobs) > A.sample:
        jobs = random.Random(A.seed).sample(jobs, A.sample)
    n = 0
    with Pool(A.workers) as pool, open(A.out, 'w') as fo:
        for r in pool.imap_unordered(work, jobs):
            fo.write(json.dumps(r) + "\n")
            fo.flush()
            n += r["realized"]
    print(json.dumps({"models": len(jobs), "realized": n}))


if __name__ == '__main__':
    main()
