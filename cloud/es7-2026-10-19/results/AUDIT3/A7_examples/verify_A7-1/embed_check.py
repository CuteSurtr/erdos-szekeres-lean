#!/usr/bin/env python3
"""Independent re-check of audit finding A7-1 (embedding dependence of the Z[zeta5] example files).

Written from scratch; does not import the project code (verify5.py) or the auditor's a7lib.py.

For each 5-fold file and each embedding zeta -> exp(2 pi i j/5), j = 1..4, a line "c0 c1 c2 c3" is the plane point
    x = sum_k c_k cos(2 pi j k/5),   y = sum_k c_k sin(2 pi j k/5).
Exact route ("Cartesian", unlike the project's Im(conj(u) v) formula): with s = sin(72 deg) > 0,
    4x = X in Z[sqrt5],  2y/s = Y in Z[sqrt5]   (closed forms of cos(2 pi m/5) and sin(2 pi m/5)/s),
and orientation(p,q,r) = sign((Xq-Xp)(Yr-Yp) - (Yq-Yp)(Xr-Xp)) (positive rescaling of the axes keeps the sign).
Numeric route (cross-check of every sign): 80-digit Decimal, pi by Machin, cos/sin by Taylor series (no closed forms).
Largest convex subset by two methods written here:
    (A) branch and bound over 4-point convexity bitmasks (a set in general position is in convex position iff every
        4 of its points are), which also returns a witness polygon;
    (B) an O(n^4) angular dynamic program anchored at the leftmost vertex.
Both are tested against exhaustive enumeration on random small subsets.
"""
import os
import random
import sys
import time
from decimal import Decimal, getcontext
from functools import cmp_to_key
from itertools import combinations

R = os.environ.get("ES7_RESULTS", ".")
FILES = [("c5_30", R + "/SYMMAX/c5_30points.txt", 7),
         ("c5_31", R + "/SYMMAX/c5_31points.txt", 7),
         ("c5_31minus_centre", R + "/SYM5/c5_31minus_centre.txt", 7),
         ("k6/c5_16", R + "/SYMMAX/k6/c5_16points.txt", 6)]


def parse(path):
    pts = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            v = tuple(int(x) for x in s.split())
            assert len(v) == 4, (path, line)
            pts.append(v)
    return pts


# ---------------- exact arithmetic in Z[sqrt5]: (a, b) means a + b*sqrt5 ----------------
C4 = {0: (4, 0), 1: (-1, 1), 2: (-1, -1), 3: (-1, -1), 4: (-1, 1)}     # 4 cos(2 pi m/5)
S2 = {0: (0, 0), 1: (2, 0), 2: (-1, 1), 3: (1, -1), 4: (-2, 0)}       # 2 sin(2 pi m/5) / sin(2 pi/5)


def add(u, v): return (u[0] + v[0], u[1] + v[1])
def sub(u, v): return (u[0] - v[0], u[1] - v[1])
def mul(u, v): return (u[0] * v[0] + 5 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])
def smul(k, u): return (k * u[0], k * u[1])


def sgn5(u):
    a, b = u
    if a >= 0 and b >= 0:
        return 1 if (a or b) else 0
    if a <= 0 and b <= 0:
        return -1
    t = a * a - 5 * b * b
    assert t != 0
    if a > 0:
        return 1 if t > 0 else -1
    return 1 if t < 0 else -1


def planar_exact(c, j):
    X, Y = (0, 0), (0, 0)
    for k in range(4):
        m = (j * k) % 5
        X = add(X, smul(c[k], C4[m]))
        Y = add(Y, smul(c[k], S2[m]))
    return X, Y


def orient_exact(p, q, r):
    dxq, dyq = sub(q[0], p[0]), sub(q[1], p[1])
    dxr, dyr = sub(r[0], p[0]), sub(r[1], p[1])
    return sgn5(sub(mul(dxq, dyr), mul(dyq, dxr)))


# ---------------- high-precision numerics (independent of the closed forms) ----------------
getcontext().prec = 80


def d_arctan_inv(x):
    x = Decimal(x)
    x2 = x * x
    term = 1 / x
    total = term
    n, sign = 1, 1
    eps = Decimal(10) ** (-(getcontext().prec + 5))
    while True:
        term /= x2
        n += 2
        sign = -sign
        t = term / n
        if t < eps:
            break
        total += sign * t
    return total


PI = 16 * d_arctan_inv(5) - 4 * d_arctan_inv(239)


def d_cos(x):
    s, t, k = Decimal(1), Decimal(1), 0
    x2 = x * x
    eps = Decimal(10) ** (-(getcontext().prec + 5))
    while True:
        k += 2
        t = -t * x2 / (k * (k - 1))
        if abs(t) < eps:
            break
        s += t
    return s


