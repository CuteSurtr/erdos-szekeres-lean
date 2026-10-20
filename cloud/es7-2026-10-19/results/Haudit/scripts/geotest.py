#!/usr/bin/env python3
"""Haudit task 4: independent geometric test of the hull-pair split of mirror sub-case (ii).

Own code: point generation, exact integer orientation, monotone-chain hull, case cubes from
mycube.py (own re-implementation of the soundness note), F read from the regenerated
m33k7int.sub.cnf.  Variable numbering of the cup/cap auxiliaries follows gen_etv.py's
allocation order (needed only to evaluate F's non-orientation clauses).

usage: geotest.py F.cnf CASES.icnf K7FILE SEED COUNT_PER_KIND OUT.jsonl
"""
import sys, json, random, itertools, math
from fractions import Fraction
import numpy as np
sys.path.insert(0, '/opt/audit'); import mycube as M

Fpath, ICNF, K7, SEED, NPER, OUT = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
N = 33; NX = 5456

# ---------- F ----------
short, long_ = [], []
with open(Fpath) as f:
    hdr = f.readline().split(); NV = int(hdr[2])
    for line in f:
        c = list(map(int, line.split()[:-1]))
        (short if len(c) <= 3 else long_).append(c)
SH = np.array([c + [c[0]] * (3 - len(c)) for c in short], dtype=np.int64)
orient_only = np.all(np.abs(SH) <= NX, axis=1)
assert all(all(abs(l) <= NX for l in c) for c in long_)
def clause_sat(A):
    """A: bool array indexed by var.  returns bool per short clause and per long clause"""
    v = A[np.abs(SH)]; v = np.where(SH > 0, v, ~v)
    return v.any(axis=1), [any(A[abs(l)] == (l > 0) for l in c) for c in long_]

# aux numbering (gen_etv.py order): cap kind first, then cup; V then E per kind
nv = NX; VID = {}; EID = {}
for kind in ("cap", "cup"):
    for x, a, b in itertools.combinations(range(1, N + 1), 3):
        for r in range(3, 7):
            if a - x >= r - 2: nv += 1; VID[(kind, x, a, b, r)] = nv
    for x, b in itertools.combinations(range(1, N + 1), 2):
        for r in range(3, 7):
            if b - x >= r - 1: nv += 1; EID[(kind, x, b, r)] = nv
assert nv == NV, (nv, NV)
# which short clauses are "forbidding" (all literals negative auxiliaries)
forbid = ~np.any((SH > 0) & (SH > NX), axis=1) & np.any(np.abs(SH) > NX, axis=1)
VKEYS = list(VID.items()); EKEYS = list(EID.items())
VK = np.array([[0 if k[0] == "cap" else 1, k[1], k[2], k[3], k[4]] for k, _ in VKEYS]); VV = np.array([v for _, v in VKEYS])
EK = np.array([[0 if k[0] == "cap" else 1, k[1], k[2], k[3]] for k, _ in EKEYS]); EV = np.array([v for _, v in EKEYS])

# ---------- cases ----------
CASES = M.cases()
icnf = [list(map(int, l.split()[1:-1])) for l in open(ICNF) if l.startswith('a')]
assert all(set(c) == M.cube(U, L) for c, (U, L) in zip(icnf, CASES))
CL = max(len(c) for c in icnf)
CU = np.array([c + [c[0]] * (CL - len(c)) for c in icnf], dtype=np.int64)
TRI = list(itertools.combinations(range(1, N + 1), 3))
assert [M.VAR[t] for t in TRI] == list(range(1, NX + 1))

# ---------- geometry ----------
def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def general_position(P):
    for a, b, c in itertools.combinations(range(len(P)), 3):
        if orient(P[a], P[b], P[c]) == 0: return False
    return True
def hull_idx(P):
    """monotone chain, strict; P sorted by x (distinct).  returns ccw list of indices"""
    def half(idx):
        h = []
        for i in idx:
            while len(h) >= 2 and orient(P[h[-2]], P[h[-1]], P[i]) <= 0: h.pop()
            h.append(i)
        return h
    n = len(P); lo = half(range(n)); up = half(range(n - 1, -1, -1))
    return lo[:-1] + up[:-1]
