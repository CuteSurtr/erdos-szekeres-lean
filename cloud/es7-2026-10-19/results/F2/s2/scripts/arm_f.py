#!/usr/bin/env python3
"""Arm F: SAT-guided exact insertion with geometric proposals, for (7,5,7)@26
(CNF tools/etv/gen_etv.py 26 5 7 7, X(i,j,k) true = ccw; labels = x-order).
State: exactly placed integer points (placed labels have increasing x) and a full CaDiCaL model M
that agrees with all exact orientations of placed triples.
Step:
 1. For every unplaced label q, LP (HiGHS) for the largest-margin point of its cell under M
    (signs M(a,b,q) for placed pairs, x between the placed label-neighbours of q).  If some
    cells are nonempty, place the label with the smallest positive margin (fail-first) at the
    cell centre: exact integer rounding (all coordinates rescaled by powers of 2 when needed) and
    exact re-check.  M stays a model.
 2. Otherwise (geometric proposal): for unplaced labels in order of increasing L1 violation,
    an L1-slack LP gives a point p in q's x-interval that violates few of M's signs; p is rounded
    exactly (--extra-props: also randomly weighted L1 points), and CaDiCaL (conflict budget) is asked for a model under the assumptions "exact
    orientations of placed points and p".  If SAT, q is placed at p and M is replaced.
 3. If no proposal is SAT, the last two placed labels are removed (bounded backtracking).
A complete 26-point set is re-checked exactly (increasing x, no collinear triple, the exact
orientations form a model of the CNF) and brute-forced later by brute26.c."""
import sys, os, json, argparse, itertools, time, random, math, collections
import numpy as np, highspy
from pysat.formula import CNF
from pysat.solvers import Solver
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("--n", type=int, default=26)
ap.add_argument("--seed", type=int, default=1); ap.add_argument("--time", type=float, default=600)
ap.add_argument("--conf", type=int, default=3000); ap.add_argument("--props", type=int, default=6)
ap.add_argument("--backtrack", type=int, default=10); ap.add_argument("--box", type=float, default=16.0)
ap.add_argument("--jitter", type=float, default=0.0, help="place at a random point of the inscribed disc, radius fraction")
ap.add_argument("--bt-depth", type=int, default=0, help="backtrack removes 1..bt_depth labels (random); 0 = always 2")
ap.add_argument("--extra-props", type=int, default=0, help="extra randomly weighted L1 proposals per label")
ap.add_argument("--smart-bt", action="store_true", help="backtrack by removing the placed labels that block the best L1 proposal")
ap.add_argument("-o", required=True)
a = ap.parse_args()
n = a.n; TR = list(itertools.combinations(range(n), 3)); nx = len(TR)
VID = np.zeros((n, n, n), dtype=np.int64)
for i, t in enumerate(TR): VID[t] = i + 1
rng = random.Random(a.seed)
s = Solver(name="cadical195", bootstrap_with=CNF(from_file=a.cnf).clauses)
def chi3(M):
    """antisymmetric sign tensor of model M"""
    C = np.zeros((n, n, n), dtype=np.int8)
    sg = np.where(np.array(M[:nx]) > 0, 1, -1).astype(np.int8)
    for (i, j, k), v in zip(TR, sg):
        C[i, j, k] = C[j, k, i] = C[k, i, j] = v; C[j, i, k] = C[i, k, j] = C[k, j, i] = -v
    return C
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def lits_placed(Pl):
    labs = sorted(Pl); L = []
    for i, j, k in itertools.combinations(labs, 3):
        d = orient(Pl[i], Pl[j], Pl[k])
        if d == 0: return None
        L.append(int(VID[i, j, k]) if d > 0 else -int(VID[i, j, k]))
    return L
def geom(Pl):
    labs = sorted(Pl); ox, oy = Pl[labs[0]]
    sc = float(max(max(abs(p[0] - ox), abs(p[1] - oy)) for p in Pl.values())) or 1.0
    ii, jj = np.triu_indices(len(labs), 1)
    la = np.array(labs)
    AX = np.array([(Pl[l][0] - ox) / sc for l in labs]); AY = np.array([(Pl[l][1] - oy) / sc for l in labs])
    DX = np.array([(Pl[la[j]][0] - Pl[la[i]][0]) / sc for i, j in zip(ii, jj)])
    DY = np.array([(Pl[la[j]][1] - Pl[la[i]][1]) / sc for i, j in zip(ii, jj)])
    Ln = np.hypot(DX, DY)
    return dict(labs=labs, la=la, ii=ii, jj=jj, ox=ox, oy=oy, sc=sc, AX=AX, AY=AY, DX=DX, DY=DY, L=Ln)
