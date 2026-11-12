#!/usr/bin/env python3
"""Independent exact verifier (standard library only) for an m-fold point set, m in {3, 4, 5}, given in the ES8SYM .pts
format: one point per line, integers w_0..w_{m-1} for the point sum_j w_j zeta^j, zeta = e^{2 pi i/m}.

Exact arithmetic:
  m = 4: Cartesian integer coordinates x = w0 - w2, y = w1 - w3 (zeta = i); rotation (x, y) -> (-y, x).
  m = 3: oblique integer coordinates z = a + b*omega, a = w0 - w2, b = w1 - w2 (omega^2 = -1 - omega); the linear map
         (a, b) -> a + b*omega has determinant sqrt(3)/2 > 0, so orientations and convex position are those of the
         integer pairs; rotation (a, b) -> (-b, a - b).
  m = 5: elements of Z[zeta_5], reduced so that w_4 = 0 (1 + zeta + ... + zeta^4 = 0).  For z = sum c_j zeta^j,
         Im z = sin(2pi/5) * [(c1 - c4) + (c2 - c3)(sqrt5 - 1)/2] and
         Re z = c0 + (c1 + c4)(sqrt5 - 1)/4 - (c2 + c3)(sqrt5 + 1)/4,
         so every orientation sign Im(conj(q - p)(r - p)) and every coordinate comparison is the sign of an element
         A + B sqrt5 of Q(sqrt5) with integers A, B (decided exactly); rotation = cyclic shift of (w_0..w_4).
Checks: distinct points, the centre is present at most as the all-zero row, closure under rotation by 2pi/m, no three
points collinear (all C(n,3) orientations nonzero), and the largest subset in convex position by two independently
anchored O(n^4) dynamic programs (anchor = lowest point in (y, x) order; anchor = leftmost point in (x, y) order).
usage: verify_indep.py M FILE.pts [K]   (K = 8: report whether there are K points in convex position)
"""
import sys, itertools, hashlib
from functools import cmp_to_key

m = int(sys.argv[1]); fn = sys.argv[2]; K = int(sys.argv[3]) if len(sys.argv) > 3 else 8
raw = open(fn, 'rb').read()
print('file', fn, 'sha256', hashlib.sha256(raw).hexdigest())
rows = []
for line in raw.decode().splitlines():
    line = line.split('#')[0].strip()
    if not line:
        continue
    w = list(map(int, line.split())); assert len(w) == m
    rows.append(w)
n = len(rows); print('m', m, 'points', n)


def sgn_q5(A, B):
    """sign of A + B*sqrt5 (integers)"""
    if A >= 0 and B >= 0:
        return 0 if A == 0 and B == 0 else 1
    if A <= 0 and B <= 0:
        return -1
    # opposite signs: compare A^2 with 5 B^2
    d = A * A - 5 * B * B
    if A > 0:
        return 1 if d > 0 else (-1 if d < 0 else 0)
    return -1 if d > 0 else (1 if d < 0 else 0)


