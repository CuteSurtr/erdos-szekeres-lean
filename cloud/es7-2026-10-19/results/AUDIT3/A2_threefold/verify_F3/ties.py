#!/usr/bin/env python3
"""F3 check: does the threefold base encoding (C3a chain CNF, c3cnf.py default options) need
"no two points of S share an x-coordinate in the frame of l"?

Own exact geometry: Eisenstein integer coordinates (a, b) = a + b*w, w = exp(2 pi i / 3).  The map to
the plane (a, b) -> (a - b/2, b*sqrt(3)/2) is linear with determinant sqrt(3)/2 > 0, so every
orientation sign is the sign of the integer determinant in (a, b).  Euclidean inner product times 2:
dotE2(p, q) = 2 pa qa - pa qb - pb qa + 2 pb qb (an integer).

Frame of l (C3-S normal form): d = direction of l = +y axis, +x axis = d turned by -90 degrees, so
  x(q) = det_E(q, d) = (sqrt3/2) det_ab(q, d)         -> we use xt(q) = det_ab(q, d)
  y(q) = <q, d>_E                                     -> we use yt(q) = dotE2(q, d)
(positive rescalings of each axis: they change no label, no sigma, no x-order, no inversion and
no orientation of S or of phi(S)).  phi(S) = {(yt/xt, 1/xt)} exactly with Fractions.

For each 3-fold set and each canonical gap (C3-S Lemma 2: label 0 a hull vertex, sigma_0 = 0, the
second hull residue a <= m // 2), l is placed
  * PARALLEL TO A SEGMENT of S lying strictly inside the gap (so some pairs share an x-coordinate), and
  * at a generic direction of the same gap (all x distinct; the documented case).
The true assignment of every C3a variable is computed from coordinates:
  C = chi' (orientation of phi(S) on label-sorted triples), s = sigma, inv_ij = [1/x_i > 1/x_j]
  (strict), B_ij = inv_ij ^ sigma_i ^ sigma_j (its defining parity; with a tie this is "the larger
  label comes first"), T = chi_S, Y and W as least fixpoint.
Checks:
  (1) every non-gon clause of C3Enc(m, k) true; no conflict in the orbit-shared variables;
  (2) gon clauses all true  <=>  no k points in convex position (exact DP, self-tested by brute force);
  (3) chain equality: max over x of (longest chain, least fixpoint, any length) + 1 == largest convex
      subset; no chain of length >= n (would mean a cycle);
  (4) layer-path units (hullcase.layer_clauses of every prefix of the true layer path) true;
  (5) labels, sigma, chi', T and the layer path are identical for every direction in the gap, while
      inv and B may differ;
  (6) B by parity == [x_i < x_j] whenever x_i != x_j, and == "larger label first" on ties.
usage: ties.py selftest
       ties.py random SEED NSETS m k [k ...]
       ties.py file PATH m k [--drop-centre] [--subsets NSUB SEED MMIN]
       ties.py basesha            (generate C3Enc(11, 7) streaming, print sha256 of the DIMACS text)
"""
import functools
import hashlib
import itertools
import json
import math
import os
import random
import sys
import time
from array import array
from fractions import Fraction

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from c3cnf import C3Enc  # noqa: E402  (code under test, byte-identical copy)
import hullcase  # noqa: E402  (code under test, byte-identical copy)


# ------------------------------------------------------------------ exact geometry (own code)
def det2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def orient(p, q, r):
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)


def rot(p):  # +120 degrees
    return (-p[1], p[0] - p[1])


def dotE2(p, q):
    return 2 * p[0] * q[0] - p[0] * q[1] - p[1] * q[0] + 2 * p[1] * q[1]


def general_position(S):
    for p, q in itertools.combinations(S, 2):
        if det2(p, q) == 0:  # collinear with the centre (also p == q or p == 0)
            return False
    for p, q, r in itertools.combinations(S, 3):
        if orient(p, q, r) == 0:
            return False
    return True


def hull_ccw(P):
    """vertices of conv(P) in ccw order (general position), Andrew's monotone chain on (a, b)."""
    Q = sorted(set(P))
    if len(Q) <= 2:
        return Q
    lo, up = [], []
    for p in Q:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(Q):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def hull_brute(P):
    """hull vertex set by definition (an edge has all other points strictly left)."""
    H = set()
    for p in P:
        for q in P:
            if p != q and all(orient(p, q, r) > 0 for r in P if r != p and r != q):
                H |= {p, q}
    return H


