#!/usr/bin/env python3
"""Cone rules: orientation signs of t nested regular m-gons (even m) that are fixed by the phase ORDER of the
(at most 3) layers involved, for every radius vector compatible with the nesting.  Exact (rational multiples of pi).
Clauses are in the variable numbering of C7UPPER/gen.py Enc(m, K, t) (triple-orbit variables and Y(i,j)).

Setting (gen.py conventions, even m): vertex (i,k) at angle beta = theta_i + 2 pi k/m, theta_0 = 0,
theta_i = psi_i in (0, 2 pi/m) for i >= 1, Y(i,j) = [psi_i < psi_j]; radii r_0 > r_1 > ... > 0, u_i = 1/r_i.

Lemma (written proof, not refereed).
 (1) Polar formula: 2 area(p,q,s) / (r_p r_q r_s) = u_p sin(b_s - b_q) + u_q sin(b_p - b_s) + u_s sin(b_q - b_p),
     so orient(p,q,s) = sign F(u), F linear in u with coefficients c_p, c_q, c_s (ES8SYM Lemma 1).
 (2) Nesting (strict, layer lemma): 0 < u_0 < u_1 < ... .  With D = d_1 < ... < d_s the distinct layers of p,q,s,
     the set of (u_d)_{d in D} that occur is exactly the open cone {0 < u_{d_1} < ... < u_{d_s}}
     = {sum_r lambda_r g_r : lambda_r > 0}, g_r = sum_{d >= d_r} e_d.  Hence F > 0 for all admissible radii iff
     G_r := F(g_r) >= 0 for all r and G_r > 0 for some r (F < 0 symmetrically).  G_r is the sum of the coefficients
     of the points on layers >= d_r.
 (3) Product forms (a + b + c = 0 for the three angle differences):
        one point:     G = sin(A);
        two points:    sin A + sin B = 2 sin((A+B)/2) cos((A-B)/2);
        three points:  sin a + sin b + sin c = -4 sin(a/2) sin(b/2) sin(c/2).
     Every factor is sin or cos of an affine function of the phases with rational-multiple-of-pi constants.
 (4) Phase cell: for a fixed order of the psi of the free layers of D (layer 0 has theta = 0), the phases range over
     an open simplex; a non-constant affine function maps it onto the open interval between its extreme values at
     the closed simplex's vertices.  If that interval contains no zero of the factor, the factor has constant sign
     on the cell; a constant factor has its exact sign.  If every G_r has a constant sign (or vanishes identically)
     on the cell, (2) decides the orientation for every configuration whose phases lie in the cell.
 Each emitted clause is (negated pattern literals) OR (orientation literal), the pattern literals being the Y
 literals of consecutive layers in the psi order (transitivity is in gen.py's CNF), as in gen.py's fam_angle.
 Genericity of the phases (distinct psi, psi_i not in {0, 2 pi/m}) is gen.py's normalisation step 0.

usage: cone_rules.py m t OUT.clauses
"""
import sys, os, itertools, importlib.util
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
s_ = importlib.util.spec_from_file_location('gen', os.path.join(HERE, 'gen.py'))
G = importlib.util.module_from_spec(s_); s_.loader.exec_module(G)


def sin_sign_const(c):
    """sign of sin(pi c), c Fraction"""
    r = c % 2
    if r == 0 or r == 1:
        return 0
    return 1 if r < 1 else -1


def factor_sign(coef, const, verts):
    """sign of sin(pi * (const + sum coef[L] theta_L)) on the open cell with closed-simplex vertices verts
    (theta in units of pi); None if not constant"""
    vals = [const + sum(coef.get(L, 0) * v[L] for L in v) for v in verts]
    lo, hi = min(vals), max(vals)
    if all(coef.get(L, 0) == 0 for L in verts[0]) or lo == hi:
        return sin_sign_const(lo)
    # open interval (lo, hi): zeros of sin(pi x) at integers
    import math
    n = math.floor(lo) + 1
    if n < hi:
        return None
    mid = (lo + hi) / 2
    return sin_sign_const(mid)


