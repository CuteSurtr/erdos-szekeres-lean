#!/usr/bin/env python3
"""High-precision (Decimal, 150 digits) version of validate2 'pts' mode for sets in Z[zeta_m] (odd m).
usage: validate_hp.py CNF FILE.pts"""
import sys, json
from decimal import Decimal as D, getcontext
getcontext().prec = 150
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gen
from validate2 import stream_check


def pi_dec():
    # Machin
    def arctan_inv(x):
        x = D(x); s = D(0); term = 1 / x; n = 1; sign = 1; x2 = x * x
        while True:
            t = term / n
            if t < D(10) ** (-160):
                break
            s += sign * t
            term /= x2; n += 2; sign = -sign
        return s
    return 4 * (4 * arctan_inv(5) - arctan_inv(239))


def cos_sin(a):
    c = D(0); s = D(0); term = D(1); n = 0
    while True:
        if abs(term) < D(10) ** (-160) and n > 2:
            break
        if n % 4 == 0: c += term
        elif n % 4 == 1: s += term
        elif n % 4 == 2: c -= term
        else: s -= term
        n += 1
        term = term * a / n
    return c, s


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conj(a):
    return (a[0], -a[1])


if __name__ == '__main__':
    cnf, fn = sys.argv[1], sys.argv[2]
    meta = json.load(open(cnf + '.json'))
    m, K, t = meta['m'], meta['K'], meta['t']
    assert m % 2 == 1
    PI = pi_dec()
    zeta = [cos_sin(2 * PI * j / m) for j in range(m)]
    half = cos_sin(PI / m)                       # e^{i pi/m}
    halfpow = [cos_sin(PI * j / m) for j in range(2 * m)]
    rows = []
    for line in open(fn):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        w = list(map(int, line.split()))
        x = sum(D(w[j]) * zeta[j][0] for j in range(m))
        y = sum(D(w[j]) * zeta[j][1] for j in range(m))
        if x * x + y * y > D(10) ** (-50):
            rows.append((x, y))
    rows.sort(key=lambda p: -(p[0] * p[0] + p[1] * p[1]))
    layers = [rows[s:s + m] for s in range(0, len(rows), m)][:t]
    # normalise: rotate so that a vertex of layer 0 is at angle 0
    v0 = layers[0][0]
    r0 = (v0[0] * v0[0] + v0[1] * v0[1]).sqrt()
    rot = (v0[0] / r0, -v0[1] / r0)
    E = gen.Enc(m, K, t)
    pts = [None] * (m * t)
    psi = []; Hb = []
    for i, L in enumerate(layers):
        for v in L:
            w = mul(v, rot)
            if i == 0:          # layer 0 sits on the sector boundaries: nearest direction
                k = max(range(m), key=lambda k: zeta[k][0] * w[0] + zeta[k][1] * w[1])
                pts[k] = (r0 * zeta[k][0], r0 * zeta[k][1])
                continue
            # sector k: angle in [2 pi k/m, 2 pi (k+1)/m)
            for k in range(m):
                a, b = zeta[k], zeta[(k + 1) % m]
                if cross(a, w) >= 0 and cross(w, b) > 0:
                    pts[i * m + k] = w
                    break
            else:
                raise RuntimeError('no sector')
        w = pts[i * m]           # vertex in sector 0: angle theta_i in [0, 2pi/m)
        if cross(w, half) > 0 or i == 0:
            Hb.append(True); psi.append(w)
        else:
            Hb.append(False); psi.append(mul(w, conj(half)))
    assert all(p is not None for p in pts)
    assign = {}
    mind = None
    for C, v in E.tvar.items():
        a, b, c = (pts[x] for x in C)
        d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        mind = abs(d) if mind is None else min(mind, abs(d))
        assign[v] = d > 0
    for (i, j), v in E.Y.items():
        assign[v] = cross(psi[i], psi[j]) > 0          # psi_i < psi_j (both in [0, pi/m))
    for i, v in E.H.items():
        assign[v] = Hb[i]
    print(fn.rsplit('/', 1)[-1], 'min|det| %.3e' % float(mind), stream_check(cnf, meta, assign, E.nv))