def largest_convex(P, witness=False):
    """size of a largest subset in convex position (exact DP over the lowest vertex);
    with witness=True also return one such polygon (ccw vertex list)."""
    n = len(P)
    if n <= 3:
        return (n, list(P)) if witness else n
    best, wit = 3, None
    for p0 in P:
        Q = [q for q in P if (q[1], q[0]) > (p0[1], p0[0])]
        Q.sort(key=functools.cmp_to_key(lambda u, v: -orient(p0, u, v)))
        r = len(Q)
        f = [[0] * r for _ in range(r)]
        par = [[-1] * r for _ in range(r)]
        for j in range(r):
            for i in range(j):
                if orient(p0, Q[i], Q[j]) <= 0:
                    continue
                v, ph = 3, -1
                for h in range(i):
                    if f[h][i] and orient(Q[h], Q[i], Q[j]) > 0 and f[h][i] + 1 > v:
                        v, ph = f[h][i] + 1, h
                f[i][j], par[i][j] = v, ph
                if orient(Q[i], Q[j], p0) > 0 and (v > best or wit is None):
                    best = max(best, v)
                    if witness and v >= best:
                        poly, a, b = [Q[j]], i, j
                        while a != -1:
                            poly.append(Q[a])
                            a, b = par[a][b], a
                        poly.append(p0)
                        wit = poly[::-1]
    if witness:
        assert len(wit) == best and len(hull_ccw(wit)) == best
        return best, wit
    return best


def largest_convex_brute(P):
    n = len(P)
    for s in range(n, 2, -1):
        for T in itertools.combinations(P, s):
            if len(hull_ccw(list(T))) == s:
                return s
    return min(n, 2)


# ------------------------------------------------------------------ frames and labellings
def updir(q):
    return q if (q[1] > 0 or (q[1] == 0 and q[0] > 0)) else (-q[0], -q[1])


def line_order(S):
    """indices of S sorted by the angle in [0, 180) of the line through c."""
    return sorted(range(len(S)), key=functools.cmp_to_key(
        lambda i, j: -1 if det2(updir(S[i]), updir(S[j])) > 0 else 1))


def gap_before(S, order, p):
    """(u, w): the open cone of directions strictly between the previous line and the line of p,
    det(u, w) > 0; every line direction in the cone has p's line as the first line ccw after it."""
    j = order.index(S.index(p))
    if j == 0:
        u, w = updir(S[order[-1]]), tuple(-x for x in updir(p))
    else:
        u, w = updir(S[order[j - 1]]), updir(p)
    assert det2(u, w) > 0
    return u, w


def in_cone(u, w, s):
    return det2(u, s) > 0 and det2(s, w) > 0