def build(m, t):
    assert m % 2 == 0
    E = G.Enc(m, 9, t)
    U = Fr(2, m)                       # phase range (0, 2/m) in units of pi
    out = set()
    nforced = 0
    for C, v in E.tvar.items():
        pts = [divmod(x, m) for x in C]
        lay = [p[0] for p in pts]
        D = sorted(set(lay))
        free = [L for L in D if L != 0]
        # angle of point j (units of pi): theta_{lay j} + 2 k_j / m ; as (coef dict, const)
        def ang(j):
            L, k = pts[j]
            return ({L: Fr(1)} if L != 0 else {}), Fr(2 * k, m)
        def lin(*terms):
            co = {}; cst = Fr(0)
            for sgn, (cd, cc) in terms:
                for L, a in cd.items():
                    co[L] = co.get(L, 0) + sgn * a
                cst += sgn * cc
            return co, cst
        def scale(f, s):
            return ({L: a * s for L, a in f[0].items()}, f[1] * s)
        # coefficient arguments: c_0 = sin(b2 - b1), c_1 = sin(b0 - b2), c_2 = sin(b1 - b0)
        A = [lin((1, ang(2)), (-1, ang(1))), lin((1, ang(0)), (-1, ang(2))), lin((1, ang(1)), (-1, ang(0)))]
        results = []
        for perm in itertools.permutations(free):
            # vertices of the closed simplex 0 <= theta_perm0 <= ... <= U
            verts = []
            n = len(perm)
            for j in range(n + 1):
                vt = {}
                for q, L in enumerate(perm):
                    vt[L] = Fr(0) if q < j else U
                verts.append(vt)
            if not verts[0]:
                verts = [{}]
            signs = []
            ok = True
            for d in D:
                S = [j for j in range(3) if lay[j] >= d]
                if len(S) == 1:
                    facs = [(1, A[S[0]])]
                elif len(S) == 2:
                    a, b = A[S[0]], A[S[1]]
                    half_sum = scale(lin((1, a), (1, b)), Fr(1, 2))
                    half_dif = scale(lin((1, a), (-1, b)), Fr(1, 2))
                    cosarg = (half_dif[0], half_dif[1] + Fr(1, 2))      # cos w = sin(w + pi/2)
                    facs = [(2, half_sum), (1, cosarg)]
                else:
                    facs = [(-4, scale(A[0], Fr(1, 2))), (1, scale(A[1], Fr(1, 2))), (1, scale(A[2], Fr(1, 2)))]
                sg = 1
                for mult, f in facs:
                    if mult < 0:
                        sg = -sg
                    fs = factor_sign(f[0], f[1], verts)
                    if fs is None:
                        ok = False; break
                    sg *= fs
                if not ok:
                    break
                signs.append(sg)
            if not ok:
                results.append((perm, None)); continue
            if all(x >= 0 for x in signs) and any(x > 0 for x in signs):
                results.append((perm, v))
            elif all(x <= 0 for x in signs) and any(x < 0 for x in signs):
                results.append((perm, -v))
            else:
                results.append((perm, None))
        concl = set(l for _, l in results)
        if len(concl) == 1 and None not in concl:
            out.add((concl.pop(),)); nforced += 1
            continue
        for perm, l in results:
            if l is None:
                continue
            lits = []
            for a, b in zip(perm, perm[1:]):
                y = E.ylit(a, b)
                lits.append(-y)
            out.add(tuple(lits + [l]))
    return E, sorted(out, key=lambda c: [abs(x) for x in c]), nforced


if __name__ == '__main__':
    m, t = int(sys.argv[1]), int(sys.argv[2])
    E, cls, nu = build(m, t)
    with open(sys.argv[3], 'w') as f:
        for c in cls:
            f.write(' '.join(map(str, c)) + ' 0\n')
    from collections import Counter
    print('m=%d t=%d cone-rule clauses %d (units %d) by length %s' % (m, t, len(cls), nu,
                                                                    dict(Counter(len(c) for c in cls))))
