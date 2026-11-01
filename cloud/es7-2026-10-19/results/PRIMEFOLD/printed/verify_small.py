#!/usr/bin/env python3
"""Independent re-verification (written from scratch) of the two small certified sets of the
"Small-cases" claim of the search for k = 5..9.

Usage: python3 -I verify_small.py PTSFILE m K [OTABFILE]

Point j of PTSFILE is sum_i w_i zeta^i, zeta = exp(2 pi i / m), m in {4, 5}.

Orientation sign orient(a,b,c) = sign((b-a) x (c-a)) is computed
  m = 4 : exactly with Gaussian integers (x = w0 - w2, y = w1 - w3);
  m = 5 : method A  exact, in Z[zeta5] via Im(conj(b-a)(c-a)) and the identity
                    Im(sum c_j zeta^j) = (sin 36deg / 2) * (p + q sqrt5), p = (c1-c4) + 2(c2-c3), q = c1-c4;
          method B  exact, explicit coordinates x in Q(sqrt5), y = sin72 * Y with Y in Q(sqrt5);
          method C  rigorous rational interval arithmetic on x, y using integer-sqrt bounds for sqrt5,
                    sqrt(10+2 sqrt5), sqrt(10-2 sqrt5) (does NOT use the sin72 factorisation);
  all methods must agree, and no orientation may be 0.

Convex position of a subset (general position assumed and checked): two independent tests,
  T1: no point of the subset lies strictly inside a triangle spanned by three other points of it;
  T2: the number of ordered pairs (p,q) with all other subset points strictly left of p->q equals |subset|.
Every k-subset, k = 3..K, is enumerated by brute force; T1 and T2 must agree on every subset.
"""
import sys, itertools, math
from fractions import Fraction as Fr


def read_pts(path):
    rows, header = [], None
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if s.startswith('#'):
                header = s
                continue
            rows.append(tuple(int(v) for v in s.split()))
    return header, rows


# ---------------------------------------------------------------- exact signs in Q(sqrt5)
def sign_q5(p, q):
    """sign of p + q*sqrt5 for rationals p, q (exact)."""
    sp = (p > 0) - (p < 0)
    sq = (q > 0) - (q < 0)
    if sq == 0:
        return sp
    if sp == 0:
        return sq
    if sp == sq:
        return sp
    # opposite signs: compare p^2 with 5 q^2 (equality impossible: sqrt5 irrational)
    d = p * p - 5 * q * q
    assert d != 0
    return sp if d > 0 else sq


# ---------------------------------------------------------------- m = 4
def canon4(w):
    return (w[0] - w[2], w[1] - w[3])


def orient4(P, a, b, c):
    ax, ay = P[a]; bx, by = P[b]; cx, cy = P[c]
    d = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    return (d > 0) - (d < 0)


# ---------------------------------------------------------------- m = 5
def canon5(w):
    return tuple(w[i] - w[4] for i in range(4))


def cyc_sub(u, v):
    return tuple(a - b for a, b in zip(u, v))


def cyc_conj(u):
    return tuple(u[(-j) % 5] for j in range(5))


def cyc_mul(u, v):
    r = [0] * 5
    for i in range(5):
        for j in range(5):
            r[(i + j) % 5] += u[i] * v[j]
    return tuple(r)


def orient5_A(W, a, b, c):
    z = cyc_mul(cyc_conj(cyc_sub(W[b], W[a])), cyc_sub(W[c], W[a]))
    q = z[1] - z[4]
    p = (z[1] - z[4]) + 2 * (z[2] - z[3])
    return sign_q5(p, q)


def coords5_B(w):
    """x = r + s sqrt5 ; Y = y / sin72 = r' + s' sqrt5 (exact rationals)."""
    w0, w1, w2, w3, w4 = w
    xr = Fr(w0) - Fr(w1 + w4, 4) - Fr(w2 + w3, 4)
    xs = Fr(w1 + w4, 4) - Fr(w2 + w3, 4)
    Yr = Fr(w1 - w4) - Fr(w2 - w3, 2)
    Ys = Fr(w2 - w3, 2)
    return (xr, xs), (Yr, Ys)


