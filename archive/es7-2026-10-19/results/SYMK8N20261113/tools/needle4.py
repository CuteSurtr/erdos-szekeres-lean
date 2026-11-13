#!/usr/bin/env python3
"""4-fold strict radial needle: arm orbit j = r_j + eps * y_j * i (Gaussian), profile B = {(r_j, y_j)}.
Necessary conditions (Proposition N and its antipodal analogue): cup(B) + cap(B) <= 7 (adjacent needles), and
B u (-B) has no convex octagon (the antipodal needles are exactly the affine image (x, eps y) of B u (-B)).
This script (HEURISTIC lower bound) searches profiles of size n by random restarts + hill climbing on the exact
octagon count of the 4n-point needle configuration and reports the largest n reached with 0 octagons, and checks the
antipodal identity on random profiles.
usage: needle4.py SEED NMAX SECONDS"""
import sys, os, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from double_exact import peval
from needle_test import cupcap, es_set


def needle4(B):
    pts = []
    for (r, y) in B:
        cur = [(0, r, 0), (1, 0, y)]
        for _ in range(4):
            pts.append(cur)
            cur = [(e, -yy, xx) for (e, xx, yy) in cur]
    return pts


def n8(B):
    ml, cnt, nz = peval(needle4(B), 8)
    return None if nz else cnt[8]


def planar_n8(P):
    ml, cnt, nz = peval([[(0, x, y)] for (x, y) in P], 8)
    return None if nz else cnt[8]


random.seed(int(sys.argv[1])); NMAX = int(sys.argv[2]); T = float(sys.argv[3])
E = sorted((x + 1, y) for (x, y) in es_set(4, 5))
print('ES profile (10 points, cup 3 cap 4): 4-fold needle octagons =', n8(E),
      '; B u -B octagons =', planar_n8(E + [(-x, -y) for (x, y) in E]), flush=True)
# antipodal identity check on random profiles: needle octagons using only rays 0 and pi = octagons of B u -B?
# (we only check the implication "B u -B has an octagon => needle has an octagon")
bad = 0
for _ in range(100):
    n = random.randint(4, 8)
    B = [(r, random.randint(-50, 50)) for r in random.sample(range(1, 80), n)]
    a = planar_n8(B + [(-x, -y) for (x, y) in B]); b = n8(B)
    if a is None or b is None:
        continue
    if a > 0 and b == 0:
        bad += 1
print('implication check (B u -B octagon => needle octagon): violations', bad, flush=True)
t0 = time.time()
best_n = 0
for n in range(4, NMAX + 1):
    found = None
    deadline = time.time() + T
    while time.time() < deadline and found is None:
        B = [(r, random.randint(-1000, 1000)) for r in sorted(random.sample(range(1, 4000), n))]
        v = n8(B)
        if v is None:
            continue
        for it in range(400):
            if v == 0:
                break
            j = random.randrange(n)
            r, y = B[j]
            C = list(B)
            if random.random() < 0.5:
                C[j] = (r, y + random.randint(-300, 300))
            else:
                nr = max(1, r + random.randint(-300, 300))
                if nr in [q[0] for q in C]:
                    continue
                C[j] = (nr, y)
            w = n8(C)
            if w is not None and w <= v:
                B, v = C, w
        if v == 0:
            found = B
    if found is None:
        print('n=%d: no octagon-free 4-fold needle found in %.0fs' % (n, T), flush=True)
        break
    cu, ca = cupcap(found)
    best_n = n
    print('n=%d: octagon-free 4-fold needle found, cup %d cap %d, profile %s (%.0fs)' % (n, cu, ca, sorted(found),
          time.time() - t0), flush=True)
print('DONE largest n found:', best_n, flush=True)
