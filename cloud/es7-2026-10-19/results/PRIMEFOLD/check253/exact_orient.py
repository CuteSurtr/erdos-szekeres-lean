#!/usr/bin/env python3
"""Independent exact verifier (written from scratch) for the 9-fold point set claimed in R9.

Points: each layer rep r = sum_k c_k zeta^k (zeta = exp(2 pi i/9)); the layer is {zeta^s r : s = 0..8};
index = layer*9 + s; centre (0) is the last index.

Exact arithmetic: for an integer vector e (coefficients of zeta^0..zeta^8)
   Im(e) = A sin20 + B sin40 + C sin60      with A = e2+e4-e5-e7, B = e1+e2-e7-e8, C = e3-e6
   2Re(e) = al + be cos20 + ga cos40        with al = 2e0-e3-e6, be = 2(e2+e7-e4-e5), ga = 2(e1+e8-e2-e7)
(uses sin80 = sin20+sin40, cos80 = cos20-cos40).  {sin20, sin40, sin60} and {1, cos20, cos40} are Q-linearly
independent, so a value is exactly zero iff its integer coefficients are all zero.
Signs of nonzero values: rigorous interval evaluation with constants derived from the minimal polynomial
8x^3-6x-1 of cos20 (integer bisection), integer square roots, and outward rounding.  No floating point is used
for any decision.

orient(P,Q,R) = Im(conj(Q-P)(R-P)) = cross(P,Q)+cross(Q,R)+cross(R,P),  cross(X,Y) = Im(conj(X) Y).
usage: exact_orient.py points.pts outdir
"""
import sys, os, time, functools, math

