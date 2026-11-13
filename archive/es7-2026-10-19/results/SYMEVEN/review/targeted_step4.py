"""Targeted test of Step 4 of Lemma 3 (the only place where the middle cluster matters).

Configuration (clusters other than n/2-1, n/2, n/2+1 empty):
  B_{n/2-1}: a cup of n/2 points near (-L,-L)   (maximal under (H5): no (n/2+1)-cup)
  B_{n/2}  : two points q, q' near the origin, arbitrary (not symmetric)
  B_{n/2+1}: a cap of n/2 points near (L, L)     (maximal under (H5): no (n/2+1)-cap)
Exactly k points. (H3) imposes nothing here (x_{n/2-1}+x_{n/2}+x_{n/2+1} = -1+0+1 = 0).
Lemma 3 says: if (H0),(H1),(H2),(H4),(H5) and general position hold, these k points are NOT in convex
position (indeed no k of them... there are only k).  We count how often the hypotheses hold and whether
the k points are in convex position; and, as a control, how often they are convex when only (H4) fails.
"""
import random, sys
from rg import orient, convex_position_bf, collinear_triples
from rhyp import check
from rconstruct import base_abscissae


def strict_chain(rng, size, kind, W, H):
    while True:
        xs = sorted(rng.sample(range(0, W), size))
        ys = []
        # random convex (kind=+1) / concave (kind=-1) sequence: increasing / decreasing slopes
        slopes = sorted(rng.sample(range(-H, H), size - 1))
        if kind < 0:
            slopes = slopes[::-1]
        y = 0
        pts = [(xs[0], 0)]
        for i in range(1, size):
            # use rational slopes s/1000 applied to dx; keep integers by scaling y by 1000
            y += slopes[i - 1] * (xs[i] - xs[i - 1])
            pts.append((xs[i], y))
        ok = all(kind * orient(pts[i - 1], pts[i], pts[i + 1]) > 0 for i in range(1, size - 1))
        if ok and not collinear_triples(pts):
            return pts


def run(k, nsamp, seed):
    rng = random.Random(seed)
    n = k - 2; mid = n // 2
    xs = base_abscissae(k)
    L = 10 ** 12
    st = dict(samples=0, hyp_ok=0, hyp_ok_convex=0, only_h4_fail=0, only_h4_fail_convex=0, other_fail=0,
              sigma0_cases=0)
    for _ in range(nsamp):
        st['samples'] += 1
        cx = rng.choice([10 ** e for e in range(3, 8)])
        cup = strict_chain(rng, mid, +1, 1000, 50)
        cap = strict_chain(rng, mid, -1, 1000, 50)
        Bl = [(-L + cx * x + rng.randint(-cx // 2, cx // 2) * 0, -L + y) for (x, y) in cup]
        Br = [(L - cx * 1000 + cx * x, L + y) for (x, y) in cap]
        if rng.random() < 0.3:           # force some exact x(p)+x(r)=0 pairs (sigma = 0 branches)
            Br = [(-Bl[i][0], L + cap[i][1]) for i in range(len(Bl))][::-1]
            Br = sorted(Br)
            # keep a cap shape: if not a cap, skip this modification
            if not all(orient(Br[i - 1], Br[i], Br[i + 1]) < 0 for i in range(1, len(Br) - 1)):
                Br = [(L - cx * 1000 + cx * x, L + y) for (x, y) in cap]
        sm = rng.choice([1, 10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7])
        q1 = (rng.randint(-sm, sm), rng.randint(-sm, sm) // 3)
        q2 = (rng.randint(-sm, sm), rng.randint(-sm, sm) // 3) if rng.random() < 0.6 else (-q1[0], -q1[1])
        if q1[0] == q2[0]:
            continue
        cl = [[] for _ in range(n + 1)]
        cl[mid - 1] = Bl; cl[mid] = [q1, q2]; cl[mid + 1] = Br
        pts = Bl + [q1, q2] + Br
        if len(set(p[0] for p in pts)) < len(pts) or collinear_triples(pts):
            continue
        rep = check(cl, k, xs)
        conv = convex_position_bf(pts)
        fails = [h for h in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5'] if not rep[h]]
        if not fails:
            st['hyp_ok'] += 1
            if rep['H4_zero_sum_skipped']:
                st['sigma0_cases'] += 1
            if conv:
                st['hyp_ok_convex'] += 1
                print("COUNTEREXAMPLE", cl)
        elif fails == ['H4']:
            st['only_h4_fail'] += 1
            st['only_h4_fail_convex'] += conv
        else:
            st['other_fail'] += 1
    print("k=%d seed=%d %s" % (k, seed, st))


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
