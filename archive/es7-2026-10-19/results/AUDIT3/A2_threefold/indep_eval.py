#!/usr/bin/env python3
"""A2 audit: independent exact test of the C3a chain encoding, the C3-S layer units and the sigma-cube
units, by evaluating every clause on the TRUE assignment of real 3-fold-symmetric point sets.

Own code (nothing from the repository) for: point generation, exact orientation, convex hulls and
layers, the largest convex subset (DP, self-tested against brute force), the canonical labelling of
C3-S Lemma 2 (line l placed in the gap before a hull vertex, sigma_0 = 0 by reversing l, a <= m//2),
every primary variable computed directly from coordinates (labels, sigma, chi' from phi(S), chi_S,
inv, x-order) and the chain variables Y/W as least fixpoints, and the mirror images.
From the repository: the encoder under test (vendored c3cnf.py, byte-identical) and the unit
generator under test (vendored hullcase.py, byte-identical).

Coordinates: integer Eisenstein pairs (a, b) = a + b*w, w = exp(2 pi i / 3).  The map to the plane,
(a, b) -> (a - b/2, b*sqrt(3)/2), is linear with determinant sqrt(3)/2 > 0, so orientations, convex
position and the cyclic order of lines through c = 0 are exact on the integer pairs.  Rotation by
+120 degrees: (a, b) -> (-b, a - b).  Complex conjugation (a reflection in a line through c):
(a, b) -> (a - b, -b).

usage: indep_eval.py random SEED NSETS m k [m k ...]  |  indep_eval.py file PATH m k [--drop-centre]
       indep_eval.py selftest"""
import functools
import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from c3cnf import C3Enc  # noqa: E402  (code under test)
import hullcase  # noqa: E402  (code under test)


# ----------------------------------------------------------------------------- exact geometry
def det2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def orient(p, q, r):
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)


def rot(p):
    return (-p[1], p[0] - p[1])


def refl(p):
    return (p[0] - p[1], -p[1])


def hull(pts):
    """ccw hull vertices (general position assumed), Andrew's monotone chain."""
    P = sorted(set(pts))
    if len(P) <= 2:
        return P
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def largest_convex(pts):
    """size of the largest subset in convex position (exact; anchor = lowest vertex)."""
    n = len(pts)
    if n <= 3:
        return n
    best = min(n, 3)
    for p0 in pts:
        Q = [q for q in pts if (q[1] > p0[1]) or (q[1] == p0[1] and q[0] > p0[0])]
        if len(Q) < 2:
            continue
        Q.sort(key=functools.cmp_to_key(lambda u, v: -1 if det2((u[0] - p0[0], u[1] - p0[1]), (v[0] - p0[0], v[1] - p0[1])) > 0 else 1))
        k = len(Q)
        f = [[0] * k for _ in range(k)]
        for j in range(k):
            for i in range(j):
                v = 3
                for h in range(i):
                    if f[h][i] and orient(Q[h], Q[i], Q[j]) > 0 and f[h][i] + 1 > v:
                        v = f[h][i] + 1
                f[i][j] = v
                if v > best:
                    best = v
    return best


def brute_has_convex(pts, k):
    for sub in itertools.combinations(pts, k):
        if len(hull(list(sub))) == k:
            return True
    return False


def general_position(S):
    n = len(S)
    if len(set(S)) != n or (0, 0) in S:
        return False
    for i, j in itertools.combinations(range(n), 2):
        if det2(S[i], S[j]) == 0:  # collinear with the centre
            return False
    for i, j, k in itertools.combinations(range(n), 3):
        if orient(S[i], S[j], S[k]) == 0:
            return False
    return True


# ----------------------------------------------------------------------------- random sets
def to_eis(x, y, scale):
    b = 2.0 * y / 3 ** 0.5
    a = x + b / 2.0
    return (int(round(a * scale)), int(round(b * scale)))