def has_k_gon_angular(P, K=7):
    """independent check: largest convex polygon >= K via anchored angular DP"""
    n = len(P)
    for s in range(n):
        p = P[s]
        Q = [q for q in P if (q[1], q[0]) > (p[1], p[0])]
        import functools
        def cmp(a, b):
            o = orient(p, a, b); return -1 if o > 0 else 1
        Q.sort(key=functools.cmp_to_key(cmp)); m = len(Q)
        if m + 1 < K: continue
        best = {}
        for i in range(m):
            for j in range(i):
                v = 2  # p, Q[j]; adding Q[i] -> 3
                for k in range(j):
                    if (j, k) in best and orient(Q[k], Q[j], Q[i]) > 0:
                        v = max(v, best[(j, k)])
                best[(i, j)] = v + 1
                if v + 1 >= K and orient(Q[j], Q[i], p) > 0: return True
    return False

def mirror_set(half, axis_y):
    """half: 16 points with x>0; returns 33 points sorted by x"""
    P = [(-x, y) for x, y in half] + [(0, axis_y)] + [(x, y) for x, y in half]
    return sorted(P)

def normalize(P):
    """P: list of (Fraction or int) pairs, symmetric in the y-axis.  separate x by a projective
    map if needed, scale to integers, sort, y-flip if X(1,2,3) false."""
    xs = [p[0] for p in P]
    if len(set(xs)) < len(xs):
        ys = [p[1] for p in P]; Y = max(abs(Fraction(y)) for y in ys) + 1
        for d in itertools.count(1):
            eps = Fraction(1, 1000 * d) / Y
            Q = [(Fraction(x) / (1 + eps * y), Fraction(y) / (1 + eps * y)) for x, y in P]
            if len(set(q[0] for q in Q)) == len(Q): P = Q; break
    if any(isinstance(c, Fraction) for p in P for c in p):
        den = 1
        for p in P:
            for c in p: den = math.lcm(den, Fraction(c).denominator)
        P = [(int(Fraction(x) * den), int(Fraction(y) * den)) for x, y in P]
    P = sorted(P)
    flipped = False
    if orient(P[0], P[1], P[2]) < 0:
        P = sorted((x, -y) for x, y in P); flipped = True
    return P, flipped

