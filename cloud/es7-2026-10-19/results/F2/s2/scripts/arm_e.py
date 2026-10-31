#!/usr/bin/env python3
"""Arm E: SAT-repaired fail-first insertion for (7,5,7)@26 (CNF tools/etv/gen_etv.py 26 5 7 7).
Keeps a full CaDiCaL model M and a set of exactly placed integer points (labels = abstract
x-order).  Invariant: M agrees with the exact orientations of all triples of placed points, and
placed labels have increasing x.  Each step computes, for every unplaced label q, the cell
  {p : M(a,b,q) * orient(a,b,p) > 0 for placed a<b (sign convention by label order),
       x between the placed label-neighbours of q}
by an LP (HiGHS, margin maximisation in local float coordinates).  If some cell is empty, M is
re-solved under assumptions = exact orientations of the placed points (random initial phases on
the other variables, conflict budget); after R failed repairs the last placed points are removed.
Otherwise the label with the smallest positive margin is placed at its cell centre, rounded to
integers (coordinates rescaled by powers of 2 when needed) and re-checked exactly.  A complete
26-point set is re-checked exactly (strictly increasing x in label order, no collinear triple,
exact orientations = a model of the CNF).  Output: JSON lines."""
import sys, os, json, argparse, itertools, time, random, math
import numpy as np, highspy
from pysat.formula import CNF
from pysat.solvers import Solver
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("--n", type=int, default=26)
ap.add_argument("--seed", type=int, default=1); ap.add_argument("--time", type=float, default=600)
ap.add_argument("--repairs", type=int, default=8); ap.add_argument("--conf", type=int, default=3000)
ap.add_argument("--backtrack", type=int, default=6); ap.add_argument("--box", type=float, default=16.0)
ap.add_argument("--pick", default="ff", help="ff = smallest positive margin first, rand = random")
ap.add_argument("--allow-empty", action="store_true", help="place a label even if other cells are empty")
ap.add_argument("-o", required=True)
a = ap.parse_args()
n = a.n; TR = list(itertools.combinations(range(n), 3)); VID = {t: i + 1 for i, t in enumerate(TR)}
nx = len(TR)
rng = random.Random(a.seed)
s = Solver(name="cadical195", bootstrap_with=CNF(from_file=a.cnf).clauses)
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def X(M, i, j, k):  # model sign of labels i<j<k
    return 1 if M[VID[(i, j, k)] - 1] > 0 else -1
def req_sign(M, a_, b_, q):
    """required sign of orient(P_a, P_b, p_q) for placed a<b and new label q"""
    t = sorted((a_, b_, q)); sg = X(M, *t)
    # parity of the permutation (a,b,q) -> sorted
    perm = [t.index(a_), t.index(b_), t.index(q)]
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j])
    return sg if inv % 2 == 0 else -sg
def lits_placed(Pl):
    labs = sorted(Pl); L = []
    for i, j, k in itertools.combinations(labs, 3):
        d = orient(Pl[i], Pl[j], Pl[k])
        if d == 0: return None
        L.append(VID[(i, j, k)] if d > 0 else -VID[(i, j, k)])
    return L
def frame(Pl):
    ref = next(iter(Pl.values())); ox, oy = ref
    sc = float(max(max(abs(p[0] - ox), abs(p[1] - oy)) for p in Pl.values())) or 1.0
    return ox, oy, sc
def cell(Pl, M, q, fr):
    ox, oy, sc = fr; labs = sorted(Pl)
    rows = []
    for a_, b_ in itertools.combinations(labs, 2):
        sv = req_sign(M, a_, b_, q)
        A, B = Pl[a_], Pl[b_]
        ax, ay = (A[0] - ox) / sc, (A[1] - oy) / sc
        dx, dy = (B[0] - A[0]) / sc, (B[1] - A[1]) / sc; L = math.hypot(dx, dy)
        rows.append((-sv * dy / L, sv * dx / L, -sv * (-dx * ay + dy * ax) / L))
    lo = [l for l in labs if l < q]; hi = [l for l in labs if l > q]
    if lo: rows.append((1.0, 0.0, (Pl[lo[-1]][0] - ox) / sc))      # x - xlo >= t
    if hi: rows.append((-1.0, 0.0, -(Pl[hi[0]][0] - ox) / sc))     # xhi - x >= t
    box = a.box; T = len(rows)
    h = highspy.Highs(); h.setOptionValue("output_flag", False); h.setOptionValue("threads", 1)
    lp = highspy.HighsLp(); lp.num_col_ = 3; lp.num_row_ = T
    lp.col_cost_ = np.array([0.0, 0.0, -1.0]); lp.col_lower_ = np.array([-box, -box, -1.0]); lp.col_upper_ = np.array([box, box, 1.0])
    lp.row_lower_ = np.array([r[2] for r in rows]); lp.row_upper_ = np.full(T, highspy.kHighsInf)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = np.arange(0, 3 * T + 1, 3, dtype=np.int32)
    lp.a_matrix_.index_ = np.tile(np.array([0, 1, 2], dtype=np.int32), T)
    lp.a_matrix_.value_ = np.array([[r[0], r[1], -1.0] for r in rows]).ravel()
    h.passModel(lp); h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal: return -1.0, None
    z = h.getSolution().col_value
    return z[2], (z[0], z[1])
