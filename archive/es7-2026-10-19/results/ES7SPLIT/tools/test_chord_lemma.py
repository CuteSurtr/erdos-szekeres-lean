#!/usr/bin/env python3
"""Sanity test of the hexagon chord lemma (proofs/hexagon_chord_lemma.md) on random convex hexagons
of a point set.  For a convex hexagon H = h_0..h_5 (ccw), i and m in {1,2,3}: a = h_i, b = h_{i+m+1},
region R(i,m) = points strictly on the dropped side of line ab, strictly left of the directed lines
h_{i-1} -> h_i and h_{i+m+1} -> h_{i+m+2}.  Lemma: if gon(S) <= 6, no m+1 points of S n R(i,m) are in
convex position together with a and b.  We report the maximum such chain length found (must be <= m)
and, as a control, the same statistic on a random set that does contain 7-gons."""
import random
import sys
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from geom import read_points, orient, in_convex_position, hull, general_position, largest_convex_subset


def convex_hexagons_sample(P, k, rng, tries=200000):
    out = []
    n = len(P)
    seen = set()
    for _ in range(tries):
        if len(out) >= k:
            break
        T = tuple(sorted(rng.sample(range(n), 6)))
        if T in seen:
            continue
        seen.add(T)
        Q = [P[i] for i in T]
        if in_convex_position(Q):
            out.append(hull(Q))  # ccw order
    return out


def max_chain(P, H, i, m):
    a, b = H[i], H[(i + m + 1) % 6]
    hm1, hb1 = H[(i - 1) % 6], H[(i + m + 2) % 6]
    dropped = H[(i + 1) % 6]
    side = orient(a, b, dropped)
    R = [p for p in P if p not in (a, b) and orient(a, b, p) * side > 0
         and orient(hm1, a, p) > 0 and orient(b, hb1, p) > 0]
    best = 0
    for r in range(1, min(len(R), m + 2) + 1):
        found = False
        for Q in combinations(R, r):
            if in_convex_position(list(Q) + [a, b]):
                found = True
                break
        if found:
            best = r
        else:
            break
    return best, len(R)


def run(P, nhex, rng):
    worst = {1: 0, 2: 0, 3: 0}
    sizes = {1: 0, 2: 0, 3: 0}
    hexes = convex_hexagons_sample(P, nhex, rng)
    for H in hexes:
        for i in range(6):
            for m in (1, 2, 3):
                c, s = max_chain(P, H, i, m)
                worst[m] = max(worst[m], c)
                sizes[m] = max(sizes[m], s)
    return len(hexes), worst, sizes


if __name__ == "__main__":
    rng = random.Random(5)
    for fn in sys.argv[1:]:
        P = read_points(fn)
        nh, worst, sizes = run(P, 150, rng)
        print(fn.rsplit('/', 1)[-1], "hexagons tested", nh, "max chain per m (must be <= m):", worst,
              "max region size:", sizes)
    # control: random set with 7-gons
    while True:
        Pc = [(rng.randint(0, 1000), rng.randint(0, 1000)) for _ in range(24)]
        if general_position(Pc) and largest_convex_subset(Pc) >= 7:
            break
    nh, worst, sizes = run(Pc, 150, rng)
    print("control random 24-set with gon", largest_convex_subset(Pc), ": hexagons", nh, "max chain per m:", worst)
