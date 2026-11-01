#!/usr/bin/env python3
"""Hull-related statistics for a 7-gon-free set (exact arithmetic).

For each hull vertex v_i (ccw order), with neighbours v_{i-1}, v_{i+1}:
  ear_i   = points strictly inside triangle v_{i-1} v_i v_{i+1}  (beyond the short chord)
  nested  = whether the ear points are pairwise nested (one inside the triangle of the chord and the other)
For every chord v_a v_b of the hull (a != b, not adjacent) we compute the longest convex chain from v_a to
v_b through points strictly beyond the chord (on the side of the dropped hull vertices) that is convex
together with the kept hull vertices, and report the slack  7 - (kept + chain)  (must be >= 1 for a
7-gon-free set; this is only a sanity check of the bookkeeping, since it is implied by 7-gon-freeness).
Also: for each hull vertex v, the longest cap / cup of S \\ {v} in the v-frame (z = v): Toth-Valtr say
no 6-cap.  And: is every point a vertex of some convex hexagon of S?
"""
import sys
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from geom import read_points, orient, sgn, hull, layers, inside_triangle, longest_z_chains, largest_convex_subset


def ears(P, H):
    h = len(H)
    out = []
    for i in range(h):
        a, v, b = H[i - 1], H[i], H[(i + 1) % h]
        E = [p for p in P if p not in (a, v, b) and inside_triangle(p, a, v, b)]
        nested = True
        for p, q in combinations(E, 2):
            if not (inside_triangle(p, a, q, b) or inside_triangle(q, a, p, b)):
                nested = False
        out.append((len(E), nested))
    return out


def vertex_frame_chains(P, H):
    res = []
    for v in H:
        Q = [p for p in P if p != v]
        z = (v[0], v[1], 1)
        cap, cup = longest_z_chains(Q, z)
        res.append((cap, cup))
    return res


def hexagon_membership(P):
    """For each point, is it a vertex of a convex 6-subset?  (brute force over 6-subsets containing it,
    pruned: uses the convex-position DP restricted to subsets is too slow, so we test 'largest convex
    subset through p' via the anchored DP.)"""
    from functools import cmp_to_key
    res = []
    for p in P:
        # largest convex polygon having p as its lowest vertex OR containing p: use the trick of
        # rotating: we compute, for each candidate lowest vertex q, chains through p.  Simpler: brute
        # force over 5-subsets of the others is C(31,5)=169911 per point - acceptable in C, slow in Python.
        res.append(None)
    return res


def main():
    P = read_points(sys.argv[1])
    H = hull(P)
    L = layers(P)
    print("points", len(P), "hull", len(H), "layers", [len(x) for x in L])
    print("ears (count, nested):", ears(P, H))
    print("v-frame (cap, cup) of S\\{v} for hull vertices:", vertex_frame_chains(P, H))


if __name__ == "__main__":
    main()
