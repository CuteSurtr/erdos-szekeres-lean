#!/usr/bin/env python3
"""Randomized exact tests of the split lemma (proofs/split_theorem.md, Lemmas 2-3 and Corollary 4):

For a z-split S = A u B (|A|, |B| >= 1) and P subset of S in convex position meeting both parts,
P n A is a z-cap and P n B is a z-cup; conversely (z-cap in A) u (z-cup in B) is in convex position.
Hence  gon(S) = max(gon(A), gon(B), cap_z(A) + cup_z(B)).

Construction: A random integer points; B random points flattened and placed far below (z = down);
then optionally an exact random projective map (line at infinity avoiding conv(S)) so that z becomes a
finite point.  We check (a) the split conditions exactly, (b) the subset statements by brute force over
all subsets (small sizes), (c) the gon formula, (d) that splits.find_z recovers a z for (A, B).
"""
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from geom import orient, sgn, general_position, in_convex_position, longest_z_chains, orient_h, z_sorted, \
    z_same_side, largest_convex_subset
import splits


def is_z_cap(Q, z):
    Q = z_sorted(Q, z)
    return all(not z_same_side(Q[i], Q[i + 2], Q[i + 1], z) for i in range(len(Q) - 2)) and \
        all(not z_same_side(Q[i], Q[k], Q[j], z) for i, j, k in combinations(range(len(Q)), 3))


def is_z_cup(Q, z):
    Q = z_sorted(Q, z)
    return all(z_same_side(Q[i], Q[k], Q[j], z) for i, j, k in combinations(range(len(Q)), 3))


def split_ok(A, B, z):
    for a, a2 in combinations(A, 2):
        for b in B:
            if not (sgn(orient(a, a2, b)) == sgn(orient_h(a, a2, z)) != 0):
                return False
    for b, b2 in combinations(B, 2):
        for a in A:
            if not (sgn(orient(b, b2, a)) == -sgn(orient_h(b, b2, z)) != 0):
                return False
    return True


def proj(p, M):
    """Exact projective map p -> (M p~) with homogeneous normalisation; M is 3x3 integer."""
    x, y = p
    u = M[0][0] * x + M[0][1] * y + M[0][2]
    v = M[1][0] * x + M[1][1] * y + M[1][2]
    w = M[2][0] * x + M[2][1] * y + M[2][2]
    return (Fraction(u, w), Fraction(v, w))


def proj_h(z, M):
    z1, z2, z3 = z
    return tuple(M[i][0] * z1 + M[i][1] * z2 + M[i][2] * z3 for i in range(3))


def to_int(points):
    """Scale rational points to integers (common denominator); affine scaling keeps everything."""
    from math import lcm
    den = 1
    for p in points:
        for c in p:
            den = lcm(den, c.denominator)
    return [(int(p[0] * den), int(p[1] * den)) for p in points], den


def trial(rng, nA, nB, projective):
    while True:
        A = [(rng.randint(0, 60), rng.randint(0, 60)) for _ in range(nA)]
        if len(set(A)) == nA and len({p[0] for p in A}) == nA and general_position(A):
            break
    while True:
        Bs = [(rng.randint(0, 600), rng.randint(0, 6)) for _ in range(nB)]
        if len(set(Bs)) == nB and len({p[0] for p in Bs}) == nB and general_position(Bs):
            break
    M0 = 10 ** 7
    B = [(x - 270, y - M0) for x, y in Bs]
    z = (0, -1, 0)
    S = A + B
    if not general_position(S):
        return None
    assert split_ok(A, B, z), "construction failed"
    if projective:
        # random projective map whose line at infinity w = 0 avoids conv(S): w = c1 x + c2 y + c3 > 0 on S
        c1, c2 = rng.randint(-3, 3), rng.randint(-3, 3)
        c3 = 1 + max(-(c1 * x + c2 * y) for x, y in S) + rng.randint(0, 10 ** 7)
        M = [[rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-50, 50)],
             [rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-50, 50)],
             [c1, c2, c3]]
        det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
               + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        if det == 0:
            return None
        SA = [proj(p, M) for p in A]
        SB = [proj(p, M) for p in B]
        allp, den = to_int(SA + SB)
        A, B = allp[:nA], allp[nA:]
        zh = proj_h(z, M)  # image of the downward point at infinity
        # homogeneous point: scale by den in the affine part: (z1/z3*den, z2/z3*den) -> (z1*den, z2*den, z3)
        swapped = False
        if zh[2] < 0:
            # the downward ray from S crosses the new line at infinity: in the new chart the side
            # relations with respect to z flip, so (B, A) is the expected split
            zh = tuple(-c for c in zh)
            swapped = True
        z = (zh[0] * den, zh[1] * den, zh[2])
        if z[2] == 0:
            # still at infinity; fine (direction)
            pass
        if swapped:
            A, B, nA, nB = B, A, nB, nA
        S = A + B
        if not general_position(S):
            return None
        if not split_ok(A, B, z):
            return ("not-split-after-map", None)
    # (b) brute-force subset statements
    n = len(S)
    idxA = set(range(nA))
    bad = 0
    gon = 0
    for r in range(3, n + 1):
        for T in combinations(range(n), r):
            Q = [S[i] for i in T]
            if in_convex_position(Q):
                gon = max(gon, r)
                QA = [S[i] for i in T if i in idxA]
                QB = [S[i] for i in T if i not in idxA]
                if QA and QB and not (is_z_cap(QA, z) and is_z_cup(QB, z)):
                    bad += 1
    capA, _ = longest_z_chains(A, z)
    _, cupB = longest_z_chains(B, z)
    formula = max(largest_convex_subset(A), largest_convex_subset(B), capA + cupB)
    # converse: every z-cap of A union every z-cup of B is convex (check maximal ones by brute force on small sets)
    conv_bad = 0
    capsA = [C for r in range(1, nA + 1) for C in combinations(A, r) if r <= 2 or is_z_cap(list(C), z)]
    cupsB = [D for r in range(1, nB + 1) for D in combinations(B, r) if r <= 2 or is_z_cup(list(D), z)]
    for C in capsA:
        for D in cupsB:
            if len(C) + len(D) >= 4 and not in_convex_position(list(C) + list(D)):
                conv_bad += 1
    # (d) finder
    zf = splits.find_z(S, frozenset(range(nA)), frozenset(range(nA, n)))
    return dict(bad=bad, conv_bad=conv_bad, gon=gon, formula=formula, found=zf is not None,
                z_infinite=(z[2] == 0))


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    stats = dict(trials=0, bad=0, conv_bad=0, formula_mismatch=0, not_found=0, projective=0, skipped=0)
    for t in range(trials):
        nA, nB = rng.randint(2, 6), rng.randint(2, 6)
        r = trial(rng, nA, nB, projective=(t % 2 == 1))
        if r is None:
            stats["skipped"] += 1
            continue
        if isinstance(r, tuple):
            stats["not_split_after_map"] = stats.get("not_split_after_map", 0) + 1
            continue
        stats["trials"] += 1
        stats["projective"] += (t % 2 == 1)
        stats["bad"] += r["bad"]
        stats["conv_bad"] += r["conv_bad"]
        stats["formula_mismatch"] += (r["gon"] != r["formula"])
        stats["not_found"] += (not r["found"])
    print(stats)


if __name__ == "__main__":
    main()
