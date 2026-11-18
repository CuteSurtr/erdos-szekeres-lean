#!/usr/bin/env python3
"""cubes.py -- structural cubes for the signotope ETV instances (see README section 3).

Upper-hull cubes.  For a real point set p_0..p_{n-1} (sorted by x, general position) the upper
convex hull is a cap  0 = h_0 < h_1 < ... < h_m = n-1  and every other point lies strictly below
the line through each hull edge.  With no (A+1)-cap, m+1 <= A.  The cube of the hull H asserts,
as orientation literals (O true = cup triple, i.e. the middle point is BELOW the chord):
  (a) for every hull edge (u,v) and every non-hull point x:
        u < x < v :  O(u,x,v) = +   (x below the segment uv)
        x < u     :  O(x,u,v) = -   (x below the line uv on its left extension: x,u,v is a cap)
        x > v     :  O(u,v,x) = -   (x below the line on the right extension: u,v,x is a cap)
  (b) for every hull edge (u,v) and every other hull vertex w: the same literals (w is below the
      line uv as well, the hull being a strictly convex chain); in particular consecutive hull
      triples are caps.
Every real point set satisfies exactly one hull cube.

Mirror reduction: the mirror image x -> -x of a set with hull (0,h_1,..,h_{m-1},n-1) has hull
(0, n-1-h_{m-1}, .., n-1-h_1, n-1), and mirroring preserves caps, cups and convex position.  So
it suffices to refute the cubes whose interior hull tuple is lexicographically <= its mirror
tuple.  For self-mirror hulls the extra symmetry clause  O(0,1,2) -> O(n-3,n-2,n-1)  may be
added (the mirror image stays in the same cube).
"""
import itertools, json, sys


def hull_units(n, H):
    """orientation literals (sign, (i,j,k)) of the hull cube H (tuple incl. 0 and n-1)."""
    lits = {}
    Hs = set(H)

    def put(t, s):
        assert t[0] < t[1] < t[2]
        if t in lits:
            assert lits[t] == s, (t, s)
        lits[t] = s
    for u, v in zip(H, H[1:]):
        for x in range(n):
            if x == u or x == v:
                continue
            if u < x < v:
                assert x not in Hs
                put((u, x, v), +1)
            elif x < u:
                put((x, u, v), -1)
            else:
                put((u, v, x), -1)
    return sorted((t, s) for t, s in lits.items())


def all_hulls(n, A):
    """all upper hulls with at most A vertices (interior tuples), as tuples incl. endpoints"""
    out = []
    for m in range(0, A - 1):          # m interior hull vertices, m+2 <= A
        for c in itertools.combinations(range(1, n - 1), m):
            out.append((0,) + c + (n - 1,))
    return out


def mirror_hull(n, H):
    return tuple(sorted(n - 1 - h for h in H))


def reduced_hulls(n, A):
    """hull cubes up to mirror: keep H with interior(H) <= interior(mirror(H)) lexicographically.
    returns list of (H, selfmirror)"""
    out = []
    for H in all_hulls(n, A):
        M = mirror_hull(n, H)
        if H <= M:
            out.append((H, H == M))
    return out


def check_cover(n, A):
    """script check: every hull is in the reduced list or its mirror is."""
    red = {H for H, _ in reduced_hulls(n, A)}
    allh = all_hulls(n, A)
    assert len(set(allh)) == len(allh)
    for H in allh:
        assert H in red or mirror_hull(n, H) in red
    for H, sm in reduced_hulls(n, A):
        assert (mirror_hull(n, H) == H) == sm
    return len(allh), len(red)


if __name__ == '__main__':
    n, A = int(sys.argv[1]), int(sys.argv[2])
    print(check_cover(n, A))
    for H, sm in reduced_hulls(n, A)[:5]:
        print(H, sm, len(hull_units(n, H)))
