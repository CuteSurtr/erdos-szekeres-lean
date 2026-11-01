"""Independent exact test (integer arithmetic) of the ingredients of Corollary 7:

  Lemma 3:  (A,B) z-split, C subset A a z-cap, D subset B a z-cup (nonempty) => C u D in convex position.
            (This is what gives c + d <= gon(S), the only geometric input of Corollary 7.)
  Lemma 2:  convex P meeting both parts => P n A is a z-cap and P n B a z-cup.
  Cor. 4:   gon(S) = max(gon A, gon B, cap_z(A) + cup_z(B)).

Splits are generated DIRECTLY from Definition 1 (no normal-form map), with z either a finite point
(z = origin, points in an open sector of angle < pi, so z is outside conv(S)) or a direction d.
All tests use only the definitions in section 1 of split_theorem.md:
  orient_h(a,b,z) = orient(a,b,z) (finite) or det(b-a, d) (direction);
  q in H_z(ab) <=> sgn orient(a,b,q) = sgn orient_h(a,b,z) != 0;
  p <_z q <=> orient_h(p,q,z) < 0;
  z-cup: q_j in H_z(q_i q_k) for i<j<k (z-order); z-cap: q_j in the opposite open half-plane.
Convex position of a general-position set: every point is a vertex of the convex hull (monotone chain, exact).
"""
import itertools
import math
import random
import sys


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


class Z:
    def __init__(self, kind, v):
        self.kind = kind  # 'pt' or 'dir'
        self.v = v

    def oh(self, a, b):
        if self.kind == 'pt':
            return orient(a, b, self.v)
        d = self.v
        return (b[0] - a[0]) * d[1] - (b[1] - a[1]) * d[0]


def in_Hz(z, a, b, q):
    s = z.oh(a, b)
    return s != 0 and sgn(orient(a, b, q)) == sgn(s)


def in_opp(z, a, b, q):
    s = z.oh(a, b)
    o = orient(a, b, q)
    return s != 0 and o != 0 and sgn(o) == -sgn(s)


def is_split(z, A, B):
    for a, a2 in itertools.combinations(A, 2):
        if z.oh(a, a2) == 0:
            return False
        for b in B:
            if not in_Hz(z, a, a2, b):
                return False
    for b, b2 in itertools.combinations(B, 2):
        if z.oh(b, b2) == 0:
            return False
        for a in A:
            if not in_opp(z, b, b2, a):
                return False
    return True


def zsort(z, X):
    # p <_z q iff oh(p,q) < 0 ; check it's a strict total order and sort
    import functools

    def cmp(p, q):
        if p == q:
            return 0
        s = z.oh(p, q)
        assert s != 0
        return -1 if s < 0 else 1

    Y = sorted(X, key=functools.cmp_to_key(cmp))
    # verify transitivity on the sorted list
    for i in range(len(Y)):
        for j in range(i + 1, len(Y)):
            assert z.oh(Y[i], Y[j]) < 0, "z-order not a strict total order"
    return Y


def is_zcap(z, X):
    Y = zsort(z, X)
    for i, j, k in itertools.combinations(range(len(Y)), 3):
        if not in_opp(z, Y[i], Y[k], Y[j]):
            return False
    return True


def is_zcup(z, X):
    Y = zsort(z, X)
    for i, j, k in itertools.combinations(range(len(Y)), 3):
        if not in_Hz(z, Y[i], Y[k], Y[j]):
            return False
    return True


def hull_size(P):
    pts = sorted(set(P))
    if len(pts) <= 2:
        return len(pts)
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower) + len(upper) - 2


def convex_position(P):
    return hull_size(P) == len(P)


def general_position(P):
    for a, b, c in itertools.combinations(P, 3):
        if orient(a, b, c) == 0:
            return False
    return True


def subsets(X):
    for r in range(1, len(X) + 1):
        for s in itertools.combinations(X, r):
            yield s


def gon(X):
    best = 0
    for s in subsets(X):
        if len(s) > best and convex_position(s):
            best = len(s)
    return best


