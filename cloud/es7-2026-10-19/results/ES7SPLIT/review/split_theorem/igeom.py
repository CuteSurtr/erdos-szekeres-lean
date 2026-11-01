"""Independent exact geometry for checking the split theorem (Theorem 5 of proofs/split_theorem.md).

Written from scratch (imports nothing from tools/ of this result).  All arithmetic is exact (int / Fraction).

A "point outside S" z is encoded as ('F', (zx, zy)) (finite) or ('D', (dx, dy)) (direction / point at infinity).
"""
from fractions import Fraction
from functools import cmp_to_key
from itertools import combinations


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(x):
    return (x > 0) - (x < 0)


def orient_h(a, b, z):
    kind, v = z
    if kind == 'F':
        return orient(a, b, v)
    return (b[0] - a[0]) * v[1] - (b[1] - a[1]) * v[0]


def on_z_side(q, a, b, z):
    """q in the OPEN half-plane of line ab that contains z (z not on ab)."""
    s, t = sgn(orient(a, b, q)), sgn(orient_h(a, b, z))
    return s != 0 and s == t


def on_far_side(q, a, b, z):
    """q in the OPEN half-plane of line ab NOT containing z (z not on ab)."""
    s, t = sgn(orient(a, b, q)), sgn(orient_h(a, b, z))
    return s != 0 and t != 0 and s == -t


def general_position(P):
    return all(orient(a, b, c) != 0 for a, b, c in combinations(P, 3))


def z_sorted(Q, z):
    def cmp(p, q):
        o = orient_h(p, q, z)
        if o == 0:
            raise ValueError("z on line pq: z-order not strict")
        return -1 if o < 0 else 1  # p <_z q iff orient_h(p,q,z) < 0
    return sorted(Q, key=cmp_to_key(cmp))


def z_order_is_total_and_transitive(Q, z):
    """Check that <_z is a strict total order on Q (antisymmetric, transitive) by brute force."""
    for p, q in combinations(Q, 2):
        if orient_h(p, q, z) == 0:
            return False
    for p in Q:
        for q in Q:
            for r in Q:
                if len({p, q, r}) == 3 and orient_h(p, q, z) < 0 and orient_h(q, r, z) < 0 and not orient_h(p, r, z) < 0:
                    return False
    return True


def is_z_cap(Q, z):
    Q = z_sorted(list(Q), z)
    return all(on_far_side(Q[j], Q[i], Q[k], z) for i, j, k in combinations(range(len(Q)), 3))


def is_z_cup(Q, z):
    Q = z_sorted(list(Q), z)
    return all(on_z_side(Q[j], Q[i], Q[k], z) for i, j, k in combinations(range(len(Q)), 3))


def in_triangle(p, a, b, c):
    o = sgn(orient(a, b, c))
    return o != 0 and sgn(orient(a, b, p)) == o and sgn(orient(b, c, p)) == o and sgn(orient(c, a, p)) == o


def convex_quads(P):
    """dict frozenset(index quadruple) -> bool convex (general position assumed)."""
    out = {}
    for quad in combinations(range(len(P)), 4):
        conv = True
        for t in range(4):
            p = P[quad[t]]
            a, b, c = [P[quad[s]] for s in range(4) if s != t]
            if in_triangle(p, a, b, c):
                conv = False
                break
        out[quad] = conv
    return out


def in_convex_position_idx(idx, quads):
    return all(quads[q] for q in combinations(sorted(idx), 4))


def in_convex_position(Q):
    Q = list(Q)
    for i, p in enumerate(Q):
        others = Q[:i] + Q[i + 1:]
        for a, b, c in combinations(others, 3):
            if in_triangle(p, a, b, c):
                return False
    return True


def is_z_split(A, B, z):
    """Definition 1 (S1), (S2); plus z outside conv(S) for finite z is checked separately."""
    for a, a2 in combinations(A, 2):
        for b in B:
            if not on_z_side(b, a, a2, z):
                return False
    for b, b2 in combinations(B, 2):
        for a in A:
            if not on_far_side(a, b, b2, z):
                return False
    return True


def finite_z_outside_hull(S, zpt):
    """z strictly outside conv(S) iff z is not in any closed triangle of S and not on a segment of S
    (S in general position, |S| >= 3).  Exact."""
    S = list(S)
    for a, b, c in combinations(S, 3):
        o = sgn(orient(a, b, c))
        s1, s2, s3 = sgn(orient(a, b, zpt)), sgn(orient(b, c, zpt)), sgn(orient(c, a, zpt))
        if all(s in (0, o) for s in (s1, s2, s3)):
            return False
    for a, b in combinations(S, 2):
        if orient(a, b, zpt) == 0:
            # on line ab: inside segment?
            if min(a[0], b[0]) <= zpt[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= zpt[1] <= max(a[1], b[1]):
                return False
    return True
