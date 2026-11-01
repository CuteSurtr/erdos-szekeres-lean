"""Independent exact (Fraction) test of Lemma 0 (finite z) as used in Corollary 7:
phi(p) = ( -u.(p-z)/w(p), -1/w(p) ),  w(p) = n.(p-z) > 0,  u = (-n_y, n_x).
Checks, for finite-z splits generated directly from Definition 1 (reusing the generator of lemma_test.py):
  (b) orientation signs preserved;  (c) p <_z q  <=>  x(phi p) < x(phi q);
  (d) q in H_z(pr) <=> phi(q) strictly below the (non-vertical) line phi(p)phi(r);
  phi(A), phi(B) is a standard-frame split (phi B below every line of phi A, phi A above every line of phi B);
  cap number of phi(A) (x-order caps) = cap_z(A); cup number of phi(B) = cup_z(B); gon preserved;
  phi(S) in general position with distinct x-coordinates.
n is chosen at random among vectors with n.(p - z) > 0 for all p in S (z = origin is outside conv S).
"""
import itertools
import random
import sys
from fractions import Fraction as F

import lemma_test as LT


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


def is_cap_x(X):
    Y = sorted(X)
    return all(orient(Y[i], Y[k], Y[j]) > 0 for i, j, k in itertools.combinations(range(len(Y)), 3))
    # orient(Yi, Yk, Yj) > 0 means Yj is to the left of Yi->Yk (Yi left of Yk): above the chord: cap


def is_cup_x(X):
    Y = sorted(X)
    return all(orient(Y[i], Y[k], Y[j]) < 0 for i, j, k in itertools.combinations(range(len(Y)), 3))


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    nsplits = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(seed)
    viol = {'b': 0, 'c': 0, 'd': 0, 'split': 0, 'cap': 0, 'cup': 0, 'gon': 0, 'gp': 0, 'xdist': 0}
    checks = {k: 0 for k in viol}
    done = 0
    while done < nsplits:
        r = LT.gen_split(rng, True, 7, 7)
        if r is None:
            continue
        z, A, B = r
        S = A + B
        if len(S) > 11:
            continue
        zz = z.v
        # random n with n.(p - z) > 0 for all p in S
        for _ in range(1000):
            n = (rng.randint(-50, 50), rng.randint(-50, 50))
            if n != (0, 0) and all(n[0] * (p[0] - zz[0]) + n[1] * (p[1] - zz[1]) > 0 for p in S):
                break
        else:
            continue
        u = (-n[1], n[0])

        def phi(p):
            w = n[0] * (p[0] - zz[0]) + n[1] * (p[1] - zz[1])
            uu = u[0] * (p[0] - zz[0]) + u[1] * (p[1] - zz[1])
            return (F(-uu, w), F(-1, w))

        P = {p: phi(p) for p in S}
        # (b)
        for p, q, s in itertools.combinations(S, 3):
            checks['b'] += 1
            if sgn(orient(P[p], P[q], P[s])) != sgn(orient(p, q, s)):
                viol['b'] += 1
        # (c) on pairs within A and within B (where z is on no line), and all pairs where defined
        for p, q in itertools.permutations(S, 2):
            o = orient(zz, p, q)
            if o == 0:
                continue
            checks['c'] += 1
            if (o < 0) != (P[p][0] < P[q][0]):
                viol['c'] += 1
        # (d)
        for p, r_ in itertools.combinations(S, 2):
            if orient(p, r_, zz) == 0:
                continue
            for q in S:
                if q in (p, r_):
                    continue
                checks['d'] += 1
                inH = LT.in_Hz(z, p, r_, q)
                a, b = (P[p], P[r_]) if P[p][0] < P[r_][0] else (P[r_], P[p])
                if a[0] == b[0]:
                    viol['d'] += 1
                    continue
                below = orient(a, b, P[q]) < 0
                if inH != below:
                    viol['d'] += 1
        # standard-frame split
        checks['split'] += 1
        ok = True
        for a1, a2 in itertools.combinations(A, 2):
            x, y = sorted([P[a1], P[a2]])
            for b in B:
                if not orient(x, y, P[b]) < 0:
                    ok = False
        for b1, b2 in itertools.combinations(B, 2):
            x, y = sorted([P[b1], P[b2]])
            for a in A:
                if not orient(x, y, P[a]) > 0:
                    ok = False
        if not ok:
            viol['split'] += 1
        # general position and distinct x within phi(S) (z generic w.r.t. S? not required: check within A, B)
        checks['gp'] += 1
        if not LT.general_position([P[p] for p in S]):
            viol['gp'] += 1
        for X in (A, B):
            checks['xdist'] += 1
            xs = [P[p][0] for p in X]
            if len(set(xs)) != len(xs):
                viol['xdist'] += 1
        # cap / cup numbers and gon
        capz = max(len(s) for s in LT.subsets(A) if LT.is_zcap(z, s))
        cupz = max(len(s) for s in LT.subsets(B) if LT.is_zcup(z, s))
        capx = max(len(s) for s in LT.subsets([P[p] for p in A]) if is_cap_x(s))
        cupx = max(len(s) for s in LT.subsets([P[p] for p in B]) if is_cup_x(s))
        checks['cap'] += 1
        checks['cup'] += 1
        if capz != capx:
            viol['cap'] += 1
        if cupz != cupx:
            viol['cup'] += 1
        # per-subset correspondence
        for s in LT.subsets(A):
            if LT.is_zcap(z, s) != is_cap_x([P[p] for p in s]):
                viol['cap'] += 1
        for s in LT.subsets(B):
            if LT.is_zcup(z, s) != is_cup_x([P[p] for p in s]):
                viol['cup'] += 1
        checks['gon'] += 1
        # gon via exact hull on Fractions
        if LT.gon(S) != LT.gon([P[p] for p in S]):
            viol['gon'] += 1
        done += 1
    print("seed", seed, "splits", done)
    print("checks", checks)
    print("violations", viol)


if __name__ == '__main__':
    main()
