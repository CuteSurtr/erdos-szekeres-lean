#!/usr/bin/env python3
"""Independent exact test of Lemma 2, Lemma 3 and Corollary 4 of split_theorem.md,
working directly with the z-definitions (finite z outside conv(S), or a direction d),
WITHOUT using the projective normal form.  Integer arithmetic only.

For random small point sets S and random z, every bipartition (A,B) is tested for
being a z-split (Definition 1).  For every split found we brute-force:
  L2: every convex P meeting A and B has P∩A a z-cap and P∩B a z-cup;
  L3: every nonempty z-cap C ⊆ A and nonempty z-cup D ⊆ B give C∪D convex;
  C4: gon(S) = max(gon(A), gon(B), cap_z(A)+cup_z(B)).
Generators include adversarial cases: z collinear with an A-B pair, z just outside
the hull, structured cap-over-cup instances, and random directions.
"""
import itertools, random, sys
from functools import cmp_to_key

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def sgn(x):
    return (x > 0) - (x < 0)

def orient_h(a, b, z):
    kind, v = z
    if kind == 'pt':
        return orient(a, b, v)
    return (b[0]-a[0])*v[1] - (b[1]-a[1])*v[0]      # det(b-a, d)

def in_Hz(a, b, q, z):
    s = orient_h(a, b, z)
    return s != 0 and sgn(orient(a, b, q)) == sgn(s)

def opp_Hz(a, b, q, z):
    s = orient_h(a, b, z); o = orient(a, b, q)
    return s != 0 and o != 0 and sgn(o) == -sgn(s)

def is_split(A, B, z):
    for a, a2 in itertools.combinations(A, 2):
        for b in B:
            if not in_Hz(a, a2, b, z):
                return False
    for b, b2 in itertools.combinations(B, 2):
        for a in A:
            if not opp_Hz(b, b2, a, z):
                return False
    return True

def general_position(P):
    return all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))

def in_closed_triangle(p, a, b, c):
    o1, o2, o3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
    return (o1 >= 0 and o2 >= 0 and o3 >= 0) or (o1 <= 0 and o2 <= 0 and o3 <= 0)

def convex_position(P):
    P = list(P)
    if len(P) <= 3:
        return True
    for i, p in enumerate(P):
        others = P[:i] + P[i+1:]
        for a, b, c in itertools.combinations(others, 3):
            if in_closed_triangle(p, a, b, c):
                return False
    return True

def z_outside_hull(S, z):
    if z[0] == 'dir':
        return True
    v = z[1]
    if v in S:
        return False
    for a, b in itertools.combinations(S, 2):        # on a segment
        if orient(a, b, v) == 0 and min(a[0], b[0]) <= v[0] <= max(a[0], b[0]) \
           and min(a[1], b[1]) <= v[1] <= max(a[1], b[1]):
            return False
    for a, b, c in itertools.combinations(S, 3):
        if in_closed_triangle(v, a, b, c):
            return False
    return True

def z_sorted(Y, z):
    """Sort by <_z (p <_z q iff orient_h(p,q,z) < 0); verify it is a strict total order."""
    def cmp(p, q):
        o = orient_h(p, q, z)
        if o == 0:
            raise ValueError('tie in z-order')
        return -1 if o < 0 else 1
    L = sorted(Y, key=cmp_to_key(cmp))
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            if not orient_h(L[i], L[j], z) < 0:
                raise ValueError('z-order not transitive')
    return L

def is_zcap(Y, z):
    L = z_sorted(Y, z)
    return all(opp_Hz(L[i], L[k], L[j], z)
               for i, j, k in itertools.combinations(range(len(L)), 3))

def is_zcup(Y, z):
    L = z_sorted(Y, z)
    return all(in_Hz(L[i], L[k], L[j], z)
               for i, j, k in itertools.combinations(range(len(L)), 3))

def subsets(X, minsize=1):
    X = list(X)
    for r in range(minsize, len(X)+1):
        for c in itertools.combinations(X, r):
            yield c

def gon(X):
    X = list(X)
    for r in range(len(X), 0, -1):
        for c in itertools.combinations(X, r):
            if convex_position(c):
                return r
    return 0

