#!/usr/bin/env python3
"""
Independent exact verifier for 8-fold point sets given as rows of 8 integers w_0..w_7,
point = sum_j w_j zeta^j with zeta = exp(2 pi i / 8).  Written from scratch (does not
import or read the producer's verify code).

Two structurally different exact orientation methods:
  M1: explicit coordinates 2x, 2y in Z[sqrt2]; orientation = sign of the 2x2 cross product,
      computed as A + B sqrt2 with integers A, B; sign decided exactly.
  M2: no coordinates: work in Z[zeta] = Z[t]/(t^4+1); orient(p,q,r) = sign Im( conj(q-p) (r-p) ),
      with Im(c0 + c1 z + c2 z^2 + c3 z^3) = c2 + (c1 + c3)/sqrt2, so
      sign Im = sign( (c1+c3) + c2 sqrt2 ).
Both must agree on every triple, and no triple may be zero.

Usage: exact_geom.py PTS OUTDIR TAG
Writes OUTDIR/TAG.myotab ("n\n" + n^3 signed bytes, a-major, then b, then c; 0 on repeated index),
       OUTDIR/TAG.orders  (line 1: indices sorted by exact (y,x)-lex; line 2: by exact (x,y)-lex),
       prints a JSON-ish summary.
"""
import sys, itertools, json, hashlib, math

def sign_ab(A, B):
    """exact sign of A + B*sqrt(2), A, B integers"""
    if A >= 0 and B >= 0:
        return 0 if (A == 0 and B == 0) else 1
    if A <= 0 and B <= 0:
        return -1
    # opposite strict signs
    a2 = A * A
    b2 = 2 * B * B
    if A > 0:           # A > 0 > B : sign(A^2 - 2B^2)
        return 1 if a2 > b2 else -1   # a2 == b2 impossible (sqrt2 irrational) unless both 0
    else:               # A < 0 < B : sign(2B^2 - A^2)
        return 1 if b2 > a2 else -1

def mul_ab(x, y):
    a, b = x; c, d = y
    return (a * c + 2 * b * d, a * d + b * c)

def sub_ab(x, y):
    return (x[0] - y[0], x[1] - y[1])

def read_pts(path):
    rows = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            w = [int(t) for t in s.split()]
            if len(w) != 8:
                raise SystemExit("bad row length %d: %r" % (len(w), s))
            rows.append(tuple(w))
    return rows

def coords(w):
    """(2x, 2y) as Z[sqrt2] pairs (A, B) meaning A + B sqrt2"""
    w0, w1, w2, w3, w4, w5, w6, w7 = w
    X = (2 * (w0 - w4), w1 - w3 - w5 + w7)
    Y = (2 * (w2 - w6), w1 + w3 - w5 - w7)
    return X, Y

def red4(w):
    """reduce to Z[t]/(t^4+1): c_j = w_j - w_{j+4}"""
    return tuple(w[j] - w[j + 4] for j in range(4))

def nmul4(s, t):
    """negacyclic product in Z[t]/(t^4+1)"""
    out = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            k = i + j
            if k < 4:
                out[k] += s[i] * t[j]
            else:
                out[k - 4] -= s[i] * t[j]
    return tuple(out)

def conj4(c):
    return (c[0], -c[3], -c[2], -c[1])

def orient_M1(P, i, j, k):
    (Xi, Yi), (Xj, Yj), (Xk, Yk) = P[i], P[j], P[k]
    ux, uy = sub_ab(Xj, Xi), sub_ab(Yj, Yi)
    vx, vy = sub_ab(Xk, Xi), sub_ab(Yk, Yi)
    A1 = mul_ab(ux, vy); A2 = mul_ab(uy, vx)
    d = sub_ab(A1, A2)
    return sign_ab(d[0], d[1]), d

def orient_M2(Q, i, j, k):
    u = tuple(Q[j][t] - Q[i][t] for t in range(4))
    v = tuple(Q[k][t] - Q[i][t] for t in range(4))
    z = nmul4(conj4(u), v)
    return sign_ab(z[1] + z[3], z[2])

def rot_zeta_coeffs(w):
    """multiply by zeta in the group ring: cyclic shift (zeta^8 = 1)"""
    return (w[7],) + tuple(w[:7])

