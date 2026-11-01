#!/usr/bin/env python3
"""End-to-end EXACT test of Lemma 1 / Proposition C for even m in {4, 6, 8} (written from scratch for the check of Theorem E).

For a random rational cluster C (outward radial frame of v_0 = (1,0)), build the actual m-fold symmetric set
S_e = union_j R^j (v_0 + e C) with EXACT coordinates in Z[sqrt d] (d = 2 for m = 8, d = 3 for m = 6, rationals for
m = 4), compute mc(S_e) exactly (orientation signs in Z[sqrt d], largest-convex-polygon DP), and compare with
  * the Lemma 1 / Prop. C formula  max(mc(C), max over subsets B' of the m-gon (|B'|>=2) of sum F(a_b, b_b)),
    F(a,b) = f_C((-a,b)) computed from the definition (sound_te.direct chain DFS);
  * the Prop. C criterion: mc(S_e) <= m  <=>  (i) and mc(C) <= m.
Two values of e are used and must give the same mc (otherwise the configuration is reported as 'e not small').
"""
import sys, random
from fractions import Fraction as Fr
from functools import cmp_to_key
from itertools import combinations
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import sound_te as st


def sgn_sqrt(a, b, d):
    """sign of a + b*sqrt(d) for integers a, b, d > 0 non-square (d = 0 means plain integer a)."""
    if d == 0 or b == 0:
        return (a > 0) - (a < 0)
    if a >= 0 and b >= 0:
        return 1 if (a or b) else 0
    if a <= 0 and b <= 0:
        return -1
    # opposite signs: compare a^2 with d b^2
    lhs, rhs = a * a, d * b * b
    if a > 0:      # a > 0 > b
        return 1 if lhs > rhs else -1   # equality impossible (d non-square)
    return 1 if rhs > lhs else -1


