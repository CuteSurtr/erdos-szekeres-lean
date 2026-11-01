#!/usr/bin/env python3
"""Exact evaluation (written from scratch for TE) of the Lemma 1 blow-up formula for ONE orbit of a cluster C at
the vertices zeta^j of a regular m-gon, plus the centre O (m prime: 5 or 7), with every sign decided exactly in
Z[zeta_m] (verify_sets.ZetaSign).  Also prints Prop. C's profile g(x) = f_C((0,x)), h(x) = f_C((-x,0)).

usage: formula_zeta.py m FILE   -- FILE as in out/rb/*.pts; C = the rows supported on coordinates {0,1} other than
                                    the zero row (the cluster at vertex zeta^0); the set must be O + union zeta^j C.
"""
import sys
from itertools import combinations
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import verify_sets as vs

m = int(sys.argv[1])
rows = vs.load_zeta(sys.argv[2], m)
zs = vs.ZetaSign(m)
zero = [0] * m
C0 = [w for w in rows if w[0] > 0 and all(100 * abs(w[t]) < w[0] for t in range(1, m))]   # rows near zeta^0
shift = lambda w, j: [w[(t - j) % m] for t in range(m)]
# structure check: rows = {0} u union_j zeta^j C0
expect = {vs.canon(zero, m)} | {vs.canon(shift(w, j), m) for w in C0 for j in range(m)}
have = {vs.canon(w, m) for w in rows}
print('cluster size |C| =', len(C0), '; set = centre + one orbit of C:', expect == have, '; |S| =', len(rows))


def cross_sign(s, t):          # sign of cross(s, t) = Im(conj(s) t), s, t in Z[zeta]
    return zs.sign_im(vs.zmul_conj(s, t, m))


def sub(a, b):
    return [a[t] - b[t] for t in range(m)]


def neg(a):
    return [-x for x in a]


def f_chain(C, s, t, half):
    """longest ccw chain of C with edge directions in the open arc from direction s ccw to direction t
    (length < pi; if half, t = -s and the arc is the open half-circle left of s)."""
    n = len(C)
    D = {(p, q): sub(C[q], C[p]) for p in range(n) for q in range(n) if p != q}

    def inside(v):
        a = cross_sign(s, v)
        if a == 0:
            raise RuntimeError('cluster direction parallel to a base direction (non-generic)')
        if half:
            return a > 0
        b = cross_sign(v, t)
        if b == 0:
            raise RuntimeError('non-generic')
        return a > 0 and b > 0
    ok = {k: inside(v) for k, v in D.items()}
    best = 1
    stack = [(p, None, 1) for p in range(n)]
    while stack:
        p, vp, k = stack.pop()
        best = max(best, k)
        for q in range(n):
            if q != p and ok[p, q]:
                v = D[p, q]
                if vp is None or cross_sign(vp, v) > 0:
                    stack.append((q, v, k + 1))
    return best


V = [shift([1] + [0] * (m - 1), j) for j in range(m)]       # vertices zeta^j
clusters = {j: [shift(w, j) for w in C0] for j in range(m)}


def polygon_value(poly):
    """poly: list of base labels in ccw order, label j = vertex zeta^j, label 'O' = centre (one-point cluster)."""
    pos = lambda b: zero if b == 'O' else V[b]
    r = len(poly)
    tot = 0
    for i, b in enumerate(poly):
        if b == 'O':
            tot += 1
            continue
        prv, nxt = poly[i - 1], poly[(i + 1) % r]
        s = sub(pos(b), pos(prv))
        t = sub(pos(nxt), pos(b))
        tot += f_chain(clusters[b], s, t, r == 2)
    return tot


best = 0
arg = None
count = 0
for r in range(2, m + 1):
    for T in combinations(range(m), r):
        val = polygon_value(list(T))
        count += 1
        if val > best:
            best, arg = val, list(T)
# polygons through O: T inside an open half-plane through O, i.e. cyclically consecutive within < m/2 steps
for start in range(m):
    for span in range(0, (m - 1) // 2 + 1):      # indices start..start+span  (span*2pi/m < pi)
        idx = [(start + q) % m for q in range(span + 1)]
        for r in range(1, len(idx) + 1):
            for T in combinations(idx, r):
                if T[0] != idx[0] and r < len(idx) and False:
                    pass
                poly = ['O'] + list(T)
                # ccw order: O, then T by increasing angle (T is listed by increasing offset from start)
                val = polygon_value(poly)
                count += 1
                if val > best:
                    best, arg = val, poly


# mc(C) exactly
n = len(C0)


def O3(a, b, c):
    return cross_sign(sub(C0[b], C0[a]), sub(C0[c], C0[a]))


def hcmp(a, b):
    s = zs.sign_im(vs.zmul_conj([1] + [0] * (m - 1), sub(C0[a], C0[b]), m))
    if s == 0:
        raise RuntimeError
    return s


mcC = vs.largest_convex(n, O3, hcmp)
# Prop C profile (arcs measured from the ccw tangent at zeta^0): direction s for -x units / t for +x units are the
# chords from the vertex zeta^{-x} to zeta^0 and from zeta^0 to zeta^x
g = []
h = []
for x in range(1, m):
    chord_in = sub(V[0], V[(-x) % m])      # direction tangent - x units
    chord_out = sub(V[x % m], V[0])        # direction tangent + x units
    tangent_dir = sub(V[1], V[m - 1])      # parallel to the tangent at zeta^0 (direction 0 units)
    g.append(f_chain(C0, tangent_dir, chord_out, False))
    h.append(f_chain(C0, chord_in, tangent_dir, False))
cond_i = all(g[x - 1] + h[x - 1] <= x + 1 for x in range(1, m))
print('polygons evaluated:', count)
print('formula (1): max over base polygons =', best, 'at', arg, '; mc(C) =', mcC,
      '; predicted mc(S_e) for small e =', max(best, mcC), '(need <= %d)' % m)
print('profile g =', g, ' h =', h, ' (i) holds:', cond_i)
