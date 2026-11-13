"""Check the 'obvious extension fails' claims (Remarks 1-3 and the controls of the first version of PROOF.md)
with referee code only.

(a) split middle: k clusters on the centre-free symmetric cubic base x = +-1,+-3,...,+-(k-1);
    types (j+2,k-j) for j<n/2 on the left, X=G(m,m+1) at x=-1, -X at x=+1, mirrors on the right.
    Also with arbitrary nonempty middle contents (2 random points each) -- the failure is structural.
(b) the proof's base, middle cluster at scale eps (same as outer clusters) or eps^(3/2) instead of eps^2.
(c) the even base x_i = 2i-n (contains 0; for n>=6 it has non-forced zero-sum triples), middle at eps^2.
(d) the even base x_i = 2i-n with the middle at scale eps (the most literal 'odd recipe' transplant).
Everything exact; the largest convex subset is computed by two independent DPs.
"""
import sys, random
from fractions import Fraction
from math import comb, lcm, isqrt
from rconstruct import G, check_G, middle_set, base_abscissae, to_int
from rg import max_convex_cupcap, max_convex_angular, convex_position_bf, collinear_triples, orient
from rhyp import check


def normG(P):
    if len(P) == 1:
        return [(Fraction(0), Fraction(0))]
    w = max(p[0] for p in P) - min(p[0] for p in P)
    h = max(p[1] for p in P) - min(p[1] for p in P)
    x0 = min(p[0] for p in P); y0 = min(p[1] for p in P)
    return [(Fraction(x - x0, w), Fraction(y - y0, h) if h else Fraction(0)) for (x, y) in P]


def build_general(k, xs, eps, mid_scale, mid_contents=None):
    n = k - 2; m = k // 2
    cl = [None] * (n + 1)
    for j in range(n // 2):
        P = normG(G(j + 2, k - j))
        q = (Fraction(xs[j]), Fraction(xs[j]) ** 3)
        Bj = [(q[0] + eps * gx, q[1] + eps * eps * gy) for (gx, gy) in P]
        cl[j] = Bj
        cl[n - j] = [(-x, -y) for (x, y) in Bj]
    M0 = middle_set(m)[0] if mid_contents is None else mid_contents
    cl[n // 2] = [(mid_scale * x, mid_scale * y) for (x, y) in M0]
    return to_int(cl)[0]


def split_middle(k, eps, mid_mode='ES', rng=None):
    n = k - 2; m = k // 2
    xl = [-(k - 1) + 2 * j for j in range(m)]           # m left positions; last one is -1
    types = [(j + 2, k - j) for j in range(n // 2)] + [(m, m + 1)]
    cl = []
    for x, (a, b) in zip(xl, types):
        if mid_mode != 'ES' and (a, b) == (m, m + 1):
            # arbitrary contents for the two central clusters: two random points (any nonempty set)
            P = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(rng.randint(-5, 5), 7))]
        else:
            P = normG(G(a, b))
        q = (Fraction(x), Fraction(x) ** 3)
        cl.append([(q[0] + eps * gx, q[1] + eps * eps * gy) for (gx, gy) in P])
    cl = cl + [[(-x, -y) for (x, y) in B] for B in cl[::-1]]
    return to_int(cl)[0]


def report(tag, cl, k, xs=None):
    pts = [p for B in cl for p in B]
    S = set(pts)
    gp = not collinear_triples(pts)
    sym = all((-x, -y) in S for (x, y) in pts)
    m1, w1 = max_convex_cupcap(pts)
    m2 = max_convex_angular(pts)
    line = "  %-58s N=%d sym=%s GP=%s maxconvex=%d/%d witness_convex=%s k-gon=%s" % (
        tag, len(pts), sym, gp, m1, m2, convex_position_bf(w1), m1 >= k)
    if xs is not None:
        rep = check(cl, k, xs)
        line += " | hyp fails=%s" % ([h for h in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5'] if not rep[h]] or 'none')
    print(line)
    sys.stdout.flush()
    return m1, w1


if __name__ == "__main__":
    rng = random.Random(5)
    for k in (6, 8):
        n = k - 2
        print("k = %d" % k)
        print(" (a) split middle (k clusters, centre-free base +-1,+-3,...)")
        for E in (64, 1024, 2 ** 16, 2 ** 24):
            report("split middle, ES contents, eps=1/%d" % E, split_middle(k, Fraction(1, E)), k)
        for E in (1024, 2 ** 20):
            report("split middle, 2 arbitrary pts per central cluster, eps=1/%d" % E,
                   split_middle(k, Fraction(1, E), mid_mode='rand', rng=rng), k)
        xs = base_abscissae(k)
        print(" (b) proof's base (odd + 0), middle cluster at other scales")
        for E in (2 ** 10, 2 ** 16, 2 ** 24):
            eps = Fraction(1, E)
            report("middle at eps^2 (as written), eps=1/%d" % E, build_general(k, xs, eps, eps * eps), k, xs)
            report("middle at eps (outer scale), eps=1/%d" % E, build_general(k, xs, eps, eps), k, xs)
            r = isqrt(E)
            report("middle at eps^(3/2), eps=1/%d" % E, build_general(k, xs, eps, eps * Fraction(1, r)), k, xs)
        print(" (c)/(d) even base x_i = 2i-n (contains 0)")
        xe = [2 * i - n for i in range(n + 1)]
        zs = [(xe[a], xe[b], xe[c]) for a in range(n + 1) for b in range(a + 1, n + 1) for c in range(b + 1, n + 1)
              if xe[a] + xe[b] + xe[c] == 0]
        print("   zero-sum base triples:", zs)
        for E in (2 ** 10, 2 ** 16, 2 ** 24):
            eps = Fraction(1, E)
            report("even base, middle at eps^2, eps=1/%d" % E, build_general(k, xe, eps, eps * eps), k, xe)
            report("even base, middle at eps, eps=1/%d" % E, build_general(k, xe, eps, eps), k, xe)
