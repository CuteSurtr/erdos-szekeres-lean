#!/usr/bin/env python3
"""Independent check of audit finding A4-1 (even-m sector normal form of symcnf.py / symcnf_layers.py).

Exact integer arithmetic only.  Geometries (centre c = origin):
  m = 2 : Z^2,                      R(x, y) = (-x, -y)
  m = 4 : Z^2 (Gaussian integers),  R(x, y) = (-y, x)
  m = 6 : Eisenstein coordinates (a, b) <-> a + b*omega, R(a, b) = (a - b, a)  (multiplication by e^{i pi/3});
          the map (a, b) -> (a - b/2, b*sqrt(3)/2) is linear with determinant sqrt(3)/2 > 0, so orientations and
          convexity computed from integer (a, b) coordinates are the Euclidean ones.

Checks
 (1) the encoder's even-m sector pattern equals the closed form [-1, +1, ..., +1], and a point satisfies the
     pattern iff it lies in the open sector (0, 2 pi/m) counter-clockwise from the ray c -> (0,0) (exact sweep);
 (2) existence: in random exact m-fold sets in general position, for every choice of orbit 0 and of (0,0),
     every other orbit has exactly one point in that open sector (two independent criteria agree);
 (3) the encoder's own SB unit clauses (symcnf.py, m = 2,4,6; symcnf_layers.py, m = 4,6) hold under the exact
     chirotope of every set labelled this way;
 (4) equivalence on a grid: an orbit has != 1 point in the open sector  iff  one of its points lies on a line
     (0,j)(0,j+m/2) through two points of orbit 0, i.e. three points of S are collinear; and for such
     degenerate sets no labelling of that orbit satisfies the sector units.
"""
import itertools
import math
import os
import random
import sys
from functools import cmp_to_key

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symcnf import SymEncoding  # byte-identical copies of SYM5/symcnf.py, SYM5/symcnf_layers.py
from symcnf_layers import LayerEncoding