def exact_place(Pl, M, q, c, fr):
    ox, oy, sc = fr; labs = sorted(Pl)
    for boost in (0, 16, 32, 48, 64):
        Q = {l: (p[0] << boost, p[1] << boost) for l, p in Pl.items()} if boost else Pl
        S_ = sc * 2 ** boost
        pt = ((ox << boost) + int(round(c[0] * S_)), (oy << boost) + int(round(c[1] * S_)))
        lo = [l for l in labs if l < q]; hi = [l for l in labs if l > q]
        if lo and pt[0] <= Q[lo[-1]][0]: continue
        if hi and pt[0] >= Q[hi[0]][0]: continue
        if all(orient(Q[a_], Q[b_], pt) * req_sign(M, a_, b_, q) > 0 for a_, b_ in itertools.combinations(labs, 2)):
            Q = dict(Q); Q[q] = pt; return Q
    return None
def resolve(Pl, phase_from=None):
    L = lits_placed(Pl)
    ph = [v if rng.random() < 0.5 else -v for v in range(1, nx + 1)]
    s.set_phases(ph); s.conf_budget(a.conf)
    if s.solve_limited(assumptions=L): return s.get_model()[:nx]
    return None
out = open(a.o, "a"); w0 = time.time(); restarts = 0; found = 0
while time.time() - w0 < a.time:
    restarts += 1
    M = resolve({}) if False else None
    s.set_phases([v if rng.random() < 0.5 else -v for v in range(1, nx + 1)])
    s.solve(); M = s.get_model()[:nx]
    q0, q1 = sorted(rng.sample(range(n), 2))
    Pl = {q0: (0, 0), q1: (1 << 20, rng.randint(-(1 << 20), 1 << 20))}
    order = [q0, q1]; bt = 0; maxk = 2
    while len(Pl) < n and time.time() - w0 < a.time:
        fr = frame(Pl); best = None; empty = False
        un = [q for q in range(n) if q not in Pl]
        cs = []
        for q in un:
            t, c = cell(Pl, M, q, fr)
            if t <= 1e-12: empty = True
            else: cs.append((t, q, c))
        if cs and (not empty or a.allow_empty):
            cs.sort(); pick = cs[0] if a.pick == "ff" else rng.choice(cs)
            Q = exact_place(Pl, M, pick[1], pick[2], fr)
            if Q is not None:
                Pl = Q; order.append(pick[1]); maxk = max(maxk, len(Pl)); continue
        # repair the model around the placed points
        M2 = None
        for _ in range(a.repairs):
            M2 = resolve(Pl)
            if M2 is None: break
            fr = frame(Pl)
            if sum(cell(Pl, M2, q, fr)[0] > 1e-12 for q in un) >= (len(un) if not a.allow_empty else 1): break
        if M2 is not None:
            M = M2
            if sum(cell(Pl, M, q, frame(Pl))[0] > 1e-12 for q in un) >= (len(un) if not a.allow_empty else 1): continue
        bt += 1
        if bt > a.backtrack or len(order) <= 3: break
        for _ in range(min(2, len(order) - 2)):
            del Pl[order.pop()]
        r = resolve(Pl)
        if r is None: break
        M = r
    if len(Pl) == n:
        P = [Pl[i] for i in range(n)]
        ok = all(P[i][0] < P[i + 1][0] for i in range(n - 1))
        L = lits_placed(Pl); ok = ok and L is not None and s.solve(assumptions=L)
        found += 1
        rec = {"id": f"E{a.seed}_{restarts}", "seed": a.seed, "restart": restarts, "exact_ok": bool(ok), "t": round(time.time() - w0),
               "max_bits": max(max(abs(x), abs(y)) for x, y in P).bit_length(), "points": [list(p) for p in P],
               "model": "".join("+" if x > 0 else "-" for x in L) if L else None}
        out.write(json.dumps(rec) + "\n"); out.flush(); print("FOUND", found, ok, flush=True)
    else:
        out.write(json.dumps({"seed": a.seed, "restart": restarts, "fail_at": len(Pl), "maxk": maxk, "t": round(time.time() - w0)}) + "\n"); out.flush()
