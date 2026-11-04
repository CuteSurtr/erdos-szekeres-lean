#!/usr/bin/env python3
"""Independent exact per-clause verifier for chord-lemma clause files (m-fold, t layers, gen.py conventions).

Shares no code with chord_rules_m.py.  Variable numbering is recomputed here from the gen.py docstring
(triple orbits in first-appearance order of itertools.combinations, canonical = lexicographically least sorted
rotation; then Y(i,j) i<j lexicographic; then H(1..t-1) for odd m) and cross-checked against the .cnf.json.

Semantics: var v (<= ntriple) true iff orient(C) = + for its canonical sorted triple C = (a,b,c).
Point x = m*i + k: layer i, angle theta_i + 360k/m (degrees), radius r_i > 0.
Phase region of a full assignment for layers S:
  layer 0: theta_0 = 0 (psi_0 = 0);
  odd m, L >= 1: psi_L in (0, 180/m), theta_L = psi_L + (0 if H_L else 180/m);
  even m, L >= 1: theta_L = psi_L in (0, 360/m);
  Y(i,j) (i<j, both >= 1) true iff psi_i < psi_j.
For each clause: enumerate every full assignment of the phase vars of the triple's layers that falsifies all the
condition literals; for each, prove sign(orient(C)) = clause sign for ALL radii r > 0 (radius-free) and all phases in
the (open) region.  2-layer triple {x,y on layer J, z on layer I}:
  orient(x,y,z)/r_J^2 = sin(c0) + lam*(sin(delta+c2) - sin(delta+c1)),  lam = r_I/r_J > 0, delta = theta_I - theta_J,
  c0 = a_y - a_x, c1 = a_z - a_x, c2 = a_z - a_y (index parts, rational degrees).
  delta ranges over the open interval (lo,hi) = image of the open phase polygon (computed from the closure's vertices).
  B(delta) = sin(delta+c2) - sin(delta+c1) vanishes exactly at delta = (180 - c1 - c2)/2 mod 180 (sin X = sin Y iff
  X = Y or X = 180 - Y mod 360; X = Y is impossible since c1 != c2 mod 360), zeros are simple.
  Radius-free condition: s*sin(c0) >= 0, B has no zero in (lo,hi), s*B(mid) > 0 (rigorous interval arithmetic).
  (If sin(c0) = 0 this gives strict s*F > 0 on the open interval; if s*sin(c0) > 0 then s*F > 0 for every lam > 0.)
1-layer triple: orient/r^2 = sin(a_b-a_a)+sin(a_c-a_b)+sin(a_a-a_c), constant; sign by interval arithmetic.
Usage: verify_exact.py m t CLAUSEFILE [CNFJSON]"""
import sys, itertools, json
from fractions import Fraction as Fr
from mpmath import iv
iv.dps = 80