def gen_split(rng, finite, maxA, maxB, tries=400):
    """Grow a z-split by rejection: each proposal goes to A or B and is accepted iff Definition 1
    (and general position) still holds."""
    if finite:
        z = Z('pt', (0, 0))
        th0 = rng.uniform(0, 2 * math.pi)
        alpha = rng.uniform(0.3, 3.0)  # sector angle < pi, so the origin is outside conv(S)

        def prop(which):
            th = th0 + rng.uniform(0, alpha)
            r = rng.uniform(5, 40) if which == 'A' else rng.uniform(1, 30)
            sc = 10 ** 5
            return (int(round(sc * r * math.cos(th))), int(round(sc * r * math.sin(th))))
    else:
        ang = rng.uniform(0, 2 * math.pi)
        d = (int(round(1000 * math.cos(ang))), int(round(1000 * math.sin(ang))))
        if d == (0, 0):
            d = (0, -1)
        z = Z('dir', d)
        # frame: e = unit along d ("down"), f perpendicular
        L = math.hypot(*d)
        ex, ey = d[0] / L, d[1] / L
        fx, fy = -ey, ex

        def prop(which):
            t = rng.uniform(-10, 10)
            h = rng.uniform(-20, 5) if which == 'A' else rng.uniform(-5, 20)  # depth along d
            sc = 10 ** 5
            return (int(round(sc * (t * fx + h * ex))), int(round(sc * (t * fy + h * ey))))

    A, B = [prop('A')], [prop('B')]
    if not is_split(z, A, B) or A[0] == B[0]:
        return None
    tA = rng.randint(1, maxA)
    tB = rng.randint(1, maxB)
    for _ in range(tries):
        if len(A) >= tA and len(B) >= tB:
            break
        which = 'A' if (len(A) < tA and (len(B) >= tB or rng.random() < 0.5)) else 'B'
        p = prop(which)
        if p in A or p in B:
            continue
        A2 = A + [p] if which == 'A' else A
        B2 = B + [p] if which == 'B' else B
        if not general_position(A2 + B2):
            continue
        if is_split(z, A2, B2):
            A, B = A2, B2
    if finite:
        # z outside conv(S): guaranteed by the sector, but check: origin not in hull
        S = A + B
        hs = hull_size(S + [(0, 0)])
        # origin is outside conv(S) iff it is a hull vertex of S + {origin}
        pts = sorted(set(S + [(0, 0)]))
        # simple check: origin is a strict hull vertex
        lower, upper = [], []
        for q in pts:
            while len(lower) >= 2 and orient(lower[-2], lower[-1], q) <= 0:
                lower.pop()
            lower.append(q)
        for q in reversed(pts):
            while len(upper) >= 2 and orient(upper[-2], upper[-1], q) <= 0:
                upper.pop()
            upper.append(q)
        if (0, 0) not in lower + upper:
            return None
    return z, A, B


def test_split(z, A, B, stats):
    S = A + B
    assert is_split(z, A, B) and general_position(S)
    capsA = [s for s in subsets(A) if is_zcap(z, s)]
    cupsB = [s for s in subsets(B) if is_zcup(z, s)]
    c = max(len(s) for s in capsA)
    d = max(len(s) for s in cupsB)
    # Lemma 3 (all pairs)
    for C in capsA:
        for D in cupsB:
            stats['L3'] += 1
            if not convex_position(list(C) + list(D)):
                stats['L3_viol'] += 1
                print("LEMMA 3 VIOLATION", z.kind, z.v, A, B, C, D)
    # Lemma 2 (all convex P meeting both parts) and gon(S)
    g = 0
    for P in subsets(S):
        if not convex_position(P):
            continue
        g = max(g, len(P))
        PA = [p for p in P if p in A]
        PB = [p for p in P if p in B]
        if PA and PB:
            stats['L2'] += 1
            if not (is_zcap(z, PA) and is_zcup(z, PB)):
                stats['L2_viol'] += 1
                print("LEMMA 2 VIOLATION", z.kind, z.v, A, B, P)
    gA, gB = gon(A), gon(B)
    stats['C4'] += 1
    if g != max(gA, gB, c + d):
        stats['C4_viol'] += 1
        print("COR 4 VIOLATION", z.kind, z.v, A, B, g, gA, gB, c, d)
    stats['types'][(len(A), len(B), c, d)] = stats['types'].get((len(A), len(B), c, d), 0) + 1


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = random.Random(seed)
    stats = {'L2': 0, 'L2_viol': 0, 'L3': 0, 'L3_viol': 0, 'C4': 0, 'C4_viol': 0, 'types': {},
             'finite': 0, 'dir': 0, 'both_ge2': 0}
    done = 0
    while done < n:
        finite = (done % 2 == 0)
        r = gen_split(rng, finite, 7, 7)
        if r is None:
            continue
        z, A, B = r
        if len(A) + len(B) > 12:
            continue
        test_split(z, A, B, stats)
        stats['finite' if finite else 'dir'] += 1
        if len(A) >= 2 and len(B) >= 2:
            stats['both_ge2'] += 1
        done += 1
    types = stats.pop('types')
    print("seed", seed, "splits", done, stats)
    sizes = {}
    for (na, nb, c, d), m in types.items():
        sizes[(na, nb)] = sizes.get((na, nb), 0) + m
    print("max |A|+|B|:", max(na + nb for (na, nb) in sizes), " distinct (|A|,|B|,c,d) types:", len(types))
    cd = {}
    for (na, nb, c, d), m in types.items():
        cd[(c, d)] = cd.get((c, d), 0) + m
    print("(c,d) histogram:", dict(sorted(cd.items())))


if __name__ == '__main__':
    main()