def analyse(P, kind, extra):
    rec = {"kind": kind, **extra}
    assert len(P) == 33
    # hypotheses
    gp = general_position(P); rec["gp"] = gp
    if not gp: rec["status"] = "reject_gp"; return rec
    P, flipped = normalize(P); rec["yflip"] = flipped
    xs = [p[0] for p in P]; assert len(set(xs)) == 33
    fails = []
    if not all(P[i][0] == -P[32 - i][0] and P[i][1] == P[32 - i][1] for i in range(33)) or P[16][0] != 0:
        fails.append("not symmetric after normalisation")
    H = hull_idx(P)
    if 16 in H: rec["status"] = "reject_axis_on_hull"; return rec
    # orientation table, 1-based
    Xv = np.zeros(NV + 1, dtype=bool)
    O = {}
    for n_, (i, j, k) in enumerate(TRI, 1):
        o = orient(P[i - 1], P[j - 1], P[k - 1]); assert o != 0
        Xv[n_] = o > 0; O[(i, j, k)] = o > 0
    if not Xv[1]: fails.append("X(1,2,3) false after flip")
    orb_bad = sum(1 for (i, j, k) in TRI if O[(i, j, k)] != O[(34 - k, 34 - j, 34 - i)])
    if orb_bad: fails.append(f"orbit rule + violated on {orb_bad} triples")
    # cup/cap tables (0-based arrays, index = point-1)
    cup = np.zeros((N, N, N), dtype=bool)
    for (i, j, k), v in O.items(): cup[i - 1, j - 1, k - 1] = v
    lt = np.zeros((N, N, N), dtype=bool)
    for i, j, k in TRI: lt[i - 1, j - 1, k - 1] = True
    capT = lt & ~cup; cupT = lt & cup
    ends = {}
    for kn, T in (("cap", capT), ("cup", cupT)):
        Vr = {3: T.copy()}
        for r in range(4, 8):
            # V[r][x,a,b] = OR_w V[r-1][x,w,a] & T[w,a,b]
            Vr[r] = np.einsum('xwa,wab->xab', Vr[r - 1].astype(np.int32), T.astype(np.int32)) > 0
        ends[kn] = Vr
    # independent 7-gon test via chains: cap(x,b,r) & cup(x,b,s), r+s-2 >= 7, or 7-cup/7-cap
    E = {kn: {r: ends[kn][r].any(axis=1) for r in range(3, 8)} for kn in ends}
    hept = bool(E["cap"][7].any() or E["cup"][7].any())
    for r in range(3, 7):
        s = 9 - r
        if 3 <= s <= 6 and (E["cap"][r] & E["cup"][s]).any(): hept = True
    rec["heptagon"] = hept
    # least model of F's auxiliaries
    capV = np.stack([ends["cap"][r] for r in range(3, 7)]); cupV = np.stack([ends["cup"][r] for r in range(3, 7)])
    allV = np.stack([capV, cupV])
    Xv[VV] = allV[VK[:, 0], VK[:, 4] - 3, VK[:, 1] - 1, VK[:, 2] - 1, VK[:, 3] - 1]
    capE = np.stack([E["cap"][r] for r in range(3, 7)]); cupE = np.stack([E["cup"][r] for r in range(3, 7)])
    allE = np.stack([capE, cupE])
    Xv[EV] = allE[EK[:, 0], EK[:, 3] - 3, EK[:, 1] - 1, EK[:, 2] - 1]
    ss, ls = clause_sat(Xv)
    oo_viol = int((~ss & orient_only).sum()) + sum(1 for s in ls if not s)
    if oo_viol: fails.append(f"{oo_viol} orientation-only clauses of F violated")
    def_viol = int((~ss & ~orient_only & ~forbid).sum())
    if def_viol: fails.append(f"{def_viol} auxiliary-definition clauses violated by least model")
    fb_viol = int((~ss & forbid).sum()); rec["forbid_viol"] = fb_viol
    if (fb_viol > 0) != hept: fails.append(f"7-gon encoding disagrees: forbidding violated {fb_viol}, chain test {hept}")
    if not hept and (oo_viol or def_viol or fb_viol): fails.append("heptagon-free set violates F")
    # hull and case
    Hp = [h + 1 for h in H]; rec["hull_size"] = len(Hp)
    if 1 not in Hp or 33 not in Hp: fails.append("1 or 33 not on hull")
    y0 = P[0][1]
    Ue = tuple(sorted(a for a in range(2, 17) if a in Hp and P[a - 1][1] > y0))
    Le = tuple(sorted(a for a in range(2, 17) if a in Hp and P[a - 1][1] < y0))
    if any(a in Hp and P[a - 1][1] == y0 for a in range(2, 17)): fails.append("hull pair at chord height")
    for a in range(2, 17):
        if (a in Hp) != ((34 - a) in Hp): fails.append("hull not mirror symmetric")
    v = Xv[np.abs(CU)]; v = np.where(CU > 0, v, ~v); sat = np.nonzero(v.all(axis=1))[0]
    satc = [CASES[i] for i in sat]
    if len(Hp) <= 6:
        exp = (Ue, Le); rec["case"] = ("U" + "-".join(map(str, Ue)) + "_L" + "-".join(map(str, Le)))
        if exp not in CASES: fails.append(f"hull {Hp} gives no listed case {exp}")
        if satc != [exp]: fails.append(f"cubes satisfied {satc}, expected [{exp}]")
        # hull order check against the note's ccw order
        if exp in CASES:
            Hn = M.hull(*exp); r0 = Hp.index(1)
            if Hp[r0:] + Hp[:r0] != Hn: fails.append(f"hull order {Hp} vs note {Hn}")
    else:
        if satc: fails.append(f"hull size {len(Hp)} but cubes satisfied {satc}")
        if not hept: fails.append("hull >= 8 vertices but no 7-gon found")
    rec["fails"] = fails; rec["status"] = "FAIL" if fails else "ok"
    if fails: rec["points"] = P
    return rec

# ---------- generators ----------
R = random.Random(SEED)
def inside(poly, p):
    return all(orient(poly[i], poly[(i + 1) % len(poly)], p) > 0 for i in range(len(poly)))

def sym_hull(nup, nlow, S=10**6, pairs=None):
    """symmetric convex polygon: endpoints (+-S,0), nup upper pairs, nlow lower pairs, ccw"""
    def angs(n, lo, hi):
        return sorted(R.uniform(lo, hi) for _ in range(n))
    import math
    up = [(round(S * math.cos(t)), round(R.uniform(0.3, 1.5) * S * math.sin(t))) for t in angs(nup, 0.15, 1.45)]
    lo = [(round(S * math.cos(t)), -round(R.uniform(0.3, 1.5) * S * math.sin(t))) for t in angs(nlow, 0.15, 1.45)]
    # ccw: (-S,0) lower chain left->right, (S,0), upper right->left
    lower = [(-S, 0)] + [(-x, y) for x, y in sorted(lo, key=lambda p: -p[0])] + [(x, y) for x, y in sorted(lo)] + [(S, 0)]
    upper = [(S, 0)] + [(x, y) for x, y in sorted(up, key=lambda p: -p[0])] + [(-x, y) for x, y in sorted(up)] + [(-S, 0)]
    poly = lower + upper[1:-1]
    return poly, up, lo

