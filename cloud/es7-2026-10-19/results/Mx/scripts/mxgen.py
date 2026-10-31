#!/usr/bin/env python3
"""Mx: independent CNF for mirror-symmetric n-point sets with no convex k-gon.

Written from first principles (no code shared with tools/etv/gen_etv.py).

Points 0..n-1 sorted by x (distinct x).  chi(i,j,k), i<j<k, is True iff the triple is
counter-clockwise, i.e. j lies strictly below the chord ik ("cup triple").
Mirror (vertical axis): point i <-> point n-1-i.  The reflection reverses the plane's
orientation AND the x-order; for the sorted triple this gives
        chi(n-1-k, n-1-j, n-1-i) = chi(i,j,k)          (same sign; see README).
We use one variable per mirror orbit of triples (orbit substitution done at generation).
With --nomirror every triple gets its own variable (plain ES control).

Signotope axiom: for a<b<c<d the 4 signs chi(abc),chi(abd),chi(acd),chi(bcd) change sign
at most once; encoded by forbidding +-+ and -+- on every 3 of the 4 positions.

No convex k-gon (my own "anchored chain" encoding): a convex k-gon with leftmost vertex p
and rightmost q is a cup p..q with s vertices plus a cap p..q with t vertices, s+t=k+2,
s,t>=2.  Aux U[p,j,q,l] ("some cup of exactly l vertices starts at p and ends with j,q")
is defined one-directionally:
   chi(p,j,q)                      -> U[p,j,q,3]
   U[p,i,j,l] & chi(i,j,q)         -> U[p,j,q,l+1]
   U[p,j,q,l]                      -> EU[p,q,l]
and likewise C/EC for caps with -chi.  Forbidden: EU[p,q,s] & EC[p,q,t] for s+t=k+2,
s,t>=3, and U[p,j,q,k] / C[p,j,q,k] (a k-cup / k-cap is a k-gon with the other chain = edge).

Modes (only meaningful with mirror and odd n; axis point a=(n-1)/2):
  all       no case split; unit chi(0,1,2)=True (y-reflection, see README)
  top       axis point is a vertex of the upper hull: chi(i,a,k)=False for all i<a<k
            (no extra unit; the y-reflection was used to choose upper over lower)
  interior  axis point is interior: OR_{i<a<k} chi(i,a,k)  and  OR_{i<a<k} -chi(i,a,k),
            plus unit chi(0,1,2)=True
  none      no case-split clause and no unit (for validation)
"""
import argparse, itertools, json, sys

def mode_clauses(n, X, mode):
    m = n - 1; a = m // 2; out = []
    if mode == 'all':
        out.append(('sym', [X(0, 1, 2)]))
    elif mode == 'top':
        for i in range(a):
            for l in range(a + 1, n): out.append(('case', [-X(i, a, l)]))
    elif mode == 'interior':
        out.append(('case', [X(i, a, l) for i in range(a) for l in range(a + 1, n)]))
        out.append(('case', [-X(i, a, l) for i in range(a) for l in range(a + 1, n)]))
        out.append(('sym', [X(0, 1, 2)]))
    return out

def build(n, k, mirror=True, mode='none'):
    m = n - 1
    rep = {}; orbits = []
    for t in itertools.combinations(range(n), 3):
        i, j, l = t
        mt = (m - l, m - j, m - i) if mirror else t
        r = min(t, mt)
        if r not in rep:
            orbits.append(r); rep[r] = len(orbits)
        rep[t] = rep[r]
    nv = [len(orbits)]
    def X(i, j, l): return rep[(i, j, l)]
    def new():
        nv[0] += 1; return nv[0]
    cls = []          # (tag, clause)
    seen = set()
    def add(tag, c):
        c = tuple(sorted(set(c)))
        if any(-x in c for x in c): return            # tautology after substitution
        if c in seen: return
        seen.add(c); cls.append((tag, list(c)))
    # signotope
    for q in itertools.combinations(range(n), 4):
        tr = [X(*t) for t in itertools.combinations(q, 3)]   # lex order abc,abd,acd,bcd
        for x, y, z in itertools.combinations(tr, 3):
            add('sig', [-x, y, -z]); add('sig', [x, -y, z])
    # anchored chains
    U = {}; C = {}; EU = {}; EC = {}
    for sgn, V, E in ((1, U, EU), (-1, C, EC)):
        for p in range(n):
            for j in range(p + 1, n):
                for q in range(j + 1, n):
                    V[(p, j, q, 3)] = new()
                    add('aux', [-sgn * X(p, j, q), V[(p, j, q, 3)]])
            for l in range(3, k):
                for i in range(p + 1, n):
                    for j in range(i + 1, n):
                        if (p, i, j, l) not in V: continue
                        for q in range(j + 1, n):
                            key = (p, j, q, l + 1)
                            if key not in V: V[key] = new()
                            add('aux', [-V[(p, i, j, l)], -sgn * X(i, j, q), V[key]])
            for q in range(p + 2, n):
                for l in range(3, k):
                    vs = [V[(p, j, q, l)] for j in range(p + 1, q) if (p, j, q, l) in V]
                    if not vs: continue
                    e = new(); E[(p, q, l)] = e
                    for v in vs: add('aux', [-v, e])
            for key, v in V.items():
                if key[0] == p and key[3] == k: add('gon', [-v])
    for p in range(n):
        for q in range(p + 2, n):
            for s in range(3, k):
                t = k + 2 - s
                if 3 <= t < k and (p, q, s) in EU and (p, q, t) in EC:
                    add('gon', [-EU[(p, q, s)], -EC[(p, q, t)]])
    for tag, c in mode_clauses(n, X, mode): add(tag, c)
    return dict(n=n, k=k, nvars=nv[0], norient=len(orbits), orbits=orbits, rep=rep,
                clauses=cls)

def write(enc, path):
    with open(path, 'w') as f:
        f.write('c mxgen n=%d k=%d orient_vars=%d\n' % (enc['n'], enc['k'], enc['norient']))
        f.write('p cnf %d %d\n' % (enc['nvars'], len(enc['clauses'])))
        for _, c in enc['clauses']: f.write(' '.join(map(str, c)) + ' 0\n')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int); ap.add_argument('k', type=int)
    ap.add_argument('--mode', default='none', choices=['none', 'all', 'top', 'interior'])
    ap.add_argument('--nomirror', action='store_true')
    ap.add_argument('-o', required=True)
    ap.add_argument('--map', help='write orbit list (json) for decoding')
    a = ap.parse_args()
    enc = build(a.n, a.k, not a.nomirror, a.mode)
    write(enc, a.o)
    if a.map:
        json.dump({'n': a.n, 'k': a.k, 'orbits': enc['orbits']}, open(a.map, 'w'))
    from collections import Counter
    print('n=%d k=%d mode=%s mirror=%s vars=%d orient=%d clauses=%d %s' % (
        a.n, a.k, a.mode, not a.nomirror, enc['nvars'], enc['norient'], len(enc['clauses']),
        dict(Counter(t for t, _ in enc['clauses']))))
