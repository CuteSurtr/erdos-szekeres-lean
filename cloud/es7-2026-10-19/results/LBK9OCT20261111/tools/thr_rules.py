#!/usr/bin/env python3
"""Threshold-order rules for t nested regular m-gons (even m), variable numbering of C7UPPER/gen.py Enc(m, K, t).

Setting as in cone_rules.py.  Fix two layers i < j and the phase pattern of the pair (i = 0: theta_j in (0, 2pi/m);
i >= 1: psi_i < psi_j or psi_i > psi_j).  Every orbit variable whose three points lie on layers {i, j} (both used)
has the form F = a u_i + b u_j.  Parametrise the admissible (u_i, u_j) (0 < u_i < u_j) projectively by
w(t) = (1 - t) g1 + t g2, t in (0, 1), g1 = (1, 1), g2 = (0, 1): F(w(t)) = (1 - t) P + t Q with P = F(g1) (sum of
all three coefficients) and Q = F(g2) (sum of the coefficients of the layer-j points); P and Q are products of
sines (cone_rules.py, (3)).

Lemma (written proof, not refereed).  Let l = s v be a literal (s = +-1), p = s P, q = s Q, and suppose the signs of
p and q are constant and opposite on the pair's phase cell.  Then l is true exactly on one side of
t*(l) = p / (p - q): on t < t* if p > 0 > q ("small side"), on t > t* if p < 0 < q ("large side").
For two such literals l1, l2 on the same side, put Delta = p1 q2 - p2 q1.  Then t*(l1) <= t*(l2) iff Delta >= 0
(for both sides: the denominators p - q have equal signs).  Hence, if Delta has a constant sign on the cell:
  small side: Delta <= 0 on the cell  =>  (not l2 or l1)   [where l2 is true, t < t*(l2) <= t*(l1)];
  large side: Delta >= 0 on the cell  =>  (not l2 or l1).
(At t = t*(l2) = t*(l1) both forms vanish; real configurations in general position never have F = 0.)
Opposite sides never give an implication.  The clauses carry the pair's Y literal as a premise (none for i = 0).

Sign of Delta on the open phase interval I (verified numerics, not exact arithmetic): Delta is a sum of two products
of sines of affine functions of the pair's phase difference d; |dDelta/dd| <= L with L computed from the product
structure (|d/dd prod sin(c_k d + e_k)| <= sum |c_k|).  Delta is evaluated in double precision on a grid of I with
spacing h; a sign is accepted only if every grid value exceeds L h / 2 + 1e-9 in absolute value with that sign
(each point of I is within h/2 of a grid point; the double-precision error of each value is far below 1e-9).
Pairs that fail the test are skipped (no clause), which is always sound.

usage: thr_rules.py m t OUT.clauses
"""
import sys, os, math, itertools, importlib.util
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
s_ = importlib.util.spec_from_file_location('gen', os.path.join(HERE, 'gen.py'))
G = importlib.util.module_from_spec(s_); s_.loader.exec_module(G)
s2_ = importlib.util.spec_from_file_location('cone', os.path.join(HERE, 'cone_rules.py'))
CR = importlib.util.module_from_spec(s2_); s2_.loader.exec_module(CR)

NGRID = 4001
MARGIN = 1e-9


