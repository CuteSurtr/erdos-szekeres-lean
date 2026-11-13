#!/usr/bin/env python3
"""Exact certificate builder/checker for m-fold symmetric nested-polygon configurations.

usage: verify_cfg.py CONFIG m C K SCALE OUTPREFIX          (CONFIG: lines "lr th", '#' comments ignored)
   or: verify_cfg.py --pts PTSFILE m C K OUTPREFIX        (re-check an existing exact point file)

Representative of each layer: nearest point of the lattice Z + Z zeta to SCALE * e^lr * e^{i th}; the layer is its
orbit {zeta^k w}.  Output:
  OUTPREFIX.pts     one point per line: integer coefficients w_0..w_{m-1} of sum_j w_j zeta^j (zeta = e^{2 pi i/m})
  OUTPREFIX.otab    binary orientation table: first line "n\\n", then n^3 signed bytes orient(a,b,c) (a major)
  OUTPREFIX.lex     n integers: rank of each point in the exact (Im, Re) lexicographic order (for cvx2.c's DP2)
Exact checks (method A, zm.ZM): distinct points (canonical forms mod Phi_m); the set is invariant under
multiplication by zeta; no zero orientation; layer structure: for every layer o, its orbit (in CCW order k = 0..m-1)
is a convex polygon and every point of every later layer lies strictly inside it.
Independent cross-check (method B, zm.IntervalGeom): every orientation sign recomputed with rigorous fixed-point
interval arithmetic (2^-300) must be decided and agree with method A; the (Im, Re) order is cross-checked likewise
where intervals separate (all comparisons must be decided).  For m = 8 a third exact method (Z[sqrt2] coordinates)
is applied to every triple as well.
"""
import sys, os, math, hashlib, struct
from functools import cmp_to_key
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zm import ZM, IntervalGeom, _sign_qirr


def z8_sqrt2_orient(p, q, r):
    """m = 8 only: exact orientation from coordinates in Z[sqrt2] (independent formula).
    sqrt2*Re(w) = (w1 - w3 - w5 + w7) + (w0 - w4) sqrt2 ; sqrt2*Im(w) = (w1 + w3 - w5 - w7) + (w2 - w6) sqrt2"""
    def X(w):
        return (w[1] - w[3] - w[5] + w[7], w[0] - w[4])
    def Y(w):
        return (w[1] + w[3] - w[5] - w[7], w[2] - w[6])
    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1])
    def mul(a, b):
        return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])
    qx, qy = sub(X(q), X(p)), sub(Y(q), Y(p))
    rx, ry = sub(X(r), X(p)), sub(Y(r), Y(p))
    d = sub(mul(qx, ry), mul(qy, rx))
    return _sign_qirr(d[0], d[1], 2)


