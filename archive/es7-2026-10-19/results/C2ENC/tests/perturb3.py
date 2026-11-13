"""Exact illustration of the centre-perturbation lemma (perturbation.md) for m = 3.

Coordinates: Eisenstein basis, a point is a + b*w with w = exp(2 pi i/3), stored as the rational pair (a, b); the
centre is 0.  The map (a, b) -> (a - b/2, b*sqrt(3)/2) to Euclidean coordinates is linear with determinant
sqrt(3)/2 > 0, so every orientation sign can be computed from (a, b) directly, exactly, with Fractions.
The rotation R is multiplication by w: (a, b) -> (-b, a - b).  The perturbation multiplies orbit j by
lam_j = 1 + eta_j * w (a rotation-scaling close to the identity, commuting with R):
  (a + b w)(1 + eta w) = (a - b eta) + (a eta + b - b eta) w.
For each test set (3 orbits share a ray from the centre, so pairs collinear with c exist before the perturbation):
  check exactly that the perturbed set is R-invariant, that every orientation sign of the points is unchanged, that no
  two points are collinear with the centre afterwards, and that the number of convex k-subsets is unchanged.
"""
import itertools
import random
import sys
from fractions import Fraction as F


def rot(p):
    a, b = p
    return (-b, a - b)


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(x):
    return (x > 0) - (x < 0)


def mul(p, eta):
    a, b = p
    return (a - b * eta, a * eta + b - b * eta)


def orbit(p):
    return [p, rot(p), rot(rot(p))]


def convex_count(P, k):
    n = len(P)
    cnt = 0
    for Q in itertools.combinations(range(n), k):
        pts = [P[i] for i in Q]
        ok = True
        for i in range(k):
            for a, b, d in itertools.combinations([x for x in range(k) if x != i], 3):
                s1, s2, s3 = sgn(orient(pts[a], pts[b], pts[i])), sgn(orient(pts[b], pts[d], pts[i])), \
                    sgn(orient(pts[d], pts[a], pts[i]))
                if s1 == s2 == s3 != 0:
                    ok = False
                    break
            if not ok:
                break
        cnt += ok
    return cnt


def main():
    rng = random.Random(3)
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    done = 0
    while done < trials:
        reps = []
        for _ in range(rng.randint(1, 2)):            # pairs of orbits whose representatives lie on one ray from c
            base = (rng.randint(-40, 40), rng.randint(-40, 40))
            k = rng.choice([2, 3, -2, -3])
            reps += [base, (k * base[0], k * base[1])]
        reps += [(rng.randint(-60, 60), rng.randint(-60, 60)) for _ in range(rng.randint(1, 2))]
        if (0, 0) in reps:
            continue
        P = [q for r in reps for q in orbit(r)]
        if len(set(P)) != len(P) or (0, 0) in P:
            continue
        if any(orient(*T) == 0 for T in itertools.combinations(P, 3)):
            continue                                  # S itself must be in general position
        before = sum(1 for x, y in itertools.combinations(P, 2) if orient((0, 0), x, y) == 0)
        assert before > 0
        # perturb: orbit j multiplied by 1 + eta_j w, eta_j = j * eta; halve eta until all checks hold
        eta = F(1, 50)
        for _ in range(40):
            Pt = [mul(q, (j // 3 + 1) * eta) for j, q in enumerate(P)]
            inv = set(map(rot, Pt)) == set(Pt)
            same = all(sgn(orient(*[Pt[i] for i in T])) == sgn(orient(*[P[i] for i in T]))
                       for T in itertools.combinations(range(len(P)), 3))
            after = sum(1 for x, y in itertools.combinations(Pt, 2) if orient((0, 0), x, y) == 0)
            if inv and same and after == 0:
                break
            eta /= 2
        else:
            print("FAILED to find a perturbation", reps)
            return
        k = 5 if len(P) <= 12 else 6
        c0, c1 = convex_count(P, k), convex_count(Pt, k)
        assert c0 == c1
        done += 1
        print(f"set {done}: {len(P)} points, {before} pairs collinear with c before, 0 after; eta = {eta}; "
              f"R-invariant {inv}; all {len(P) * (len(P) - 1) * (len(P) - 2) // 6} orientation signs unchanged; "
              f"convex {k}-subsets {c0} -> {c1}")
    print(f"PERTURBATION CHECK PASSED on {done} sets")


if __name__ == "__main__":
    main()
