#!/usr/bin/env python3
"""Binned refinement of the cone rules and threshold-order rules (cone_rules.py, thr_rules2.py) for even m.

New variables Z(i, b) = [psi_i < b U / B] for layers i = 1..t-1 and b = 1..B-1 (U = 2 pi / m), numbered after
NV0 (the variable count of the base CNF): Z(i, b) = NV0 + (i - 1)(B - 1) + b.  Ladder clauses Z(i,b) -> Z(i,b+1).
A cell of a triple (or of a layer pair) is a psi-order pattern of its free layers together with a bin for each of
them; the phase region of the cell is an open convex polytope (order chain intersected with the open bin boxes).
 * Cone rules on cells: as cone_rules.py, with the closed polytope's vertices (exact enumeration) in place of the
   simplex's; clause = (negated order literals) or (negated bin literals) or (orientation literal), emitted only
   where the order-only cone rule does not already give that literal.
 * Threshold-order rules on cells: as thr_rules2.py on the open interval of the pair's phase difference
   d = theta_j - theta_i over the cell (exact endpoints, multiples of U/B); exact endpoint values in
   Q(zeta_{16B}); emitted only where thr_rules2's order-only clause is absent.
Bin literals of layer L in bin b (0-based): Z(L, b+1) if b < B-1, and -Z(L, b) if b > 0.
Soundness: every real configuration (generic phases, gen.py step 0, also psi_i not equal to any bin boundary,
which a further small perturbation of the phases achieves) gives Z its truth values, satisfying the ladder; its
phases then lie in exactly one cell per triple/pair, where the lemma of cone_rules.py / thr_rules2.py applies.
usage: cell_rules.py m t B NV0 OUT.clauses"""
import sys, os, math, itertools, importlib.util
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m
G = _load('gen', 'gen.py'); CR = _load('cone', 'cone_rules.py'); T2 = _load('thr2', 'thr_rules2.py')


