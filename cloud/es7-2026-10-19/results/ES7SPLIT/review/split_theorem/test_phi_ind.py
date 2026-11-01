#!/usr/bin/env python3
"""Independent exact test of Lemma 0 (finite z): phi(p) = (-u.(p-z)/w(p), -1/w(p)), w = n.(p-z), u = (-n_y, n_x),
for ANY n with n.(x - z) > 0 on X.  Checks for all points/triples of X:
 (b) sgn orient(phi p, phi q, phi r) = sgn orient(p, q, r)
 (c) p <_z q  iff  x(phi p) < x(phi q), and ties <-> ties (we also plant ties: points collinear with z)
 (d) for z not on pr, q not on pr: q in H_z(pr) iff phi(q) strictly below line phi(p)phi(r), which is non-vertical
 and: z-caps / z-cups of X map exactly to caps / cups (x-sorted) of phi(X); convex position preserved.
Also the direction case (rotation taking d to (0,-1)) is checked with an exact rational rotation-like map:
we use the orientation-preserving linear map sending d to (0, -|d|^2)-multiple (a rotation composed with scaling).
"""
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from igeom import orient, sgn, orient_h, on_z_side, on_far_side, general_position, is_z_cap, is_z_cup, in_convex_position


def phi_finite(p, z, n):
    u = (-n[1], n[0])
    w = n[0] * (p[0] - z[0]) + n[1] * (p[1] - z[1])
    assert w > 0
    uv = u[0] * (p[0] - z[0]) + u[1] * (p[1] - z[1])
    return (Fraction(-uv, w), Fraction(-1, w))


def phi_dir(p, d):
    # linear map L with L d = (0, -(dx^2+dy^2)), det L > 0: L = [[-dy, dx], [-dx, -dy]]; det = dy^2 + dx^2 > 0
    return (-d[1] * p[0] + d[0] * p[1], -d[0] * p[0] - d[1] * p[1])


def is_cap_x(Q):
    Q = sorted(Q)
    return all(orient(Q[i], Q[k], Q[j]) > 0 for i, j, k in combinations(range(len(Q)), 3))  # Q_j above chord


def is_cup_x(Q):
    Q = sorted(Q)
    return all(orient(Q[i], Q[k], Q[j]) < 0 for i, j, k in combinations(range(len(Q)), 3))


def below(q, p, r):
    """q strictly below non-vertical line pr."""
    if p[0] > r[0]:
        p, r = r, p
    return orient(p, r, q) < 0


def trial(rng, kind):
    viol = dict(orient=0, order=0, side=0, vertical=0, capcup=0, convex=0)
    if kind == 'F':
        z = (rng.randint(-50, 50), rng.randint(-50, 50))
        while True:
            n = (rng.randint(-9, 9), rng.randint(-9, 9))
            if n != (0, 0):
                break
        X = []
        while len(X) < 7:
            p = (rng.randint(-200, 200), rng.randint(-200, 200))
            w = n[0] * (p[0] - z[0]) + n[1] * (p[1] - z[1])
            if w <= 0 or p in X:
                continue
            if any(orient(a, b, p) == 0 for a, b in combinations(X, 2)):
                continue
            X.append(p)
        # plant a tie with probability 1/3: replace last point by one collinear with z and X[0] (if still valid)
        if rng.random() < 1 / 3:
            t = rng.randint(2, 4)
            p = (z[0] + t * (X[0][0] - z[0]), z[1] + t * (X[0][1] - z[1]))
            cand = X[:-1] + [p]
            if general_position(cand):
                X = cand
        img = {p: phi_finite(p, z, n) for p in X}
        zz = ('F', z)
    else:
        while True:
            d = (rng.randint(-9, 9), rng.randint(-9, 9))
            if d != (0, 0):
                break
        X = []
        while len(X) < 7:
            p = (rng.randint(-200, 200), rng.randint(-200, 200))
            if p in X or any(orient(a, b, p) == 0 for a, b in combinations(X, 2)):
                continue
            X.append(p)
        img = {p: phi_dir(p, d) for p in X}
        zz = ('D', d)
    for p, q, r in combinations(X, 3):
        if sgn(orient(img[p], img[q], img[r])) != sgn(orient(p, q, r)):
            viol['orient'] += 1
    for p in X:
        for q in X:
            if p == q:
                continue
            oh = orient_h(p, q, zz)
            lhs = oh < 0
            rhs = img[p][0] < img[q][0]
            if lhs != rhs or ((oh == 0) != (img[p][0] == img[q][0])):
                viol['order'] += 1
    for p, r in combinations(X, 2):
        if orient_h(p, r, zz) == 0:
            continue
        if img[p][0] == img[r][0]:
            viol['vertical'] += 1
            continue
        for q in X:
            if q in (p, r):
                continue
            if on_z_side(q, p, r, zz) != below(img[q], img[p], img[r]):
                viol['side'] += 1
    # caps/cups and convex position for every subset (only meaningful where z-order strict on the subset)
    for k in range(3, len(X) + 1):
        for Q in combinations(X, k):
            if any(orient_h(a, b, zz) == 0 for a, b in combinations(Q, 2)):
                continue
            IQ = [img[q] for q in Q]
            if is_z_cap(Q, zz) != is_cap_x(IQ) or is_z_cup(Q, zz) != is_cup_x(IQ):
                viol['capcup'] += 1
            if in_convex_position(Q) != in_convex_position(IQ):
                viol['convex'] += 1
    return viol


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    tot = {}
    for t in range(trials):
        v = trial(rng, 'F' if t % 4 else 'D')
        for k, x in v.items():
            tot[k] = tot.get(k, 0) + x
    print(dict(trials=trials, violations=tot))


if __name__ == '__main__':
    main()
