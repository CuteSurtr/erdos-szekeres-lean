#!/usr/bin/env python3
"""Exact labelling of an 8-fold set (rows = Z[zeta_8] coefficients, zeta = e^{2 pi i/8}) in the convention of
C7UPPER/gen.py Enc(8, K, t): layers by strictly decreasing radius, theta_0 = 0 at a chosen vertex p0 of layer 0,
vertex (i,k) = the vertex of layer i whose angle relative to p0 lies in [2 pi k/8, 2 pi (k+1)/8), and
Y(i,j) = [psi_i < psi_j].  All arithmetic is exact in Z[sqrt2] (pairs (a, b) = a + b sqrt2): coordinates are scaled
by 2, X = 2(w0 - w4) + sqrt2 (w1 - w3 - w5 + w7), Y = 2(w2 - w6) + sqrt2 (w1 + w3 - w5 - w7).

usage: label8.py SET.pts OUT.json [--p0 s]    (s = which vertex of the outer layer is (0,0); default 0)
OUT.json: {"t", "val": {var: bool} for triple-orbit vars and Y vars, "pts": exact coords of point id i*8+k}
"""
import sys, json, itertools, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))


def zsign(a, b):
    """sign of a + b sqrt2 (integers)"""
    if a >= 0 and b >= 0:
        return 0 if (a == 0 and b == 0) else 1
    if a <= 0 and b <= 0:
        return -1
    # opposite signs
    if a > 0:            # b < 0: a + b sqrt2 > 0 iff a^2 > 2 b^2
        d = a * a - 2 * b * b
    else:                # a < 0, b > 0: > 0 iff 2 b^2 > a^2
        d = 2 * b * b - a * a
    return (d > 0) - (d < 0)


def zmul(x, y):
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def zsub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def zadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def coords(w):
    w = list(w) + [0] * (8 - len(w))
    X = (2 * (w[0] - w[4]), w[1] - w[3] - w[5] + w[7])
    Y = (2 * (w[2] - w[6]), w[1] + w[3] - w[5] - w[7])
    return (X, Y)


def det(p, q):
    return zsub(zmul(p[0], q[1]), zmul(p[1], q[0]))


def orient(p, q, r):
    return zsign(*det((zsub(q[0], p[0]), zsub(q[1], p[1])), (zsub(r[0], p[0]), zsub(r[1], p[1]))))


def rot45(p):
    """sqrt2 * (zeta p): coordinates (X - Y, X + Y); same direction as zeta p"""
    return (zsub(p[0], p[1]), zadd(p[0], p[1]))


def read_pts(fn):
    rows = []
    for line in open(fn):
        line = line.split('#')[0].split()
        if line:
            rows.append(tuple(int(x) for x in line))
    return rows


def label(rows, p0sel=0):
    n = len(rows)
    assert n % 8 == 0
    P = [coords(w) for w in rows]
    # orbits: rows 8o..8o+7 must be zeta^k * row 8o (checked exactly on coefficients)
    def mulzeta(w):
        w = list(w) + [0] * (8 - len(w))
        return tuple([w[7]] + w[:7])          # zeta^8 = 1: cyclic shift
    layers = []
    for o in range(n // 8):
        seed = rows[8 * o]
        cur = tuple(list(seed) + [0] * (8 - len(seed)))
        for k in range(8):
            r = tuple(list(rows[8 * o + k]) + [0] * (8 - len(rows[8 * o + k])))
            assert r == cur, ('row is not zeta^k * seed', o, k)
            cur = mulzeta(cur)
        layers.append([8 * o + k for k in range(8)])
    # distinct points
    assert len(set(P)) == n
    # radii (squared, times 4) exactly; sort decreasing
    r2 = [zadd(zmul(P[L[0]][0], P[L[0]][0]), zmul(P[L[0]][1], P[L[0]][1])) for L in layers]
    import functools
    def cmp(a, b):
        return zsign(*zsub(r2[b], r2[a]))
    order = sorted(range(len(layers)), key=functools.cmp_to_key(cmp))
    for a, b in zip(order, order[1:]):
        assert zsign(*zsub(r2[a], r2[b])) > 0, 'equal radii'
    t = len(layers)
    p0 = P[layers[order[0]][p0sel]]
    zp0 = rot45(p0)
    ids = {}
    reps = []
    for i, o in enumerate(order):
        if i == 0:
            s = p0sel
        else:
            cand = []
            for s_ in range(8):
                v = P[layers[o][s_]]
                d1 = zsign(*det(p0, v)); d2 = zsign(*det(v, zp0))
                assert d1 != 0 and d2 != 0, 'phase on a sector boundary (non-generic labelling)'
                if d1 > 0 and d2 > 0:
                    cand.append(s_)
            assert len(cand) == 1, cand
            s = cand[0]
        for k in range(8):
            ids[i * 8 + k] = layers[o][(s + k) % 8]
        reps.append(P[layers[o][s]])
    return t, P, ids, reps


def assignment(t, P, ids, reps, m=8, K=9):
    s = importlib.util.spec_from_file_location('gen', os.path.join(HERE, 'gen.py'))
    G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
    E = G.Enc(m, K, t)
    val = {}
    for C, v in E.tvar.items():
        o = orient(P[ids[C[0]]], P[ids[C[1]]], P[ids[C[2]]])
        assert o != 0, ('collinear', C)
        val[v] = (o > 0)
    for (i, j), v in E.Y.items():
        d = zsign(*det(reps[i], reps[j]))
        assert d != 0
        val[v] = (d > 0)
    return E, val


if __name__ == '__main__':
    fn, out = sys.argv[1], sys.argv[2]
    p0sel = int(sys.argv[sys.argv.index('--p0') + 1]) if '--p0' in sys.argv else 0
    rows = read_pts(fn)
    t, P, ids, reps = label(rows, p0sel)
    E, val = assignment(t, P, ids, reps)
    # phase order of layers
    ph = sorted(range(1, t), key=lambda i: sum(1 for j in range(1, t) if j != i and
                                                 ((val[E.Y[(j, i)]] if j < i else not val[E.Y[(i, j)]]))))
    json.dump({'t': t, 'n': len(rows), 'val': {str(k): v for k, v in val.items()},
               'phase_order': ph}, open(out, 'w'))
    print('t=%d n=%d triple vars %d Y vars %d; phase order (psi increasing): %s' % (
        t, len(rows), E.ntriplevars, len(E.Y), ph))