def fill(poly, hullhalf, S):
    """add symmetric interior points so the total is 33; returns half (x>0) list + axis y"""
    half = [p for p in hullhalf if p[0] > 0]
    ys = [p[1] for p in poly]
    tries = 0
    while len(half) < 16:
        tries += 1
        if tries > 100000: return None
        p = (R.randint(1, S - 1), R.randint(min(ys), max(ys)))
        if inside(poly, p) and inside(poly, (-p[0], p[1])) and all(q[0] != p[0] for q in half): half.append(p)
    while True:
        tries += 1
        if tries > 200000: return None
        ay = R.randint(min(ys), max(ys))
        if inside(poly, (0, ay)): return half, ay

def gen_hull_kind():
    k = R.choice([1, 2]); nup = R.randint(0, k); nlow = k - nup
    S = 10**6; poly, up, lo = sym_hull(nup, nlow, S)
    hh = [(S, 0)] + up + lo
    r = fill(poly, hh, S)
    if r is None: return None
    half, ay = r
    return mirror_set(half, ay), {"intended": [nup, nlow]}

def gen_uniform():
    S = R.choice([100, 10**4, 10**6])
    half = []
    while len(half) < 16:
        p = (R.randint(1, S), R.randint(-S, S))
        if all(q[0] != p[0] for q in half): half.append(p)
    return mirror_set(half, R.randint(-S, S)), {"S": S}