def tie_directions(S, u, w):
    """distinct line directions of segments of S strictly inside the cone (u, w)."""
    out = {}
    for p, q in itertools.combinations(S, 2):
        s = (q[0] - p[0], q[1] - p[1])
        for t in (s, (-s[0], -s[1])):
            if in_cone(u, w, t):
                g = math.gcd(abs(t[0]), abs(t[1]))
                out[(t[0] // g, t[1] // g)] = True
    return list(out)


def generic_direction(S, u, w, rng):
    for _ in range(2000):
        al, be = rng.randint(1, 60), rng.randint(1, 60)
        d = (al * u[0] + be * w[0], al * u[1] + be * w[1])
        xs = [det2(q, d) for q in S]
        if 0 not in xs and len(set(xs)) == len(xs):
            return d
    return None


class Frame:
    """labelling of S for the line l with direction d (oriented so that p has x > 0)."""

    def __init__(self, S, m, d, p):
        n = 3 * m
        if det2(p, d) < 0:
            d = (-d[0], -d[1])  # same line, frame turned by 180 degrees (= Lemma 2(b))
        self.d = d
        xt = {q: det2(q, d) for q in S}
        yt = {q: dotE2(q, d) for q in S}
        assert all(v != 0 for v in xt.values()), "l meets S"
        key = {q: Fraction(yt[q], xt[q]) for q in S}
        assert len(set(key.values())) == n
        self.lab = sorted(S, key=lambda q: key[q])
        self.idx = {q: i for i, q in enumerate(self.lab)}
        assert self.lab[0] == p, "label 0 is not p"
        for i, q in enumerate(self.lab):
            assert self.idx[rot(q)] == (i - m) % n, "R(i) != i - m"
        self.x = [xt[q] for q in self.lab]
        self.sig = [int(v < 0) for v in self.x]
        assert self.sig[0] == 0
        for r in range(m):
            assert self.sig[r + m] == 1 - self.sig[r] and self.sig[r + 2 * m] == self.sig[r], "sigma pattern"
        X = [key[q] for q in self.lab]
        Y = [Fraction(1, v) for v in self.x]
        self.chip, self.chis = {}, {}
        for i, j, k in itertools.combinations(range(n), 3):
            dd = (X[j] - X[i]) * (Y[k] - Y[i]) - (Y[j] - Y[i]) * (X[k] - X[i])
            assert dd != 0
            self.chip[(i, j, k)] = 1 if dd > 0 else -1
            self.chis[(i, j, k)] = orient(self.lab[i], self.lab[j], self.lab[k])
        self.inv, self.B, self.ties = {}, {}, []
        for i, j in itertools.combinations(range(n), 2):
            self.inv[(i, j)] = int(Y[i] > Y[j])
            b = self.inv[(i, j)] ^ self.sig[i] ^ self.sig[j]
            self.B[(i, j)] = b
            if self.x[i] == self.x[j]:
                self.ties.append((i, j))
                assert b == 0, "tie: B should put the larger label first"
            else:
                assert b == int(self.x[i] < self.x[j]), "B != strict x-order"


def layer_path(F, m):
    rest = list(F.lab)
    path = []
    while rest:
        H = hull_ccw(rest) if len(rest) > 3 else list(rest)
        res = sorted({F.idx[q] % m for q in H})
        assert len(H) == 3 * len(res), "layer is not a union of orbits"
        if len(res) > 2:
            break  # >= 9-point layer: no unit clauses (the set has a 9-gon)
        path.append([(res[0], None)] if len(res) == 1 else [(r, F.sig[r]) for r in res])
        Hs = set(H)
        rest = [q for q in rest if q not in Hs]
    if path:
        path[0] = [(r, F.sig[r]) for r, _ in path[0]]
    return path


def canonical_gaps(S, m):
    """(p, (u, w)) for every hull vertex p that can be label 0 of a canonical labelling."""
    H = hull_ccw(S)
    order = line_order(S)
    out = []
    for p in H:
        u, w = gap_before(S, order, p)
        out.append((p, (u, w)))
    return H, out


# ------------------------------------------------------------------ encoder evaluation
class Sink:
    def __init__(self):
        self.lits = array("i")
        self.lens = array("i")

    def append(self, c):
        self.lits.extend(c)
        self.lens.append(len(c))

    def __len__(self):
        return len(self.lens)


class Enc:
    def __init__(self, m, k):
        e = C3Enc(m, k)
        e.clauses = Sink()
        e.build()
        self.e = e
        self.m, self.k, self.n = m, k, 3 * m
        lens = np.frombuffer(e.clauses.lens, dtype=np.int32).astype(np.int64)
        self.lits = np.frombuffer(e.clauses.lits, dtype=np.int32).astype(np.int64)
        self.starts = np.concatenate([[0], np.cumsum(lens)[:-1]])
        self.nclauses = len(lens)
        self.secs = e.sections
        self.gon_start = [s for s in e.sections if s[0] == "gon"][0][1]
        assert self.gon_start + [s for s in e.sections if s[0] == "gon"][0][2] == self.nclauses
        self.Wkeys = {}
        for (r, x, a, b), v in e.W.items():
            self.Wkeys.setdefault(r, []).append((x, a, b, v))
        self.Ykeys = {}
        for (x, b, c), v in e.Y.items():
            self.Ykeys.setdefault(x, []).append((b, c, v))

    def section_of(self, ci):
        for name, st, cnt in self.secs:
            if st <= ci < st + cnt:
                return name
        return "?"

    def evaluate(self, F):
        e, n, k = self.e, self.n, self.k
        A = np.zeros(e.nv + 1, dtype=bool)
        setv = {}
        conflicts = []

        def setlit(lit, val, what):
            v, want = abs(lit), (val if lit > 0 else not val)
            if setv.get(v, want) != want:
                conflicts.append(what)
            setv[v] = want
            A[v] = want

        for t, lit in e.C.items():
            setlit(lit, F.chip[t] > 0, ("C", t))
        for i in range(n):
            setlit(e.sig(i), bool(F.sig[i]), ("s", i))
        for p, v in e.inv.items():
            setlit(v, bool(F.inv[p]), ("inv", p))
        for p, v in e.Bv.items():
            setlit(v, bool(F.B[p]), ("B", p))
        for t, lit in e.T.items():
            setlit(lit, F.chis[t] > 0, ("T", t))
        ccw = np.zeros((n, n, n), dtype=bool)
        for (i, j, l), s in F.chis.items():
            for (a, b, c), sg in (((i, j, l), 1), ((j, l, i), 1), ((l, i, j), 1),
                                  ((j, i, l), -1), ((i, l, j), -1), ((l, j, i), -1)):
                ccw[a, b, c] = (s * sg) > 0
        bef = np.zeros((n, n), dtype=bool)
        for (i, j), b in F.B.items():
            bef[i, j] = bool(b)
            bef[j, i] = not b
        ccw_i = ccw.astype(np.int32)
        maxlen = []
        cycle = False
        Wr = {}
        for x in range(n):
            Y = bef[x][None, :] & ccw[x]
            np.fill_diagonal(Y, False)
            Y[x, :] = False
            Y[:, x] = False
            W = bef[x][:, None] & Y  # W2
            best = 2 if W.any() else (1 if bef[x].any() else 0)
            r = 2
            while W.any():
                if r <= k - 2:
                    Wr[(r, x)] = W
                if r >= n:
                    cycle = True
                    break
                best = r
                W = (np.einsum("ab,abc->bc", W.astype(np.int32), ccw_i) > 0) & Y
                r += 1
            maxlen.append(best)
            for b, c, v in self.Ykeys[x]:
                A[v] = Y[b, c]
        for r, lst in self.Wkeys.items():
            for x, a, b, v in lst:
                W = Wr.get((r, x))
                A[v] = bool(W[a, b]) if W is not None else False
        val = A[np.abs(self.lits)] ^ (self.lits < 0)
        sat = np.logical_or.reduceat(val, self.starts)
        bad = np.nonzero(~sat[:self.gon_start])[0]
        gon_ok = bool(sat[self.gon_start:].all())
        return {"conflicts": conflicts[:5], "bad_core": int(len(bad)),
                "bad_sections": sorted({self.section_of(int(c)) for c in bad[:50]}),
                "gon_ok": gon_ok, "chain_max_polygon": max(maxlen) + 1, "cycle": cycle, "A": A}


def unit_ok(enc, F, path, A):
    e, m = enc.e, enc.m
    bad = tot = 0
    for j in range(len(path)):
        for c in hullcase.layer_clauses(m, path[:j + 1], e.ccw, e.sig):
            tot += 1
            if not any(A[abs(l)] ^ (l < 0) for l in c):
                bad += 1
    return bad, tot


# ------------------------------------------------------------------ point sets
def to_eis(x, y, scale):
    b = round(2 * y / math.sqrt(3) * scale)
    a = round(x * scale + b / 2)
    return (a, b)


def random_set(m, rng):
    while True:
        shape = rng.choice(["disk", "thin", "thin", "cluster", "far", "far", "nested", "spiral"])
        reps = []
        for t in range(m):
            if shape == "disk":
                r, th = math.sqrt(rng.random()), rng.uniform(0, 2 * math.pi)
            elif shape == "thin":
                r, th = rng.uniform(0.3, 1.0), rng.gauss(0.0, 0.02)
            elif shape == "cluster":
                cx, cy = (0.6, 0.1) if t % 2 else (0.2, 0.5)
                x, y = cx + rng.gauss(0, 0.08), cy + rng.gauss(0, 0.08)
                r, th = math.hypot(x, y), math.atan2(y, x)
            elif shape == "far":  # 1 or 2 far points: hull 3 or 6 likely
                if t < (1 if m < 4 else rng.choice([1, 2])):
                    r, th = rng.uniform(0.9, 1.0), rng.uniform(0, 2 * math.pi)
                else:
                    r, th = rng.uniform(0.02, 0.25), rng.gauss(0.5, 0.3)
            elif shape == "nested":
                r, th = 10 ** rng.uniform(-1.5, 0), rng.uniform(0, 2 * math.pi)
            else:
                r, th = 0.1 + 0.9 * (t + rng.random()) / m, 2.4 * t + rng.gauss(0, 0.2)
            reps.append(to_eis(r * math.cos(th), r * math.sin(th), rng.choice([400, 1500, 6000])))
        S = []
        for p in reps:
            S += [p, rot(p), rot(rot(p))]
        if general_position(S):
            return S, shape


def read_set(path, drop_centre):
    pts = []
    for line in open(path):
        t = line.split()
        if len(t) >= 2:
            pts.append((int(t[0]), int(t[1])))
    if drop_centre:
        pts = [p for p in pts if p != (0, 0)]
    assert (0, 0) not in pts
    orbits = []
    seen = set()
    for p in pts:
        if p in seen:
            continue
        o = [p, rot(p), rot(rot(p))]
        assert all(q in pts for q in o), "not 3-fold symmetric"
        seen |= set(o)
        orbits.append(p)
    return orbits


def from_reps(reps):
    S = []
    for p in reps:
        S += [p, rot(p), rot(rot(p))]
    return S


# ------------------------------------------------------------------ driver
def norm_dir(s):
    g = math.gcd(abs(s[0]), abs(s[1]))
    return (s[0] // g, s[1] // g)


def priority_segments(S, wit):
    """segments of convex polygons: the edges of a maximum convex polygon, then of every convex layer."""
    segs = [(wit[i], wit[(i + 1) % len(wit)]) for i in range(len(wit))]
    rest = list(S)
    while len(rest) >= 3:
        Hc = hull_ccw(rest)
        segs += [(Hc[i], Hc[(i + 1) % len(Hc)]) for i in range(len(Hc))]
        Hs = set(Hc)
        rest = [q for q in rest if q not in Hs]
    return segs


def chain_max(F, m, drop_ties):
    """per-x longest chain (least fixpoint of the Y/W recursion, any length); drop_ties=True removes
    the tied pairs from the B relation in both directions (a strict x-order relation)."""
    n = 3 * m
    ccw = np.zeros((n, n, n), dtype=bool)
    for (i, j, l), s in F.chis.items():
        for (a, b, c), sg in (((i, j, l), 1), ((j, l, i), 1), ((l, i, j), 1),
                              ((j, i, l), -1), ((i, l, j), -1), ((l, j, i), -1)):
            ccw[a, b, c] = (s * sg) > 0
    bef = np.zeros((n, n), dtype=bool)
    for (i, j), bb in F.B.items():
        bef[i, j] = bool(bb)
        bef[j, i] = not bb
    if drop_ties:
        for (i, j) in F.ties:
            bef[i, j] = bef[j, i] = False
    ci = ccw.astype(np.int32)
    out = []
    for x in range(n):
        Y = bef[x][None, :] & ccw[x]
        np.fill_diagonal(Y, False)
        Y[x, :] = False
        Y[:, x] = False
        W = bef[x][:, None] & Y
        best = 2 if W.any() else (1 if bef[x].any() else 0)
        r = 2
        while W.any() and r < n:
            best = r
            W = (np.einsum("ab,abc->bc", W.astype(np.int32), ci) > 0) & Y
            r += 1
        out.append(best)
    return out


def angular_transitive(F, m):
    """for every x: ccw(x, ., .) restricted to P_x = {p : B(x, p)} (B by its parity) is a strict total
    order.  This is sufficient for 'every chain from x is a convex polygon' (fan of angle < 180 degrees
    with all turns left).  Returns the number of x where it fails and the number of tied p in P_x."""
    n = 3 * m
    ccw = np.zeros((n, n, n), dtype=bool)
    for (i, j, l), s in F.chis.items():
        for (a, b, c), sg in (((i, j, l), 1), ((j, l, i), 1), ((l, i, j), 1),
                              ((j, i, l), -1), ((i, l, j), -1), ((l, j, i), -1)):
            ccw[a, b, c] = (s * sg) > 0
    bad, tied_in_P = 0, 0
    tset = set(F.ties)
    for x in range(n):
        P = [p for p in range(n) if p != x and (F.B[(x, p)] if x < p else 1 - F.B[(p, x)])]
        tied_in_P += sum(1 for p in P if (min(x, p), max(x, p)) in tset)
        if len(P) < 3:
            continue
        M = ccw[x][np.ix_(P, P)].astype(np.int32)
        # tournament: exactly one of M[a,b], M[b,a] for a != b
        if not np.array_equal(M + M.T, 1 - np.eye(len(P), dtype=np.int32)):
            bad += 1
            continue
        if ((M @ M > 0) & (M == 0) & ~np.eye(len(P), dtype=bool)).any():
            bad += 1
    return bad, tied_in_P


def test_set(S, m, encs, rng, stats, max_tie_dirs=6, tag=""):
    n = 3 * m
    g, wit = largest_convex(S, witness=True)
    H, gaps = canonical_gaps(S, m)
    stats["sets"] += 1
    stats["hull_hist"][len(H)] = stats["hull_hist"].get(len(H), 0) + 1
    stats["g_hist"][g] = stats["g_hist"].get(g, 0) + 1
    psegs = priority_segments(S, wit)
    wit_edges = {norm_dir((q[0] - p[0], q[1] - p[1])) for p, q in psegs[:len(wit)]}
    wit_edges |= {(-a, -b) for a, b in wit_edges}
    for p, (u, w) in gaps:
        dg = generic_direction(S, u, w, rng)
        prio = []
        for s0, s1 in psegs:
            s = (s1[0] - s0[0], s1[1] - s0[1])
            for t in (s, (-s[0], -s[1])):
                if in_cone(u, w, t) and norm_dir(t) not in prio:
                    prio.append(norm_dir(t))
        others = [d for d in tie_directions(S, u, w) if d not in prio]
        rng.shuffle(others)
        tdirs = (prio + others)[:max_tie_dirs]
        frames = []
        for d, kind in [(dg, "generic")] + [(d, "tie") for d in tdirs]:
            if d is None:
                continue
            F = Frame(S, m, d, p)
            frames.append((F, kind, d))
        if not frames:
            continue
        F0 = frames[0][0]
        hres = sorted({F0.idx[q] % m for q in H})
        canonical = len(hres) in (1, 2) and (len(hres) == 1 or hres[1] <= m // 2)
        stats["canonical_gaps"] += int(canonical)
        path0 = layer_path(F0, m) if canonical else None
        for F, kind, d in frames:
            same = (F.lab == F0.lab and F.sig == F0.sig and F.chip == F0.chip and F.chis == F0.chis)
            if not same:
                stats["fail"].append({"tag": tag, "why": "labels/sigma/chi' change inside the gap"})
            if F.inv != F0.inv:
                stats["inv_differs_in_gap"] += 1
            tb, tip = angular_transitive(F, m)
            stats["angular_order_failures"] += tb
            stats["tied_points_inside_some_Px"] += tip
            if tb:
                stats["fail"].append({"tag": tag, "kind": kind, "why": "angular relation on P_x not a total order"})
            if kind == "tie":
                stats["tie_frames"] += 1
                stats["tied_pairs"] += len(F.ties)
                stats["tie_frames_on_max_polygon_edge"] += int(norm_dir(d) in wit_edges)
                if len(F.ties) == 0:
                    stats["fail"].append({"tag": tag, "why": "tie direction without a tie"})
                with_t = chain_max(F, m, drop_ties=False)
                without = chain_max(F, m, drop_ties=True)
                if with_t != without:
                    stats["tie_frames_tie_changes_some_chain"] += 1
                if max(with_t) != max(without):
                    stats["tie_frames_tie_changes_max_chain"] += 1
                if max(without) + 1 != g:
                    stats["tie_frames_strict_relation_misses_max_polygon"] += 1
            else:
                stats["generic_frames"] += 1
                assert not F.ties
            path = None
            if canonical:
                path = layer_path(F, m)
                if path != path0:
                    stats["fail"].append({"tag": tag, "why": "layer path changes inside the gap"})
            for enc in encs:
                r = enc.evaluate(F)
                key = f"{kind}_k{enc.k}"
                st = stats["by"].setdefault(key, {"frames": 0, "gon": 0, "nogon": 0, "units_checked": 0,
                                                  "unit_clauses": 0})
                st["frames"] += 1
                has = g >= enc.k
                st["gon" if has else "nogon"] += 1
                bad_units = 0
                if canonical:
                    bad_units, tot = unit_ok(enc, F, path, r["A"])
                    st["units_checked"] += 1
                    st["unit_clauses"] += tot
                ok = (not r["conflicts"] and r["bad_core"] == 0 and (r["gon_ok"] == (not has))
                      and r["chain_max_polygon"] == g and not r["cycle"] and bad_units == 0)
                if not ok:
                    stats["fail"].append({"tag": tag, "kind": kind, "k": enc.k, "g": g, "ties": len(F.ties),
                                          "conflicts": r["conflicts"], "bad_core": r["bad_core"],
                                          "bad_sections": r["bad_sections"], "gon_ok": r["gon_ok"],
                                          "chain_max_polygon": r["chain_max_polygon"], "cycle": r["cycle"],
                                          "bad_units": bad_units})
    return g


def new_stats():
    return {"sets": 0, "hull_hist": {}, "g_hist": {}, "canonical_gaps": 0, "tie_frames": 0,
            "generic_frames": 0, "tied_pairs": 0, "inv_differs_in_gap": 0,
            "tie_frames_on_max_polygon_edge": 0, "tie_frames_tie_changes_some_chain": 0,
            "tie_frames_tie_changes_max_chain": 0, "tie_frames_strict_relation_misses_max_polygon": 0,
            "angular_order_failures": 0, "tied_points_inside_some_Px": 0, "by": {}, "fail": []}


def main():
    mode = sys.argv[1]
    t0 = time.time()
    if mode == "selftest":
        rng = random.Random(7)
        nt = 0
        for _ in range(300):
            m = rng.randint(1, 4)
            S, _ = random_set(m, rng)
            assert largest_convex(S) == largest_convex_brute(S), S
            assert set(hull_ccw(S)) == hull_brute(S)
            nt += 1
        print(json.dumps({"selftest": "ok", "sets": nt, "secs": round(time.time() - t0, 1)}))
        return
    if mode == "basesha":
        e = C3Enc(11, 7)
        e.clauses = Sink()
        e.build()
        h = hashlib.sha256()
        h.update(f"p cnf {e.nv} {len(e.clauses)}\n".encode())
        lits, lens = e.clauses.lits, e.clauses.lens
        pos = 0
        buf = []
        for L in lens:
            buf.append(" ".join(map(str, lits[pos:pos + L])) + " 0\n")
            pos += L
            if len(buf) >= 100000:
                h.update("".join(buf).encode())
                buf = []
        h.update("".join(buf).encode())
        sec = {s[0]: s[2] for s in e.sections}
        print(json.dumps({"vars": e.nv, "clauses": len(lens), "sha256": h.hexdigest(), "sections": sec,
                          "xsig": e.xsig, "acy": e.acy, "gon": e.gon, "secs": round(time.time() - t0, 1)}))
        return
    if mode == "random":
        seed, nsets, m = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        ks = [int(a) for a in sys.argv[5:]]
        rng = random.Random(seed)
        encs = [Enc(m, k) for k in ks]
        stats = new_stats()
        stats.update({"mode": "random", "seed": seed, "m": m, "ks": ks})
        for t in range(nsets):
            S, shape = random_set(m, rng)
            test_set(S, m, encs, rng, stats, tag=f"{seed}:{t}:{shape}")
        stats["secs"] = round(time.time() - t0, 1)
        print(json.dumps(stats))
        return
    if mode == "file":
        path, m, k = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        drop = "--drop-centre" in sys.argv
        reps = read_set(path, drop)
        rng = random.Random(12345)
        stats = new_stats()
        stats.update({"mode": "file", "path": os.path.basename(path), "k": k})
        if "--subsets" in sys.argv:
            i = sys.argv.index("--subsets")
            nsub, sseed, mmin = int(sys.argv[i + 1]), int(sys.argv[i + 2]), int(sys.argv[i + 3])
            srng = random.Random(sseed)
            encs = {}
            stats["subsets"] = nsub
            for t in range(nsub):
                mm = srng.randint(mmin, len(reps) - 1)
                sub = srng.sample(reps, mm)
                if mm not in encs:
                    encs[mm] = Enc(mm, k)
                test_set(from_reps(sub), mm, [encs[mm]], rng, stats, max_tie_dirs=3, tag=f"sub{t}:m{mm}")
        else:
            assert len(reps) == m
            enc = Enc(m, k)
            test_set(from_reps(reps), m, [enc], rng, stats, max_tie_dirs=40, tag="full")
        stats["secs"] = round(time.time() - t0, 1)
        print(json.dumps(stats))
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
