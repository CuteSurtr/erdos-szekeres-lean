#!/usr/bin/env python3
"""Arm D: SAT-guided exact insertion, left to right.
State: exact integer points P_0 < ... < P_{k-1} (strictly increasing x); labels = x-order, so their
orientations are a partial assignment of the (7,5,7)@26 signotope CNF (gen_etv.py 26 5 7 7).
Step k: CaDiCaL (conflict budget, random phases on the variables X(i,j,k)) returns a full model
under the prefix assumptions; its signs s_ij = X(i,j,k) define the cell
   {p : s_ij * orient(P_i, P_j, p) > 0 for all i<j<k,  x(p) > x(P_{k-1})},
a convex polygon.  An LP (HiGHS, local float coordinates) maximises the margin; its centre is
rounded to integers (all coordinates are rescaled by a power of 2 when the cell is small) and the
new orientations are re-checked exactly.  If several models give nonempty cells the one with the
largest relative margin is taken.  A complete 26-point set is re-checked exactly (distinct x,
general position, orientations = a model of the CNF) before it is written.  Dead ends backtrack."""
import sys, os, json, argparse, itertools, time, random, math
import numpy as np, highspy
from pysat.formula import CNF
from pysat.solvers import Solver
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("--n", type=int, default=26)
ap.add_argument("--seed", type=int, default=1); ap.add_argument("--time", type=float, default=600)
ap.add_argument("--models", type=int, default=6, help="SAT models tried per step")
ap.add_argument("--conf", type=int, default=5000); ap.add_argument("--maxfail", type=int, default=4)
ap.add_argument("--assume", type=int, default=3, help="random unit assumptions on X(i,j,k) per extra model")
ap.add_argument("-o", required=True)
a = ap.parse_args()
n = a.n; VID = {t: i + 1 for i, t in enumerate(itertools.combinations(range(n), 3))}
rng = random.Random(a.seed)
s = Solver(name="cadical195", bootstrap_with=CNF(from_file=a.cnf).clauses)
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def lits(P):
    L = []
    for t in itertools.combinations(range(len(P)), 3):
        d = orient(P[t[0]], P[t[1]], P[t[2]])
        if d == 0: return None
        L.append(VID[t] if d > 0 else -VID[t])
    return L
def cell_center(P, sg):
    """max t s.t. sg_ij*orient(Pi,Pj,p)/|PiPj| >= t (local coords), x >= x_last + t, |coords|<=box"""
    k = len(P)
    xs = np.array([float(p[0]) for p in P]); ys = np.array([float(p[1]) for p in P])
    # exact local frame: shift by the last point, scale by the bbox
    ox, oy = P[-1]; sc = float(max(max(abs(p[0] - ox), abs(p[1] - oy)) for p in P)) or 1.0
    X = np.array([(p[0] - ox) / sc for p in P]); Y = np.array([(p[1] - oy) / sc for p in P])
    rows = []
    for (i, j), sv in sg.items():
        ax, ay = X[i], Y[i]
        dx, dy = (P[j][0] - P[i][0]) / sc, (P[j][1] - P[i][1]) / sc   # exact integer differences
        L = math.hypot(dx, dy)
        # sv*(dx*(py-ay) - dy*(px-ax)) / L >= t
        rows.append((-sv * dy / L, sv * dx / L, -sv * (-dx * ay + dy * ax) / L))
    rows.append((1.0, 0.0, 0.0))  # px - 0 >= t  (x beyond the last point, which is the origin)
    box = 64.0
    T = len(rows)
    h = highspy.Highs(); h.setOptionValue("output_flag", False); h.setOptionValue("threads", 1)
    lp = highspy.HighsLp(); lp.num_col_ = 3; lp.num_row_ = T
    lp.col_cost_ = np.array([0.0, 0.0, -1.0]); lp.col_lower_ = np.array([-box, -box, -1.0]); lp.col_upper_ = np.array([box, box, 1.0])
    lp.row_lower_ = np.array([r[2] for r in rows]); lp.row_upper_ = np.full(T, highspy.kHighsInf)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = np.arange(0, 3 * T + 1, 3, dtype=np.int32)
    lp.a_matrix_.index_ = np.tile(np.array([0, 1, 2], dtype=np.int32), T)
    lp.a_matrix_.value_ = np.array([[r[0], r[1], -1.0] for r in rows]).ravel()
    h.passModel(lp); h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal: return None
    z = h.getSolution().col_value
    return z[2], (z[0], z[1]), (ox, oy, sc)
def place(P, sg):
    r = cell_center(P, sg)
    if r is None or r[0] <= 1e-13: return None, P
    t, (cx, cy), (ox, oy, sc) = r
    for boost in (0, 20, 40, 60):
        Q = [(x << boost, y << boost) for x, y in P] if boost else P
        S_ = sc * 2 ** boost
        c = ((ox << boost) + int(round(cx * S_)), (oy << boost) + int(round(cy * S_)))
        if c[0] <= Q[-1][0]: continue
        if all((orient(Q[i], Q[j], c) > 0) == (v > 0) and orient(Q[i], Q[j], c) != 0 for (i, j), v in sg.items()):
            return (t, c), Q
    return None, P
out = open(a.o, "a"); w0 = time.time(); found = 0; restarts = 0; maxk = 0
while time.time() - w0 < a.time:
    restarts += 1
    P = []; base = []; fails = [0] * (n + 1)
    while len(P) < n and time.time() - w0 < a.time:
        k = len(P)
        if k < 2:
            P.append((0, 0) if k == 0 else (1 << 40, rng.randint(-(1 << 40), 1 << 40))); base = lits(P); continue
        best = None; bestQ = None; seen = set()
        kv = [VID[(i, j, k)] for i, j in itertools.combinations(range(k), 2)]
        for _ in range(a.models):
            s.set_phases([v if rng.random() < 0.5 else -v for v in kv])
            asm = [v if rng.random() < 0.5 else -v for v in rng.sample(kv, min(len(kv), a.assume))] if _ else []
            s.conf_budget(a.conf)
            if not s.solve_limited(assumptions=base + asm): continue
            mdl = s.get_model()
            sg = {(i, j): (1 if mdl[VID[(i, j, k)] - 1] > 0 else -1) for i, j in itertools.combinations(range(k), 2)}
            key = tuple(sg.values())
            if key in seen: continue
            seen.add(key)
            r, Q = place(P, sg)
            if r and (best is None or r[0] > best[0]): best, bestQ, bsg = r, Q, sg
        if best is None:
            fails[k] += 1
            if fails[k] > a.maxfail or k <= 3: break
            P.pop(); base = lits(P); continue
        P = bestQ + [best[1]]; base = lits(P)
        if base is None: break
        maxk = max(maxk, len(P))
    if len(P) == n:
        ok = all(P[i][0] < P[i + 1][0] for i in range(n - 1))
        L = lits(P); ok = ok and L is not None and s.solve(assumptions=L)
        found += 1
        rec = {"id": f"D{a.seed}_{restarts}", "seed": a.seed, "restart": restarts, "exact_ok": bool(ok), "t": round(time.time() - w0),
               "max_bits": max(max(abs(x), abs(y)) for x, y in P).bit_length(),
               "points": [list(p) for p in P], "model": "".join("+" if x > 0 else "-" for x in L) if L else None}
        out.write(json.dumps(rec) + "\n"); out.flush()
        print("FOUND", found, ok, round(time.time() - w0), flush=True)
    else:
        out.write(json.dumps({"seed": a.seed, "restart": restarts, "fail_at": len(P), "maxk": maxk, "t": round(time.time() - w0)}) + "\n"); out.flush()