def q5_sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def q5_mul(u, v):
    return (u[0] * v[0] + 5 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def orient5_B(CB, a, b, c):
    (axx, ayy), (bxx, byy), (cxx, cyy) = CB[a], CB[b], CB[c]
    t1 = q5_mul(q5_sub(bxx, axx), q5_sub(cyy, ayy))
    t2 = q5_mul(q5_sub(byy, ayy), q5_sub(cxx, axx))
    d = q5_sub(t1, t2)
    return sign_q5(d[0], d[1])


# rigorous rational intervals
PREC = 2 ** 400


def isqrt_lo_hi(lo, hi):
    """rational bounds L <= sqrt(lo), sqrt(hi) <= H for rationals 0 <= lo <= hi."""
    a = math.floor(lo * PREC * PREC)
    L = Fr(math.isqrt(a), PREC)
    b = math.ceil(hi * PREC * PREC)
    r = math.isqrt(b)
    if r * r < b:
        r += 1
    H = Fr(r, PREC)
    assert L * L <= lo and H * H >= hi
    return L, H


S5 = isqrt_lo_hi(Fr(5), Fr(5))
S10p = isqrt_lo_hi(10 + 2 * S5[0], 10 + 2 * S5[1])
S10m = isqrt_lo_hi(10 - 2 * S5[1], 10 - 2 * S5[0])


def iv(a, b=None):
    return (a, a) if b is None else (a, b)


def iadd(u, v):
    return (u[0] + v[0], u[1] + v[1])


def isub(u, v):
    return (u[0] - v[1], u[1] - v[0])


def imul(u, v):
    ps = [u[0] * v[0], u[0] * v[1], u[1] * v[0], u[1] * v[1]]
    return (min(ps), max(ps))


def iscale(k, u):
    return imul(iv(Fr(k)), u)


COS72 = iscale(Fr(1, 4), isub(S5, iv(Fr(1))))           # (sqrt5 - 1)/4
COS144 = iscale(Fr(-1, 4), iadd(S5, iv(Fr(1))))         # -(sqrt5 + 1)/4
SIN72 = iscale(Fr(1, 4), S10p)                          # sqrt(10 + 2 sqrt5)/4
SIN144 = iscale(Fr(1, 4), S10m)                         # sqrt(10 - 2 sqrt5)/4


def coords5_C(w):
    w0, w1, w2, w3, w4 = w
    x = iadd(iadd(iv(Fr(w0)), iscale(w1 + w4, COS72)), iscale(w2 + w3, COS144))
    y = iadd(iscale(w1 - w4, SIN72), iscale(w2 - w3, SIN144))
    return x, y


def orient5_C(CC, a, b, c):
    (ax, ay), (bx, by), (cx, cy) = CC[a], CC[b], CC[c]
    d = isub(imul(isub(bx, ax), isub(cy, ay)), imul(isub(by, ay), isub(cx, ax)))
    if d[0] > 0:
        return 1
    if d[1] < 0:
        return -1
    return None  # undecided


# ---------------------------------------------------------------- combinatorial tests
def convex_T1(O, S):
    for d in S:
        others = [x for x in S if x != d]
        for a, b, c in itertools.combinations(others, 3):
            s = O[a][b][c]
            if O[a][b][d] == s and O[b][c][d] == s and O[c][a][d] == s:
                return False
    return True


def convex_T2(O, S):
    edges = 0
    for p in S:
        for q in S:
            if p == q:
                continue
            if all(O[p][q][r] > 0 for r in S if r != p and r != q):
                edges += 1
    return edges == len(S)


def hull_vertices(O, S):
    """vertices of conv(S) (general position): points not strictly inside a triangle of others."""
    res = []
    for d in S:
        inside = False
        others = [x for x in S if x != d]
        for a, b, c in itertools.combinations(others, 3):
            s = O[a][b][c]
            if O[a][b][d] == s and O[b][c][d] == s and O[c][a][d] == s:
                inside = True
                break
        if not inside:
            res.append(d)
    return res


def main():
    path, m, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    otab = sys.argv[4] if len(sys.argv) > 4 else None
    header, W = read_pts(path)
    n = len(W)
    print('file', path)
    print('header', header)
    print('m', m, 'K', K, 'n', n)
    assert all(len(w) == m for w in W)
    canon = canon4 if m == 4 else canon5

    # distinctness
    C = [canon(w) for w in W]
    print('distinct points:', len(set(C)) == n)

    # rotation by zeta = cyclic shift of the coefficient vector
    def rot(w):
        return tuple(w[(j - 1) % m] for j in range(m))
    S = set(C)
    print('set invariant under rotation by zeta:', set(canon(rot(w)) for w in W) == S)
    # orbit / row structure
    centre = (m == 5 and n % m == 1)
    t = n // m
    rows_ok = True
    for o in range(t):
        base = W[o * m]
        cur = base
        for k in range(m):
            if canon(W[o * m + k]) != canon(cur):
                rows_ok = False
            cur = rot(cur)
        if canon(cur) != canon(base):
            rows_ok = False
    print('rows o*m+k = zeta^k * row o*m for all', t, 'layers:', rows_ok)
    if centre:
        print('last row is the centre 0:', all(v == 0 for v in C[-1]))
    print('layers t =', t, 'centre =', centre)

    # orientation table
    O = [[[0] * n for _ in range(n)] for _ in range(n)]
    zero = 0
    if m == 4:
        P = [canon4(w) for w in W]
        print('integer coordinates (Gaussian):', P)
        for a, b, c in itertools.product(range(n), repeat=3):
            if len({a, b, c}) < 3:
                continue
            O[a][b][c] = orient4(P, a, b, c)
        ntrip = 0
        mindet = None
        for a, b, c in itertools.combinations(range(n), 3):
            ntrip += 1
            ax, ay = P[a]; bx, by = P[b]; cx, cy = P[c]
            d = abs((bx - ax) * (cy - ay) - (by - ay) * (cx - ax))
            mindet = d if mindet is None else min(mindet, d)
            if d == 0:
                zero += 1
        print('triples', ntrip, 'zero orientations', zero, 'min |det| (integer)', mindet)
        R2 = [x * x + y * y for x, y in P]
        radcmp = lambda i, j: (R2[i] > R2[j]) - (R2[i] < R2[j])
    else:
        CB = [coords5_B(w) for w in W]
        CCI = [coords5_C(w) for w in W]
        disagreeAB = disagreeAC = undecC = 0
        ntrip = 0
        for a, b, c in itertools.product(range(n), repeat=3):
            if len({a, b, c}) < 3:
                continue
            sA = orient5_A(W, a, b, c)
            sB = orient5_B(CB, a, b, c)
            sC = orient5_C(CCI, a, b, c)
            if sA != sB:
                disagreeAB += 1
            if sC is None:
                undecC += 1
            elif sC != sA:
                disagreeAC += 1
            if sA == 0:
                zero += 1
            O[a][b][c] = sA
            ntrip += 1
        print('ordered triples', ntrip, 'zero orientations', zero,
              'A/B disagreements', disagreeAB, 'A/C disagreements', disagreeAC, 'C undecided', undecC)
        # squared radius |P|^2 = x^2 + sin^2(72) Y^2, sin^2 72 = (10 + 2 sqrt5)/16, exact in Q(sqrt5)
        sin2 = (Fr(10, 16), Fr(2, 16))
        R2 = []
        for (xx, YY) in CB:
            v = q5_mul(xx, xx)
            u = q5_mul(sin2, q5_mul(YY, YY))
            R2.append((v[0] + u[0], v[1] + u[1]))
        radcmp = lambda i, j: sign_q5(R2[i][0] - R2[j][0], R2[i][1] - R2[j][1])
        # float picture for the reader
        fl = [(float(x[0]) + float(x[1]) * 5 ** 0.5, (float(Y[0]) + float(Y[1]) * 5 ** 0.5) * math.sin(2 * math.pi / 5)) for x, Y in CB]
        print('float coordinates:', [(round(x, 3), round(y, 3)) for x, y in fl])

    # antisymmetry of the table
    bad = 0
    for a, b, c in itertools.permutations(range(n), 3):
        s = O[a][b][c]
        if not (O[b][c][a] == s and O[c][a][b] == s and O[b][a][c] == -s and O[a][c][b] == -s and O[c][b][a] == -s):
            bad += 1
    print('orientation table antisymmetry violations:', bad)

    # compare with the original otab (if given)
    if otab:
        raw = open(otab, 'rb').read()
        nl = raw.index(b'\n')
        nn = int(raw[:nl])
        body = raw[nl + 1:]
        assert nn == n and len(body) == n ** 3, (nn, len(body))
        mism = 0
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    v = body[(a * n + b) * n + c]
                    v = v - 256 if v > 127 else v
                    if v != O[a][b][c]:
                        mism += 1
        print('comparison with original otab', otab, ': mismatching entries', mism, 'of', n ** 3)

    # convex layers (onion peeling) with exact orientations only
    rem = list(range(n))
    layers = []
    while rem:
        if len(rem) <= 2:
            hv = list(rem)
        else:
            hv = hull_vertices(O, rem)
        layers.append(sorted(hv))
        rem = [x for x in rem if x not in hv]
    print('convex layers (onion peeling):', layers)
    print('convex layer sizes:', [len(L) for L in layers])
    expect = [list(range(o * m, o * m + m)) for o in range(t)] + ([[n - 1]] if centre else [])
    print('convex layers == symmetry orbits (outermost first):', layers == expect)
    # radii strictly decreasing across orbits, equal within an orbit
    within = all(radcmp(o * m, o * m + k) == 0 for o in range(t) for k in range(m))
    decr = all(radcmp(o * m, (o + 1) * m) > 0 for o in range(t - 1))
    print('radius constant on each orbit:', within, ' radii strictly decreasing outward->inward:', decr)

    # brute-force convex k-subset counts with two independent tests
    counts = {}
    for k in range(3, K + 1):
        c1 = c2 = dis = 0
        for Ssub in itertools.combinations(range(n), k):
            r1 = convex_T1(O, Ssub)
            r2 = convex_T2(O, Ssub)
            c1 += r1
            c2 += r2
            dis += (r1 != r2)
        counts[k] = (c1, c2, dis)
        print('k=%d: subsets %d, convex by T1 %d, by T2 %d, T1/T2 disagreements %d' % (k, math.comb(n, k), c1, c2, dis))
    largest = max([k for k in counts if counts[k][0] > 0])
    print('largest convex subset size (hereditary: none of size K => none larger):', largest if counts[K][0] == 0 else '>= K')
    ok = (zero == 0 and counts[K][0] == 0 and counts[K][1] == 0 and all(v[2] == 0 for v in counts.values())
          and layers == expect and bad == 0)
    print('OVERALL', 'PASS' if ok else 'FAIL')


if __name__ == '__main__':
    main()
