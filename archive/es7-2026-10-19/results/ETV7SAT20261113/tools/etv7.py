#!/usr/bin/env python3
"""etv7.py -- CNF for the Erdos-Tuza-Valtr instance "n points, no (A+1)-cap, no (B+1)-cup,
no convex G-gon" in the signotope (x-monotone triple orientation) relaxation.

Derived from theory310-20261113/etv_sat2.py (SHA-256 ecc8a4e9...), with optional extras.

Points 0..n-1 are sorted by x.  Base variables O(i,j,k), i<j<k: true = cup triple
(k above the line ij, positive orientation), false = cap triple.

BASE (identical in meaning to etv_sat2.py):
  signotope axioms on every 4-tuple (the sequence O(ijk),O(ijl),O(ikl),O(jkl) changes sign at
  most once);
  SU_b(s,j,k), 3<=b<=B: "some b-cup starts at s and ends with the pair (j,k)" (one-sided);
  SC_a(s,j,k), 3<=a<=A: the same for caps;
  no (B+1)-cup, no (A+1)-cap;
  U_b(s,t), K_a(s,t): "some b-cup / a-cap from s to t" (one-sided);
  not K_a(s,t) or not U_b(s,t) whenever a+b = G+2 (an a-cap and a b-cup on common endpoints are
  a+b-2 = G points in convex position).

EXTRAS (each is satisfied by the semantic assignment of a real point set, see README section 2):
  --back   : mirror chains  TU_b(i,j,t) "some b-cup starts with the pair (i,j) and ends at t",
             TC_a(i,j,t); they also imply U_b / K_a.
  --lab    : unanchored pair labels EU_b(j,k) "some b-cup ends with (j,k)", EC_a(j,k), and (with
             --back) FU_b(i,j) "some b-cup starts with (i,j)", FC_a(i,j), with their growth and
             ceiling clauses.
  --sym    : mirror symmetry breaking  O(0,1,2) -> O(n-3,n-2,n-1)   (see README section 3).
  --units FILE : extra unit literals in the form "+i,j,k" / "-i,j,k" (orientation literals),
             one cube per line is NOT handled here (see cubes.py); FILE lists units for a single
             cube.
Output: DIMACS CNF, plus a JSON variable map (out + '.map.json') for decoding.
"""
import itertools, sys, json, argparse


