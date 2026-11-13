#!/usr/bin/env python3
"""Cross-check of orientation signs by a third numeric route (written from scratch for R11):
coordinates in 250-digit Decimal from t = 2cos(2pi/p) (Decimal bisection on m), cos(k theta) = V_k(t)/2,
sin(k theta) = sin(theta) U_{k-1}(t), sin(theta) = sqrt(1 - t^2/4) (Decimal sqrt).  No Taylor series, no pi.
Compares (a) my es_orient bit table on random + same-sector + same-cluster triples, (b) the claimant's sample file.
usage: cross_sample.py points.pts prefix claimant_sample.txt nsample"""
import sys, random
from decimal import Decimal as Dm, getcontext
getcontext().prec = 250
pts_file, prefix, sample_file, NS = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
lines = [l for l in open(pts_file) if l.strip() and not l.lstrip().startswith('#')]
p, t, C = map(int, lines[0].split())
reps = [list(map(int, l.split())) for l in lines[1:1 + t]]
assert len(reps) == t and all(len(r) == p for r in reps)
h = (p - 1) // 2
# m(x) = 1 + sum_{k=1}^h V_k(x)
def polyV(k):
    V = [[2], [0, 1]]
    for j in range(1, k):
        a = [0] + V[j]; b = V[j - 1] + [0] * (len(a) - len(V[j - 1]))
        V.append([x - y for x, y in zip(a, b)])
    return V
V = polyV(p)
m = [0] * (h + 1); m[0] = 1
for k in range(1, h + 1):
    for d, c in enumerate(V[k]): m[d] += c
def mval(x):
    s = Dm(0)
    for c in reversed(m): s = s * x + c
    return s
lo, hi = Dm(2) * Dm(0.999) * 0 + Dm(1), Dm(2)   # [1,2] contains exactly the largest root for p=11 (checked below)
assert mval(lo) < 0 < mval(hi)
for _ in range(840):
    mid = (lo + hi) / 2
    if mval(mid) < 0: lo = mid
    else: hi = mid
tt = (lo + hi) / 2
cosk = [Dm(0)] * p; sink = [Dm(0)] * p
Vv = [Dm(2), tt]; Uv = [Dm(1), tt]
for k in range(2, p + 1): Vv.append(tt * Vv[-1] - Vv[-2]); Uv.append(tt * Uv[-1] - Uv[-2])
s1 = (1 - tt * tt / 4).sqrt()
for k in range(p):
    cosk[k] = Vv[k] / 2
    sink[k] = s1 * Uv[k - 1] if k >= 1 else Dm(0)
n = p * t + C
X = [None] * n; Y = [None] * n
for l in range(t):
    for k in range(p):
        c = [reps[l][(j - k) % p] for j in range(p)]
        X[l * p + k] = sum(Dm(c[j]) * cosk[j] for j in range(p) if c[j])
        Y[l * p + k] = sum(Dm(c[j]) * sink[j] for j in range(p) if c[j])
if C: X[n - 1] = Dm(0); Y[n - 1] = Dm(0)
def det(a, b, c): return (X[b] - X[a]) * (Y[c] - Y[a]) - (Y[b] - Y[a]) * (X[c] - X[a])
bits = open(prefix + '.signs', 'rb').read()
def c3(k): return k * (k - 1) * (k - 2) // 6
def c2(k): return k * (k - 1) // 2
def mysign(a, b, c):
    x = sorted([a, b, c]); par = 0
    perm = [a, b, c]
    # parity of permutation from (a,b,c) to sorted
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j]); par = inv & 1
    idx = c3(x[2]) + c2(x[1]) + x[0]
    s = 1 if (bits[idx >> 3] >> (idx & 7)) & 1 else -1
    return -s if par else s
maxc = max(abs(v) for r in reps for v in r)
errb = Dm(maxc) ** 2 * Dm(10) ** -230     # generous bound on the Decimal error of a determinant
random.seed(20261102)
mism = 0; cnt = 0; minabs = None; und = 0
for it in range(NS):
    mode = it % 3
    if mode == 0:
        a, b, c = random.randrange(n), random.randrange(n), random.randrange(n)
    elif mode == 1:   # same sector, any layers
        s0 = random.randrange(p); a, b, c = [random.randrange(t) * p + s0 for _ in range(3)]
    else:             # same sector, consecutive layers (same cluster neighbourhood)
        s0 = random.randrange(p); l0 = random.randrange(t - 6); a, b, c = [(l0 + random.randrange(7)) * p + s0 for _ in range(3)]
    if len({a, b, c}) < 3: continue
    d = det(a, b, c)
    if abs(d) <= errb: und += 1; continue
    sd = 1 if d > 0 else -1
    if sd != mysign(a, b, c): mism += 1
    if minabs is None or abs(d) < minabs: minabs = abs(d)
    cnt += 1
print('my table vs 250-digit Decimal (t-route): %d triples, %d mismatches, %d undecided, min |det| %.4E, error bound %.2E' % (cnt, mism, und, minabs, errb))
# claimant sample
cm = 0; cc = 0; cu = 0; cmine = 0
for l in open(sample_file):
    a, b, c, s = map(int, l.split())
    d = det(a, b, c)
    if abs(d) <= errb: cu += 1; continue
    sd = 1 if d > 0 else -1
    if sd != s: cm += 1
    if mysign(a, b, c) != s: cmine += 1
    cc += 1
print('claimant sample: %d triples, Decimal-vs-claimant mismatches %d, my-table-vs-claimant mismatches %d, undecided %d' % (cc, cm, cmine, cu))