def main():
    args = sys.argv[1:]
    if args[0] == '--pts':
        ptsfile, m, C, K, out = args[1], int(args[2]), int(args[3]), int(args[4]), args[5]
        P = []
        for l in open(ptsfile):
            if l.startswith('#') or not l.strip():
                continue
            P.append([int(v) for v in l.split()])
        Z = ZM(m)
        t = (len(P) - C) // m
        layer = [i // m for i in range(t * m)] + ([t] if C else [])
        scale = None
    else:
        cfg, m, C, K, scale, out = args[0], int(args[1]), int(args[2]), int(args[3]), float(args[4]), args[5]
        L = []
        for l in open(cfg):
            if l.startswith('#') or not l.strip():
                continue
            a, b = map(float, l.split()[:2])
            L.append((a, b))
        L.sort(key=lambda x: -x[0])        # outermost first
        Z = ZM(m)
        reps = [Z.from_complex_Zzeta(scale * math.exp(a) * complex(math.cos(b), math.sin(b))) for a, b in L]
        P, layer = [], []
        for o, w in enumerate(reps):
            for k in range(m):
                P.append(Z.rot(w, k))
                layer.append(o)
        if C:
            P.append([0] * m)
            layer.append(len(reps))
        t = len(reps)
    n = len(P)
    assert len(P[0]) == m
    if C:
        assert all(v == 0 for v in P[-1])
    # orbit structure of the point list: point o*m + k = zeta^k * point o*m
    orbit_ok = all(Z.canon(P[o * m + k]) == Z.canon(Z.rot(P[o * m], k)) for o in range(t) for k in range(m))
    canon = [Z.canon(p) for p in P]
    distinct = len(set(canon)) == n
    cs = set(canon)
    invariant = all(Z.canon(Z.rot(p)) in cs for p in P)
    G = IntervalGeom(m)
    XY = [G.xy(p) for p in P]
    # orientation table (sorted triples), method A + method B (+ method C for m = 8)
    T = {}
    zero = 0
    mismatch_B = 0
    undecided_B = 0
    mismatch_C = 0
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                s = Z.orient(P[a], P[b], P[c])
                if s == 0:
                    zero += 1
                sB, _ = IntervalGeom.orient_xy(XY[a], XY[b], XY[c])
                if sB is None:
                    undecided_B += 1
                elif sB != s:
                    mismatch_B += 1
                if m == 8 and z8_sqrt2_orient(P[a], P[b], P[c]) != s:
                    mismatch_C += 1
                T[(a, b, c)] = s

    def orient(a, b, c):
        if a == b or b == c or a == c:
            return 0
        if a < b < c:
            return T[(a, b, c)]
        x = sorted((a, b, c))
        s = T[tuple(x)]
        perm = [x.index(a), x.index(b), x.index(c)]
        inv = (perm[0] > perm[1]) + (perm[0] > perm[2]) + (perm[1] > perm[2])
        return s if inv % 2 == 0 else -s
    # layers
    layers_ok = True
    for o in range(t):
        idx = [o * m + k for k in range(m)]
        for k in range(m):
            e0, e1 = idx[k], idx[(k + 1) % m]
            for k2 in range(m):
                if k2 != k and k2 != (k + 1) % m and orient(e0, e1, idx[k2]) <= 0:
                    layers_ok = False
            for q in range(n):
                if layer[q] > o and orient(e0, e1, q) <= 0:
                    layers_ok = False
    # radii strictly decreasing along the layer list (exact)
    radii_ok = all(Z.r2cmp(P[o * m], P[(o + 1) * m]) > 0 for o in range(t - 1))
    # exact (Im, Re) order, cross-checked by intervals
    lexB_bad = 0

    def key_cmp(i, j):
        nonlocal lexB_bad
        s = Z.lexcmp(P[i], P[j])
        # interval cross-check: Im difference, then Re difference
        dy = XY[i][1] - XY[j][1]
        sy = dy.sign()
        if sy is None:
            # Im equal or undecided: require exact Im equal and decide Re by intervals
            if Z.sign_im(Z.sub(P[i], P[j])) != 0:
                lexB_bad += 1
            dx = XY[i][0] - XY[j][0]
            sx = dx.sign()
            if sx is None or sx != s:
                lexB_bad += 1
        elif sy != s:
            lexB_bad += 1
        return s
    order = sorted(range(n), key=cmp_to_key(key_cmp))
    rank = [0] * n
    for r, i in enumerate(order):
        rank[i] = r
    # write files
    with open(out + '.pts', 'w') as f:
        f.write('# m=%d C=%d n=%d layers=%d scale=%s ; point = sum_j w_j zeta^j, zeta = e^(2 pi i/%d); layer o = rows o*m..o*m+m-1 (outermost first)\n' % (m, C, n, t, scale, m))
        for p in P:
            f.write(' '.join(map(str, p)) + '\n')
    with open(out + '.otab', 'wb') as f:
        f.write(b'%d\n' % n)
        buf = bytearray(n * n * n)
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    buf[(a * n + b) * n + c] = orient(a, b, c) & 0xff
        f.write(bytes(buf))
    with open(out + '.lex', 'w') as f:
        f.write(' '.join(map(str, rank)) + '\n')
    maxc = max(max(abs(x) for x in p) for p in P)
    res = dict(m=m, C=C, n=n, layers=t, orbit_structure=orbit_ok, distinct=distinct, invariant=invariant,
               zero_orientations=zero, intervalB_mismatch=mismatch_B, intervalB_undecided=undecided_B,
               lexorder_intervalB_bad=lexB_bad, layers_are_nested_convex_orbits=layers_ok, radii_decreasing=radii_ok,
               max_abs_coeff=maxc)
    if m == 8:
        res['z8_sqrt2_mismatch'] = mismatch_C
    print(res)
    ok = orbit_ok and distinct and invariant and zero == 0 and mismatch_B == 0 and undecided_B == 0 and layers_ok \
        and radii_ok and lexB_bad == 0 and (m != 8 or mismatch_C == 0)
    for ext in ('.pts', '.otab', '.lex'):
        print('sha256 %s%s %s' % (os.path.basename(out), ext, hashlib.sha256(open(out + ext, 'rb').read()).hexdigest()))
    print('EXACT-PREP PASS' if ok else 'EXACT-PREP FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