def numbering(m, t):
    n = m * t
    tv = {}
    canon_of = {}
    for T in itertools.combinations(range(n), 3):
        best = None
        for s in range(m):
            R = tuple(sorted((x // m) * m + (x % m + s) % m for x in T))
            if best is None or R < best:
                best = R
        if best not in tv:
            tv[best] = len(tv) + 1
    inv = {v: C for C, v in tv.items()}
    nv = len(tv)
    Y = {}
    for i in range(1, t):
        for j in range(i + 1, t):
            nv += 1
            Y[(i, j)] = nv
    H = {}
    if m % 2:
        for i in range(1, t):
            nv += 1
            H[i] = nv
    return tv, inv, Y, H


def ivsin_deg(q):
    q = Fr(q)
    return iv.sin(iv.pi * iv.mpf(q.numerator) / iv.mpf(q.denominator * 180))


def ivsign(x):
    if x.a > 0:
        return 1
    if x.b < 0:
        return -1
    return 0   # inconclusive


def sin_sign_exact(q):
    """exact sign of sin(q degrees), q rational"""
    r = Fr(q) % 360
    if r == 0 or r == 180:
        return 0
    return 1 if r < 180 else -1


def perm_parity(src, dst):
    """sign of permutation taking sequence src to dst (same elements)"""
    p = [src.index(x) for x in dst]
    s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]:
                s = -s
    return s


def delta_interval(m, I, J, asg, Y, H):
    """open interval of delta = theta_I - theta_J for the full assignment asg (var -> bool). Exact Fractions."""
    odd = m % 2 == 1
    P = Fr(180, m) if odd else Fr(360, m)
    off = {}
    for L in (I, J):
        if L == 0:
            off[L] = None
        else:
            off[L] = Fr(0) if (not odd or asg[H[L]]) else Fr(180, m)
    # closure vertices of the psi region
    cand = []
    rngI = [Fr(0)] if I == 0 else [Fr(0), P]
    rngJ = [Fr(0)] if J == 0 else [Fr(0), P]
    # order constraint (only if both >= 1): psi_I < psi_J iff ...
    order = None
    if I != 0 and J != 0:
        a, b = min(I, J), max(I, J)
        ylt = asg[Y[(a, b)]]           # psi_a < psi_b
        IltJ = ylt if I == a else (not ylt)
        order = IltJ
    pts = set()
    for pI in rngI:
        for pJ in rngJ:
            pts.add((pI, pJ))
    if order is not None:
        # add intersections of diagonal psi_I = psi_J with the box
        pts |= {(Fr(0), Fr(0)), (P, P)}
        pts = {(a, b) for a, b in pts if ((a <= b) if order else (a >= b))}
    vals = []
    for pI, pJ in pts:
        thI = Fr(0) if I == 0 else pI + off[I]
        thJ = Fr(0) if J == 0 else pJ + off[J]
        vals.append(thI - thJ)
    return min(vals), max(vals)


def verify_clause(cl, m, t, ntr, inv, Y, H, Yinv, Hinv):
    odd = m % 2 == 1
    W = Fr(360, m)
    tl = [x for x in cl if abs(x) <= ntr]
    cond = [x for x in cl if abs(x) > ntr]
    if len(tl) != 1:
        return False, 'not exactly one triple literal'
    lit = tl[0]
    s = 1 if lit > 0 else -1
    C = inv[abs(lit)]
    lay = {x: x // m for x in C}
    S = sorted(set(lay.values()))
    if len(S) == 3:
        return False, 'three-layer triple: not covered by this verifier'
    # phase vars of S
    pv = [Y[(a, b)] for a, b in itertools.combinations([L for L in S if L != 0], 2)]
    if odd:
        pv += [H[L] for L in S if L != 0]
    fixed = {}
    for c in cond:
        v = abs(c)
        if v not in pv:
            return False, 'condition var %d not on the triple layers' % v
        val = (c < 0)        # literal must be false
        if v in fixed and fixed[v] != val:
            return False, 'condition part is a tautology?'
        fixed[v] = val
    free = [v for v in pv if v not in fixed]
    ncase = 0
    for bits in itertools.product([False, True], repeat=len(free)):
        asg = dict(fixed)
        asg.update(zip(free, bits))
        ncase += 1
        if len(S) == 1:
            a, b, c = C
            ang = {x: W * (x % m) for x in C}
            F = ivsin_deg(ang[b] - ang[a]) + ivsin_deg(ang[c] - ang[b]) + ivsin_deg(ang[a] - ang[c])
            if ivsign(F) != s:
                return False, 'single-layer sign mismatch'
            continue
        # two layers: which has two points
        cnt = {L: [x for x in C if lay[x] == L] for L in S}
        J = [L for L in S if len(cnt[L]) == 2][0]
        I = [L for L in S if len(cnt[L]) == 1][0]
        x, y = cnt[J]
        z = cnt[I][0]
        par = perm_parity([x, y, z], list(C))     # orient(C) = par * orient(x,y,z)
        target = s * par                          # need sign(orient(x,y,z)) = target
        kx, ky, kz = x % m, y % m, z % m
        c0 = W * (ky - kx)
        c1 = W * (kz - kx)
        c2 = W * (kz - ky)
        lo, hi = delta_interval(m, I, J, asg, Y, H)
        if not lo < hi:
            return False, 'empty/degenerate delta interval'
        sA = sin_sign_exact(c0)
        if sA * target < 0:
            return False, 'constant term has wrong sign (needs radius order) case %s' % asg
        z0 = (Fr(180) - c1 - c2) / 2
        # any zero z0 + 180n in the open interval (lo,hi)?
        import math
        n_lo = math.floor((lo - z0) / 180)
        bad = False
        for nn in range(n_lo - 1, n_lo + 4):
            zz = z0 + 180 * nn
            if lo < zz < hi:
                bad = True
        if bad:
            return False, 'B changes sign inside delta interval (%s,%s) case %s' % (lo, hi, asg)
        mid = (lo + hi) / 2
        Bm = ivsin_deg(mid + c2) - ivsin_deg(mid + c1)
        sb = ivsign(Bm)
        if sb == 0:
            return False, 'inconclusive interval sign'
        if sb != target:
            return False, 'B has wrong sign on interval (%s,%s) case %s' % (lo, hi, asg)
    return True, ncase


def main():
    m, t, fn = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    tv, inv, Y, H = numbering(m, t)
    ntr = len(tv)
    if len(sys.argv) > 4:
        meta = json.load(open(sys.argv[4]))
        assert meta['ntriple'] == ntr, (meta['ntriple'], ntr)
        assert {tuple(map(int, k.split(','))): v for k, v in meta['Y'].items()} == Y
        assert {int(k): v for k, v in meta.get('H', {}).items()} == H
        print('numbering matches', sys.argv[4])
    Yinv = {v: k for k, v in Y.items()}
    Hinv = {v: k for k, v in H.items()}
    ok = bad = 0
    ncases = 0
    from collections import Counter
    fails = Counter()
    for line in open(fn):
        cl = [int(x) for x in line.split()]
        assert cl[-1] == 0
        cl = cl[:-1]
        res, info = verify_clause(cl, m, t, ntr, inv, Y, H, Yinv, Hinv)
        if res:
            ok += 1
            ncases += info
        else:
            bad += 1
            fails[info.split(' case')[0]] += 1
            if bad <= 20:
                print('FAIL', cl, info)
    print('%s: %d clauses verified (%d cases), %d failed %s' % (fn, ok, ncases, bad, dict(fails)))


if __name__ == '__main__':
    main()
