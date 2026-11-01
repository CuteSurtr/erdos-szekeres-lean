#!/usr/bin/env python3
"""Check a polygon (point indices, layer*p + sector convention, centre = p*t) for strict convex position using my
es_orient bit table: all cyclic turns left AND no vertex inside a triangle of three others.
usage: check_witness.py prefix i1 i2 ..."""
import sys, itertools
prefix = sys.argv[1]; W = list(map(int, sys.argv[2:]))
p, t, C, n = map(int, open(prefix + '.meta').readline().split())
bits = open(prefix + '.signs', 'rb').read()
def c3(k): return k * (k - 1) * (k - 2) // 6
def c2(k): return k * (k - 1) // 2
def o(a, b, c):
    perm = [a, b, c]; x = sorted(perm)
    par = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j]) & 1
    idx = c3(x[2]) + c2(x[1]) + x[0]
    s = 1 if (bits[idx >> 3] >> (idx & 7)) & 1 else -1
    return -s if par else s
L = len(W)
left = all(o(W[q], W[(q + 1) % L], W[(q + 2) % L]) > 0 for q in range(L))
inside = 0
for x in W:
    for a, b, c in itertools.combinations([y for y in W if y != x], 3):
        s1, s2, s3 = o(a, b, x), o(b, c, x), o(c, a, x)
        if s1 == s2 == s3: inside += 1
print('polygon of %d points: distinct %s, all turns left %s, vertex-in-triangle incidences %d -> convex position %s'
      % (L, len(set(W)) == L, left, inside, left and inside == 0 and len(set(W)) == L))