def solve3(rows, rhs):
    """exact solve of a square linear system (Fractions); None if singular"""
    n = len(rows)
    M = [list(r) + [b] for r, b in zip(rows, rhs)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [M[r][n] / M[r][r] for r in range(n)]


_VCACHE = {}


def polytope_vertices(order, bins, U, B):
    key = (len(order), tuple(bins[L] for L in order), U, B)
    if key not in _VCACHE:
        pos = list(range(len(order)))
        _VCACHE[key] = _polytope_vertices(pos, {k: bins[L] for k, L in enumerate(order)}, U, B)
    return [{L: v[k] for k, L in enumerate(order)} for v in _VCACHE[key]]


def _polytope_vertices(order, bins, U, B):
    """closed polytope {0 <= th_o1 <= ... <= th_on <= U} cap {b_L U/B <= th_L <= (b_L+1) U/B};
    returns list of vertex dicts, [] if the open polytope is empty"""
    n = len(order)
    if n == 0:
        return [{}]
    # constraints a.x <= c
    cons = []
    def e(k):
        v = [Fr(0)] * n; v[k] = Fr(1); return v
    for k in range(n - 1):
        v = [Fr(0)] * n; v[k] = Fr(1); v[k + 1] = Fr(-1); cons.append((v, Fr(0)))
    for k, L in enumerate(order):
        lo = Fr(bins[L]) * U / B; hi = Fr(bins[L] + 1) * U / B
        cons.append((e(k), hi)); cons.append(([-x for x in e(k)], -lo))
    verts = []
    for S in itertools.combinations(range(len(cons)), n):
        x = solve3([cons[s][0] for s in S], [cons[s][1] for s in S])
        if x is None:
            continue
        if all(sum(a * b for a, b in zip(c_[0], x)) <= c_[1] for c_ in cons):
            vt = {L: x[k] for k, L in enumerate(order)}
            if vt not in verts:
                verts.append(vt)
    # open polytope nonempty iff the closed one has full dimension: check strict feasibility of the centroid
    if not verts:
        return []
    cen = {L: sum(v[L] for v in verts) / len(verts) for L in order}
    x = [cen[L] for L in order]
    if not all(sum(a * b for a, b in zip(c_[0], x)) < c_[1] for c_ in cons):
        return []
    return verts


def build(m, t, B, NV0):
    E = G.Enc(m, 9, t)
    U = Fr(2, m)
    def Z(i, b):
        return NV0 + (i - 1) * (B - 1) + b
    def binlits(L, b):      # literals that are TRUE when psi_L is in bin b; the clause gets their negations
        r = []
        if b < B - 1: r.append(Z(L, b + 1))
        if b > 0: r.append(-Z(L, b))
        return r
    out = []
    for i in range(1, t):
        for b in range(1, B - 1):
            out.append((-Z(i, b), Z(i, b + 1)))
    # order-only cone rules for comparison
    _, cone_cls, _ = CR.build(m, t)
    cone_set = set(cone_cls)
    ncone = 0
    for C, v in E.tvar.items():
        pts = [divmod(x, m) for x in C]
        lay = [p[0] for p in pts]
        D = sorted(set(lay)); free = [L for L in D if L != 0]
        if not free:
            continue
        def ang(j):
            L, k = pts[j]
            return ({L: Fr(1)} if L != 0 else {}), Fr(2 * k, m)
        def lin(*terms):
            co = {}; cst = Fr(0)
            for sgn, (cd, cc) in terms:
                for L, a in cd.items(): co[L] = co.get(L, 0) + sgn * a
                cst += sgn * cc
            return co, cst
        def scale(f, s): return ({L: a * s for L, a in f[0].items()}, f[1] * s)
        A = [lin((1, ang(2)), (-1, ang(1))), lin((1, ang(0)), (-1, ang(2))), lin((1, ang(1)), (-1, ang(0)))]
        for perm in itertools.permutations(free):
            olits = [E.ylit(a, b) for a, b in zip(perm, perm[1:])]
            base_clause_pos = tuple(sorted([-y for y in olits] + [v], key=abs))
            base_clause_neg = tuple(sorted([-y for y in olits] + [-v], key=abs))
            if (v,) in cone_set or (-v,) in cone_set or base_clause_pos in cone_set or base_clause_neg in cone_set:
                continue
            for bs in itertools.product(range(B), repeat=len(perm)):
                if any(bs[k] > bs[k + 1] for k in range(len(bs) - 1)):
                    continue
                if B == 1:
                    continue
                bins = dict(zip(perm, bs))
                verts = polytope_vertices(perm, bins, U, B)
                if not verts:
                    continue
                signs = []; ok = True
                for d in D:
                    S = [j for j in range(3) if lay[j] >= d]
                    if len(S) == 1:
                        facs = [(1, A[S[0]])]
                    elif len(S) == 2:
                        a_, b_ = A[S[0]], A[S[1]]
                        hs = scale(lin((1, a_), (1, b_)), Fr(1, 2)); hd = scale(lin((1, a_), (-1, b_)), Fr(1, 2))
                        facs = [(2, hs), (1, (hd[0], hd[1] + Fr(1, 2)))]
                    else:
                        facs = [(-4, scale(A[0], Fr(1, 2))), (1, scale(A[1], Fr(1, 2))), (1, scale(A[2], Fr(1, 2)))]
                    sg = 1
                    for mult, f in facs:
                        if mult < 0: sg = -sg
                        fs = CR.factor_sign(f[0], f[1], verts)
                        if fs is None: ok = False; break
                        sg *= fs
                    if not ok: break
                    signs.append(sg)
                if not ok:
                    continue
                if all(x >= 0 for x in signs) and any(x > 0 for x in signs):
                    lit = v
                elif all(x <= 0 for x in signs) and any(x < 0 for x in signs):
                    lit = -v
                else:
                    continue
                bl = []
                for L in perm:
                    bl += [-x for x in binlits(L, bins[L])]
                out.append(tuple([-y for y in olits] + bl + [lit])); ncone += 1
    return out, ncone


if __name__ == '__main__':
    m, t, B, NV0 = map(int, sys.argv[1:5])
    out, nc = build(m, t, B, NV0)
    with open(sys.argv[5], 'w') as f:
        for c in out:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print('m=%d t=%d B=%d: %d clauses (cell cone rules %d, ladder %d)' % (m, t, B, len(out), nc, len(out) - nc))
