#!/usr/bin/env python3
"""Find all nontrivial z-splits of a point set (exact one-sidedness tests + LP for z).

Definition (see proofs/split_theorem.md).  A partition S = A u B is a z-split, for a point z of the
projective plane outside conv(S) (a finite point outside the hull, or a point at infinity given by a
direction), if
  (1) for all distinct a, a' in A, every b in B lies strictly on the same side of line aa' as z, and
  (2) for all distinct b, b' in B, every a in A lies strictly on the opposite side of line bb' from z.
(For z the downward point at infinity this says: B lies below every line spanned by A and A lies
above every line spanned by B, i.e. B is "deep below" A.)

Algorithm.  A and B are separated by a line (proof in split_theorem.md), so we enumerate all linear
partitions (lines through two points, 4 assignments of those two points), keep those with
|A|, |B| >= 2 that pass the exact one-sidedness tests, and decide the existence of z by a linear
program in homogeneous coordinates zh = (z1, z2, z3), z3 >= 0, with all strict inequalities written
as >= 1 (they are homogeneous, so this is equivalent), plus "z beyond hull edge e" for each hull edge e.
The LP solution is then re-verified with exact rational arithmetic.
"""
import sys
from fractions import Fraction
from itertools import combinations
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from geom import read_points, orient, sgn, hull, orient_h, longest_z_chains, largest_convex_subset


def linear_partitions(P):
    n = len(P)
    seen = set()
    out = []
    for i, j in combinations(range(n), 2):
        L = [k for k in range(n) if k not in (i, j) and orient(P[i], P[j], P[k]) > 0]
        R = [k for k in range(n) if k not in (i, j) and orient(P[i], P[j], P[k]) < 0]
        for X in (L + [i], L + [j], L + [i, j], L):
            X = frozenset(X)
            Y = frozenset(range(n)) - X
            if len(X) < 2 or len(Y) < 2:
                continue
            for A, B in ((X, Y), (Y, X)):  # both roles: A above B and B above A
                if (A, B) in seen:
                    continue
                seen.add((A, B))
                out.append((A, B))
    return out


def side_vector(P, X, Y):
    """For each pair x, x' in X: the common sign of orient(x, x', y) over y in Y, or None if Y is split."""
    res = {}
    for a, b in combinations(sorted(X), 2):
        s = None
        for c in Y:
            o = sgn(orient(P[a], P[b], P[c]))
            if s is None:
                s = o
            elif o != s:
                return None
        res[(a, b)] = s
    return res


def find_z(P, A, B):
    """Return an exact homogeneous z (tuple of Fractions) making (A, B) a z-split, or None."""
    sA = side_vector(P, A, B)
    if sA is None:
        return None
    sB = side_vector(P, B, A)
    if sB is None:
        return None
    rows = []  # each row r: require r . zh >= 1
    for (a, b), s in sA.items():
        # z on the same side as B:  s * orient_h(Pa, Pb, z) > 0
        pa, pb = P[a], P[b]
        coef = (pb[1] - pa[1], -(pb[0] - pa[0]), pa[0] * pb[1] - pa[1] * pb[0])
        # orient_h(a, b, z) = z1*(by - ay)... derive: det[[ax,ay,1],[bx,by,1],[z1,z2,z3]]
        #   = z1*(ay - by) - z2*(ax - bx) + z3*(ax*by - ay*bx)
        coef = (pa[1] - pb[1], pb[0] - pa[0], pa[0] * pb[1] - pa[1] * pb[0])
        rows.append(tuple(s * c for c in coef))
    for (a, b), s in sB.items():
        # z on the side opposite to A: -s * orient_h(Pa, Pb, z) > 0
        pa, pb = P[a], P[b]
        coef = (pa[1] - pb[1], pb[0] - pa[0], pa[0] * pb[1] - pa[1] * pb[0])
        rows.append(tuple(-s * c for c in coef))
    H = hull(P)
    for e in range(len(H)):
        h0, h1 = H[e], H[(e + 1) % len(H)]
        coef = (h0[1] - h1[1], h1[0] - h0[0], h0[0] * h1[1] - h0[1] * h1[0])
        # z strictly beyond edge e (outside):  orient_h(h0, h1, z) < 0  ->  -coef . z >= 1
        allrows = rows + [tuple(-c for c in coef)]
        Aub = -np.array(allrows, dtype=float)
        # normalise rows for numerical stability
        norms = np.linalg.norm(Aub, axis=1)
        Aub_n = Aub / norms[:, None]
        bub = -np.ones(len(allrows)) / norms
        res = linprog(c=[0, 0, 0], A_ub=Aub_n, b_ub=bub, bounds=[(None, None), (None, None), (0, None)],
                      method="highs")
        if res.status == 0:
            z = res.x
            # exact re-verification with rationals (round to a fine grid, then check)
            for scale in (10 ** 6, 10 ** 9, 10 ** 12):
                zq = tuple(Fraction(round(v * scale)) for v in z)
                if zq[2] < 0:
                    continue
                if all(sum(Fraction(r[i]) * zq[i] for i in range(3)) > 0 for r in allrows):
                    return zq
            # LP said feasible but rounding failed: report as numeric-only
            return ("numeric", tuple(z))
    return None


def all_splits(P):
    out = []
    for A, B in linear_partitions(P):
        z = find_z(P, A, B)
        if z is not None:
            out.append((A, B, z))
    return out


def describe(P, A, B, z):
    PA = [P[i] for i in sorted(A)]
    PB = [P[i] for i in sorted(B)]
    if isinstance(z, tuple) and z and z[0] == "numeric":
        return dict(sizes=(len(A), len(B)), z="numeric-only", note="exact verification failed")
    capA, cupA = longest_z_chains(PA, z)
    capB, cupB = longest_z_chains(PB, z)
    return dict(sizes=(len(A), len(B)), z=tuple(str(v) for v in z), z_at_infinity=(z[2] == 0),
                capA=capA, cupB=cupB, c_plus_d=capA + cupB,
                gonA=largest_convex_subset(PA), gonB=largest_convex_subset(PB))


if __name__ == "__main__":
    P = read_points(sys.argv[1])
    S = all_splits(P)
    print(f"{sys.argv[1]}: {len(P)} points, {len(S)} nontrivial z-splits")
    for A, B, z in S:
        print(describe(P, A, B, z))