def random_set(rng, m):
    shape = rng.choice(["disk", "ring", "clusters", "radial", "spiral", "nested"])
    reps = []
    for t in range(m):
        if shape == "disk":
            while True:
                x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
                if x * x + y * y < 1:
                    break
        elif shape == "ring":
            import math
            r, th = rng.uniform(0.6, 1.0), rng.uniform(0, 2 * math.pi)
            x, y = r * math.cos(th), r * math.sin(th)
        elif shape == "clusters":
            import math
            c = rng.randrange(3)
            cx, cy = [(0.9, 0.1), (-0.3, 0.7), (0.2, -0.5)][c]
            x, y = cx + rng.gauss(0, 0.12), cy + rng.gauss(0, 0.12)
        elif shape == "radial":
            import math
            th = rng.choice([0.3, 1.4, 2.2]) + rng.gauss(0, 0.04)
            r = rng.uniform(0.05, 1.0)
            x, y = r * math.cos(th), r * math.sin(th)
        elif shape == "spiral":
            import math
            r = 0.1 + 0.9 * (t + rng.random()) / m
            th = 2.4 * t + rng.gauss(0, 0.2)
            x, y = r * math.cos(th), r * math.sin(th)
        else:  # nested: radii spread over orders of magnitude, few angles (deep layer paths)
            import math
            r = 10 ** rng.uniform(-1.5, 0)
            th = rng.uniform(0, 2 * math.pi)
            x, y = r * math.cos(th), r * math.sin(th)
        reps.append(to_eis(x, y, rng.choice([300, 1000, 5000])))
    S = []
    for p in reps:
        S += [p, rot(p), rot(rot(p))]
    return S, shape


# ----------------------------------------------------------------------------- canonical labelling
def updir(q):
    return q if (q[1] > 0 or (q[1] == 0 and q[0] > 0)) else (-q[0], -q[1])


def frame_for(S, p, rng):
    """direction d of l (pointing to +y) strictly inside the gap just before the line of p (ccw),
    oriented so that p has x > 0; generic so that all x-coordinates are distinct."""
    order = sorted(range(len(S)), key=functools.cmp_to_key(
        lambda i, j: -1 if det2(updir(S[i]), updir(S[j])) > 0 else 1))
    j = order.index(S.index(p))
    if j == 0:
        u, w = updir(S[order[-1]]), tuple(-x for x in updir(p))
    else:
        u, w = updir(S[order[j - 1]]), updir(p)
    assert det2(u, w) > 0
    for _ in range(1000):
        al, be = rng.randint(1, 50), rng.randint(1, 50)
        d = (al * u[0] + be * w[0], al * u[1] + be * w[1])
        if det2(p, d) < 0:
            d = (-d[0], -d[1])
        xs = [det2(q, d) for q in S]
        if 0 not in xs and len(set(xs)) == len(xs):
            return d
    raise RuntimeError("no generic d")


def labelling(S, d, m):
    n = 3 * m
    e = (d[1], -d[0])
    assert det2(e, d) > 0
    key = {q: Fraction(det2(e, q), det2(q, d)) for q in S}
    lab = sorted(S, key=lambda q: key[q])
    assert len(set(key.values())) == n
    idx = {q: i for i, q in enumerate(lab)}
    # R(i) = (i - m) mod n
    for i, q in enumerate(lab):
        if idx[rot(q)] != (i - m) % n:
            raise AssertionError(("R(i) != i - m", i, idx[rot(q)]))
    sig = [int(det2(q, d) < 0) for q in lab]
    for r in range(m):
        if not (sig[r + m] == 1 - sig[r] and sig[r + 2 * m] == sig[r]):
            raise AssertionError("sigma orbit pattern")
    return lab, idx, sig, e


def layer_path(lab, idx, sig, m):
    rest = list(lab)
    path = []
    while rest:
        H = hull(rest)
        if len(rest) <= 2:
            H = rest
        res = sorted({idx[q] % m for q in H})
        if len(H) != 3 * len(res):
            raise AssertionError("layer not a union of orbits")
        if len(res) == 1:
            path.append([(res[0], None)])
        elif len(res) == 2:
            path.append([(r, sig[r]) for r in res])
        else:
            path.append([(r, sig[r]) for r in res])  # >= 3 orbits: only possible with a big convex layer
        Hs = set(H)
        rest = [q for q in rest if q not in Hs]
    # top layer carries sigma 0 for residue 0 (and sigma_a), as the tree names it
    path[0] = [(r, sig[r]) for r, _ in path[0]]
    return path


