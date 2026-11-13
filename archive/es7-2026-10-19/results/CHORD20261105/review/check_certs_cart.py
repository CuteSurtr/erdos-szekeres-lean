#!/usr/bin/env python3
"""Reviewer's certificate checker in CARTESIAN seed coordinates with exact Q(sqrt3) arithmetic.

Seeds z_i = (x_i, y_i) = vertex (i,0), i = 0..9; variable index i -> x_i, 10+i -> y_i.
Vertex (i,k) = Rot(60 k) z_i, Rot(60) = [[1/2, -sqrt3/2], [sqrt3/2, 1/2]] (exact Q(sqrt3) entries).
Record forms (each strictly positive in every normal-form configuration in which its literal holds):
  triple   (t, var, sg): sg * (2/sqrt3) * orient(t),  orient(a,b,c) = det(a,b)+det(b,c)+det(c,a);
           literal: sg*var  (orient(canonical triple of var) has sign sg).  t must be the canonical triple of var.
  phase_sign (i,j,sg):  sg * det(z_i,z_j)/sqrt3 = sg r_i r_j sin(theta_j - theta_i)/sqrt3;  literal Y(i,j) if sg=+1,
           -Y(i,j) if sg=-1 (i >= 1);  for i = 0 only sg = +1 (theta_0 = 0 < theta_j < 60), no literal.
  phase_plus (i,j):  dot(z_i,z_j) + det(z_i,z_j)/sqrt3 = (2/sqrt3) r_i r_j sin(theta_j - theta_i + 60) > 0, no literal.
  phase_minus(i,j):  dot(z_i,z_j) - det(z_i,z_j)/sqrt3 = (2/sqrt3) r_i r_j sin(60 - theta_j + theta_i) > 0, no literal.
           (theta_j - theta_i in (-60,60) for all normal-form configurations.)
  radius   (a<b): |z_a|^2 - |z_b|^2 > 0 (radii strictly decrease), no literal.
Accept iff (1) every weight is a positive integer, (2) every negated record literal is in the clause, and (3)
P = sum w * form is negative semidefinite (exact symmetric elimination over the ordered field Q(sqrt3)).
Soundness: if the clause were false in a configuration, every record literal would hold, so P > 0 there."""
import sys, json
from fractions import Fraction as F
from q3 import Q3, cos30, sin30
from indep_enc import TRIPLE_OF, Y as YVAR, NTRIP

NV = 20
INV_SQ3 = Q3(0, F(1, 3))          # 1/sqrt3
TWO_OVER_SQ3 = Q3(0, F(2, 3))     # 2/sqrt3


def point(x):
    i, k = divmod(x, 6)
    c, s = cos30(2 * k), sin30(2 * k)
    # (c x - s y, s x + c y)
    return ({i: c, 10 + i: -s}, {i: s, 10 + i: c})


def zero():
    return [[Q3(0) for _ in range(NV)] for _ in range(NV)]


def addprod(S, f, g, coef):
    """S += coef * f(z) g(z) (symmetrised)"""
    for u, a in f.items():
        for v, b in g.items():
            c = coef * a * b
            if c.iszero():
                continue
            if u == v:
                S[u][u] = S[u][u] + c
            else:
                h = c * F(1, 2)
                S[u][v] = S[u][v] + h
                S[v][u] = S[v][u] + h


def adddet(S, P, Q, coef):
    addprod(S, P[0], Q[1], coef)
    addprod(S, P[1], Q[0], -coef)


def adddot(S, P, Q, coef):
    addprod(S, P[0], Q[0], coef)
    addprod(S, P[1], Q[1], coef)


def nsd(S):
    A = [[-x for x in row] for row in S]
    idx = list(range(NV))
    while idx:
        for u in idx:
            d = A[u][u].sign()
            if d < 0:
                return False
            if d == 0 and any(not A[u][v].iszero() for v in idx):
                return False
        idx = [u for u in idx if not A[u][u].iszero()]
        if not idx:
            return True
        p = idx.pop(0)
        piv = A[p][p].inv()
        for u in idx:
            if A[u][p].iszero():
                continue
            f = A[u][p] * piv
            for v in idx:
                if not A[p][v].iszero():
                    A[u][v] = A[u][v] - f * A[p][v]
    return True


