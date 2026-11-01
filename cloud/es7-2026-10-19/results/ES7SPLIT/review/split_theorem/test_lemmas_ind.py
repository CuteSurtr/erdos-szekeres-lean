#!/usr/bin/env python3
"""Independent randomized exact tests of Lemma 2, Lemma 3 and Corollary 4 of proofs/split_theorem.md.

Generators (none of them uses the construction of tools/test_split_lemma.py, "flatten B and push it far below"):
  F : finite z = (0,0); S sampled in the upper half-plane (so z is outside conv(S)); A and B grown point by
      point by rejection, accepting a point only if (S1),(S2) stay true and general position holds.
      A is sampled in a far band, B in a near band, with random band overlap (so y-separation in any frame is
      not imposed), plus uniform proposals.
  D : z a random rational direction; A, B grown by rejection in overlapping boxes.
  W : z finite but CLOSE to S (z just outside the hull of a pre-sampled set), sets grown by rejection.

For each split we check by brute force over all subsets:
  L2 : every convex P meeting A and B has P n A a z-cap and P n B a z-cup,
  L3 : every (nonempty z-cap of A) u (nonempty z-cup of B) is in convex position,
  C4 : gon(S) = max(gon(A), gon(B), cap_z(A) + cup_z(B)),
  also that <_z is a strict total order on A and on B, and that z is outside conv(S).
"""
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from igeom import (orient, on_z_side, on_far_side, general_position, is_z_cap, is_z_cup, convex_quads,
                   in_convex_position_idx, is_z_split, finite_z_outside_hull, z_order_is_total_and_transitive)


def grow(rng, nA, nB, z, propA, propB, max_tries=400000):
    A, B = [], []
    tries = 0
    while len(A) < nA or len(B) < nB:
        tries += 1
        if tries > max_tries:
            return None
        want = [x for x, need in (('A', len(A) < nA), ('B', len(B) < nB)) if need]
        part = rng.choice(want)
        p = propA(rng) if part == 'A' else propB(rng)
        S = A + B
        if p in S or any(orient(a, b, p) == 0 for a, b in combinations(S, 2)):
            continue
        if part == 'A':
            if all(on_z_side(b, p, a, z) for a in A for b in B) and \
                    all(on_far_side(p, b, b2, z) for b, b2 in combinations(B, 2)):
                A.append(p)
        else:
            if all(on_z_side(p, a, a2, z) for a, a2 in combinations(A, 2)) and \
                    all(on_far_side(a, p, b, z) for b in B for a in A):
                B.append(p)
    return A, B


def gen_F(rng, nA, nB):
    z = ('F', (0, 0))
    R = 10 ** 4
    farlo = rng.randint(1, R // 2)
    nearhi = rng.randint(R // 10, R)

    def propA(r):
        if r.random() < 0.3:
            return (r.randint(-R, R), r.randint(1, R))
        return (r.randint(-R, R), r.randint(farlo, R))

    def propB(r):
        if r.random() < 0.3:
            return (r.randint(-R, R), r.randint(1, R))
        return (r.randint(-R, R), r.randint(1, nearhi))
    g = grow(rng, nA, nB, z, propA, propB)
    return None if g is None else (g[0], g[1], z)


def gen_D(rng, nA, nB):
    while True:
        d = (rng.randint(-20, 20), rng.randint(-20, 20))
        if d != (0, 0):
            break
    z = ('D', d)
    R = 1000
    shift = rng.randint(0, 3 * R)

    def propA(r):
        return (r.randint(-R, R), r.randint(-R, R))

    def propB(r):
        return (r.randint(-R, R) + d[0] * shift // 20, r.randint(-R, R) + d[1] * shift // 20)
    g = grow(rng, nA, nB, z, propA, propB)
    return None if g is None else (g[0], g[1], z)


def gen_W(rng, nA, nB):
    """z finite and close to the points: z = (0, 0); all points in the half-plane y > 0 but with small y allowed
    and wide x range, so that the angular order from z spreads over almost pi."""
    z = ('F', (0, 0))
    R = 3000

    def propA(r):
        return (r.randint(-R, R), r.randint(1, R // 3))

    def propB(r):
        return (r.randint(-R, R), r.randint(1, R // 3))
    g = grow(rng, nA, nB, z, propA, propB, max_tries=200000)
    return None if g is None else (g[0], g[1], z)


def check(A, B, z):
    S = A + B
    n = len(S)
    nA = len(A)
    assert general_position(S)
    assert is_z_split(A, B, z)
    if z[0] == 'F':
        assert finite_z_outside_hull(S, z[1])
    assert z_order_is_total_and_transitive(A, z) and z_order_is_total_and_transitive(B, z)
    quads = convex_quads(S)
    res = dict(L2=0, L3=0, C4=0)
    gon = min(n, 3)
    gonA = min(nA, 3)
    gonB = min(n - nA, 3)
    for r in range(4, n + 1):
        for T in combinations(range(n), r):
            if in_convex_position_idx(T, quads):
                gon = max(gon, r)
                TA = [i for i in T if i < nA]
                TB = [i for i in T if i >= nA]
                if not TB:
                    gonA = max(gonA, r)
                if not TA:
                    gonB = max(gonB, r)
                if TA and TB:
                    if not (is_z_cap([S[i] for i in TA], z) and is_z_cup([S[i] for i in TB], z)):
                        res['L2'] += 1
    # mixed triples are always convex; with |T| = 3 L2 still demands cap/cup of parts (trivial: parts have <= 2 pts)
    capsA = [C for r in range(1, nA + 1) for C in combinations(range(nA), r) if r <= 2 or is_z_cap([S[i] for i in C], z)]
    cupsB = [D for r in range(1, n - nA + 1) for D in combinations(range(nA, n), r)
             if r <= 2 or is_z_cup([S[i] for i in D], z)]
    capA = max(len(C) for C in capsA)
    cupB = max(len(D) for D in cupsB)
    for C in capsA:
        for D in cupsB:
            if len(C) + len(D) >= 4 and not in_convex_position_idx(C + D, quads):
                res['L3'] += 1
    if gon != max(gonA, gonB, capA + cupB):
        res['C4'] += 1
    res.update(gon=gon, gonA=gonA, gonB=gonB, capA=capA, cupB=cupB)
    return res


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    rng = random.Random(seed)
    tot = dict(trials=0, gen_fail=0, L2=0, L3=0, C4=0)
    by_gen = {}
    mixed_big = 0
    for t in range(trials):
        gname = ['F', 'D', 'W'][t % 3]
        gen = dict(F=gen_F, D=gen_D, W=gen_W)[gname]
        nA, nB = rng.randint(2, 7), rng.randint(2, 7)
        g = gen(rng, nA, nB)
        if g is None:
            tot['gen_fail'] += 1
            continue
        A, B, z = g
        r = check(A, B, z)
        tot['trials'] += 1
        for k in ('L2', 'L3', 'C4'):
            tot[k] += r[k]
        by_gen[gname] = by_gen.get(gname, 0) + 1
        if r['capA'] + r['cupB'] >= 5:
            mixed_big += 1
    print(dict(seed=seed, **tot, by_gen=by_gen, splits_with_capA_plus_cupB_ge5=mixed_big))


if __name__ == '__main__':
    main()