def d_sin(x):
    s, t, k = x, x, 1
    x2 = x * x
    eps = Decimal(10) ** (-(getcontext().prec + 5))
    while True:
        k += 2
        t = -t * x2 / (k * (k - 1))
        if abs(t) < eps:
            break
        s += t
    return s


COSD = [d_cos(2 * PI * m / 5) for m in range(5)]
SIND = [d_sin(2 * PI * m / 5) for m in range(5)]
SQRT5 = Decimal(5).sqrt()


def check_closed_forms():
    s1 = SIND[1]
    worst = Decimal(0)
    for m in range(5):
        cf = (C4[m][0] + C4[m][1] * SQRT5) / 4
        sf = s1 * (S2[m][0] + S2[m][1] * SQRT5) / 2
        worst = max(worst, abs(cf - COSD[m]), abs(sf - SIND[m]))
    return worst


def planar_num(c, j):
    x = sum(c[k] * COSD[(j * k) % 5] for k in range(4))
    y = sum(c[k] * SIND[(j * k) % 5] for k in range(4))
    return x, y


def det_num(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


# ---------------- symmetry in coefficient space ----------------
def mul_zeta(c):        # zeta * (c0 + c1 z + c2 z^2 + c3 z^3), using z^4 = -1 - z - z^2 - z^3
    return (-c[3], c[0] - c[3], c[1] - c[3], c[2] - c[3])


def orbits_of(pts):
    S = set(pts)
    seen, orbs = set(), []
    for p in pts:
        if p in seen:
            continue
        o = [p]
        q = mul_zeta(p)
        while q != p:
            assert q in S, "not closed under multiplication by zeta"
            o.append(q)
            q = mul_zeta(q)
        seen.update(o)
        orbs.append(o)
    return orbs


# ---------------- convexity ----------------
def inside(O, p, x, y, z):
    return O[x][y][p] == O[y][z][p] == O[z][x][p]


def conv4(O, a, b, c, d):
    return not (inside(O, a, b, c, d) or inside(O, b, a, c, d) or inside(O, c, a, b, d) or inside(O, d, a, b, c))


def convex_position(O, idx):
    return all(conv4(O, *q) for q in combinations(idx, 4))


def max_convex_bb(O, n, count=False, cap=None):
    """(A) branch and bound / full enumeration of convex subsets; returns (max, witness, counts)."""
    masks = {}
    for a, b, c in combinations(range(n), 3):
        m = 0
        for d in range(n):
            if d != a and d != b and d != c and conv4(O, a, b, c, d):
                m |= 1 << d
        masks[(a, b, c)] = m
    best = [min(n, 3), list(range(min(n, 3)))]
    counts = [0] * (n + 1)

    def rec(S, cand):
        k = len(S)
        if count:
            counts[k] += 1
        if k > best[0]:
            best[0], best[1] = k, list(S)
        if not count and k + bin(cand).count("1") <= best[0]:
            return
        c = cand
        while c:
            low = c & -c
            d = low.bit_length() - 1
            c ^= low
            nc = cand & ~((1 << (d + 1)) - 1)
            for x, y in combinations(S, 2):
                nc &= masks[(x, y, d)]
                if not nc:
                    break
            S.append(d)
            rec(S, nc)
            S.pop()

    rec([], (1 << n) - 1)
    return best[0], best[1], counts


def max_convex_dp(O, P, idx):
    """(B) angular DP; P[i] = exact (X, Y); idx = list of point indices to use."""
    def lexless(p, q):
        sx = sgn5(sub(q[0], p[0]))
        if sx:
            return sx > 0
        return sgn5(sub(q[1], p[1])) > 0
    n = len(idx)
    best = min(n, 3)
    for a in idx:
        Rr = [p for p in idx if p != a and lexless(P[a], P[p])]
        Rr.sort(key=cmp_to_key(lambda p, q: -1 if O[a][p][q] > 0 else 1))
        m = len(Rr)
        L = [[0] * m for _ in range(m)]
        for jj in range(m):
            pj = Rr[jj]
            for ii in range(jj):
                pi = Rr[ii]
                assert O[a][pi][pj] > 0
                v = 3
                for hh in range(ii):
                    if O[Rr[hh]][pi][pj] > 0 and L[hh][ii] + 1 > v:
                        v = L[hh][ii] + 1
                L[ii][jj] = v
                if O[pi][pj][a] > 0 and v > best:
                    best = v
    return best


def brute_max(O, idx):
    best = min(len(idx), 3)
    for k in range(4, len(idx) + 1):
        if any(convex_position(O, s) for s in combinations(idx, k)):
            best = k
        else:
            break
    return best


def cyclic_left_turn_check(O, Pn, wit):
    """sort the witness by angle about its (numeric) centroid, then check every consecutive triple is a left turn."""
    import math
    cx = sum(float(Pn[i][0]) for i in wit) / len(wit)
    cy = sum(float(Pn[i][1]) for i in wit) / len(wit)
    order = sorted(wit, key=lambda i: math.atan2(float(Pn[i][1]) - cy, float(Pn[i][0]) - cx))
    k = len(order)
    return all(O[order[t]][order[(t + 1) % k]][order[(t + 2) % k]] > 0 for t in range(k)), order


def main():
    out = []
    def say(*a):
        s = " ".join(str(x) for x in a)
        print(s)
        out.append(s)
        sys.stdout.flush()

    say("closed forms of cos/sin(2 pi m/5) vs 80-digit Taylor values: max abs diff =", "%.3e" % check_closed_forms())
    random.seed(20261101)
    for name, path, K in FILES:
        pts = parse(path)
        n = len(pts)
        orbs = orbits_of(pts)
        sizes = sorted(len(o) for o in orbs)
        orbit_id = {p: i for i, o in enumerate(orbs) for p in o}
        say("=" * 100)
        say("%s: %d points, %d distinct, orbit sizes %s, closed under *zeta: yes (asserted)" % (
            name, n, len(set(pts)), sizes))
        for j in (1, 2, 3, 4):
            t0 = time.time()
            P = [planar_exact(c, j) for c in pts]
            Pn = [planar_num(c, j) for c in pts]
            # numeric check that multiplication by zeta is the rotation by 2 pi j/5 in this embedding
            cr, sr = COSD[j % 5], SIND[j % 5]
            rot_err = max(max(abs((Pn[i][0] * cr - Pn[i][1] * sr) - planar_num(mul_zeta(pts[i]), j)[0]),
                              abs((Pn[i][0] * sr + Pn[i][1] * cr) - planar_num(mul_zeta(pts[i]), j)[1]))
                          for i in range(n))
            O = [[[0] * n for _ in range(n)] for _ in range(n)]
            zero = mismatch = 0
            mindet = None
            maxdet = Decimal(0)
            for a in range(n):
                for b in range(n):
                    if b == a:
                        continue
                    for c in range(n):
                        if c == a or c == b:
                            continue
                        o = orient_exact(P[a], P[b], P[c])
                        O[a][b][c] = o
                        if a < b < c:
                            dn = det_num(Pn[a], Pn[b], Pn[c])
                            sn = (dn > 0) - (dn < 0)
                            if o == 0:
                                zero += 1
                            if sn != o:
                                mismatch += 1
                            ad = abs(dn)
                            mindet = ad if mindet is None or ad < mindet else mindet
                            maxdet = max(maxdet, ad)
            # antisymmetry spot check
            anti = all(O[a][b][c] == -O[b][a][c] == O[b][c][a] for a, b, c in combinations(range(n), 3))
            # convexity
            full = (j in (1, 4))
            mbb, wit, counts = max_convex_bb(O, n, count=full)
            mdp = max_convex_dp(O, P, list(range(n)))
            line = ("  j=%d: collinear triples=%d, exact/numeric sign mismatches=%d, min|det|=%.3e (max %.3e), "
                    "rot err=%.1e, antisym=%s | max convex: B&B=%d, DP=%d -> %s" % (
                        j, zero, mismatch, mindet, maxdet, rot_err, anti, mbb, mdp,
                        "no convex %d-gon" % K if max(mbb, mdp) < K else "HAS a convex %d-gon" % K))
            say(line)
            if full:
                say("        convex k-subset counts (k=4..%d): %s ; convex %d-subsets: %d" % (
                    mbb, counts[4:mbb + 1], K, counts[K] if K <= n else 0))
            if mbb >= K:
                ok4 = convex_position(O, wit)
                okc, order = cyclic_left_turn_check(O, Pn, wit)
                orbs_used = sorted(set(orbit_id[pts[i]] for i in order))
                say("        witness convex %d-gon (4-point criterion: %s; cyclic left turns: %s), orbits used %s:" % (
                    len(wit), ok4, okc, orbs_used))
                say("        " + "  ".join("[%s]" % " ".join(map(str, pts[i])) for i in order))
            # random cross-check of B&B and DP against brute force on small subsets
            bad = 0
            for _ in range(25):
                k = random.randint(6, 11)
                sub_idx = sorted(random.sample(range(n), k))
                bf = brute_max(O, sub_idx)
                # remap for bb
                Os = [[[O[sub_idx[x]][sub_idx[y]][sub_idx[z]] for z in range(k)] for y in range(k)] for x in range(k)]
                b1 = max_convex_bb(Os, k)[0]
                b2 = max_convex_dp(O, P, sub_idx)
                if not (bf == b1 == b2):
                    bad += 1
            say("        random-subset cross-check (25 subsets of size 6..11): brute == B&B == DP failures: %d  [%.1fs]" % (
                bad, time.time() - t0))
    return out


if __name__ == "__main__":
    main()
