#!/usr/bin/env python3
"""Independent exact verification of a 7-fold point set in Z[zeta_7] (E8 check).

usage: verify64.py FILE [--dump OUT.npy-like text]
Checks: distinctness, 7-fold invariance, centre, exact orientation table (no zero), mpmath cross-check of
all signs, exact (y,x)-lexicographic order, exact counts of convex k-gons by anchor DP, largest convex subset.
"""
import sys, hashlib, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import z7exact as Z
from functools import cmp_to_key
import dec_trig as DT
from decimal import Decimal

path = sys.argv[1]
raw = open(path, 'rb').read()
print('file', path)
print('sha256', hashlib.sha256(raw).hexdigest())
pts = Z.read_pts(path)
n = len(pts)
print('n =', n)

# distinctness (canonical representatives in Z[zeta])
can = [Z.canon(w) for w in pts]
assert len(set(can)) == n, 'duplicate points'
print('distinct: yes')

# 7-fold invariance: rotation by zeta permutes the set
idx = {c: i for i, c in enumerate(can)}
perm = []
for w in pts:
    r = Z.canon(Z.rot(w))
    assert r in idx, 'rotation image not in set'
    perm.append(idx[r])
assert sorted(perm) == list(range(n))
fixed = [i for i in range(n) if perm[i] == i]
print('rotation by 2pi/7 maps set onto itself: yes; fixed points:', fixed,
      'coords:', [pts[i] for i in fixed])
# orbit structure
seen = set(); orbits = []
for i in range(n):
    if i in seen:
        continue
    o = [i]; j = perm[i]
    while j != i:
        o.append(j); j = perm[j]
    seen.update(o); orbits.append(o)
print('orbit sizes:', sorted(len(o) for o in orbits))

t0 = time.time()
O = Z.orient_table(pts)
print('exact orientation table computed in %.1fs' % (time.time() - t0))
zeros = sum(1 for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n) if O[i][j][k] == 0)
print('collinear triples (exact):', zeros)
assert zeros == 0

# decimal cross-check (independent numeric method, 110 digits)
DT.setup(110)
PI = DT.pi()
cs = []; sn = []
for j in range(7):
    c_, s_ = DT.cos_sin(2 * PI * j / 7)
    cs.append(c_); sn.append(s_)
X = [sum((Decimal(w[j]) * cs[j] for j in range(7)), Decimal(0)) for w in pts]
Y = [sum((Decimal(w[j]) * sn[j] for j in range(7)), Decimal(0)) for w in pts]
mind = None; bad = 0
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            d = (X[j] - X[i]) * (Y[k] - Y[i]) - (Y[j] - Y[i]) * (X[k] - X[i])
            s = 1 if d > 0 else -1
            if s != O[i][j][k]:
                bad += 1
            ad = abs(d)
            if mind is None or ad < mind:
                mind = ad
print('decimal(110 digits) sign disagreements:', bad, ' min |det| = %.4e' % mind,
      ' max |coord| = %.4e' % max(max(abs(x) for x in X), max(abs(y) for y in Y)))
assert bad == 0

# rotation is an automorphism of the oriented matroid (sanity)
autbad = sum(1 for i in range(n) for j in range(n) for k in range(n)
             if O[i][j][k] != O[perm[i]][perm[j]][perm[k]])
print('rotation preserves orientation table:', autbad == 0)


# exact lexicographic order by (y, x)
def cmp_yx(a, b):
    if a == b:
        return 0
    s = Z.sign_im_diff(pts[a], pts[b])
    if s != 0:
        return s
    s = Z.sign_re_diff(pts[a], pts[b])
    assert s != 0
    return s


order = sorted(range(n), key=cmp_to_key(cmp_yx))
rank = [0] * n
for r, i in enumerate(order):
    rank[i] = r
# sanity vs mpmath
for a, b in zip(order, order[1:]):
    assert (Y[a] < Y[b]) or (Y[a] == Y[b] and X[a] < X[b]), 'lex order mismatch'
ties = sum(1 for a, b in zip(order, order[1:]) if Z.sign_im_diff(pts[a], pts[b]) == 0)
print('exact (y,x) order computed; equal-y adjacent pairs:', ties)

# anchor DP counting convex k-gons
KMAX = 10
counts = [0] * (KMAX + 1)
for p in range(n):
    above = [q for q in range(n) if rank[q] > rank[p]]
    # angular sort around p: q before r iff orient(p,q,r) > 0 (all in half-open upper half plane)
    above.sort(key=cmp_to_key(lambda q, r: -O[p][q][r]))
    m = len(above)
    for a in range(m):
        for b in range(a + 1, m):
            assert O[p][above[a]][above[b]] > 0
    Op = O[p]
    # cnt[k][i][j]
    prev = [[1 if i < j else 0 for j in range(m)] for i in range(m)]  # k = 3
    for i in range(m):
        for j in range(i + 1, m):
            if O[above[i]][above[j]][p] > 0:
                counts[3] += 1
    for k in range(4, KMAX + 1):
        cur = [[0] * m for _ in range(m)]
        anyc = False
        for j in range(m):
            aj = above[j]
            for i in range(j):
                ai = above[i]
                Oi = O[ai]
                s = 0
                for h in range(i):
                    v = prev[h][i]
                    if v and O[above[h]][ai][aj] > 0:
                        s += v
                if s:
                    cur[i][j] = s
                    anyc = True
                    if Oi[aj][p] > 0:
                        counts[k] += s
        prev = cur
        if not anyc:
            break
print('convex k-gon counts (k=3..%d):' % KMAX, counts[3:])
mc = max(k for k in range(3, KMAX + 1) if counts[k] > 0)
print('largest convex subset (exact):', mc)

if len(sys.argv) > 2:
    out = sys.argv[2]
    with open(out, 'w') as fh:
        fh.write('%d\n' % n)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    fh.write('+' if O[i][j][k] > 0 else '-')
        fh.write('\n')
    print('wrote sign string (i<j<k lex) to', out)