def maxsize(X, pred):
    best = 0
    for c in subsets(X):
        if len(c) > best and pred(c):
            best = len(c)
    return best

def check_split(S, A, B, z, stats):
    Aset = set(A)
    # Lemma 2
    for P in subsets(S, 2):
        PA = [p for p in P if p in Aset]; PB = [p for p in P if p not in Aset]
        if PA and PB and convex_position(P):
            if not is_zcap(PA, z) or not is_zcup(PB, z):
                stats['L2_fail'] += 1
                print('L2 FAIL', S, A, B, z, P); sys.stdout.flush()
    # Lemma 3
    caps = [c for c in subsets(A) if is_zcap(c, z)]
    cups = [d for d in subsets(B) if is_zcup(d, z)]
    for c in caps:
        for d in cups:
            if not convex_position(list(c) + list(d)):
                stats['L3_fail'] += 1
                print('L3 FAIL', S, A, B, z, c, d); sys.stdout.flush()
    # Corollary 4
    capA = max(len(c) for c in caps); cupB = max(len(d) for d in cups)
    lhs = gon(S); rhs = max(gon(A), gon(B), capA + cupB)
    if lhs != rhs:
        stats['C4_fail'] += 1
        print('C4 FAIL', S, A, B, z, lhs, rhs); sys.stdout.flush()
    stats['splits'] += 1
    if len(A) >= 2 and len(B) >= 2:
        stats['nontrivial'] += 1
        if z[0] == 'pt':
            stats['nontrivial_finite'] += 1
        stats['types'].add((len(A), len(B), capA, cupB))

def rand_pts(n, R, rng):
    while True:
        P = list({(rng.randint(-R, R), rng.randint(-R, R)) for _ in range(n)})
        if len(P) == n and general_position(P):
            return P

def structured(rng):
    """A near a downward arch (with noise, so cup triples occur), B near an upward bowl below."""
    while True:
        k = rng.randint(2, 5); m = rng.randint(2, 5)
        A = [(x, 400 - (x*x)//rng.randint(3, 12) + rng.randint(-40, 40))
             for x in rng.sample(range(-40, 41), k)]
        B = [(x, -400 + (x*x)//rng.randint(3, 12) + rng.randint(-40, 40))
             for x in rng.sample(range(-40, 41), m)]
        S = A + B
        if len(set(S)) == len(S) and general_position(S):
            return S

def rand_z(S, rng, R):
    t = rng.random()
    if t < 0.35:
        while True:
            d = (rng.randint(-5, 5), rng.randint(-5, 5))
            if d != (0, 0):
                return ('dir', d)
    if t < 0.55:
        # adversarial: z on the extension of a line through two points of S, outside the hull
        for _ in range(100):
            a, b = rng.sample(S, 2)
            k = rng.choice([2, 3, 5, 10, -1, -2, -4, -9])
            v = (a[0] + k*(b[0]-a[0]), a[1] + k*(b[1]-a[1]))
            z = ('pt', v)
            if z_outside_hull(S, z):
                return z
    while True:
        v = (rng.randint(-4*R, 4*R), rng.randint(-4*R, 4*R))
        z = ('pt', v)
        if z_outside_hull(S, z):
            return z

def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = random.Random(seed)
    stats = {'splits': 0, 'nontrivial': 0, 'nontrivial_finite': 0,
             'L2_fail': 0, 'L3_fail': 0, 'C4_fail': 0, 'types': set(), 'instances': 0}
    for t in range(trials):
        if t % 2 == 0:
            S = rand_pts(rng.randint(5, 8), 30, rng); R = 30
        else:
            S = structured(rng); R = 400
        for _ in range(4):
            z = rand_z(S, rng, R)
            stats['instances'] += 1
            n = len(S)
            for mask in range(1, (1 << n) - 1):
                A = [S[i] for i in range(n) if mask >> i & 1]
                B = [S[i] for i in range(n) if not mask >> i & 1]
                if is_split(A, B, z):
                    check_split(S, A, B, z, stats)
    types = sorted(stats.pop('types'))
    print('seed', seed, stats)
    print('distinct nontrivial (|A|,|B|,cap_z(A),cup_z(B)) types:', len(types))
    print(types)

if __name__ == '__main__':
    main()
