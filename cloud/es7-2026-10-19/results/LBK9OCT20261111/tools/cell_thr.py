#!/usr/bin/env python3
"""[cell_thr.py] Cell (bin) version of thr_rules2.py: same lemma and verification, applied on the phase-difference
interval of a cell (order pattern of the pair plus a bin of each free layer, B bins of width U/B; bin variables
Z(i, b) = [psi_i < b U / B] numbered NV0 + (i - 1)(B - 1) + b as in cell_rules.py).  Exact endpoint arithmetic in
Q(zeta_{2N}), zeta = e^{i pi/N}, N = 8B.  Clauses are emitted only where the order-only clause of thr_rules2.py is
absent.  usage: cell_thr.py m t B NV0 THR2_CLAUSES OUT.clauses
--- docstring of thr_rules2.py follows ---
Threshold-order rules, version 2 (same lemma as thr_rules.py; see its docstring), with a sign verification of
Delta on the open phase interval that also handles zeros of Delta at the interval's endpoints:
  * exact values of Delta and Delta' at the endpoints in Q(zeta_16) (all arguments there are multiples of pi/8):
    exact zero test; if Delta(e) = 0, the one-sided derivative D1 = dir * Delta'(e) must be nonzero with the
    required sign, and then |Delta(e + dir x)| >= |D1| x - L2 x^2 / 2 > 0 for 0 < x < 2|D1|/L2;
  * on the rest, a second-order bisection with rigorous bounds: on [x0, x1] with centre c and width w,
    sigma Delta(y) >= sigma Delta(c) - |Delta'(c)| w/2 - L2 w^2/8 for all y in [x0, x1];
    accepted when this exceeds 1e-9 (double-precision values; their rounding error is far below 1e-9).
  L2 bounds |Delta''| from the product structure: |(prod_k sin(pi(c_k d + e_k)))''| <= pi^2 (sum |c_k|)^2.
Pairs that fail are skipped (sound).  d is measured in units of pi.
usage: thr_rules2.py m t OUT.clauses"""
import sys, os, math, importlib.util
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
s_ = importlib.util.spec_from_file_location('gen', os.path.join(HERE, 'gen.py'))
G = importlib.util.module_from_spec(s_); s_.loader.exec_module(G)
s2_ = importlib.util.spec_from_file_location('cone', os.path.join(HERE, 'cone_rules.py'))
CR = importlib.util.module_from_spec(s2_); s2_.loader.exec_module(CR)

MARGIN = 1e-9
PI = math.pi

# ---------------- exact arithmetic in Q(zeta_16), zeta = e^{i pi/8}, zeta^8 = -1
NF = 8          # set in main: zeta = e^{i pi/NF}, zeta^NF = -1

def zpow(p):
    p %= 2 * NF
    v = [Fr(0)] * NF
    if p < NF:
        v[p] = Fr(1)
    else:
        v[p - NF] = Fr(-1)
    return v

def zadd(a, b): return [x + y for x, y in zip(a, b)]
def zsub(a, b): return [x - y for x, y in zip(a, b)]
def zscale(a, s): return [x * s for x in a]
def zmul(a, b):
    r = [Fr(0)] * NF
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b):
            if y == 0: continue
            k = i + j
            if k < NF: r[k] += x * y
            else: r[k - NF] -= x * y
    return r