def canonical(S, m, rng):
    """all canonical frames (label 0 on the hull, sigma_0 = 0, a <= m//2): list of (d, lab, idx, sig, e, path)."""
    H = hull(S)
    out = []
    for p in H:
        d = frame_for(S, p, rng)
        lab, idx, sig, e = labelling(S, d, m)
        assert lab[0] == p and sig[0] == 0
        hres = sorted({idx[q] % m for q in H})
        if len(hres) == 2 and hres[1] > m // 2:
            continue
        out.append((d, lab, idx, sig, e, layer_path(lab, idx, sig, m)))
    return out


# ----------------------------------------------------------------------------- encoder evaluation
class Enc:
    """C3Enc(m, k) built once; clauses kept as flat int32 arrays."""

    def __init__(self, m, k):
        e = C3Enc(m, k)
        import array
        lits, lens = array.array("i"), array.array("i")

        class Sink:
            def __init__(s):
                s.n = 0

            def append(s, c):
                lits.extend(c)
                lens.append(len(c))
                s.n += 1

            def __len__(s):
                return s.n

        e.clauses = Sink()
        e.build()
        self.e, self.m, self.k = e, m, k
        self.lits = np.frombuffer(lits, dtype=np.int32).copy()
        del lits
        self.lens = np.frombuffer(lens, dtype=np.int32).astype(np.int64)
        self.starts = np.concatenate([[0], np.cumsum(self.lens)[:-1]])
        self.alits = np.abs(self.lits)
        self.neg = self.lits < 0
        self.sec = {nm: (st, cnt) for nm, st, cnt in e.sections}
        self.nv = e.nv
        self.Yk = list(e.Y.items())
        self.Wk = list(e.W.items())

    def assignment(self, lab, sig, d, e2):
        m, n, E = self.m, 3 * self.m, self.e
        P = lab
        X = [det2(q, d) for q in P]           # x up to the positive factor det(e,d)
        Ded = det2(e2, d)
        Xp = [Fraction(det2(e2, q), x) for q, x in zip(P, X)]   # X' = y/x
        Yp = [Fraction(Ded, x) for x in X]                       # Y' = 1/x
        val = np.full(self.nv + 1, -1, dtype=np.int8)
        bad = []

        def setv(lit, truth):
            v, t = abs(lit), int(bool(truth) ^ (lit < 0))
            if val[v] != -1 and val[v] != t:
                bad.append(("orbit/variable conflict", lit))
            val[v] = t

        for t in itertools.combinations(range(n), 3):
            i, j, k = t
            chip = (Xp[j] - Xp[i]) * (Yp[k] - Yp[i]) - (Yp[j] - Yp[i]) * (Xp[k] - Xp[i])
            assert chip != 0
            setv(E.C[t], chip > 0)
            setv(E.T[t], orient(P[i], P[j], P[k]) > 0)
        for r in range(m):
            setv(E.s[r], sig[r])
        for (i, j), v in E.inv.items():
            setv(v, Yp[i] > Yp[j])
        for (i, j), v in E.Bv.items():
            setv(v, X[i] < X[j])
        # chain variables: least fixpoint, from the true B and chi_S
        Bm = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(n):
                if i != j:
                    Bm[i, j] = X[i] < X[j]
        CCW = np.zeros((n, n, n), dtype=bool)
        for i, j, k in itertools.permutations(range(n), 3):
            CCW[i, j, k] = orient(P[i], P[j], P[k]) > 0
        Yarr = Bm[:, None, :] & CCW                      # Y[x,b,c] = B(x,c) and ccw(x,b,c)
        for (x, b, c), v in self.Yk:
            setv(v, Yarr[x, b, c])
        W = {2: Bm[:, :, None] & Yarr}                   # W2[x,a,b] = B(x,a) and Y[x,a,b]
        for r in range(2, self.k - 2):
            tmp = np.einsum("xab,abc->xbc", W[r].astype(np.int32), CCW.astype(np.int32)) > 0
            W[r + 1] = Yarr & tmp
        for (r, x, a, b), v in self.Wk:
            setv(v, W[r][x, a, b])
        unset = int((val[1:] == -1).sum())
        return val, bad, unset

    def evaluate(self, val):
        truth = (val[self.alits] == 1) ^ self.neg
        sat = np.logical_or.reduceat(truth, self.starts)
        g0, gc = self.sec["gon"]
        nongon_false = int((~sat[:g0]).sum() + (~sat[g0 + gc:]).sum())
        gon_false = int((~sat[g0:g0 + gc]).sum())
        return nongon_false, gon_false