def xbounds(G, Pl, q):
    lo = [l for l in G["labs"] if l < q]; hi = [l for l in G["labs"] if l > q]
    xl = (Pl[lo[-1]][0] - G["ox"]) / G["sc"] if lo else None
    xh = (Pl[hi[0]][0] - G["ox"]) / G["sc"] if hi else None
    return xl, xh
def run_lp(ncol, cost, lo, hi, rows_A, rows_lo):
    h = highspy.Highs(); h.setOptionValue("output_flag", False); h.setOptionValue("threads", 1)
    T = rows_A.shape[0]
    lp = highspy.HighsLp(); lp.num_col_ = ncol; lp.num_row_ = T
    lp.col_cost_ = cost; lp.col_lower_ = lo; lp.col_upper_ = hi
    lp.row_lower_ = rows_lo; lp.row_upper_ = np.full(T, highspy.kHighsInf)
    A = rows_A.tocoo() if hasattr(rows_A, "tocoo") else None
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    nz = rows_A != 0
    starts = np.concatenate([[0], np.cumsum(nz.sum(1))]).astype(np.int32)
    idx = np.nonzero(nz)
    lp.a_matrix_.start_ = starts; lp.a_matrix_.index_ = idx[1].astype(np.int32); lp.a_matrix_.value_ = rows_A[idx]
    h.passModel(lp); h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal: return None
    return np.array(h.getSolution().col_value), h.getInfo().objective_function_value
def rows_for(G, C, q):
    sv = C[G["la"][G["ii"]], G["la"][G["jj"]], q].astype(float)
    ax, ay = G["AX"][G["ii"]], G["AY"][G["ii"]]; dx, dy, L = G["DX"], G["DY"], G["L"]
    # sv*(dx*(py-ay) - dy*(px-ax))/L = gx*px + gy*py + g0
    gx, gy, g0 = -sv * dy / L, sv * dx / L, sv * (-dx * ay + dy * ax) / L
    return gx, gy, g0
def cell(G, Pl, C, q):
    gx, gy, g0 = rows_for(G, C, q)
    xl, xh = xbounds(G, Pl, q)
    R = [np.column_stack([gx, gy, -np.ones_like(gx)])]; lo = [-g0]
    if xl is not None: R.append(np.array([[1.0, 0.0, -1.0]])); lo.append([xl])
    if xh is not None: R.append(np.array([[-1.0, 0.0, -1.0]])); lo.append([-xh])
    b = a.box
    r = run_lp(3, np.array([0.0, 0.0, -1.0]), np.array([-b, -b, -1.0]), np.array([b, b, 1.0]), np.vstack(R), np.concatenate(lo))
    if r is None: return -1.0, None
    z, _ = r; return z[2], (z[0], z[1])
def l1_point(G, Pl, C, q, eps, w=None):
    """min sum (w *) slack s.t. g(p) + slack >= eps, x in (xl, xh) with margin eps"""
    gx, gy, g0 = rows_for(G, C, q); m = len(gx)
    xl, xh = xbounds(G, Pl, q)
    A = np.zeros((m, 2 + m)); A[:, 0] = gx; A[:, 1] = gy; A[np.arange(m), 2 + np.arange(m)] = 1.0
    R = [A]; lo = [eps - g0]
    if xl is not None: r_ = np.zeros((1, 2 + m)); r_[0, 0] = 1.0; R.append(r_); lo.append([xl + eps])
    if xh is not None: r_ = np.zeros((1, 2 + m)); r_[0, 0] = -1.0; R.append(r_); lo.append([-xh + eps])
    b = a.box
    cost = np.concatenate([[0.0, 0.0], np.ones(m) if w is None else w(m)])
    r = run_lp(2 + m, cost, np.concatenate([[-b, -b], np.zeros(m)]), np.concatenate([[b, b], np.full(m, highspy.kHighsInf)]),
               np.vstack(R), np.concatenate(lo))
    if r is None: return None
    z, obj = r; return obj, (z[0], z[1])
def to_exact(Pl, G, q, c, C=None):
    """round local point c to integers; check x-interval and (if C given) the required signs exactly"""
    labs = G["labs"]
    for boost in (0, 16, 32, 48, 64):
        Q = {l: (p[0] << boost, p[1] << boost) for l, p in Pl.items()} if boost else Pl
        S_ = G["sc"] * 2 ** boost
        pt = ((G["ox"] << boost) + int(round(c[0] * S_)), (G["oy"] << boost) + int(round(c[1] * S_)))
        lo = [l for l in labs if l < q]; hi = [l for l in labs if l > q]
        if lo and pt[0] <= Q[lo[-1]][0]: continue
        if hi and pt[0] >= Q[hi[0]][0]: continue
        bad = False
        for x_, y_ in itertools.combinations(labs, 2):
            d = orient(Q[x_], Q[y_], pt)
            if d == 0 or (C is not None and (d > 0) != (C[x_, y_, q] > 0)): bad = True; break
        if not bad:
            Q = dict(Q); Q[q] = pt; return Q
    return None