def build(n, A, B, G, out, back=False, lab=False, sym=False, extra_clauses=None, write_map=True):
    nv = 0

    def new():
        nonlocal nv
        nv += 1
        return nv
    C3 = list(itertools.combinations(range(n), 3))
    pairs = list(itertools.combinations(range(n), 2))
    O = {t: new() for t in C3}
    SU = {b: {t: new() for t in C3} for b in range(3, B + 1)}
    SC = {a: {t: new() for t in C3} for a in range(3, A + 1)}
    U = {b: {p: new() for p in pairs} for b in range(3, B + 1)}
    K = {a: {p: new() for p in pairs} for a in range(3, A + 1)}
    cl = []
    # signotope axioms
    for i, j, k, l in itertools.combinations(range(n), 4):
        seq = [O[(i, j, k)], O[(i, j, l)], O[(i, k, l)], O[(j, k, l)]]
        for a, b, c in itertools.combinations(range(4), 3):
            x, y, z = seq[a], seq[b], seq[c]
            cl.append((-x, y, -z))
            cl.append((x, -y, z))
    # forward chains anchored at their first point
    for s, j, k in C3:
        cl.append((-O[(s, j, k)], SU[3][(s, j, k)]))
        cl.append((O[(s, j, k)], SC[3][(s, j, k)]))
    for s, i, j, k in itertools.combinations(range(n), 4):
        o = O[(i, j, k)]
        for b in range(4, B + 1):
            cl.append((-SU[b - 1][(s, i, j)], -o, SU[b][(s, j, k)]))
        cl.append((-SU[B][(s, i, j)], -o))          # no (B+1)-cup
        for a in range(4, A + 1):
            cl.append((-SC[a - 1][(s, i, j)], o, SC[a][(s, j, k)]))
        cl.append((-SC[A][(s, i, j)], o))           # no (A+1)-cap
    for s, j, t in C3:
        for b in range(3, B + 1):
            cl.append((-SU[b][(s, j, t)], U[b][(s, t)]))
        for a in range(3, A + 1):
            cl.append((-SC[a][(s, j, t)], K[a][(s, t)]))
    # polygons
    for p in pairs:
        for a in range(3, A + 1):
            b = G + 2 - a
            if 3 <= b <= B:
                cl.append((-K[a][p], -U[b][p]))
    vmap = {'n': n, 'A': A, 'B': B, 'G': G, 'O_first': 1, 'O_last': len(C3)}
    if back:
        TU = {b: {t: new() for t in C3} for b in range(3, B + 1)}
        TC = {a: {t: new() for t in C3} for a in range(3, A + 1)}
        for i, j, t in C3:
            cl.append((-O[(i, j, t)], TU[3][(i, j, t)]))
            cl.append((O[(i, j, t)], TC[3][(i, j, t)]))
        for h, i, j, t in itertools.combinations(range(n), 4):
            o = O[(h, i, j)]
            for b in range(4, B + 1):
                cl.append((-TU[b - 1][(i, j, t)], -o, TU[b][(h, i, t)]))
            cl.append((-TU[B][(i, j, t)], -o))
            for a in range(4, A + 1):
                cl.append((-TC[a - 1][(i, j, t)], o, TC[a][(h, i, t)]))
            cl.append((-TC[A][(i, j, t)], o))
        for s, j, t in C3:
            for b in range(3, B + 1):
                cl.append((-TU[b][(s, j, t)], U[b][(s, t)]))
            for a in range(3, A + 1):
                cl.append((-TC[a][(s, j, t)], K[a][(s, t)]))
    if lab:
        EU = {b: {p: new() for p in pairs} for b in range(3, B + 1)}
        EC = {a: {p: new() for p in pairs} for a in range(3, A + 1)}
        for i, j, k in C3:
            o = O[(i, j, k)]
            cl.append((-o, EU[3][(j, k)]))
            cl.append((o, EC[3][(j, k)]))
            for b in range(4, B + 1):
                cl.append((-EU[b - 1][(i, j)], -o, EU[b][(j, k)]))
            cl.append((-EU[B][(i, j)], -o))
            for a in range(4, A + 1):
                cl.append((-EC[a - 1][(i, j)], o, EC[a][(j, k)]))
            cl.append((-EC[A][(i, j)], o))
        if back:
            FU = {b: {p: new() for p in pairs} for b in range(3, B + 1)}
            FC = {a: {p: new() for p in pairs} for a in range(3, A + 1)}
            for i, j, k in C3:
                o = O[(i, j, k)]
                cl.append((-o, FU[3][(i, j)]))
                cl.append((o, FC[3][(i, j)]))
                for b in range(4, B + 1):
                    cl.append((-FU[b - 1][(j, k)], -o, FU[b][(i, j)]))
                cl.append((-FU[B][(j, k)], -o))
                for a in range(4, A + 1):
                    cl.append((-FC[a - 1][(j, k)], o, FC[a][(i, j)]))
                cl.append((-FC[A][(j, k)], o))
    if sym:
        cl.append((-O[(0, 1, 2)], O[(n - 3, n - 2, n - 1)]))
    if extra_clauses:
        for c in extra_clauses:
            cl.append(tuple((1 if s > 0 else -1) * O[t] for s, t in c))
    with open(out, 'w') as f:
        f.write(f'p cnf {nv} {len(cl)}\n')
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    if write_map:
        with open(out + '.map.json', 'w') as f:
            json.dump(vmap, f)
    return nv, len(cl)


def ovar(n, i, j, k):
    """index of O(i,j,k) (1-based), combinations order"""
    # rank of the 3-subset in lexicographic order
    from math import comb
    r = 0
    prev = -1
    for pos, x in enumerate((i, j, k)):
        for y in range(prev + 1, x):
            r += comb(n - 1 - y, 2 - pos)
        prev = x
    return r + 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('A', type=int, help='longest allowed cap (no (A+1)-cap)')
    ap.add_argument('B', type=int, help='longest allowed cup (no (B+1)-cup)')
    ap.add_argument('G', type=int, help='forbidden convex G-gon')
    ap.add_argument('out')
    ap.add_argument('--back', action='store_true')
    ap.add_argument('--lab', action='store_true')
    ap.add_argument('--sym', action='store_true')
    a = ap.parse_args()
    print(build(a.n, a.A, a.B, a.G, a.out, back=a.back, lab=a.lab, sym=a.sym))