def ONE_(): return zpow(0)
def HALF_OVER_I_(): return zscale(zpow(NF // 2), Fr(-1, 2))          # 1/(2i) = -i/2

def zsin(r):
    """sin(pi r), r a Fraction with denominator dividing 8"""
    p = r * NF; assert p.denominator == 1; p = int(p)
    return zmul(zsub(zpow(p), zpow(-p)), HALF_OVER_I_())

def zcos(r):
    p = r * NF; assert p.denominator == 1; p = int(p)
    return zscale(zadd(zpow(p), zpow(-p)), Fr(1, 2))

def zfloat(a):
    z = sum(complex(float(x)) * complex(math.cos(PI * k / NF), math.sin(PI * k / NF)) for k, x in enumerate(a))
    return z.real

def ziszero(a): return all(x == 0 for x in a)

# ---------------- products of sines: (mult, [(c, e)]) means mult * prod sin(pi (c d + e))
def pval(P, d):
    m, fs = P
    r = m
    for c, e in fs:
        r *= math.sin(PI * (c * d + e))
    return r

def pder(P, d):
    m, fs = P
    tot = 0.0
    for k, (c, e) in enumerate(fs):
        t = m * PI * c * math.cos(PI * (c * d + e))
        for l, (c2, e2) in enumerate(fs):
            if l != k:
                t *= math.sin(PI * (c2 * d + e2))
        tot += t
    return tot

def pval_exact(P, d):
    m, fs = P
    r = zscale(ONE_(), Fr(m))
    for c, e in fs:
        r = zmul(r, zsin(c * d + e))
    return r

def pder_exact(P, d):
    """derivative / pi"""
    m, fs = P
    tot = [Fr(0)] * NF
    for k, (c, e) in enumerate(fs):
        t = zscale(zcos(c * d + e), Fr(m) * c)
        for l, (c2, e2) in enumerate(fs):
            if l != k:
                t = zmul(t, zsin(c2 * d + e2))
        tot = zadd(tot, t)
    return tot

def bounds(P):
    m, fs = P
    S = sum(abs(float(c)) for c, _ in fs)
    return abs(m), abs(m) * PI * S, abs(m) * PI * PI * S * S


def verify(Pa, Qa, Pb, Qb, sg, sigma, dlo, dhi):
    """True if sigma * sg * (Pa Qb - Pb Qa) > 0 on the open interval (dlo, dhi) (Fractions, units of pi)"""
    Ba, Ca, Da = bounds(Pa); Bqa, Cqa, Dqa = bounds(Qa)
    Bb, Cb, Db = bounds(Pb); Bqb, Cqb, Dqb = bounds(Qb)
    L2 = (Da * Bqb + 2 * Ca * Cqb + Ba * Dqb) + (Db * Bqa + 2 * Cb * Cqa + Bb * Dqa)
    def D(x):
        return sg * (pval(Pa, x) * pval(Qb, x) - pval(Pb, x) * pval(Qa, x))
    def Dp(x):
        return sg * (pder(Pa, x) * pval(Qb, x) + pval(Pa, x) * pder(Qb, x)
                     - pder(Pb, x) * pval(Qa, x) - pval(Pb, x) * pder(Qa, x))
    lo, hi = float(dlo), float(dhi)
    for e, dirn in ((dlo, 1), (dhi, -1)):
        ex = zsub(zmul(pval_exact(Pa, e), pval_exact(Qb, e)), zmul(pval_exact(Pb, e), pval_exact(Qa, e)))
        if ziszero(ex):
            d1 = zsub(zadd(zmul(pder_exact(Pa, e), pval_exact(Qb, e)), zmul(pval_exact(Pa, e), pder_exact(Qb, e))),
                      zadd(zmul(pder_exact(Pb, e), pval_exact(Qa, e)), zmul(pval_exact(Pb, e), pder_exact(Qa, e))))
            if ziszero(d1):
                return False
            D1 = dirn * sg * PI * zfloat(d1)
            if abs(D1) < 1e-9 or (D1 > 0) != (sigma > 0):
                return False
            eta = 2 * abs(D1) / L2
            if dirn > 0: lo = float(e) + eta / 2
            else: hi = float(e) - eta / 2
        else:
            v = sg * zfloat(ex)
            if abs(v) < 1e-9 or (v > 0) != (sigma > 0):
                return False
    if lo >= hi:
        return True
    stack = [(lo, hi)]
    nodes = 0
    while stack:
        x0, x1 = stack.pop()
        nodes += 1
        if nodes > 20000:
            return False
        c = (x0 + x1) / 2; w = x1 - x0
        val = sigma * D(c) - abs(Dp(c)) * w / 2 - L2 * w * w / 8
        if val > MARGIN:
            continue
        if sigma * D(c) <= 0 or w < 1e-10:
            return False
        stack.append((x0, c)); stack.append((c, x1))
    return True


def build(m, t, B, NV0, thr2_set):
    E = G.Enc(m, 9, t)
    U = Fr(2, m); W = U / B
    def Z(i, b): return NV0 + (i - 1) * (B - 1) + b
    def binneg(L, b):        # negations of the literals true when psi_L is in bin b
        r = []
        if b < B - 1: r.append(-Z(L, b + 1))
        if b > 0: r.append(Z(L, b))
        return r
    bypair = {}
    for C, v in E.tvar.items():
        pts = [divmod(x, m) for x in C]
        D = sorted(set(p[0] for p in pts))
        if len(D) == 2:
            bypair.setdefault(tuple(D), []).append((v, pts))
    out = []
    st = {'tested': 0, 'clauses': 0, 'rejected': 0, 'dup': 0}
    for (i, j), lst in sorted(bypair.items()):
        cells = []
        if i == 0:
            for bj in range(B):
                cells.append(([], binneg(j, bj), (bj * W, (bj + 1) * W)))
        else:
            y = E.Y[(i, j)]
            for bi in range(B):
                for bj in range(B):
                    lo_i, hi_i, lo_j, hi_j = bi * W, (bi + 1) * W, bj * W, (bj + 1) * W
                    if bi <= bj:      # psi_i < psi_j
                        cells.append(([-y], binneg(i, bi) + binneg(j, bj), (max(Fr(0), lo_j - hi_i), hi_j - lo_i)))
                    if bj <= bi:      # psi_i > psi_j
                        cells.append(([y], binneg(i, bi) + binneg(j, bj), (lo_j - hi_i, min(Fr(0), hi_j - lo_i))))
        for prem, bneg, (dlo, dhi) in cells:
            if not dlo < dhi:
                continue
            forms = []
            for v, pts in lst:
                def ang(q):
                    L, k = pts[q]
                    return (Fr(1) if L == j else Fr(0)), Fr(2 * k, m)
                def lin(*terms):
                    cd = Fr(0); cc = Fr(0)
                    for sgn, (a_, b_) in terms:
                        cd += sgn * a_; cc += sgn * b_
                    return cd, cc
                A = [lin((1, ang(2)), (-1, ang(1))), lin((1, ang(0)), (-1, ang(2))), lin((1, ang(1)), (-1, ang(0)))]
                lay = [p[0] for p in pts]
                def gf(S):
                    if len(S) == 1:
                        return (1, [A[S[0]]])
                    if len(S) == 2:
                        a_, b_ = A[S[0]], A[S[1]]
                        return (2, [((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2), ((a_[0] - b_[0]) / 2, (a_[1] - b_[1]) / 2 + Fr(1, 2))])
                    return (-4, [(A[q][0] / 2, A[q][1] / 2) for q in range(3)])
                P = gf([0, 1, 2]); Q = gf([q for q in range(3) if lay[q] == j])
                def fsign(F):
                    sg = 1 if F[0] > 0 else -1
                    for cd, cc in F[1]:
                        f = CR.factor_sign({'d': cd}, cc, [{'d': dlo}, {'d': dhi}])
                        if f is None:
                            return None
                        sg *= f
                    return sg
                ps, qs = fsign(P), fsign(Q)
                if ps is None or qs is None or ps * qs >= 0:
                    continue
                forms.append((v, P, Q, ps, qs))
            for a in range(len(forms)):
                for b in range(len(forms)):
                    if a == b:
                        continue
                    va, Pa, Qa, psa, qsa = forms[a]
                    vb, Pb, Qb, psb, qsb = forms[b]
                    for s1 in (1, -1):
                        for s2 in (1, -1):
                            p1 = s1 * psa; p2 = s2 * psb
                            if (p1 > 0) != (p2 > 0):
                                continue
                            l1, l2 = s1 * va, -(s2 * vb)
                            if tuple(prem + [l2, l1]) in thr2_set:
                                st['dup'] += 1
                                continue
                            sigma = -1 if p1 > 0 else 1
                            st['tested'] += 1
                            if verify(Pa, Qa, Pb, Qb, s1 * s2, sigma, dlo, dhi):
                                out.append(tuple(prem + bneg + [l2, l1]))
                                st['clauses'] += 1
                            else:
                                st['rejected'] += 1
    return out, st


if __name__ == '__main__':
    m, t, B, NV0 = map(int, sys.argv[1:5])
    NF = 8 * B
    thr2_set = set()
    for line in open(sys.argv[5]):
        if line.strip():
            thr2_set.add(tuple(int(x) for x in line.split()[:-1]))
    out, st = build(m, t, B, NV0, thr2_set)
    with open(sys.argv[6], 'w') as f:
        for c in out:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print('m=%d t=%d B=%d cell threshold-order clauses %d; %s' % (m, t, B, len(out), st))