if m in (3, 4):
    if m == 4:
        P = [(w[0] - w[2], w[1] - w[3]) for w in rows]
        rot = lambda p: (-p[1], p[0])
    else:
        P = [(w[0] - w[2], w[1] - w[2]) for w in rows]
        rot = lambda p: (-p[1], p[0] - p[1])
    keyval = P

    def orient(i, j, k):
        o, p, q = P[i], P[j], P[k]
        v = (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
        return (v > 0) - (v < 0)

    def ylex(i):
        return (P[i][1], P[i][0])

    def xlex(i):
        return (P[i][0], P[i][1])
    pts_key = P
elif m == 5:
    V = [tuple(c - w[4] for c in w[:4]) + (0,) for w in rows]   # reduced representation
    P = V
    def red(c):
        return tuple(x - c[4] for x in c[:4]) + (0,)

    def rot(c):   # multiply by zeta: coefficient of zeta^j <- c_{j-1}; reduce
        return red(tuple(c[(j - 1) % 5] for j in range(5)))

    def mul(a, b):
        r = [0] * 5
        for i in range(5):
            if a[i] == 0:
                continue
            for j in range(5):
                r[(i + j) % 5] += a[i] * b[j]
        return r

    def conj(a):
        return tuple(a[(-j) % 5] for j in range(5))

    def im_sign(c):
        # 2 * [(c1 - c4) + (c2 - c3)(sqrt5 - 1)/2] = 2(c1 - c4) - (c2 - c3) + (c2 - c3) sqrt5
        X = c[1] - c[4]; Y = c[2] - c[3]
        return sgn_q5(2 * X - Y, Y)

    def re_val(c):
        # 4 Re z = 4 c0 + (c1 + c4)(sqrt5 - 1) - (c2 + c3)(sqrt5 + 1) = A + B sqrt5
        return (4 * c[0] - (c[1] + c[4]) - (c[2] + c[3]), (c[1] + c[4]) - (c[2] + c[3]))

    def im_val(c):
        X = c[1] - c[4]; Y = c[2] - c[3]
        return (2 * X - Y, Y)      # proportional (factor sin(2pi/5)/2 > 0)

    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    OT = {}

    def orient(i, j, k):
        a, b, c = P[i], P[j], P[k]
        return im_sign(mul(conj(sub(b, a)), sub(c, a)))

    def cmpq5(u, v):
        return sgn_q5(u[0] - v[0], u[1] - v[1])

    def ylex(i):
        return i

    def xlex(i):
        return i
else:
    raise SystemExit('m must be 3, 4 or 5')

# (1) distinct, centre, rotation closure
S = set(map(tuple, P))
assert len(S) == n, 'duplicate points'
zero = tuple([0] * len(P[0]))
ncentre = sum(1 for p in P if tuple(p) == zero)
print('centre present:', ncentre == 1)
assert all(tuple(rot(tuple(p))) in S for p in P), 'not closed under rotation by 2pi/m'
print('distinct, rotation-closed: OK')

# (2) general position; orientation table
O = {}
zc = 0
for i, j, k in itertools.combinations(range(n), 3):
    s = orient(i, j, k)
    if s == 0:
        zc += 1
    O[(i, j, k)] = s; O[(j, k, i)] = s; O[(k, i, j)] = s
    O[(j, i, k)] = -s; O[(i, k, j)] = -s; O[(k, j, i)] = -s
print('collinear triples', zc); assert zc == 0


def cr(i, j, k):
    return O[(i, j, k)]


# exact total orders for the anchors
if m == 5:
    def less_y(i, j):   # (y, x) lexicographic
        a = cmpq5(im_val(P[i]), im_val(P[j]))
        if a:
            return a < 0
        return cmpq5(re_val(P[i]), re_val(P[j])) < 0

    def less_x(i, j):
        a = cmpq5(re_val(P[i]), re_val(P[j]))
        if a:
            return a < 0
        return cmpq5(im_val(P[i]), im_val(P[j])) < 0
else:
    def less_y(i, j):
        return (P[i][1], P[i][0]) < (P[j][1], P[j][0])

    def less_x(i, j):
        return (P[i][0], P[i][1]) < (P[j][0], P[j][1])


def largest(less):
    best = 0
    for p in range(n):
        Q = [q for q in range(n) if q != p and less(p, q)]
        Q.sort(key=cmp_to_key(lambda u, v: -1 if cr(p, u, v) > 0 else 1))
        mq = len(Q); L = {}
        for j in range(mq):
            for i in range(j):
                v = 3
                for h in range(i):
                    if (h, i) in L and cr(Q[h], Q[i], Q[j]) > 0 and L[(h, i)] + 1 > v:
                        v = L[(h, i)] + 1
                L[(i, j)] = v
                if cr(Q[i], Q[j], p) > 0 and v > best:
                    best = v
    return best


k1 = largest(less_y); print('largest convex subset (anchor lowest):', k1)
k2 = largest(less_x); print('largest convex subset (anchor leftmost):', k2)
print('RESULT', 'NO %d POINTS IN CONVEX POSITION' % K if max(k1, k2) < K else 'CONTAINS %d POINTS IN CONVEX POSITION' % K,
      'max', max(k1, k2))
