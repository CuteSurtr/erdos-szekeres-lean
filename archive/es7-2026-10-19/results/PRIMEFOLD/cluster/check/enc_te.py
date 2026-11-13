#!/usr/bin/env python3
"""Independent re-implementation (written from scratch for the TE verification) of a sound SAT relaxation of
Proposition C (i) for an n-point generic tiny cluster C and an m-gon orbit.

Facts used (each holds for every real generic cluster satisfying F(1,1) = 1, which is itself forced by the full
orbit polygon):
  * work in the frame whose x-axis is the INWARD radial direction (a rotation by pi of the outward radial frame, so
    orientations are preserved); no segment of C is within pi/m of the tangent, so x-coordinates are distinct:
    label the points 0..n-1 by increasing x.
  * for i<j, t_ij = (angle(p_j - p_i) + pi/2) * m / pi  lies in (1, m-1), is never an integer (genericity), and is a
    strictly increasing function of the slope.  bin b_ij = floor(t_ij) in {1..m-2}.
  * for i<j<k: orient(p_i,p_j,p_k) > 0  <=>  slope_ij < slope_jk  <=>  t_ij < t_jk, and t_ik lies strictly between
    t_ij and t_jk.  Hence  left  => b_ij <= b_ik <= b_jk ;  right => b_ij >= b_ik >= b_jk.
  * (optional, flag sig) signotope axiom: for i<j<k<l the sign sequence (ijk, ijl, ikl, jkl) changes at most once.
  * a cup = x-increasing chain with left turns at consecutive triples (t increasing), a cap = right turns (t decr.).
    g(x) = longest cup whose last edge has t < x (i.e. b <= x-1), h(x) = longest cap whose last edge has t > m-x
    (i.e. b >= m-x).   Constraint (i): g(x) + h(x) <= x + 1 for x = 1..m-1.
Variables (all "forcing direction only", so the true values of a real cluster satisfy every clause):
  O[i,j,k]  : orient(p_i,p_j,p_k) > 0
  Q[i,j,v]  : b_ij >= v            (v = 2..m-2; v <= 1 is constant true, v >= m-1 constant false)
  U[l,i,j]  : some cup with >= l points ends with edge (i,j)     (l = 3..m; l = 2 is constant true)
  V[l,i,j]  : some cap with >= l points ends with edge (i,j)
  G[x,a]    : g(x) >= a   (a = 2..x+1)          H[x,b] : h(x) >= b
usage: enc_te.py m n sig out.cnf
"""
import sys
from itertools import combinations

TRUE, FALSE = 'T', 'F'


class Enc:
    def __init__(self):
        self.nv = 0
        self.clauses = []

    def var(self):
        self.nv += 1
        return self.nv

    def add(self, lits):
        out = []
        for l in lits:
            if l == TRUE:
                return
            if l == FALSE:
                continue
            out.append(l)
        if not out:
            raise RuntimeError('empty clause generated directly')
        self.clauses.append(out)


def neg(l):
    if l == TRUE:
        return FALSE
    if l == FALSE:
        return TRUE
    return -l


def build(m, n, sig):
    e = Enc()
    pairs = list(combinations(range(n), 2))
    O = {t: e.var() for t in combinations(range(n), 3)}
    Q = {(i, j, v): e.var() for (i, j) in pairs for v in range(2, m - 1)}

    def ge(i, j, v):          # literal for b_ij >= v
        if v <= 1:
            return TRUE
        if v >= m - 1:
            return FALSE
        return Q[i, j, v]

    # order encoding: b >= v+1 -> b >= v
    for (i, j) in pairs:
        for v in range(2, m - 2):
            e.add([-Q[i, j, v + 1], Q[i, j, v]])
    # turn / bin coupling
    for (i, j, k), o in O.items():
        for v in range(2, m - 1):
            # left:  b_ij >= v -> b_ik >= v ;  b_ik >= v -> b_jk >= v
            e.add([-o, neg(ge(i, j, v)), ge(i, k, v)])
            e.add([-o, neg(ge(i, k, v)), ge(j, k, v)])
            # right: b_jk >= v -> b_ik >= v ;  b_ik >= v -> b_ij >= v
            e.add([o, neg(ge(j, k, v)), ge(i, k, v)])
            e.add([o, neg(ge(i, k, v)), ge(i, j, v)])
    if sig:
        for (i, j, k, l) in combinations(range(n), 4):
            s = [O[i, j, k], O[i, j, l], O[i, k, l], O[j, k, l]]
            for a, b, c in combinations(range(4), 3):
                e.add([-s[a], s[b], -s[c]])
                e.add([s[a], -s[b], s[c]])
    U = {}
    V = {}
    for l in range(3, m + 1):
        for (i, j) in pairs:
            U[l, i, j] = e.var()
            V[l, i, j] = e.var()

    def cup(l, i, j):
        return TRUE if l == 2 else U[l, i, j]

    def cap(l, i, j):
        return TRUE if l == 2 else V[l, i, j]

    for (i, j, k), o in O.items():
        for l in range(3, m + 1):
            e.add([neg(cup(l - 1, i, j)), -o, U[l, j, k]])
            e.add([neg(cap(l - 1, i, j)), o, V[l, j, k]])
    G = {}
    H = {}
    for x in range(1, m):
        for a in range(2, x + 2):
            G[x, a] = e.var()
            H[x, a] = e.var()
    for x in range(1, m):
        for a in range(2, x + 2):
            for (i, j) in pairs:
                # cup of >= a points ending with (i,j) and b_ij <= x-1 (i.e. not b_ij >= x)  ->  g(x) >= a
                e.add([neg(cup(a, i, j)), ge(i, j, x), G[x, a]])
                # cap of >= a points ending with (i,j) and b_ij >= m-x  ->  h(x) >= a
                e.add([neg(cap(a, i, j)), neg(ge(i, j, m - x)), H[x, a]])
        # g(x) + h(x) <= x+1 with g, h >= 1:  forbid g >= a and h >= b for a + b = x + 2
        for a in range(1, x + 2):
            b = x + 2 - a
            ga = TRUE if a == 1 else G[x, a]
            hb = TRUE if b == 1 else H[x, b]
            e.add([neg(ga), neg(hb)])
    return e, dict(O=O, Q=Q, U=U, V=V, G=G, H=H)


if __name__ == '__main__':
    m, n, sig, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    e, _ = build(m, n, sig)
    with open(out, 'w') as f:
        f.write('p cnf %d %d\n' % (e.nv, len(e.clauses)))
        for c in e.clauses:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print('m=%d n=%d sig=%d vars=%d clauses=%d' % (m, n, sig, e.nv, len(e.clauses)))
