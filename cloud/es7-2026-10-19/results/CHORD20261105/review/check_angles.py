#!/usr/bin/env python3
"""Reviewer's independent exact validity check of chord-rule clauses (no certificates, no (D,E) coordinates).

For a clause  L  or  L v ylit  (L = +-var of a triple orbit, ylit a Y literal):
the triple variable means  orient(C) > 0  for the canonical sorted triple C (rotation by 60 deg is a symmetry of the
configuration, so this is well defined).  Point (i,k) = r_i * e(theta_i + 60 k), theta_0 = 0, theta_i in (0,60) deg.
orient(P1,P2,P3) = det(P1,P2) + det(P2,P3) + det(P3,P1),  det(r e(a), s e(b)) = r s sin(b - a).

* one-layer triple: orient = rho^2 * A with A an exact element of Q(sqrt3); clause valid iff sign(A) = sign(L).
* two-layer triple (two points in layer j, one in layer i), delta = theta_i - theta_j:
      orient = rho^2 * A + rho * r * G(delta),  G(delta) = alpha cos(delta) + beta sin(delta),  alpha, beta in Q(sqrt3).
  delta ranges: j = 0 -> (0,60); i = 0 -> (-60,0); else (-60,0) [theta_i < theta_j] and (0,60) [theta_i > theta_j].
  In each delta-scenario where the clause's Y literal is not already true, we require (radius free, all rho, r > 0):
      s*A >= 0  and  s*G >= 0 on the open interval,  and if A = 0 then s*G > 0 on it   (s = sign of L).
  For an interval of length 60 < 180, a sinusoid is >= 0 on the closed interval iff it is >= 0 at both endpoints
  (its negative set is a union of open intervals of length exactly 180), and a nonzero sinusoid that is >= 0 on a
  closed interval is > 0 on its interior (all zeros of a nonzero sinusoid are sign changes).  Endpoints are in
  {-60, 0, 60} deg, so everything is an exact sign test in Q(sqrt3).
  If the radius-free test fails, a radius-aware test (r_i > r_j iff i < j) is attempted and reported separately.
* three-layer triples: reported as UNHANDLED (none expected).
A clause passes only if every scenario passes.
"""
import sys, json, math, random
from fractions import Fraction as F
from q3 import Q3, cos30, sin30
from indep_enc import TRIPLE_OF, YINV, NTRIP


def sin_deg_mult60(m):        # sin(60 m)
    return sin30(2 * m)