def det(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(x):
    return (x > 0) - (x < 0)


C = (0, 0)
ROT = {2: lambda p: (-p[0], -p[1]),
       4: lambda p: (-p[1], p[0]),
       6: lambda p: (p[0] - p[1], p[0])}


def orbit(p, m):
    out = [p]
    for _ in range(m - 1):
        out.append(ROT[m](out[-1]))
    assert ROT[m](out[-1]) == p
    return out


def in_gp(P):
    return all(det(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))


def hull(P):
    pts = sorted(set(P))
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and det(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and det(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def layers(P):
    rest, out = list(P), []
    while rest:
        V = hull(rest)
        out.append(V)
        Vs = set(V)
        rest = [p for p in rest if p not in Vs]
    return out


def encoder_pattern(m):
    """the float computation of symcnf.py add_sb (even m), copied verbatim in effect"""
    h = m // 2
    qx, qy = math.cos(math.pi / m), math.sin(math.pi / m)
    pat = []
    for j in range(h):
        ax, ay = math.cos(2 * math.pi * j / m), math.sin(2 * math.pi * j / m)
        bx, by = -ax, -ay
        d = (bx - ax) * (qy - ay) - (by - ay) * (qx - ax)
        pat.append(1 if d > 0 else -1)
    return pat


def in_open_sector(p, O0, m):
    """angular criterion at c: p strictly between the rays c->(0,0) and c->(0,1) (counter-clockwise)"""
    if m == 2:
        return det(C, O0[0], p) > 0
    return det(C, O0[0], p) > 0 and det(C, p, O0[1]) > 0


def pattern_ok(p, O0, m, pat):
    h = m // 2
    return all(sgn(det(O0[j], O0[j + h], p)) == pat[j] for j in range(h))


def sb_units(enc):
    enc.stats = {}
    enc.clauses.mem = []
    enc.clauses.n = 0
    enc.add_sb()
    return [list(cl) for cl in enc.clauses.mem]


def eval_clauses(enc, lab, clauses):
    """value of each triple-orbit variable from the exact chirotope of labelled points lab[0..P-1]"""
    val = {}
    for (a, b, c), (v, sg) in enc.tv.items():
        s = sgn(det(lab[a], lab[b], lab[c]))
        if s == 0:
            return None, "degenerate triple"
        x = sg * s
        if val.setdefault(v, x) != x:
            return None, "symmetry inconsistency"
    bad = 0
    for cl in clauses:
        if not any((L > 0 and val[L] == 1) or (L < 0 and val[-L] == -1) for L in cl):
            bad += 1
    return bad, None


def label(orbs, o0, i0, m, pat, order):
    """orbs: list of orbits (each a list of m points with R(orb[r]) = orb[r+1]); o0 = index of orbit 0;
    i0 = index of (0,0) in it.  order = 'angle' (symcnf.py) or 'layers' (orbs already outermost-first, o0 = 0).
    Returns labelled points or raises AssertionError if the normal form does not exist."""
    O0 = orbs[o0][i0:] + orbs[o0][:i0]
    reps = []
    for k, O in enumerate(orbs):
        if k == o0:
            continue
        cand_a = [p for p in O if in_open_sector(p, O0, m)]
        cand_p = [p for p in O if pattern_ok(p, O0, m, pat)]
        assert len(cand_a) == 1 and cand_a == cand_p, (k, cand_a, cand_p)
        reps.append(cand_a[0])
    if order == "angle":
        reps.sort(key=cmp_to_key(lambda p, q: -sgn(det(O0[0], p, q))))
        for i in range(len(reps)):
            for j in range(i + 1, len(reps)):
                assert det(O0[0], reps[i], reps[j]) > 0, "angular order about (0,0) not total"
    lab = list(O0)
    for p in reps:
        lab.extend(orbit(p, m))
    return lab


def random_set(m, t, B, rnd, nested):
    while True:
        orbs = []
        r = B
        for o in range(t):
            if nested:
                r *= rnd.uniform(0.45, 0.95)   # ratio < cos(pi/m) guarantees nesting; larger ratios test the rest
                th = rnd.uniform(0, 2 * math.pi)
                if m == 6:   # Euclidean (x, y) -> Eisenstein (a, b): b = 2y/sqrt3, a = x + b/2
                    x, y = r * math.cos(th), r * math.sin(th)
                    b = round(2 * y / math.sqrt(3)); a = round(x + b / 2)
                    p = (a, b)
                else:
                    p = (round(r * math.cos(th)), round(r * math.sin(th)))
            else:
                p = (rnd.randint(-B, B), rnd.randint(-B, B))
            if p == (0, 0):
                break
            orbs.append(orbit(p, m))
        if len(orbs) < t:
            continue
        P = [q for O in orbs for q in O]
        if len(set(P)) == len(P) and in_gp(P):
            return orbs, P


def main():
    rnd = random.Random(20261101)
    out = []
    # ---- (1) pattern: closed form and exact characterisation of the open sector
    for m in (2, 4, 6, 8, 10, 12, 14, 16):
        pat = encoder_pattern(m)
        assert pat == [-1] + [1] * (m // 2 - 1), (m, pat)
    out.append("(1a) encoder float pattern == [-1, +1, ..., +1] for m = 2..16 even: OK")
    G = 40
    for m in (2, 4, 6):
        pat = encoder_pattern(m)
        for O0 in (orbit((7, 2), m), orbit((-3, 11), m)):
            n_in = 0
            for x in range(-G, G + 1):
                for y in range(-G, G + 1):
                    p = (x, y)
                    if p == (0, 0):
                        continue
                    a, b = in_open_sector(p, O0, m), pattern_ok(p, O0, m, pat)
                    assert a == b, (m, O0, p, a, b)
                    n_in += a
            assert n_in > 0
    out.append(f"(1b) sector units <=> open sector (0, 2pi/m), exact sweep of the {2*G+1}^2 grid, m = 2,4,6: OK")

    # ---- (4) grid equivalence: no unique sector point  <=>  a point of the orbit on a diameter of orbit 0
    #          <=> three collinear points of S; and then no labelling satisfies the sector units
    for m in (2, 4, 6):
        pat = encoder_pattern(m)
        h = m // 2
        O0 = orbit((9, 4), m)
        n_deg = n_ok = 0
        for x in range(-G, G + 1):
            for y in range(-G, G + 1):
                p = (x, y)
                if p == (0, 0) or p in O0:
                    continue
                O = orbit(p, m)
                if set(O) & set(O0):
                    continue
                cnt = sum(in_open_sector(q, O0, m) for q in O)
                on_diam = any(det(O0[j], O0[j + h], q) == 0 for j in range(h) for q in O)
                assert (cnt != 1) == on_diam, (m, p, cnt, on_diam)
                if on_diam:
                    n_deg += 1
                    assert not in_gp(O0 + O)                      # three points of S collinear
                    assert not any(pattern_ok(q, O0, m, pat) for q in O)   # no labelling satisfies the units
                else:
                    n_ok += 1
                    assert cnt == 1
        out.append(f"(4) m={m}: {n_ok} orbits off the diameters -> exactly one sector point; {n_deg} orbits meeting "
                   f"a diameter -> collinear triple in S and no labelling satisfies the sector units")

    # ---- (2) + (3) random exact sets in general position: existence for every (orbit 0, (0,0)); encoder SB units
    stats = {}
    for m, t, layered in ((2, 4, False), (2, 6, False), (4, 3, False), (4, 4, False), (4, 3, True), (4, 4, True),
                          (4, 5, True), (6, 2, False), (6, 3, False), (6, 2, True), (6, 3, True)):
        N = m * t
        pat = encoder_pattern(m)
        if layered:
            enc = LayerEncoding(N, 7, m, body=None)
        else:
            enc = SymEncoding(N, 7, m, body=None)
        units = sb_units(enc)
        assert all(len(cl) == 1 for cl in units)
        n_sets = n_lab = n_bad = 0
        tries = 0
        while n_sets < (25 if N <= 16 else 10) and tries < 5000:
            tries += 1
            orbs, P = random_set(m, t, 10 ** 6, rnd, nested=layered)
            if layered:
                L = layers(P)
                if not (len(L) == t and all(len(V) == m and set(V) in [set(O) for O in orbs] for V in L)):
                    continue
                # order the orbits as the layers, outermost first; orbit 0 = hull orbit
                orbs = [next(O for O in orbs if set(O) == set(V)) for V in L]
                choices = [(0, i0) for i0 in range(m)]
            else:
                choices = [(o0, i0) for o0 in range(t) for i0 in range(m)]
            n_sets += 1
            for o0, i0 in choices:
                lab = label(orbs, o0, i0, m, pat, "layers" if layered else "angle")
                bad, err = eval_clauses(enc, lab, units)
                assert err is None, err
                n_lab += 1
                n_bad += bad
                # negative control: move (o,0) of orbit 1 to the next point of its orbit -> must violate a unit
                if t >= 2:
                    lab2 = list(lab)
                    lab2[m:2 * m] = lab[m + 1:2 * m] + lab[m:m + 1]
                    bad2, err2 = eval_clauses(enc, lab2, units)
                    assert err2 is None and bad2 > 0, (m, t, layered, bad2, err2)
        key = f"m={m} t={t} {'layers' if layered else 'angle '}"
        stats[key] = (n_sets, n_lab, n_bad, len(units))
        assert n_bad == 0
    for k, (s, l, b, u) in stats.items():
        out.append(f"(2,3) {k}: {s} exact GP sets, {l} labellings (all orbit-0 / (0,0) choices), every other orbit had "
                   f"exactly one open-sector point; {u} SB units, violated: {b}; shifted-representative controls all caught")
    print("\n".join(out))


if __name__ == "__main__":
    main()