def mul(x, y, d):
    return (x[0] * y[0] + d * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def rot_table(m):
    """2*cos(2 pi j/m), 2*sin(2 pi j/m) as (a, b) meaning a + b sqrt(d); returns d and the table."""
    if m == 4:
        d = 0
        cs = [(2, 0), (0, 0), (-2, 0), (0, 0)]
        sn = [(0, 0), (2, 0), (0, 0), (-2, 0)]
    elif m == 6:
        d = 3
        cs = [(2, 0), (1, 0), (-1, 0), (-2, 0), (-1, 0), (1, 0)]
        sn = [(0, 0), (0, 1), (0, 1), (0, 0), (0, -1), (0, -1)]
    elif m == 8:
        d = 2
        cs = [(2, 0), (0, 1), (0, 0), (0, -1), (-2, 0), (0, -1), (0, 0), (0, 1)]
        sn = [(0, 0), (0, 1), (2, 0), (0, 1), (0, 0), (0, -1), (-2, 0), (0, -1)]
    else:
        raise ValueError
    return d, cs, sn


def build_set(C, m, E, Den):
    """C: list of (cx, cy) integers meaning (cx/Den, cy/Den); e = 1/E.  Coordinates scaled by 2*Den*E (and by the
    factor 2 of the rotation table) -> all coordinates are integer pairs (a, b) = a + b sqrt(d)."""
    d, cs, sn = rot_table(m)
    pts = []
    for j in range(m):
        for (cx, cy) in C:
            X = (Den * E + cx, 0)     # scaled point at v_0 (factor Den*E); rotation multiplies by 2
            Y = (cy, 0)
            px = sub(mul(cs[j], X, d), mul(sn[j], Y, d))
            py = (mul(sn[j], X, d)[0] + mul(cs[j], Y, d)[0], mul(sn[j], X, d)[1] + mul(cs[j], Y, d)[1])
            pts.append((px, py))
    return pts, d


def mc_exact(pts, d):
    N = len(pts)
    O = {}
    for i in range(N):
        for j in range(N):
            if j == i:
                continue
            for k in range(N):
                if k == i or k == j:
                    continue
                if (i, j, k) in O:
                    continue
                a, b, c = pts[i], pts[j], pts[k]
                det = sub(mul(sub(b[0], a[0]), sub(c[1], a[1]), d), mul(sub(b[1], a[1]), sub(c[0], a[0]), d))
                s = sgn_sqrt(det[0], det[1], d)
                if s == 0:
                    raise ValueError('collinear triple in S_e')
                for (p, q, r), sg in (((i, j, k), s), ((j, k, i), s), ((k, i, j), s), ((j, i, k), -s), ((i, k, j), -s), ((k, j, i), -s)):
                    O[p, q, r] = sg
    # height functional h = y*K + x with K irrational-ish large: compare exactly
    K = (10**9 + 7, 0)

    def hcmp(i, j):
        hi = (pts[i][1][0] * K[0] + pts[i][0][0], pts[i][1][1] * K[0] + pts[i][0][1])
        hj = (pts[j][1][0] * K[0] + pts[j][0][0], pts[j][1][1] * K[0] + pts[j][0][1])
        s = sgn_sqrt(hi[0] - hj[0], hi[1] - hj[1], d)
        if s == 0:
            raise ValueError('height tie')
        return s
    best = min(N, 2)
    for p in range(N):
        Q = [q for q in range(N) if q != p and hcmp(q, p) > 0]
        Q.sort(key=cmp_to_key(lambda a, b: -O[p, a, b]))   # a before b iff orient(p, a, b) > 0
        L = len(Q)
        dp = {}
        for j in range(L):
            for i in range(j):
                v = 3
                qi, qj = Q[i], Q[j]
                for k in range(i):
                    if (k, i) in dp and O[Q[k], qi, qj] > 0:
                        if dp[k, i] + 1 > v:
                            v = dp[k, i] + 1
                dp[i, j] = v
                if O[qi, qj, p] > 0 and v > best:
                    best = v
        if L >= 1 and best < 2:
            best = 2
    return best


def formula(C_fr, m):
    """Lemma 1 formula for the single orbit (no centre) and Prop. C (i); C_fr: list of Fraction points."""
    n = len(C_fr)
    vec = {(p, q): (C_fr[q][0] - C_fr[p][0], C_fr[q][1] - C_fr[p][1]) for p in range(n) for q in range(n) if p != q}

    def f(lo, hi):
        best = 1
        stack = [(p, None, 1) for p in range(n)]
        while stack:
            p, vprev, k = stack.pop()
            best = max(best, k)
            for q in range(n):
                if q != p:
                    v = vec[p, q]
                    if st.xsgn(st.u_out(lo, m), v) > 0 and st.xsgn(st.u_out(hi, m), v) < 0 and (
                            vprev is None or st.cross_exact(vprev, v) > 0):
                        stack.append((q, v, k + 1))
        return best
    F = {}
    for a in range(1, m):
        for b in range(1, m - a + 1):
            F[a, b] = f(-a, b)
    best = 0
    for r in range(2, m + 1):
        for S in combinations(range(m), r):
            gaps = [(S[(i + 1) % r] - S[i]) % m or m for i in range(r)]
            tot = 0
            for i in range(r):
                a = gaps[i - 1]      # gap before vertex S[i]
                b = gaps[i]          # gap after
                tot += F[a, b]
            best = max(best, tot)
    g = {x: f(0, x) for x in range(1, m)}
    h = {x: f(-x, 0) for x in range(1, m)}
    cond_i = all(g[x] + h[x] <= x + 1 for x in range(1, m))
    return best, cond_i, g, h


def mc_cluster(C_fr):
    pts = [((Fr(x).numerator * 0 + x), y) for (x, y) in C_fr]
    # exact rational DP via the same routine with d = 0: scale to integers
    den = 1
    for (x, y) in C_fr:
        den = den * Fr(x).denominator * Fr(y).denominator // 1
    P = [((int(x * den), 0), (int(y * den), 0)) for (x, y) in C_fr]
    return mc_exact(P, 0) if len(P) >= 3 else len(P)


if __name__ == '__main__':
    seed = int(sys.argv[1]); trials = int(sys.argv[2])
    rng = random.Random(seed)
    stats = dict(tested=0, formula_mismatch=0, propC_mismatch=0, e_not_small=0, skipped=0, small_mc=0)
    Den = 10**4
    for tr in range(trials):
        m = rng.choice([4, 6, 8])
        n = rng.randint(2, {4: 5, 6: 6, 8: 6}[m])
        ang = rng.uniform(-1.4, 1.4)
        C = []
        import math
        for _ in range(n):
            r = rng.uniform(-1, 1); s = rng.uniform(-0.3, 0.3)
            C.append((int(Den * (r * math.cos(ang) - s * math.sin(ang))), int(Den * (r * math.sin(ang) + s * math.cos(ang)))))
        if len(set(C)) < n:
            stats['skipped'] += 1; continue
        C_fr = [(Fr(x, Den), Fr(y, Den)) for (x, y) in C]
        try:
            g0, h0, F11 = st.direct_profile(C_fr, m)
            fval, cond_i, g, h = formula(C_fr, m)
            mcC = mc_cluster(C_fr)
            mc1 = mc_exact(*build_set(C, m, 10**7, Den))
            mc2 = mc_exact(*build_set(C, m, 10**11, Den))
        except ValueError as ex:
            stats['skipped'] += 1; continue
        if mc1 != mc2:
            stats['e_not_small'] += 1; continue
        stats['tested'] += 1
        pred = max(mcC, fval)
        if pred != mc1:
            stats['formula_mismatch'] += 1
            print('FORMULA MISMATCH m=%d C=%s mc=%d formula=%d mcC=%d' % (m, C, mc1, fval, mcC))
        if (mc1 <= m) != (cond_i and mcC <= m):
            stats['propC_mismatch'] += 1
            print('PROP C MISMATCH m=%d C=%s mc=%d (i)=%s g=%s h=%s' % (m, C, mc1, cond_i, g, h))
        stats['small_mc'] += (mc1 <= m)
    print('seed', seed, stats)