def unit_true(val, lit):
    return bool((val[abs(lit)] == 1) ^ (lit < 0))


# ----------------------------------------------------------------------------- one set
def predicted_mirror(path, m):
    top = path[0]
    if len(top) == 1:
        f = lambda L: sorted(((m - r) % m, None if s is None else 1 - s) for r, s in L)  # noqa: E731
    else:
        a, s0 = top[1]
        f = lambda L: sorted(((a - r) % m, None if g is None else g ^ int(r < a) ^ int(s0 == 0)) for r, g in L)  # noqa: E731
    return [top] + [f(L) for L in path[1:]]


def predicted_mirror_mut_nosigma(path, m):
    top = path[0]
    if len(top) == 1:
        f = lambda L: sorted(((m - r) % m, s) for r, s in L)  # noqa: E731
    else:
        a, s0 = top[1]
        f = lambda L: sorted(((a - r) % m, g) for r, g in L)  # noqa: E731
    return [top] + [f(L) for L in path[1:]]


def check_set(S, m, k, enc, rng, frames=1, full_eval=True):
    out = {"m": m, "k": k, "fail": []}
    lc = largest_convex(S)
    out["largest_convex"] = lc
    out["has_kgon"] = lc >= k
    can = canonical(S, m, rng)
    if not can:
        out["fail"].append("no canonical frame")
        return out
    bigtop = len(can[0][5][0]) > 2          # hull with >= 9 points: outside the normal form (has a 9-gon)
    paths = {json.dumps(c[5]) for c in can}
    out["n_canonical_frames"] = len(can)
    out["unique_path"] = len(paths) == 1
    if m % 2 == 1 and not bigtop and len(paths) != 1:
        out["fail"].append("canonical path not unique (m odd)")
    d, lab, idx, sig, e2, path = can[0]
    out["path"] = hullcase.layers_name(path) if all(len(L) <= 2 for L in path) else str(path)
    out["depth"] = len(path)
    bigl = any(len(L) > 2 for L in path)
    out["big_layer"] = bigl
    if bigl and not out["has_kgon"] and k <= 9:
        out["fail"].append("layer with >= 9 points but no k-gon")
    # mirror lemma (H3: Lemma 5, H6: Lemma H6M), with a mutation that must fail somewhere
    Sm = [refl(q) for q in S]
    canm = canonical(Sm, m, rng)
    if not bigl and canm:
        pms = [c[5] for c in canm]
        out["mirror_ok"] = all(predicted_mirror(c[5], m) in pms for c in can)
        out["mirror_mut_nosigma_ok"] = all(predicted_mirror_mut_nosigma(c[5], m) in pms for c in can)
        if not out["mirror_ok"]:
            out["fail"].append("mirror prediction")
        # reduced tree at depth 1: S's layer 2 kept, or M(S)'s
        if len(path) >= 2:
            ks, km = [], []
            for c in can:
                kept = [json.dumps(x) for x in hullcase.tree_children(m, k, [c[5][0]], mirror=True, mirror_h6=True)]
                ks.append(json.dumps(c[5][:2]) in kept)
                pm = predicted_mirror(c[5], m)
                km.append(json.dumps(c[5][:2]) in kept or json.dumps(pm[:2]) in kept)
            out["kept_self"] = all(ks)
            out["kept_self_or_mirror"] = all(km)
            if not out["kept_self_or_mirror"]:
                out["fail"].append("neither S nor M(S) in the reduced tree")
    # every deeper layer is a child of the unreduced tree
    if not bigl:
        for j in range(1, len(path)):
            ch = [json.dumps(c) for c in hullcase.tree_children(m, k, path[:j], mirror=False, mirror_h6=False)]
            if json.dumps(path[:j + 1]) not in ch:
                out["fail"].append(f"layer {j + 1} not a tree child")
    if not full_eval:
        return out
    E = enc.e
    nf = 0
    for fr in range(frames):
        if fr > 0:  # another generic l in a (random) canonical gap
            c = can[rng.randrange(len(can))]
            d = frame_for(S, c[1][0], rng)
            lab, idx, sig, e2 = labelling(S, d, m)
            path = layer_path(lab, idx, sig, m)
        val, bad, unset = enc.assignment(lab, sig, d, e2)
        if bad:
            out["fail"].append(f"variable conflicts {len(bad)}: {bad[:3]}")
        if unset:
            out["fail"].append(f"unset variables {unset}")
        ng, gf = enc.evaluate(val)
        out.setdefault("nongon_false", []).append(ng)
        out.setdefault("gon_false", []).append(gf)
        if ng:
            out["fail"].append(f"non-gon clauses false: {ng}")
        if out["has_kgon"] != (gf > 0):
            out["fail"].append(f"gon clauses: has_kgon={out['has_kgon']} but {gf} false")
        if not bigl:
            # units of every node on the path (these include the top-case hull units and sigma_a)
            nu = 0
            for j in range(1, len(path) + 1):
                for cl in hullcase.layer_clauses(m, path[:j], E.ccw, E.sig):
                    nu += 1
                    if not unit_true(val, cl[0]):
                        nf += 1
            out.setdefault("units_checked", []).append(nu)
            # mutation: reversed ring orders must give false units
            mutf = 0
            for cl in hullcase.layer_clauses(m, path, lambda p, q, r: E.ccw(q, p, r), E.sig):
                if not unit_true(val, cl[0]):
                    mutf += 1
            out.setdefault("mut_reversed_false_units", []).append(mutf)
            if mutf == 0:
                out["fail"].append("reversed-ring mutation not detected")
            # a random sigma cube on the free residues, with the true values, and with one bit flipped
            used = {r for L in path for r, _ in L}
            free = [r for r in range(1, m) if r not in used]
            if free:
                bits = sorted(rng.sample(free, rng.randint(1, len(free))))
                C = [(r, sig[r]) for r in bits]
                name = hullcase.node_name(path, C)
                us = hullcase.node_units(m, name, E.ccw, E.sig)
                f1 = sum(1 for u in us if not unit_true(val, u))
                nf += f1
                Cbad = [(r, v if i else 1 - v) for i, (r, v) in enumerate(C)]
                f2 = sum(1 for u in hullcase.node_units(m, hullcase.node_name(path, Cbad), E.ccw, E.sig) if not unit_true(val, u))
                out.setdefault("mut_flipped_cube_false_units", []).append(f2)
                if f2 != 1:
                    out["fail"].append("flipped cube bit not detected exactly once")
        # mutation: flip one sigma bit in the assignment -> some base clause must fail
        val2 = val.copy()
        rr = rng.randrange(m)
        val2[E.s[rr]] ^= 1
        ng2, _ = enc.evaluate(val2)
        out.setdefault("mut_sigma_flip_nongon_false", []).append(ng2)
        if ng2 == 0:
            out["fail"].append("sigma flip mutation not detected")
    out["false_units"] = nf
    if nf:
        out["fail"].append(f"false node units: {nf}")
    return out