def gen_degenerate():
    sub = R.choice(["chord", "edge", "axis", "xclose", "xequal"])
    S = 10**6; k = R.choice([1, 2]); nup = R.randint(0, k); nlow = k - nup
    poly, up, lo = sym_hull(nup, nlow, S)
    if sub == "chord":
        # make one hull pair almost at chord height
        if up: x, y = up[0]; up[0] = (x, R.randint(1, 3))
        elif lo: x, y = lo[0]; lo[0] = (x, -R.randint(1, 3))
        lower = [(-S, 0)] + [(-x, y) for x, y in sorted(lo, key=lambda p: -p[0])] + [(x, y) for x, y in sorted(lo)] + [(S, 0)]
        upper = [(S, 0)] + [(x, y) for x, y in sorted(up, key=lambda p: -p[0])] + [(-x, y) for x, y in sorted(up)] + [(-S, 0)]
        poly = lower + upper[1:-1]
    hh = [(S, 0)] + up + lo
    half = [p for p in hh if p[0] > 0]
    if sub == "edge":
        # interior points just inside hull edges (offset 1..3 units inward along the normal direction)
        for _ in range(R.randint(2, 6)):
            i = R.randrange(len(poly)); a, b = poly[i], poly[(i + 1) % len(poly)]
            t = Fraction(R.randint(1, 999), 1000)
            px, py = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
            nx, ny = -(b[1] - a[1]), b[0] - a[0]  # inward normal (left of ccw edge)
            L = max(abs(nx), abs(ny)); d = R.randint(1, 3)
            p = (round(px + d * nx / L), round(py + d * ny / L))
            if p[0] < 0: p = (-p[0], p[1])
            if p[0] > 0 and inside(poly, p) and all(q[0] != p[0] for q in half) and len(half) < 16: half.append(p)
    ys = [p[1] for p in poly]
    tries = 0
    while len(half) < 16:
        tries += 1
        if tries > 100000: return None
        p = (R.randint(1, S - 1), R.randint(min(ys), max(ys)))
        if sub == "xclose" and half and R.random() < 0.5:
            q = R.choice(half); p = (q[0] + R.choice([-1, 1]), q[1] + R.randint(-S // 3, S // 3))
        if sub == "xequal" and half and R.random() < 0.3:
            q = R.choice(half); p = (q[0], q[1] + R.randint(-S // 3, S // 3))
        if p[0] > 0 and inside(poly, p) and inside(poly, (-p[0], p[1])) and (sub == "xequal" or all(q[0] != p[0] for q in half)) and p not in half:
            half.append(p)
    if sub == "axis":
        # axis point just inside the hull edge crossing the axis (top or bottom)
        top = [i for i in range(len(poly)) if poly[i][0] > 0 and poly[(i + 1) % len(poly)][0] < 0][0]
        bot = [i for i in range(len(poly)) if poly[i][0] < 0 and poly[(i + 1) % len(poly)][0] > 0][0]
        i = R.choice([top, bot]); a, b = poly[i], poly[(i + 1) % len(poly)]
        yb = Fraction(a[1]) + Fraction(-a[0], b[0] - a[0]) * (b[1] - a[1])
        ay = (int(yb) - R.randint(1, 3)) if i == top else (int(yb) + R.randint(1, 3))
    else:
        while True:
            tries += 1
            if tries > 200000: return None
            ay = R.randint(min(ys), max(ys))
            if inside(poly, (0, ay)): break
    return mirror_set(half, ay), {"sub": sub, "intended": [nup, nlow]}

K7 = [list(map(int, l.split()[4:])) for l in open(K7)]
def gen_k7():
    row = R.choice(K7); pts = [(row[2 * i], row[2 * i + 1]) for i in range(32)]
    if R.random() < 0.5: pts = [(y, x) for x, y in pts]
    pts.sort()
    mode = R.choice(["left16", "random16"])
    sel = pts[:16] if mode == "left16" else R.sample(pts, 16)
    span = max(abs(c) for p in pts for c in p) + 1
    gap = R.randint(1, span)
    cx = max(p[0] for p in sel) + gap
    half = []
    for x, y in sel:
        p = (cx - x + R.randint(-2, 2) * 0, y + R.randint(-3, 3))
        if p[0] <= 0: p = (1, p[1])
        while any(q[0] == p[0] for q in half): p = (p[0] + 1, p[1])
        half.append(p)
    ys = [y for _, y in half]
    P0 = mirror_set(half, 0)
    poly = [P0[i] for i in hull_idx(P0)]
    for _ in range(10000):
        ay = R.randint(min(ys), max(ys))
        if inside(poly, (0, ay)): return mirror_set(half, ay), {"mode": mode}
    return None


TCOUNT = [0]
def gen_targeted():
    """aim at case CASES[t mod 450]: hull vertices at the x-ranks of the labels, on a parabola"""
    U, L = CASES[TCOUNT[0] % len(CASES)]; TCOUNT[0] += 1
    S = 10**6
    xs = sorted(R.sample(range(1, S), 16), reverse=True)   # xs[a-1] = |x| of label a (a = 1..16)
    X = xs[0]
    def xof(a): return -xs[a - 1]
    k = Fraction(R.randint(1, 3), X)
    up = [(xof(a), int(k * (X * X - xof(a) ** 2)) + 1) for a in U]
    lo = [(xof(a), -int(k * (X * X - xof(a) ** 2)) - 1) for a in L]
    up_all = sorted([(-X, 0)] + up + [(-x, y) for x, y in up] + [(X, 0)])
    lo_all = sorted([(-X, 0)] + lo + [(-x, y) for x, y in lo] + [(X, 0)])
    def interp(chain, x):
        for (x0, y0), (x1, y1) in zip(chain, chain[1:]):
            if x0 <= x <= x1: return Fraction(y0) + Fraction(x - x0, x1 - x0) * (y1 - y0)
    half = [(-xof(a), y) for a, y in [(a, None) for a in []]]
    hv = {a: y for (x, y), a in zip(up, U)}; hv.update({a: y for (x, y), a in zip(lo, L)})
    pts = []
    for a in range(1, 17):
        x = xof(a)
        if a == 1: pts.append((X, 0)); continue
        if a in hv: pts.append((-x, hv[a])); continue
        ylo, yhi = interp(lo_all, x), interp(up_all, x)
        if yhi - ylo < 3: return None
        pts.append((-x, R.randint(int(ylo) + 1, int(yhi) - 1)))
    ylo, yhi = interp(lo_all, 0), interp(up_all, 0)
    if yhi - ylo < 3: return None
    return mirror_set(pts, R.randint(int(ylo) + 1, int(yhi) - 1)), {"target": "U" + "-".join(map(str, U)) + "_L" + "-".join(map(str, L))}

GEN = {"targeted": gen_targeted, "hull46": gen_hull_kind, "uniform": gen_uniform, "degenerate": gen_degenerate, "k7mirror": gen_k7}
import os
if os.environ.get("KINDS"): GEN = {k: v for k, v in GEN.items() if k in os.environ["KINDS"].split(",")}
with open(OUT, "w") as out:
    for kind, g in GEN.items():
        got = 0; att = 0
        while got < NPER:
            att += 1
            r = g()
            if r is None: continue
            P, extra = r
            rec = analyse(P, kind, extra)
            if rec["status"].startswith("reject"): out.write(json.dumps({"kind": kind, "status": rec["status"]}) + "\n"); continue
            if R.random() < 0.02 and rec["status"] == "ok":
                Pn, _ = normalize(P); ang = has_k_gon_angular(Pn)
                rec["angular_check"] = ang
                if ang != rec["heptagon"]: rec["status"] = "FAIL"; rec["fails"].append(f"angular 7-gon {ang} vs chain {rec['heptagon']}")
            out.write(json.dumps(rec) + "\n"); out.flush(); got += 1