def G_at(alpha, beta, d):     # d in degrees, multiple of 30
    return alpha * cos30(d // 30) + beta * sin30(d // 30)


def analyse(clause):
    tl = [l for l in clause if abs(l) <= NTRIP]
    yl = [l for l in clause if abs(l) > NTRIP]
    if len(tl) != 1 or len(yl) > 1:
        return False, 'unexpected clause shape'
    L = tl[0]; s = 1 if L > 0 else -1
    C = TRIPLE_OF[abs(L)]
    pts = [divmod(x, 6) for x in C]
    layers = [p[0] for p in pts]
    ls = sorted(set(layers))
    if len(ls) == 1:
        A = Q3(0)
        for (la, ka), (lb, kb) in zip(pts, pts[1:] + pts[:1]):
            A = A + sin_deg_mult60(kb - ka)
        ok = A.sign() == s
        return ok, 'one-layer A=%s sign %d want %d' % (A, A.sign(), s)
    if len(ls) == 3:
        return False, 'UNHANDLED three-layer triple %s' % (C,)
    j = max(ls, key=layers.count); i = min(ls, key=layers.count)
    assert layers.count(j) == 2 and layers.count(i) == 1
    # angle = e*delta + 60k (theta_j factored out), e = 1 for layer i
    A = Q3(0); alpha = Q3(0); beta = Q3(0)
    for (la, ka), (lb, kb) in zip(pts, pts[1:] + pts[:1]):
        ea = 1 if la == i else 0; eb = 1 if lb == i else 0
        c = 60 * (kb - ka)          # sin((eb-ea) delta + c)
        eps = eb - ea
        if eps == 0:
            assert la == lb == j
            A = A + sin30(c // 30)
        else:
            # sin(eps*delta + c) = sin c cos delta + eps cos c sin delta
            alpha = alpha + sin30(c // 30)
            beta = beta + eps * cos30(c // 30)
    # scenarios
    if j == 0:
        scen = [((0, 60), None)]
    elif i == 0:
        scen = [((-60, 0), None)]
    else:
        scen = [((-60, 0), 'i<j'), ((0, 60), 'i>j')]
    yinfo = None
    if yl:
        y = yl[0]; a, b = YINV[abs(y)]
        yinfo = (a, b, y > 0)
    msgs = []
    allok = True
    for (lo, hi), rel in scen:
        # is the clause's Y literal true throughout this scenario?
        ytrue = False
        if yinfo and rel is not None and {yinfo[0], yinfo[1]} == {i, j}:
            a, b, pos = yinfo
            # Y(a,b) = [theta_a < theta_b]
            thi_lt_thj = (rel == 'i<j')
            Yval = thi_lt_thj if (a, b) == (i, j) else (not thi_lt_thj)
            ytrue = (Yval == pos)
        if ytrue:
            msgs.append('(%d,%d):Y-true' % (lo, hi)); continue
        g_lo = G_at(alpha, beta, lo); g_hi = G_at(alpha, beta, hi)
        sA = A.sign()
        Gzero = alpha.iszero() and beta.iszero()
        ok = (s * sA >= 0) and (s * g_lo.sign() >= 0) and (s * g_hi.sign() >= 0) and not (sA == 0 and Gzero)
        # float cross-check of the endpoint lemma by dense sampling (diagnostic only)
        if ok:
            fa, fb = float(alpha), float(beta)
            for t in range(1, 600):
                d = math.radians(lo + (hi - lo) * t / 600)
                gv = fa * math.cos(d) + fb * math.sin(d)
                if s * gv < -1e-12:
                    raise AssertionError('endpoint lemma contradicted numerically %s' % (clause,))
        if not ok:
            # radius-aware attempt: t = r_i / r_j in (0,1) if i > j else (1, inf); need s*(A + t G(delta)) > 0
            ok2 = radius_aware(A, alpha, beta, lo, hi, s, i > j)
            msgs.append('(%d,%d):radius-free FAIL A=%s G(lo)=%s G(hi)=%s radius-aware=%s' % (lo, hi, A, g_lo, g_hi, ok2))
            allok = False
        else:
            msgs.append('(%d,%d):ok' % (lo, hi))
    return allok, 'two-layer j=%d i=%d C=%s ' % (j, i, C) + ' '.join(msgs)


def radius_aware(A, alpha, beta, lo, hi, s, inner):
    """numerical diagnostic only (dense sampling); returns 'plausible'/'violated'"""
    fA, fa, fb = float(A), float(alpha), float(beta)
    ts = [10 ** (-k / 4) for k in range(1, 60)] if inner else [10 ** (k / 4) for k in range(1, 60)]
    for t in ts:
        for u in range(1, 400):
            d = math.radians(lo + (hi - lo) * u / 400)
            v = fA + t * (fa * math.cos(d) + fb * math.sin(d))
            if s * v <= 0:
                return 'violated(t=%g,delta=%g)' % (t, math.degrees(d))
    return 'plausible'


if __name__ == '__main__':
    fn = sys.argv[1]
    n = bad = 0
    kinds = {}
    for line in open(fn):
        line = line.strip()
        if not line or line[0] in 'cp':
            continue
        lits = list(map(int, line.split()))
        assert lits[-1] == 0 and 0 not in lits[:-1]
        cl = lits[:-1]
        ok, msg = analyse(cl)
        n += 1
        key = msg.split(' C=')[0] if ok else 'FAIL'
        if not ok:
            bad += 1
            print('FAIL', cl, msg)
        kinds[(len(cl), msg.split()[0])] = kinds.get((len(cl), msg.split()[0]), 0) + 1
    print(json.dumps({'file': fn, 'clauses': n, 'failed': bad,
                      'by_shape': {'%d-lit/%s' % k: v for k, v in sorted(kinds.items())}}))