# ----------------------------------------------------------------------------- drivers
def selftest():
    rng = random.Random(1)
    cnt = 0
    for _ in range(300):
        m = rng.randint(2, 4)
        S, _ = random_set(rng, m)
        if not general_position(S):
            continue
        lc = largest_convex(S)
        for k in range(4, 3 * m + 1):
            if brute_has_convex(S, k) != (lc >= k):
                print("DP MISMATCH", S, k, lc)
                return 1
        cnt += 1
    print(json.dumps({"selftest_largest_convex_vs_brute_force_sets": cnt, "mismatches": 0}))
    return 0


def run_random(seed, nsets, mks, logf):
    rng = random.Random(seed)
    encs = {}
    summ = {}
    for i in range(nsets):
        m, k = mks[i % len(mks)]
        if (m, k) not in encs:
            t = time.time()
            encs[(m, k)] = Enc(m, k)
            print(f"built C3Enc({m},{k}): {len(encs[(m, k)].lens)} clauses in {time.time() - t:.1f}s", flush=True)
        while True:
            S, shape = random_set(rng, m)
            if general_position(S):
                break
        r = check_set(S, m, k, encs[(m, k)], rng, frames=2)
        r["shape"] = shape
        logf.write(json.dumps(r) + "\n")
        s = summ.setdefault(f"m{m}k{k}", {"sets": 0, "kgon_free": 0, "fail": 0, "H3": 0, "H6": 0, "max_depth": 0,
                                          "mirror_checked": 0, "mirror_mut_caught": 0, "kept_via_mirror": 0,
                                          "frames": 0})
        s["sets"] += 1
        s["kgon_free"] += (not r.get("has_kgon"))
        s["fail"] += bool(r["fail"])
        if r.get("path", "").startswith("0s0-"):
            s["H6"] += 1
        else:
            s["H3"] += 1
        s["max_depth"] = max(s["max_depth"], r.get("depth", 0))
        if "mirror_ok" in r:
            s["mirror_checked"] += 1
            s["mirror_mut_caught"] += (not r["mirror_mut_nosigma_ok"])
        if r.get("kept_self") is False and r.get("kept_self_or_mirror"):
            s["kept_via_mirror"] += 1
        s["frames"] += len(r.get("nongon_false", []))
        if r["fail"]:
            print("FAIL", json.dumps(r)[:600], flush=True)
    return summ


