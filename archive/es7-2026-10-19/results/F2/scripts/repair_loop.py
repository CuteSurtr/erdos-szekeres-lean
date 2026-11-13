#!/usr/bin/env python3
"""Geometry-guided generation of abstract (no 5-cap, no 7-cup, no 7-gon) 26-point models, with
realization attempts.  Each chain starts from a random point set P (several random families; no
annealing toward heptagon-freeness, no classical construction) and repeats:
  1. sort P by x and take its exact-sign chirotope chi(P) (float sign; only a phase hint);
  2. ask CaDiCaL (sat_server, forcephase) for a model M of the ETV CNF with phases chi(P);
  3. penalty descent of the realizer (realize.penalty_descent, mode free) on M started from P;
     if it reaches 0 violations and integer rounding re-checks exactly, M is realized;
  4. otherwise P := best configuration found, back to 1.
Every model M is written to models.txt (bit string) and every attempt to log.jsonl.
usage: repair_loop.py OUTDIR SEED HOURS [--N 26] [--rounds 12]"""
import argparse, itertools, json, os, subprocess, sys, time, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
import realize as R  # noqa
from chiro import verify_exact, largest_convex_subset  # noqa

def rand_points(rng, n):
    fam = int(rng.integers(0, 5))
    if fam == 0:
        X, Y = rng.uniform(size=n), rng.uniform(size=n)
    elif fam == 1:
        c = rng.integers(0, 4, size=n); r = np.exp(-5 * rng.uniform(size=n))
        X = c * 0.3 + r * rng.normal(size=n); Y = (c * c % 5) * 0.2 + r * rng.normal(size=n)
    elif fam == 2:
        X = rng.uniform(size=n); Y = rng.choice([-1, 1], size=n) * X * X * 0.5 + 0.2 * rng.normal(size=n)
    elif fam == 3:
        X = rng.normal(size=n); Y = rng.normal(size=n) * np.exp(2 * rng.normal(size=n))
    else:  # random points on a few random small circles of mixed scale
        k = int(rng.integers(2, 6)); c = rng.integers(0, k, size=n)
        cx, cy, rad = rng.normal(size=k) * 3, rng.normal(size=k) * 3, np.exp(rng.normal(size=k))
        t = rng.uniform(0, 2 * np.pi, size=n)
        X = cx[c] + rad[c] * np.cos(t) + 0.01 * rng.normal(size=n); Y = cy[c] + rad[c] * np.sin(t)
    return X, Y, fam

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("seed", type=int); ap.add_argument("hours", type=float)
    ap.add_argument("--N", type=int, default=26); ap.add_argument("--rounds", type=int, default=12)
    ap.add_argument("--steps", type=int, default=500); ap.add_argument("--cnf", required=True)
    ap.add_argument("--server", required=True); ap.add_argument("--fullbudget", type=float, default=0); ap.add_argument("--maxit", type=int, default=200); ap.add_argument("--R", type=int, default=16); ap.add_argument("--free", type=float, default=0.3)
    a = ap.parse_args()
    n = a.N; os.makedirs(a.out, exist_ok=True)
    tr = list(itertools.combinations(range(n), 3))
    TA = np.array([t[0] for t in tr]); TB = np.array([t[1] for t in tr]); TC = np.array([t[2] for t in tr])
    srv = subprocess.Popen([a.server, a.cnf, str(n), str(a.seed), str(a.maxit)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    rng = np.random.default_rng(a.seed)
    end = time.time() + a.hours * 3600
    fm = open(os.path.join(a.out, f"models_{a.seed}.txt"), "a"); fl = open(os.path.join(a.out, f"log_{a.seed}.jsonl"), "a")
    chain = 0
    while time.time() < end:
        chain += 1
        X, Y, fam = rand_points(rng, n)
        for rd in range(a.rounds):
            o = np.argsort(X); X, Y = X[o], Y[o]
            D = (X[TB] - X[TA]) * (Y[TC] - Y[TA]) - (Y[TB] - Y[TA]) * (X[TC] - X[TA])
            ph = "".join("1" if d > 0 else "0" for d in D)
            # assume only the robust orientations: |det| normalised by the two shortest sides
            la = np.hypot(X[TB] - X[TA], Y[TB] - Y[TA]); lb = np.hypot(X[TC] - X[TA], Y[TC] - Y[TA])
            lc = np.hypot(X[TC] - X[TB], Y[TC] - Y[TB])
            g = np.abs(D) * np.maximum(np.maximum(la, lb), lc) / (la * lb * lc + 1e-300)
            thr = np.quantile(g, a.free)
            mask = "".join("1" if x > thr else "0" for x in g)
            srv.stdin.write(ph + " " + mask + "\n"); srv.stdin.flush()
            M = srv.stdout.readline().strip()
            if len(M) != len(tr):
                print("server error", M[:100], flush=True); return
            ham = sum(1 for u, v in zip(ph, M) if u != v)
            fm.write(M + "\n"); fm.flush()
            chi = {t: (1 if M[v] == '1' else -1) for v, t in enumerate(tr)}
            prob = R.Prob(chi, n)
            t0 = time.process_time()
            pts, bv, bxy = R.penalty_descent(prob, rng, time.process_time() + 30, mode="free", R=a.R,
                                             steps=a.steps, init=(X, Y), max_rounds=1)
            rec = {"chain": chain, "fam": fam, "round": rd, "ham": ham, "viol": bv, "cpu": round(time.process_time() - t0, 2),
                   "id": f"{a.seed}_{chain}_{rd}"}
            if pts is None and a.fullbudget > 0 and rd == a.rounds - 1:
                res = R.realize(chi, n, budget=a.fullbudget, seed=a.seed * 1000 + chain)
                if res["realized"]:
                    pts = [tuple(p) for p in res["points"]]; rec["method"] = res["method"]
            if pts is not None:
                ok, bad, zero = verify_exact([tuple(p) for p in pts], chi)
                rec.update(realized=True, exact=[ok, bad, zero], lcs=largest_convex_subset([tuple(p) for p in pts]))
                with open(os.path.join(a.out, f"real_{rec['id']}.pts"), "w") as g:
                    for x, y in pts: g.write(f"{x} {y}\n")
                with open(os.path.join(a.out, f"real_{rec['id']}.model"), "w") as g:
                    g.write(M + "\n")
                fl.write(json.dumps(rec) + "\n"); fl.flush()
                print("REALIZED", rec, flush=True)
                break
            fl.write(json.dumps(rec) + "\n"); fl.flush()
            if bxy is None: break
            X, Y = np.array(bxy[0]), np.array(bxy[1])

if __name__ == "__main__":
    main()