def build(m, t):
    E = G.Enc(m, 9, t)
    U = Fr(2, m)
    # group 2-layer orbit variables by layer pair
    bypair = {}
    for C, v in E.tvar.items():
        pts = [divmod(x, m) for x in C]
        D = sorted(set(p[0] for p in pts))
        if len(D) == 2:
            bypair.setdefault(tuple(D), []).append((v, pts))
    out = []
    stats = {'pairs_tested': 0, 'clauses': 0, 'skipped_nonconst': 0}
    for (i, j), lst in sorted(bypair.items()):
        # patterns: list of (premise literals, interval of d = theta_j - theta_i in units of pi)
        if i == 0:
            pats = [([], (Fr(0), U))]
        else:
            y = E.Y[(i, j)]             # psi_i < psi_j
            pats = [([-y], (Fr(0), U)), ([y], (-U, Fr(0)))]
        for prem, (dlo, dhi) in pats:
            # each form: P, Q as lists of (mult, [(cd, cc)]) with argument cd*d + cc (units of pi)
            forms = []
            for v, pts in lst:
                def ang(q):
                    L, k = pts[q]
                    return (Fr(1) if L == j else Fr(0)), Fr(2 * k, m)    # theta_i := 0 (rotation invariance)
                def lin(*terms):
                    cd = Fr(0); cc = Fr(0)
                    for sg, (a, b) in terms:
                        cd += sg * a; cc += sg * b
                    return cd, cc
                A = [lin((1, ang(2)), (-1, ang(1))), lin((1, ang(0)), (-1, ang(2))), lin((1, ang(1)), (-1, ang(0)))]
                lay = [p[0] for p in pts]
                def gen_factors(S):
                    if len(S) == 1:
                        return 1, [A[S[0]]]
                    if len(S) == 2:
                        a, b = A[S[0]], A[S[1]]
                        hs = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                        hd = ((a[0] - b[0]) / 2, (a[1] - b[1]) / 2 + Fr(1, 2))
                        return 2, [hs, hd]
                    return -4, [(A[0][0] / 2, A[0][1] / 2), (A[1][0] / 2, A[1][1] / 2), (A[2][0] / 2, A[2][1] / 2)]
                Pm, Pf = gen_factors([0, 1, 2])
                Qm, Qf = gen_factors([q for q in range(3) if lay[q] == j])
                # exact constant signs on the open interval (dlo, dhi)
                def fsign(mult, facs):
                    sg = 1 if mult > 0 else -1
                    for cd, cc in facs:
                        f = CR.factor_sign({'d': cd}, cc, [{'d': dlo}, {'d': dhi}])
                        if f is None:
                            return None
                        sg *= f
                    return sg
                ps, qs = fsign(Pm, Pf), fsign(Qm, Qf)
                if ps is None or qs is None:
                    stats['skipped_nonconst'] += 1
                    continue
                if ps * qs >= 0:
                    continue          # forced (cone rule) or degenerate: no threshold
                forms.append((v, Pm, Pf, Qm, Qf, ps, qs))
            if len(forms) < 2:
                continue
            # numeric grid on the closed interval
            dd = np.linspace(float(dlo), float(dhi), NGRID)
            h = float(dhi - dlo) / (NGRID - 1)
            def val(mult, facs):
                r = np.full_like(dd, float(mult))
                for cd, cc in facs:
                    r = r * np.sin(math.pi * (float(cd) * dd + float(cc)))
                return r
            def lip(mult, facs):
                return abs(mult) * math.pi * sum(abs(float(cd)) for cd, _ in facs)
            PV = [val(f[1], f[2]) for f in forms]
            QV = [val(f[3], f[4]) for f in forms]
            PL = [lip(f[1], f[2]) for f in forms]
            QL = [lip(f[3], f[4]) for f in forms]
            PB = [abs(f[1]) for f in forms]      # |P| <= |mult|
            QB = [abs(f[3]) for f in forms]
            for s1 in (1, -1):
                for s2 in (1, -1):
                    for a in range(len(forms)):
                        for b in range(len(forms)):
                            if a == b:
                                continue
                            fa, fb = forms[a], forms[b]
                            p1, q1 = s1 * fa[5], s1 * fa[6]
                            p2, q2 = s2 * fb[5], s2 * fb[6]
                            side1 = 'S' if p1 > 0 else 'L'
                            side2 = 'S' if p2 > 0 else 'L'
                            if side1 != side2:
                                continue
                            stats['pairs_tested'] += 1
                            # Delta = p1 q2 - p2 q1 with p = s P, q = s Q (numeric values)
                            Dv = (s1 * s2) * (PV[a] * QV[b] - PV[b] * QV[a])
                            L = (PL[a] * QB[b] + PB[a] * QL[b] + PL[b] * QB[a] + PB[b] * QL[a])
                            thr = L * h / 2 + MARGIN
                            if os.environ.get('THR_SAMPLED'):      # exploration only: open-interval samples, no bound
                                Dv = Dv[1:-1]; thr = 1e-12
                            if side1 == 'S':
                                ok = bool(np.all(Dv < -thr))
                            else:
                                ok = bool(np.all(Dv > thr))
                            if ok:
                                l1 = s1 * fa[0]; l2 = s2 * fb[0]
                                out.append(tuple(prem + [-l2, l1]))
                                stats['clauses'] += 1
    return E, out, stats


if __name__ == '__main__':
    m, t = int(sys.argv[1]), int(sys.argv[2])
    E, cls, st = build(m, t)
    with open(sys.argv[3], 'w') as f:
        for c in cls:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print('m=%d t=%d threshold-order clauses %d; %s' % (m, t, len(cls), st))