def rot_zeta_exact(X, Y):
    """rotate (2x, 2y) by 45 degrees exactly: x' = (x - y)/sqrt2, y' = (x + y)/sqrt2.
    (a + b sqrt2)/sqrt2 = b + (a/2) sqrt2 ; need a even for integrality."""
    def div_s2(z):
        a, b = z
        if a % 2:
            raise ValueError("odd")
        return (b, a // 2)
    Xn = div_s2(sub_ab(X, Y))
    Yn = div_s2((X[0] + Y[0], X[1] + Y[1]))
    return Xn, Yn

def cmp_ab(x, y):
    d = sub_ab(x, y)
    return sign_ab(d[0], d[1])

def main():
    pts_path, outdir, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    m = 8
    raw = open(pts_path, 'rb').read()
    rows = read_pts(pts_path)
    n = len(rows)
    rep = {'file': pts_path, 'sha256': hashlib.sha256(raw).hexdigest(), 'n': n}
    if n % m:
        raise SystemExit("n not a multiple of 8")
    t = n // m
    rep['layers'] = t
    P = [coords(w) for w in rows]
    Q = [red4(w) for w in rows]

    # 1. orbit structure: row o*8+k = zeta^k row o*8 (both as coefficient shift and as exact point)
    orbit_ok_coeff = True
    orbit_ok_exact = True
    for o in range(t):
        base = rows[o * m]
        w = base
        Xc, Yc = P[o * m]
        for k in range(m):
            if rows[o * m + k] != w:
                orbit_ok_coeff = False
            if P[o * m + k] != (Xc, Yc):
                orbit_ok_exact = False
            w = rot_zeta_coeffs(w)
            Xc, Yc = rot_zeta_exact(Xc, Yc)
        # after 8 rotations we must be back
        if (Xc, Yc) != P[o * m]:
            orbit_ok_exact = False
    rep['orbit_structure_coeff_shift'] = orbit_ok_coeff
    rep['orbit_structure_exact_rotation'] = orbit_ok_exact

    # 2. invariance of the SET under rotation by zeta (exact points)
    S = set(P)
    rep['distinct'] = (len(S) == n)
    rot = set(rot_zeta_exact(X, Y) for (X, Y) in P)
    rep['set_invariant_under_zeta'] = (rot == S)
    rep['contains_origin'] = (((0, 0), (0, 0)) in S)

    # 3. orientation of all C(n,3) triples, two methods
    zeros = 0; mism = 0
    tab = bytearray(n * n * n)
    mindet = None
    for i, j, k in itertools.combinations(range(n), 3):
        s1, d = orient_M1(P, i, j, k)
        s2 = orient_M2(Q, i, j, k)
        if s1 == 0 or s2 == 0:
            zeros += 1
        if s1 != s2:
            mism += 1
        # float magnitude of 4*det (for reporting only)
        val = abs(d[0] + d[1] * math.sqrt(2.0)) / 4.0
        if mindet is None or val < mindet:
            mindet = val
        sb = s1 & 0xFF
        nb = (-s1) & 0xFF
        tab[(i * n + j) * n + k] = sb
        tab[(j * n + k) * n + i] = sb
        tab[(k * n + i) * n + j] = sb
        tab[(i * n + k) * n + j] = nb
        tab[(k * n + j) * n + i] = nb
        tab[(j * n + i) * n + k] = nb
    rep['triples'] = n * (n - 1) * (n - 2) // 6
    rep['zero_orientations'] = zeros
    rep['M1_M2_mismatches'] = mism
    rep['min_abs_det_float_approx'] = mindet

    # 4. radii^2 exactly: |p|^2 = x^2 + y^2 ; 4|p|^2 = X^2 + Y^2 in Z[sqrt2]
    r2 = []
    for o in range(t):
        X, Y = P[o * m]
        a = mul_ab(X, X); b = mul_ab(Y, Y)
        r2.append((a[0] + b[0], a[1] + b[1]))
    dec = all(cmp_ab(r2[o], r2[o + 1]) > 0 for o in range(t - 1))
    rep['radii_strictly_decreasing'] = dec
    # equal radius within each orbit
    same = True
    for o in range(t):
        for k in range(m):
            X, Y = P[o * m + k]
            a = mul_ab(X, X); b = mul_ab(Y, Y)
            if (a[0] + b[0], a[1] + b[1]) != r2[o]:
                same = False
    rep['orbit_points_equal_radius'] = same
    rep['radius_float'] = [math.sqrt(max(0.0, (z[0] + z[1] * math.sqrt(2.0)))) / 2.0 for z in r2]

    # 5. nesting: every point of layers o' > o strictly inside conv(layer o) (CCW octagon order k=0..7)
    def O(i, j, k):
        v = tab[(i * n + j) * n + k]
        return v - 256 if v > 127 else v
    nested = True
    octagon_ccw = True
    for o in range(t):
        L = [o * m + k for k in range(m)]
        # CCW check: all consecutive triples left turns
        for k in range(m):
            if O(L[k], L[(k + 1) % m], L[(k + 2) % m]) != 1:
                octagon_ccw = False
        for q in range((o + 1) * m, n):
            for k in range(m):
                if O(L[k], L[(k + 1) % m], q) != 1:
                    nested = False
    rep['each_layer_strictly_convex_ccw'] = octagon_ccw
    rep['later_layers_strictly_inside'] = nested
    # also: earlier layers strictly outside later octagons? (each point of earlier layer is outside conv(later))
    outside = True
    for o in range(t):
        L = [o * m + k for k in range(m)]
        for q in range(0, o * m):
            if all(O(L[k], L[(k + 1) % m], q) == 1 for k in range(m)):
                outside = False
    rep['earlier_points_not_inside_later_hulls'] = outside

    # 6. exact lexicographic orders
    import functools
    def cmp_yx(i, j):
        c = cmp_ab(P[i][1], P[j][1])
        if c:
            return c
        return cmp_ab(P[i][0], P[j][0])
    def cmp_xy(i, j):
        c = cmp_ab(P[i][0], P[j][0])
        if c:
            return c
        return cmp_ab(P[i][1], P[j][1])
    oy = sorted(range(n), key=functools.cmp_to_key(cmp_yx))
    ox = sorted(range(n), key=functools.cmp_to_key(cmp_xy))
    # ties
    rep['ties_in_y'] = sum(1 for a, b in zip(oy, oy[1:]) if cmp_ab(P[a][1], P[b][1]) == 0)
    rep['ties_in_x'] = sum(1 for a, b in zip(ox, ox[1:]) if cmp_ab(P[a][0], P[b][0]) == 0)

    with open('%s/%s.myotab' % (outdir, tag), 'wb') as f:
        f.write(('%d\n' % n).encode())
        f.write(bytes(tab))
    with open('%s/%s.orders' % (outdir, tag), 'w') as f:
        f.write(' '.join(map(str, oy)) + '\n')
        f.write(' '.join(map(str, ox)) + '\n')
    h = hashlib.sha256()
    h.update(('%d\n' % n).encode()); h.update(bytes(tab))
    rep['myotab_sha256'] = h.hexdigest()
    rep['max_abs_coeff'] = max(abs(x) for w in rows for x in w)
    print(json.dumps(rep, indent=1))

if __name__ == '__main__':
    main()