out = open(a.o, "a"); w0 = time.time(); restarts = 0; found = 0
while time.time() - w0 < a.time:
    restarts += 1
    s.set_phases([v if rng.random() < 0.5 else -v for v in range(1, nx + 1)])
    s.solve(); M = s.get_model()[:nx]; C = chi3(M)
    q0, q1 = sorted(rng.sample(range(n), 2))
    Pl = {q0: (0, 0), q1: (1 << 24, rng.randint(-(1 << 24), 1 << 24))}
    order = [q0, q1]; bt = 0; maxk = 2; props = 0; sats = 0
    while len(Pl) < n and time.time() - w0 < a.time:
        G = geom(Pl); un = [q for q in range(n) if q not in Pl]
        cs = []
        for q in un:
            t, c = cell(G, Pl, C, q)
            if t > 1e-12: cs.append((t, q, c))
        placed = False
        if cs:
            cs.sort()
            for t, q, c in cs[:3]:
                if a.jitter:  # random point of the inscribed disc (radius t) instead of its centre
                    ang = rng.uniform(0, 2 * math.pi); rr = t * a.jitter * math.sqrt(rng.random())
                    c = (c[0] + rr * math.cos(ang), c[1] + rr * math.sin(ang))
                Q = to_exact(Pl, G, q, c, C)
                if Q is not None: Pl = Q; order.append(q); placed = True; break
        if not placed:
            cand = []
            for q in un:
                r = l1_point(G, Pl, C, q, 1e-6)
                if r is not None: cand.append((r[0], q, r[1]))
            cand.sort()
            todo = []
            for obj, q, c in cand[:a.props]:
                todo.append((q, c))
                for _ in range(a.extra_props):
                    r = l1_point(G, Pl, C, q, 1e-6, w=lambda m: np.exp(rng.gauss(0, 1) * np.ones(m) + np.array([rng.gauss(0, 1.5) for _ in range(m)])))
                    if r is not None: todo.append((q, r[1]))
            for q, c in todo:
                Q = to_exact(Pl, G, q, c, None)
                if Q is None: continue
                L = lits_placed(Q); props += 1
                if L is None: continue
                s.conf_budget(a.conf)
                if s.solve_limited(assumptions=L):
                    sats += 1; M = s.get_model()[:nx]; C = chi3(M); Pl = Q; order.append(q); placed = True; break
        if placed:
            maxk = max(maxk, len(Pl)); continue
        bt += 1
        if bt > a.backtrack or len(order) <= 3: break
        nrem = min(rng.randint(1, a.bt_depth) if a.bt_depth else 2, len(order) - 2)
        if a.smart_bt and not placed and cand:
            # remove the placed labels most often on the wrong side for the best L1 proposal
            _, q, c = cand[0]; gx, gy, g0 = rows_for(G, C, q)
            viol = np.nonzero(gx * c[0] + gy * c[1] + g0 <= 0)[0]
            cnt = collections.Counter()
            for v in viol: cnt[int(G["la"][G["ii"][v]])] += 1; cnt[int(G["la"][G["jj"][v]])] += 1
            for lab, _ in cnt.most_common(nrem):
                if len(order) > 3 and lab in Pl: del Pl[lab]; order.remove(lab)
        else:
            for _ in range(nrem): del Pl[order.pop()]
        s.set_phases([v if rng.random() < 0.5 else -v for v in range(1, nx + 1)])
        s.conf_budget(a.conf * 4)
        if not s.solve_limited(assumptions=lits_placed(Pl)): break
        M = s.get_model()[:nx]; C = chi3(M)
    if len(Pl) == n:
        P = [Pl[i] for i in range(n)]
        ok = all(P[i][0] < P[i + 1][0] for i in range(n - 1))
        L = lits_placed(Pl); ok = ok and L is not None and s.solve(assumptions=L)
        found += 1
        rec = {"id": f"F{a.seed}_{restarts}", "seed": a.seed, "restart": restarts, "exact_ok": bool(ok), "t": round(time.time() - w0),
               "max_bits": max(max(abs(x), abs(y)) for x, y in P).bit_length(), "props": props, "prop_sat": sats,
               "points": [list(p) for p in P], "model": "".join("+" if x > 0 else "-" for x in L) if L else None}
        out.write(json.dumps(rec) + "\n"); out.flush(); print("FOUND", found, ok, round(time.time() - w0), flush=True)
    else:
        out.write(json.dumps({"seed": a.seed, "restart": restarts, "fail_at": len(Pl), "maxk": maxk, "props": props,
                              "prop_sat": sats, "t": round(time.time() - w0)}) + "\n"); out.flush()