def check(cert):
    S = zero()
    need = set()
    recs = cert['records']
    if not recs:
        return False, 'no records'
    for r in recs:
        w = r['weight']
        if type(w) is not int or w <= 0:
            return False, 'bad weight'
        k = r['kind']
        if k == 'triple':
            t = tuple(r['triple']); sg = r['sign']; v = r['var']
            if sg not in (1, -1) or not (1 <= v <= NTRIP) or TRIPLE_OF[v] != t:
                return False, 'bad triple record'
            P = [point(x) for x in t]
            for a, b in zip(P, P[1:] + P[:1]):
                adddet(S, a, b, TWO_OVER_SQ3 * (w * sg))
            need.add(-sg * v)
        elif k == 'phase_sign':
            i, j = r['pair']; sg = r['sign']
            if not (0 <= i < j <= 9) or sg not in (1, -1):
                return False, 'bad phase_sign'
            if i == 0:
                if sg != 1:
                    return False, 'phase_sign with layer 0 must be +'
            else:
                y = YVAR[(i, j)]
                need.add(-y if sg == 1 else y)
            adddet(S, point(6 * i), point(6 * j), INV_SQ3 * (w * sg))
        elif k in ('phase_plus', 'phase_minus'):
            i, j = r['pair']
            if not (0 <= i <= 9 and 0 <= j <= 9 and i != j):
                return False, 'bad pair'
            e = 1 if k == 'phase_plus' else -1
            adddot(S, point(6 * i), point(6 * j), Q3(w))
            adddet(S, point(6 * i), point(6 * j), INV_SQ3 * (w * e))
        elif k == 'radius':
            a, b = r['pair']
            if not (0 <= a < b <= 9):
                return False, 'bad radius'
            adddot(S, point(6 * a), point(6 * a), Q3(w))
            adddot(S, point(6 * b), point(6 * b), Q3(-w))
        else:
            return False, 'unknown kind ' + k
    cl = set(cert['clause'])
    if not need <= cl:
        return False, 'clause misses negated record literal(s) %s' % sorted(need - cl)
    if not nsd(S):
        return False, 'not NSD'
    return True, 'ok' + ('' if need == cl else ' (clause is a weakening)')


if __name__ == '__main__':
    certf, clf = sys.argv[1], sys.argv[2]
    certs = [json.loads(l) for l in open(certf)]
    cls = [tuple(sorted(map(int, l.split()[:-1]), key=abs)) for l in open(clf) if l.strip()]
    cert_cls = [tuple(sorted(c['clause'], key=abs)) for c in certs]
    print('clauses', len(cls), 'certs', len(certs), 'cert clause set == clause file set:', set(cls) == set(cert_cls),
          'duplicates in cert file:', len(cert_cls) - len(set(cert_cls)))
    n = bad = 0
    for c in certs:
        ok, why = check(c)
        n += 1
        if not ok:
            bad += 1
            print('FAIL', why, c['clause'])
        elif why != 'ok':
            print('NOTE', why, c['clause'])
    print(json.dumps({'certs': n, 'failed': bad}))
    if len(sys.argv) > 3:
        # mutation tests: every mutated certificate must be rejected
        import random
        random.seed(12345)
        rej = tot = 0
        for c in certs:
            for mode in ('flip_triple', 'flip_phase', 'drop_phase', 'weight'):
                c2 = json.loads(json.dumps(c))
                recs = c2['records']
                if mode == 'flip_triple':
                    recs[0]['sign'] *= -1
                elif mode == 'flip_phase':
                    ps = [r for r in recs if r['kind'] == 'phase_sign']
                    if not ps: continue
                    ps[0]['sign'] *= -1
                elif mode == 'drop_phase':
                    ps = [r for r in recs if r['kind'] != 'triple']
                    if not ps: continue
                    recs.remove(random.choice(ps))
                else:
                    r = random.choice(recs); r['weight'] += random.choice([1, 2, 5])
                tot += 1
                rej += (not check(c2)[0])
        print(json.dumps({'mutations': tot, 'rejected': rej}))
