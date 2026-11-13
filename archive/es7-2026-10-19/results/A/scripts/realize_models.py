#!/usr/bin/env python3
"""Try to realize SAT models near the original coordinates, then verify exactly.

Library use: realize(job) with job = dict(M, model, old_pts, new) where old_pts are the x-sorted
integer coordinates of the old points (old point a -> a-th index of 1..M not in `new`).
Initial x: old points keep their (normalised) x; new points are spread evenly inside their slot
(several placements are tried). lp_realize then alternates an LP in y (x fixed) and an LP in x
(y fixed), maximising the worst normalised orientation margin.

Exact check of a candidate: the printed doubles are exact dyadic rationals; they are scaled to
integers by a common power of two and every orientation is recomputed with Python ints and
compared with the model; general position is checked; the signotope of the exact points is
recomputed from the coordinates and brute_kgon counts its convex 7-subsets.

CLI: realize_models.py WORKDIR MODELS.jsonl OUT.jsonl [workers]
  MODELS.jsonl lines: {"label","tag","M","model","old_pts":[[x,y],...],"new":[...]}
"""
import json
import os
import subprocess
import sys
from fractions import Fraction
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import orient, to_sig, brute, new_map  # noqa: E402

WD = None


def initial_x(M, old_pts, new, frac):
    mp = new_map(M, new)
    xs = [None] * (M + 1)
    for a, t in enumerate(mp):
        xs[t] = float(old_pts[a][0])
    lo, hi = float(old_pts[0][0]), float(old_pts[-1][0])
    span = (hi - lo) or 1.0
    t = 1
    while t <= M:
        if xs[t] is not None:
            t += 1
            continue
        s = t
        while t <= M and xs[t] is None:
            t += 1
        e = t  # new points occupy s..e-1
        cnt = e - s
        left = xs[s - 1] if s > 1 else None
        right = xs[e] if e <= M else None
        for r in range(cnt):
            if left is not None and right is not None:
                if cnt == 1:
                    xs[s + r] = left + (right - left) * frac
                else:
                    xs[s + r] = left + (right - left) * (r + 1) / (cnt + 1)
            elif left is None:
                xs[s + r] = right - span * 0.05 * (cnt - r)
            else:
                xs[s + r] = left + span * 0.05 * (r + 1)
    return xs[1:]


def initial_y(M, old_pts, new):
    mp = new_map(M, new)
    ys = [None] * M  # None = new point (y unknown, written as '?')
    for a, t in enumerate(mp):
        ys[t - 1] = float(old_pts[a][1])
    return ys


def exact_check(M, model, X, Y):
    fx = [Fraction(v) for v in X]
    fy = [Fraction(v) for v in Y]
    den = 1
    for v in fx + fy:
        den = max(den, v.denominator)
    P = [(int(a * den), int(b * den)) for a, b in zip(fx, fy)]
    assert all(Fraction(p[0], den) == a and Fraction(p[1], den) == b for p, a, b in zip(P, fx, fy))
    mism = 0
    idx = 0
    zero = 0
    for i in range(M):
        for j in range(i + 1, M):
            for k in range(j + 1, M):
                o = orient(P[i], P[j], P[k])
                if o == 0:
                    zero += 1
                elif ('+' if o > 0 else '-') != model[idx]:
                    mism += 1
                idx += 1
    xs_sorted = all(P[i][0] < P[i + 1][0] for i in range(M - 1))
    return P, mism, zero, xs_sorted


def _fmt(M, model, xs, ys):
    return (f"{M}\n{model}\n" + " ".join(repr(v) for v in xs) + "\n" +
            " ".join('?' if v is None else repr(v) for v in ys) + "\n")


def _parse_xy(lines):
    X = [float(v) for v in next(l for l in lines if l.startswith('X')).split()[1:]]
    Y = [float(v) for v in next(l for l in lines if l.startswith('Y')).split()[1:]]
    return X, Y


