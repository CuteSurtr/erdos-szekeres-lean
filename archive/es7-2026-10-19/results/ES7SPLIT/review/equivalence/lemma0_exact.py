#!/usr/bin/env python3
"""Independent exact test of Lemma 0 (finite z) of split_theorem.md.
phi(p) = ( -u.(p-z)/w(p), -1/w(p) ),  w(p) = n.(p-z) > 0 on X,  u = (-n_y, n_x).
Checks for random X and random z outside conv(X) (including z on lines through two
points of X):
 (b) sign of orientation preserved;
 (c) orient(z,p,q) < 0  <=>  x(phi p) < x(phi q), ties <=> ties;
 (d) for z not on pr: line phi(p)phi(r) is non-vertical and q in H_z(pr) <=> phi(q) below it;
 and: for every bipartition, (A,B) is a z-split <=> phi(B) below all phi(A)-lines and
      phi(A) above all phi(B)-lines (the 'final sentence' of Lemma 0), whenever z is on no
      line through two points of X.
"""
import itertools, os, random, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from direct_lemmas import orient, sgn, in_Hz, opp_Hz, is_split, general_position, z_outside_hull

def phi_factory(z, n):
    u = (-n[1], n[0])
    def phi(p):
        w = n[0]*(p[0]-z[0]) + n[1]*(p[1]-z[1])
        assert w > 0
        return (F(-(u[0]*(p[0]-z[0]) + u[1]*(p[1]-z[1])), w), F(-1, w))
    return phi

def below_line(q, p, r):
    """q strictly below the non-vertical line through p, r (exact)."""
    assert p[0] != r[0]
    yl = p[1] + (r[1]-p[1]) * (q[0]-p[0]) / (r[0]-p[0])
    return q[1] < yl

def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    rng = random.Random(seed)
    viol = {'b': 0, 'c': 0, 'd': 0, 'vertical': 0, 'split_equiv': 0}
    counts = {'triples': 0, 'pairs': 0, 'sides': 0, 'partitions': 0, 'splits': 0, 'z_on_line_cases': 0}
    for t in range(trials):
        n_pts = rng.randint(4, 8)
        while True:
            X = list({(rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(n_pts)})
            if len(X) == n_pts and general_position(X):
                break
        # z: sometimes on a line through two points of X, outside the hull
        while True:
            if rng.random() < 0.4:
                a, b = rng.sample(X, 2); k = rng.choice([2, 3, 4, -1, -2, -3])
                zv = (a[0]+k*(b[0]-a[0]), a[1]+k*(b[1]-a[1]))
            else:
                zv = (rng.randint(-60, 60), rng.randint(-60, 60))
            if z_outside_hull(X, ('pt', zv)):
                break
        z = ('pt', zv)
        on_line = any(orient(p, q, zv) == 0 for p, q in itertools.combinations(X, 2))
        counts['z_on_line_cases'] += on_line
        # separating normal n with n.(x - z) > 0 for all x in X
        while True:
            n = (rng.randint(-50, 50), rng.randint(-50, 50))
            if n != (0, 0) and all(n[0]*(x[0]-zv[0]) + n[1]*(x[1]-zv[1]) > 0 for x in X):
                break
        phi = phi_factory(zv, n)
        Y = {p: phi(p) for p in X}
        for p, q, r in itertools.permutations(X, 3):
            counts['triples'] += 1
            if sgn(orient(Y[p], Y[q], Y[r])) != sgn(orient(p, q, r)):
                viol['b'] += 1
        for p, q in itertools.permutations(X, 2):
            counts['pairs'] += 1
            o = orient(zv, p, q)
            if (o < 0) != (Y[p][0] < Y[q][0]) or (o == 0) != (Y[p][0] == Y[q][0]):
                viol['c'] += 1
        for p, r in itertools.combinations(X, 2):
            if orient(p, r, zv) == 0:
                continue
            if Y[p][0] == Y[r][0]:
                viol['vertical'] += 1; continue
            for q in X:
                if q in (p, r):
                    continue
                counts['sides'] += 1
                if in_Hz(p, r, q, z) != below_line(Y[q], Y[p], Y[r]):
                    viol['d'] += 1
        if not on_line:
            m = len(X)
            for mask in range(1, (1 << m) - 1):
                A = [X[i] for i in range(m) if mask >> i & 1]
                B = [X[i] for i in range(m) if not mask >> i & 1]
                counts['partitions'] += 1
                sp = is_split(A, B, z)
                counts['splits'] += sp
                std = all(below_line(Y[b], Y[a], Y[a2]) for a, a2 in itertools.combinations(A, 2) for b in B) and \
                      all(not below_line(Y[a], Y[b], Y[b2]) and
                          orient(Y[b], Y[b2], Y[a]) != 0
                          for b, b2 in itertools.combinations(B, 2) for a in A)
                if sp != std:
                    viol['split_equiv'] += 1
    print('seed', seed, 'trials', trials)
    print('counts', counts)
    print('violations', viol)

if __name__ == '__main__':
    main()
