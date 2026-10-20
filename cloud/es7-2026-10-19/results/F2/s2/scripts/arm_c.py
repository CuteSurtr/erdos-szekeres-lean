#!/usr/bin/env python3
"""Arm C: SAT-guided left-to-right geometric construction of (7,5,7)@26 sets.
Points are added in increasing x with exact integer coordinates.  Labels 0..k-1 are the k
leftmost points, so the exact orientations of the current points are a partial assignment of the
signotope CNF (tools/etv/gen_etv.py 26 5 7 7; X(i,j,k) true = ccw).  A candidate new point (sampled
at random, multi-scale) is accepted only if CaDiCaL finds a full 26-point model under the
assumptions given by the exact orientations of all current points plus the candidate; i.e. the
current set is abstractly extendable.  Dead ends backtrack.  A completed 26-point set is a CNF
model realized by construction; it is re-checked exactly (orientations vs. the model, distinct x,
no collinear triple) before it is reported.  Output: JSON lines."""
import sys, os, json, argparse, itertools, time, random, math
from pysat.formula import CNF
from pysat.solvers import Solver
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("--n", type=int, default=26)
ap.add_argument("--seed", type=int, default=1); ap.add_argument("--time", type=float, default=600)
ap.add_argument("--samples", type=int, default=300); ap.add_argument("--maxfail", type=int, default=6)
ap.add_argument("--conf", type=int, default=20000, help="conflict budget per SAT call (undecided = reject)")
ap.add_argument("--verbose", action="store_true")
ap.add_argument("-o", required=True)
a = ap.parse_args()
n = a.n; VID = {t: i + 1 for i, t in enumerate(itertools.combinations(range(n), 3))}
rng = random.Random(a.seed)
s = Solver(name="cadical195", bootstrap_with=CNF(from_file=a.cnf).clauses)
def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
SCALE = 10 ** 30
def sample(P):
    """candidate integer point to the right of all of P (multi-scale)"""
    k = len(P)
    if k == 0: return (0, 0)
    if k == 1: return (SCALE, rng.randint(-SCALE, SCALE))
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    span = max(xs) - min(xs) + 1; yspan = max(ys) - min(ys) + 1
    mode = rng.random()
    if mode < 0.45:
        # near the extension of a line through two current points, perpendicular offset multi-scale
        i, j = sorted(rng.sample(range(k), 2)); p, q = P[i], P[j]
        dx = int(span * 10 ** rng.uniform(-3, 0.7)) + 1
        x = P[-1][0] + dx
        y0 = p[1] + (q[1] - p[1]) * (x - p[0]) // max(1, q[0] - p[0])
        off = int(yspan * 10 ** rng.uniform(-6, 0.3)) * rng.choice((-1, 1))
        return (x, y0 + off)
    elif mode < 0.75:
        # close to the last point (fine scale)
        sc = 10 ** rng.uniform(-6, -0.5)
        return (P[-1][0] + int(span * sc * rng.random()) + 1, P[-1][1] + int(yspan * sc * rng.gauss(0, 1)))
    else:
        dx = int(span * 10 ** rng.uniform(-2, 1)) + 1
        return (P[-1][0] + dx, rng.choice(ys) + int(yspan * 10 ** rng.uniform(-3, 1) * rng.gauss(0, 1)))
def lits(P):
    L = []
    for t in itertools.combinations(range(len(P)), 3):
        d = orient(P[t[0]], P[t[1]], P[t[2]])
        if d == 0: return None
        L.append(VID[t] if d > 0 else -VID[t])
    return L
def new_lits(P, c):
    k = len(P); L = []
    for i, j in itertools.combinations(range(k), 2):
        d = orient(P[i], P[j], c)
        if d == 0: return None
        L.append(VID[(i, j, k)] if d > 0 else -VID[(i, j, k)])
    return L
out = open(a.o, "a"); w0 = time.time(); found = 0; restarts = 0; sat_calls = 0; maxk = 0
while time.time() - w0 < a.time:
    restarts += 1
    P = []; base = []; stack_fail = [0] * (n + 1)
    while len(P) < n and time.time() - w0 < a.time:
        k = len(P); tried = set(); cand = None
        for _ in range(a.samples):
            c = sample(P)
            if k and c[0] <= P[-1][0]: continue
            nl = new_lits(P, c) if k >= 2 else []
            if nl is None: continue
            key = tuple(nl)
            if key in tried: continue
            tried.add(key); sat_calls += 1
            t1 = time.time()
            r = s.solve_limited(assumptions=base + nl, expect_interrupt=False) if a.conf == 0 else None
            if a.conf:
                s.conf_budget(a.conf); r = s.solve_limited(assumptions=base + nl)
            if a.verbose: print(k, len(tried), r, round(time.time() - t1, 3), flush=True)
            if r:
                cand = (c, nl); break
            if len(tried) > 40: break
        if cand is None:
            stack_fail[k] += 1
            if not P or stack_fail[k] > a.maxfail: break   # restart
            P.pop(); base = lits(P); continue
        P.append(cand[0]); base = base + cand[1]
        if len(P) > maxk:
            maxk = len(P)
    if len(P) == n:
        # exact re-check: distinct x, no collinear triple, orientations form a model of the CNF
        ok = all(P[i][0] < P[i + 1][0] for i in range(n - 1))
        L = lits(P); ok = ok and L is not None and s.solve(assumptions=L)
        found += 1
        rec = {"seed": a.seed, "restart": restarts, "exact_ok": bool(ok), "points": [list(p) for p in P],
               "model": "".join("+" if x > 0 else "-" for x in L) if L else None}
        out.write(json.dumps(rec) + "\n"); out.flush()
        print("FOUND", found, ok, round(time.time() - w0), flush=True)
    else:
        out.write(json.dumps({"seed": a.seed, "restart": restarts, "fail_at": len(P), "maxk": maxk, "sat_calls": sat_calls,
                              "t": round(time.time() - w0)}) + "\n"); out.flush()