def run_lp(M, model, xs, ys, rounds):
    out = subprocess.run([os.path.join(WD, 'lp_realize'), str(rounds)], input=_fmt(M, model, xs, ys),
                         capture_output=True, text=True, timeout=900)
    lines = out.stdout.splitlines()
    b = [l for l in lines if l.startswith('BEST')]
    if not b:
        return None, None, None
    X, Y = _parse_xy(lines)
    return float(b[0].split()[1]), X, Y


def run_nl(M, model, xs, ys, restarts, iters, seed):
    out = subprocess.run([os.path.join(WD, 'nl_realize'), str(restarts), str(iters), str(seed)],
                         input=_fmt(M, model, xs, ys), capture_output=True, text=True, timeout=900)
    lines = out.stdout.splitlines()
    b = [l for l in lines if l.startswith('BEST')]
    if not b:
        return None, None, None
    X, Y = _parse_xy(lines)
    return int(b[0].split()[1]), X, Y


def try_exact(M, model, X, Y):
    P, mism, zero, xs_sorted = exact_check(M, model, X, Y)
    rec = {"exact_mismatches": mism, "collinear": zero, "x_sorted": xs_sorted, "realized": False}
    if mism == 0 and zero == 0 and xs_sorted:
        spts, sg, _ = to_sig(P)  # recomputed from the exact points alone
        bk = brute(os.path.join(WD, 'brute_kgon'), M, 7, sg, os.path.join(WD, 'tmp'), f"real_{os.getpid()}")
        rec.update({"recomputed_equals_model": sg == model, "brute_violations": bk["violations"],
                    "brute_convex7": bk["convex"], "points": [list(p) for p in P]})
        rec["realized"] = (sg == model and bk["violations"] == 0)
    return rec


def realize(job, rounds=8, fracs=(0.5, 0.2, 0.8), nl=True):
    M, model, old_pts, new = job["M"], job["model"], job["old_pts"], job["new"]
    tried = []
    best_lp = None
    for frac in fracs:
        xs, ys = initial_x(M, old_pts, new, frac), initial_y(M, old_pts, new)
        t, X, Y = run_lp(M, model, xs, ys, rounds)
        rec = {"method": "lp", "frac": frac, "lp_margin": t}
        if t is not None and (best_lp is None or t > best_lp):
            best_lp = t
        if t is not None and t > 0:
            rec.update(try_exact(M, model, X, Y))
        tried.append(rec)
        if rec.get("realized"):
            return {"label": job["label"], "tag": job["tag"], "realized": True, "method": "lp", "attempts": tried}
    best_nl = None
    if nl:
        xs, ys = initial_x(M, old_pts, new, 0.5), initial_y(M, old_pts, new)
        v, X, Y = run_nl(M, model, xs, ys, 4, 20000, 1)
        rec = {"method": "nl", "violated": v}
        best_nl = v
        if v == 0:
            rec.update(try_exact(M, model, X, Y))
        tried.append(rec)
        if rec.get("realized"):
            return {"label": job["label"], "tag": job["tag"], "realized": True, "method": "nl", "attempts": tried}
        if X is not None:  # polish the nonlinear result with the alternating LPs
            t, X2, Y2 = run_lp(M, model, X, Y, 4)
            rec = {"method": "nl+lp", "lp_margin": t}
            if t is not None and t > 0:
                rec.update(try_exact(M, model, X2, Y2))
            tried.append(rec)
            if rec.get("realized"):
                return {"label": job["label"], "tag": job["tag"], "realized": True, "method": "nl+lp",
                        "attempts": tried}
    return {"label": job["label"], "tag": job["tag"], "realized": False, "best_lp_margin": best_lp,
            "best_nl_violated": best_nl, "attempts": tried}


def _init(wd):
    global WD
    WD = wd


def main():
    wd, models, out = sys.argv[1:4]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else os.cpu_count()
    jobs = [json.loads(l) for l in open(models) if l.strip()]
    n_ok = 0
    with Pool(workers, initializer=_init, initargs=(os.path.abspath(wd),)) as pool, open(out, 'w') as fo:
        for r in pool.imap_unordered(realize, jobs):
            fo.write(json.dumps(r) + "\n")
            fo.flush()
            n_ok += r["realized"]
    print(json.dumps({"models": len(jobs), "realized": n_ok}))


if __name__ == '__main__':
    main()