def main():
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    if sys.argv[1] == "random":
        seed, nsets = int(sys.argv[2]), int(sys.argv[3])
        mks = [(int(a), int(b)) for a, b in zip(sys.argv[4::2], sys.argv[5::2])]
        logp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", f"indep_random_s{seed}.jsonl")
        with open(logp, "w") as lf:
            summ = run_random(seed, nsets, mks, lf)
        print(json.dumps(summ, indent=1))
    elif sys.argv[1] == "subsets":
        # orbit-deleted subsets of a 7-gon-free 3-fold set (deleting whole orbits keeps it 7-gon-free)
        path, k, seed, per = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        msizes = [int(x) for x in sys.argv[6].split(",")]
        pts = [tuple(int(x) for x in l.split()) for l in open(path) if l.strip()]
        pts = [p for p in pts if p != (0, 0)]
        orbs, seen = [], set()
        for p in pts:
            if p in seen:
                continue
            o = [p, rot(p), rot(rot(p))]
            seen |= set(o)
            orbs.append(o)
        rng = random.Random(seed)
        logp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs",
                            f"indep_subsets_{os.path.basename(path).split('.')[0]}_k{k}_s{seed}.jsonl")
        summ = {}
        with open(logp, "w") as lf:
            for mm in msizes:
                enc = Enc(mm, k)
                done = set()
                for _ in range(per):
                    for _t in range(50):
                        pick = tuple(sorted(rng.sample(range(len(orbs)), mm)))
                        if pick not in done:
                            break
                    done.add(pick)
                    S = [q for i in pick for q in orbs[i]]
                    assert general_position(S)
                    r = check_set(S, mm, k, enc, rng, frames=2)
                    r["orbits"] = pick
                    lf.write(json.dumps(r) + "\n")
                    s_ = summ.setdefault(f"m{mm}k{k}", {"sets": 0, "kgon_free": 0, "fail": 0, "paths": set(), "max_depth": 0,
                                                        "frames": 0, "units_checked": 0})
                    s_["sets"] += 1
                    s_["kgon_free"] += (not r["has_kgon"])
                    s_["fail"] += bool(r["fail"])
                    s_["paths"].add(r.get("path"))
                    s_["max_depth"] = max(s_["max_depth"], r.get("depth", 0))
                    s_["frames"] += len(r.get("nongon_false", []))
                    s_["units_checked"] += sum(r.get("units_checked", []))
                    if r["fail"]:
                        print("FAIL", json.dumps(r)[:600], flush=True)
                del enc
        for v in summ.values():
            v["distinct_paths"] = len(v.pop("paths"))
        print(json.dumps(summ, indent=1))
    elif sys.argv[1] == "extend":
        # a 7-gon-free 30-point 3-fold set plus one random orbit -> m = 11 sets (for k = 8, 9 these are
        # usually k-gon-free, so every clause of the m = 11 encoder must be true; for k = 7 any set
        # without a 7-gon would contradict Theorem 1)
        path, seed, nsets = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        ks = [int(x) for x in sys.argv[5].split(",")]
        base = [tuple(int(x) for x in l.split()) for l in open(path) if l.strip()]
        base = [q for q in base if q != (0, 0)]
        assert len(base) == 30
        rng = random.Random(seed)
        encs = {k: Enc(11, k) for k in ks}
        R0 = max(max(abs(a), abs(b)) for a, b in base)
        logp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs",
                            f"indep_extend_{os.path.basename(path).split('.')[0]}_s{seed}.jsonl")
        summ = {}
        with open(logp, "w") as lf:
            for i in range(nsets):
                while True:
                    import math
                    rr = R0 * (10 ** rng.uniform(-1.3, 0.25))
                    th = rng.uniform(0, 2 * math.pi)
                    q = to_eis(rr * math.cos(th), rr * math.sin(th), 1)
                    S = base + [q, rot(q), rot(rot(q))]
                    if general_position(S):
                        break
                for k in ks:
                    r = check_set(S, 11, k, encs[k], rng, frames=2)
                    r["added"] = q
                    lf.write(json.dumps(r) + "\n")
                    s_ = summ.setdefault(f"m11k{k}", {"sets": 0, "kgon_free": 0, "fail": 0, "largest_convex": {}, "H3": 0, "H6": 0,
                                                      "max_depth": 0, "units_checked": 0, "frames": 0, "mirror_checked": 0})
                    s_["sets"] += 1
                    s_["kgon_free"] += (not r["has_kgon"])
                    s_["fail"] += bool(r["fail"])
                    lc = str(r["largest_convex"])
                    s_["largest_convex"][lc] = s_["largest_convex"].get(lc, 0) + 1
                    s_["H3" if r.get("path", "").split("_")[0] == "0s0" else "H6"] += 1
                    s_["max_depth"] = max(s_["max_depth"], r.get("depth", 0))
                    s_["units_checked"] += sum(r.get("units_checked", []))
                    s_["frames"] += len(r.get("nongon_false", []))
                    s_["mirror_checked"] += ("mirror_ok" in r)
                    if r["fail"]:
                        print("FAIL", json.dumps(r)[:600], flush=True)
                    if k == 7 and not r["has_kgon"]:
                        print("NO 7-GON AT 33 POINTS", json.dumps(r)[:600], flush=True)
        print(json.dumps(summ, indent=1))
    elif sys.argv[1] == "file":
        path, m, k = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        pts = [tuple(int(x) for x in l.split()) for l in open(path) if l.strip()]
        if "--drop-centre" in sys.argv:
            pts = [p for p in pts if p != (0, 0)]
        assert len(pts) == 3 * m, len(pts)
        assert set(rot(p) for p in pts) == set(pts), "not invariant under the rotation"
        if "--perturb" in sys.argv:
            # the WLOG step of C3a/C3-S: a small R-equivariant perturbation that keeps every triple
            # orientation (so the order type and the absence of k-gons) and makes no two points
            # collinear with the centre.  Verified exactly below.
            prng = random.Random(11)
            orig = list(pts)
            reps, seen = [], set()
            for q in orig:
                if q not in seen:
                    reps.append(q)
                    seen |= {q, rot(q), rot(rot(q))}
            for attempt in range(100):
                newpos = {}
                for q in reps:
                    q2 = (q[0] * 1000 + prng.randint(-3, 3), q[1] * 1000 + prng.randint(-3, 3))
                    newpos[q], newpos[rot(q)], newpos[rot(rot(q))] = q2, rot(q2), rot(rot(q2))
                new = [newpos[q] for q in orig]
                same = all(orient(orig[i], orig[j], orig[k]) == orient(new[i], new[j], new[k])
                           for i, j, k in itertools.combinations(range(len(orig)), 3))
                if same and general_position(new):
                    print(f"perturbed (attempt {attempt}): all {len(orig) * (len(orig) - 1) * (len(orig) - 2) // 6} triple orientations kept", flush=True)
                    pts = new
                    break
            else:
                raise SystemExit("no good perturbation")
        assert general_position(pts)
        t = time.time()
        enc = Enc(m, k)
        print(f"built C3Enc({m},{k}): {len(enc.lens)} clauses in {time.time() - t:.1f}s", flush=True)
        rng = random.Random(7)
        res = []
        for rep in range(int(os.environ.get("A2_REPS", "3"))):
            r = check_set(pts, m, k, enc, rng, frames=3)
            res.append(r)
            print(json.dumps({x: r.get(x) for x in ("path", "largest_convex", "has_kgon", "n_canonical_frames", "unique_path",
                                                     "mirror_ok", "mirror_mut_nosigma_ok", "kept_self", "kept_self_or_mirror",
                                                     "nongon_false", "gon_false", "false_units", "mut_reversed_false_units",
                                                     "mut_flipped_cube_false_units", "mut_sigma_flip_nongon_false", "fail")}), flush=True)


if __name__ == "__main__":
    main()