def parse(path):
    lines = [l.split() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    p, t, c = map(int, lines[0])
    assert len(lines) == 1 + t, (len(lines), t)
    reps = [list(map(int, l)) for l in lines[1:]]
    assert all(len(r) == p for r in reps)
    return p, t, c, reps

def constants(N):
    one = 1 << N
    def g(c):  # 2^(3N) * f(c/2^N), f(x) = 8x^3 - 6x - 1, increasing for x > 1/2
        return 8 * c ** 3 - 6 * c * one * one - one ** 3
    lo, hi = (9 * one) // 10, one
    assert g(lo) < 0 < g(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if g(mid) <= 0: lo = mid
        else: hi = mid
    assert g(lo) < 0 < g(hi)            # root cos20 strictly inside (lo, hi)/2^N
    cL, cH = lo, hi
    K = {}
    K['c20'] = (cL, cH)
    K['c40'] = ((2 * cL * cL) // one - one, -((-2 * cH * cH) // one) - one)      # 2c^2-1, increasing in c>0
    sL = math.isqrt(one * one - cH * cH); sH = math.isqrt(one * one - cL * cL) + 1  # sqrt(1-c^2), decreasing
    K['s20'] = (sL, sH)
    K['s40'] = ((2 * sL * cL) // one, -((-2 * sH * cH) // one))                  # 2 s c
    r3 = math.isqrt(3 * one * one // 4)                                           # sqrt(3)/2 * 2^N  (3*4^N/4 exact)
    K['s60'] = (r3, r3 + 1)
    for k, (L, H) in K.items():
        assert L < H, k
    return K

def im_abc(e):
    return (e[2] + e[4] - e[5] - e[7], e[1] + e[2] - e[7] - e[8], e[3] - e[6])

def re2_abc(e):
    return (2 * e[0] - e[3] - e[6], 2 * (e[2] + e[7] - e[4] - e[5]), 2 * (e[1] + e[8] - e[2] - e[7]))

class Signer:
    def __init__(self, N):
        self.N = N; self.K = constants(N)
        self.sinL = [self.K['s20'][0], self.K['s40'][0], self.K['s60'][0]]
        self.sinD = [self.K['s20'][1] - self.K['s20'][0], self.K['s40'][1] - self.K['s40'][0], self.K['s60'][1] - self.K['s60'][0]]
        self.cosL = [self.K['c20'][0], self.K['c40'][0]]
        self.cosD = [self.K['c20'][1] - self.K['c20'][0], self.K['c40'][1] - self.K['c40'][0]]
    def sign_sin(self, A, B, C):
        """certified sign of A sin20 + B sin40 + C sin60; returns (sign, value_scaled_lowerbound_estimate) or None"""
        L = self.sinL; D = self.sinD
        V = A * L[0] + B * L[1] + C * L[2]
        E = abs(A) * D[0] + abs(B) * D[1] + abs(C) * D[2]
        if V > E: return 1
        if V < -E: return -1
        if A == 0 and B == 0 and C == 0: return 0
        return None
    def sign_re2(self, al, be, ga):
        L = self.cosL; D = self.cosD
        one = 1 << self.N
        V = al * one + be * L[0] + ga * L[1]
        E = abs(be) * D[0] + abs(ga) * D[1]
        if V > E: return 1
        if V < -E: return -1
        if al == 0 and be == 0 and ga == 0: return 0
        return None

def main():
    path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    p, t, cflag, reps = parse(path)
    assert p == 9 and cflag in (0, 1)
    n = p * t + cflag
    pts = []
    for l in range(t):
        for s in range(p):
            pts.append([reps[l][(j - s) % p] for j in range(p)])   # zeta^s * rep
    if cflag: pts.append([0] * p)
    assert len(pts) == n
    log = open(os.path.join(outdir, 'exact_orient.log'), 'w')
    def out(*a):
        s = ' '.join(str(x) for x in a); print(s); log.write(s + '\n'); log.flush()
    out('file', path, 'p', p, 't', t, 'centre', cflag, 'n', n)
    sg = Signer(256); sg_hi = Signer(1024)
    # sanity: constants against floating point
    for k, (L, H) in sg.K.items():
        val = {'c20': math.cos(math.radians(20)), 'c40': math.cos(math.radians(40)), 's20': math.sin(math.radians(20)),
               's40': math.sin(math.radians(40)), 's60': math.sin(math.radians(60))}[k]
        assert abs(L / 2 ** 256 - val) < 1e-15 and abs(H / 2 ** 256 - val) < 1e-15, k
        out('const', k, 'width (units 2^-256):', H - L, 'float check ok')
    # identities used (float sanity)
    s = lambda d: math.sin(math.radians(d)); c = lambda d: math.cos(math.radians(d))
    assert abs(s(80) - s(20) - s(40)) < 1e-15 and abs(c(80) - c(20) + c(40)) < 1e-15
    # float coordinates for cross-checking the coefficient formulas
    def fcoord(e):
        return (sum(e[k] * math.cos(2 * math.pi * k / 9) for k in range(9)), sum(e[k] * math.sin(2 * math.pi * k / 9) for k in range(9)))
    for e in [[1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [3, -1, 4, 1, -5, 9, 2, -6, 5]]:
        x, y = fcoord(e)
        A, B, C = im_abc(e); al, be, ga = re2_abc(e)
        assert abs(y - (A * s(20) + B * s(40) + C * s(60))) < 1e-12
        assert abs(2 * x - (al + be * c(20) + ga * c(40))) < 1e-12
    out('coefficient formulas: float sanity ok')
    # distinctness of points / layers (exact): two points equal iff Re and Im differences are exactly zero
    def cmp_pts(i, j, primary):
        e = [pts[j][k] - pts[i][k] for k in range(9)]
        if primary == 'y':
            s1 = sg.sign_sin(*im_abc(e))
            if s1 is None: s1 = sg_hi.sign_sin(*im_abc(e))
            if s1 != 0: return -s1      # i before j iff y_i < y_j
            s2 = sg.sign_re2(*re2_abc(e))
            if s2 is None: s2 = sg_hi.sign_re2(*re2_abc(e))
            assert s2 != 0, ('identical points', i, j)
            return -s2
        else:
            s1 = sg.sign_re2(*re2_abc(e))
            if s1 is None: s1 = sg_hi.sign_re2(*re2_abc(e))
            if s1 != 0: return -s1
            s2 = sg.sign_sin(*im_abc(e))
            if s2 is None: s2 = sg_hi.sign_sin(*im_abc(e))
            assert s2 != 0, ('identical points', i, j)
            return -s2
    t0 = time.time()
    yorder = sorted(range(n), key=functools.cmp_to_key(lambda i, j: cmp_pts(i, j, 'y')))
    xorder = sorted(range(n), key=functools.cmp_to_key(lambda i, j: cmp_pts(i, j, 'x')))
    # verify the orders are strict by checking consecutive pairs again
    for o, nm in ((yorder, 'y'), (xorder, 'x')):
        for a, b in zip(o, o[1:]):
            assert cmp_pts(a, b, nm) < 0
    yrank = [0] * n; xrank = [0] * n
    for r, i in enumerate(yorder): yrank[i] = r
    for r, i in enumerate(xorder): xrank[i] = r
    ties_y = 0
    for a, b in zip(yorder, yorder[1:]):
        e = [pts[b][k] - pts[a][k] for k in range(9)]
        if im_abc(e) == (0, 0, 0): ties_y += 1
    ties_x = 0
    for a, b in zip(xorder, xorder[1:]):
        e = [pts[b][k] - pts[a][k] for k in range(9)]
        if re2_abc(e) == (0, 0, 0): ties_x += 1
    out('exact y-order and x-order computed (all points distinct); exact ties in y:', ties_y, 'ties in x:', ties_x, '%.1fs' % (time.time() - t0))
    with open(os.path.join(outdir, 'ranks.txt'), 'w') as f:
        f.write('%d\n' % n)
        for i in range(n): f.write('%d %d\n' % (yrank[i], xrank[i]))
    # cross table
    t0 = time.time()
    CA = [[0] * n for _ in range(n)]; CB = [[0] * n for _ in range(n)]; CC = [[0] * n for _ in range(n)]
    for i in range(n):
        x = pts[i]
        for j in range(n):
            y = pts[j]
            w = [sum(x[a] * y[(a + m) % 9] for a in range(9) if x[a]) for m in range(9)]
            A, B, C = im_abc(w)
            CA[i][j] = A; CB[i][j] = B; CC[i][j] = C
    for i in range(n):
        for j in range(n):
            assert CA[i][j] == -CA[j][i] and CB[i][j] == -CB[j][i] and CC[i][j] == -CC[j][i]
    out('cross table built and antisymmetric', '%.1fs' % (time.time() - t0))
    # all triples i<j<k
    t0 = time.time()
    table = bytearray(n * n * n)
    n2 = n * n
    zeros = 0; undecided = 0; hi_used = 0; npos = 0; nneg = 0
    L0, L1, L2 = sg.sinL; D0, D1, D2 = sg.sinD
    minabs = None; minabs_trip = None
    for i in range(n):
        CAi = CA[i]; CBi = CB[i]; CCi = CC[i]
        for j in range(i + 1, n):
            a1 = CAi[j]; b1 = CBi[j]; c1 = CCi[j]
            CAj = CA[j]; CBj = CB[j]; CCj = CC[j]
            base = i * n2 + j * n
            for k in range(j + 1, n):
                A = a1 + CAj[k] - CAi[k]      # cross(i,j)+cross(j,k)+cross(k,i), cross(k,i) = -cross(i,k)
                B = b1 + CBj[k] - CBi[k]
                C = c1 + CCj[k] - CCi[k]
                V = A * L0 + B * L1 + C * L2
                E = (A if A >= 0 else -A) * D0 + (B if B >= 0 else -B) * D1 + (C if C >= 0 else -C) * D2
                if V > E:
                    table[base + k] = 1; npos += 1
                elif V < -E:
                    table[base + k] = 255; nneg += 1
                else:
                    sgn = sg_hi.sign_sin(A, B, C); hi_used += 1
                    if sgn is None:
                        undecided += 1; out('UNDECIDED', i, j, k, A, B, C)
                    elif sgn == 0:
                        zeros += 1; out('COLLINEAR', i, j, k)
                    else:
                        table[base + k] = 1 if sgn > 0 else 255
                        if sgn > 0: npos += 1
                        else: nneg += 1
                    continue
                av = V if V >= 0 else -V
                if minabs is None or av < minabs:
                    minabs = av; minabs_trip = (i, j, k)
        if i % 25 == 0:
            print('  i=%d %.0fs' % (i, time.time() - t0), flush=True)
    ntrip = n * (n - 1) * (n - 2) // 6
    out('triples:', ntrip, 'positive', npos, 'negative', nneg, 'collinear(zero)', zeros, 'undecided', undecided,
        'needed 1024-bit fallback', hi_used, '%.1fs' % (time.time() - t0))
    out('smallest |orient| among filter-certified triples ~ %.4e at triple %s' % (minabs / 2 ** 256, minabs_trip))
    with open(os.path.join(outdir, 'orient_upper.bin'), 'wb') as f:
        f.write(table)
    out('wrote orient_upper.bin (n^3 bytes; entry [i][j][k] for i<j<k: 1 = ccw, 255 = cw)')
    import hashlib
    out('sha256 orient_upper.bin', hashlib.sha256(table).hexdigest())
    ok = zeros == 0 and undecided == 0 and npos + nneg == ntrip
    out('GENERAL POSITION (no three collinear, all signs certified):', 'YES' if ok else 'NO')
    # rotation consistency: orient(rot i, rot j, rot k) == orient(i,j,k)
    def rot(x, r):
        if x == n - 1 and cflag: return x
        return (x // 9) * 9 + (x % 9 + r) % 9
    def ori(a, b, c):
        s = 1
        tr = [a, b, c]
        # sort with parity
        if tr[0] > tr[1]: tr[0], tr[1] = tr[1], tr[0]; s = -s
        if tr[1] > tr[2]: tr[1], tr[2] = tr[2], tr[1]; s = -s
        if tr[0] > tr[1]: tr[0], tr[1] = tr[1], tr[0]; s = -s
        v = table[tr[0] * n2 + tr[1] * n + tr[2]]
        v = 1 if v == 1 else (-1 if v == 255 else 0)
        return s * v
    import random
    rng = random.Random(20261102)
    bad = 0
    for _ in range(300000):
        a, b, c = rng.sample(range(n), 3); r = rng.randrange(1, 9)
        if ori(a, b, c) != ori(rot(a, r), rot(b, r), rot(c, r)) or ori(a, b, c) != ori(b, c, a) or ori(a, b, c) != -ori(b, a, c):
            bad += 1
    out('rotation/cyclic/antisymmetry consistency on 300000 random triples: violations', bad)
    log.close()

if __name__ == '__main__':
    main()
