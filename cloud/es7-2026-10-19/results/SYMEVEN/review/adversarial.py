"""Adversarial falsification attempts for Lemma 3 (referee's own generator and checkers).

Lemma 3 assumes only (H0)-(H5) plus general position: no symmetry, no cubic base, no ES contents.
So the generator varies exactly what the lemma leaves free:
  * outer cluster contents: ES sets (random sub-samples and affine distortions), greedy random sets,
    or a maximal cup/cap ("chain") plus random extras -- always subject to the (H5) bounds;
  * outer clusters symmetric (B_{n-j} = -B_j), independent, or "x-mirrored with perturbed y" (so many
    pairs have x(p)+x(r)=0 with r != -p, which exercises the sigma=0 branches of Step 4);
  * middle cluster: Lemma-2 set, greedy random set, random centrally symmetric set, or just 2 points;
    optionally off-centre; its scale is random OR pushed to the largest value at which (H4) still holds;
  * base points: cubic with abscissae x_j, optionally perturbed.
Every sample is checked exactly; whenever (H0)-(H5)+GP all hold, the largest convex subset is
computed (two independent DPs) and must be <= k-1.
"""
import random, sys, time
from math import comb
from rg import orient, longest_cup_cap, max_convex_cupcap, max_convex_angular, convex_position_bf
from rhyp import check
from rconstruct import G, base_abscissae, middle_set


def gp_ok_with(pts, p):
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if orient(pts[i], pts[j], p) == 0:
                return False
    return True


def greedy(rng, cupmax, capmax, target, W, H, seed=None, tries=3000, sym=False):
    pts = list(seed or [])
    xs = set(p[0] for p in pts)
    t = 0
    while len(pts) < target and t < tries:
        t += 1
        p = (rng.randint(-W, W), rng.randint(-H, H))
        if sym:
            if p[0] == 0 or p[0] in xs or -p[0] in xs:
                continue
            q = (-p[0], -p[1])
            if not gp_ok_with(pts, p):
                continue
            if not gp_ok_with(pts + [p], q):
                continue
            cand = pts + [p, q]
        else:
            if p[0] in xs or not gp_ok_with(pts, p):
                continue
            cand = pts + [p]
        lc, lk = longest_cup_cap(cand)
        if lc <= cupmax and lk <= capmax:
            pts = cand
            xs = set(z[0] for z in pts)
    return pts


def chain(rng, kind, size, W):
    """A cup (kind=+1) or cap (kind=-1) of the given size with integer coordinates."""
    xs = sorted(rng.sample(range(-W, W), size))
    pts = []
    for x in xs:
        pts.append((x, kind * (x * x) // max(1, W // 8) + rng.randint(-2, 2)))
    # repair: verify it is a strict cup/cap; if not, fall back to an exact parabola
    ok = all(kind * orient(pts[i - 1], pts[i], pts[i + 1]) > 0 for i in range(1, size - 1))
    if not ok:
        pts = [(x, kind * x * x) for x in xs]
    return pts


def normalize(P):
    if not P:
        return P
    x0 = min(p[0] for p in P); y0 = min(p[1] for p in P)
    return [(p[0] - x0, p[1] - y0) for p in P]


def outer_contents(rng, k, j, mode):
    cupmax, capmax = j + 1, k - j - 1
    maxsize = comb(k - 2, j)
    if mode == 'es':
        P = G(j + 2, k - j)
        if rng.random() < 0.5 and len(P) > 1:
            P = [p for p in P if rng.random() < 0.75] or P[:1]
        beta = rng.choice([1, 2, 3, 5]); gam = rng.randint(-3, 3)
        P = [(x, beta * y + gam * x) for (x, y) in P]
        if rng.random() < 0.5:           # tiny random perturbation, kept only if (H5)+GP survive
            Q = [(x * 64 + rng.randint(-3, 3), y * 64 + rng.randint(-3, 3)) for (x, y) in P]
            if len(set(q[0] for q in Q)) == len(Q):
                lc, lk = longest_cup_cap(Q)
                from rg import collinear_triples
                if lc <= cupmax and lk <= capmax and not collinear_triples(Q):
                    P = Q
    elif mode == 'chain':
        if j < (k - 2) // 2:
            seed = chain(rng, +1, cupmax, 200)
        else:
            seed = chain(rng, -1, capmax, 200)
        P = greedy(rng, cupmax, capmax, rng.randint(len(seed), maxsize), 300, 300, seed=seed, tries=400)
    else:
        P = greedy(rng, cupmax, capmax, rng.randint(1, maxsize), 300, 300, tries=600)
    lc, lk = longest_cup_cap(P) if len(P) > 0 else (0, 0)
    assert lc <= cupmax and lk <= capmax
    return normalize(P)


def middle_contents(rng, m, mode):
    if mode == 'M0':
        M0, t = middle_set(m)
        from math import lcm
        from fractions import Fraction
        D = 1
        for (x, y) in M0:
            D = lcm(D, Fraction(x).denominator, Fraction(y).denominator)
        return [(int(x * D), int(y * D)) for (x, y) in M0]
    if mode == 'sym':
        return greedy(rng, m, m, rng.randint(1, comb(2 * m - 2, m - 1) // 2) * 2, 400, 60, sym=True, tries=800)
    if mode == 'pair':
        while True:
            a = (rng.randint(-400, 400), rng.randint(-60, 60))
            b = (rng.randint(-400, 400), rng.randint(-60, 60)) if rng.random() < 0.5 else (-a[0], -a[1])
            if a[0] != b[0]:
                return [a, b]
    return greedy(rng, m, m, rng.randint(2, comb(2 * m - 2, m - 1)), 400, 60, tries=800)


def assemble(k, base, outer, mid, c_out, s_mid, mid_off):
    n = k - 2
    cl = []
    for j in range(n + 1):
        if j == n // 2:
            cl.append([(s_mid * x + mid_off[0], s_mid * y + mid_off[1]) for (x, y) in mid])
        else:
            P = outer[j]
            if not P:
                cl.append([]); continue
            w = max(p[0] for p in P); h = max(p[1] for p in P)
            cx, cy = (w // 2), (h // 2)
            cl.append([(base[j][0] + c_out * (x - cx), base[j][1] + (y - cy)) for (x, y) in P])
    return cl


def sample(rng, k, LAM, mode_bias=None, tune_h4=False):
    n = k - 2; mid = n // 2; m = k // 2
    xs = base_abscissae(k)
    base = []
    pert = rng.random() < 0.5
    for j in range(n + 1):
        bx, by = LAM * xs[j], LAM * xs[j] ** 3
        if pert and j != mid:
            bx += rng.randint(-LAM // 1000, LAM // 1000); by += rng.randint(-LAM // 1000, LAM // 1000)
        base.append((bx, by))
    if pert and rng.random() < 0.5:   # keep the base itself symmetric half of the time
        for j in range(mid):
            base[n - j] = (-base[j][0], -base[j][1])
    sym_mode = rng.choice(['sym', 'indep', 'xmirror'])
    outer = {}
    for j in range(mid):
        md = rng.choice(['es', 'greedy', 'chain'])
        if j == mid - 1:
            md = 'chain' if rng.random() < 0.7 else md      # the dangerous cluster of Step 4
        outer[j] = outer_contents(rng, k, j, md)
        if sym_mode == 'sym':
            outer[n - j] = normalize([(-x, -y) for (x, y) in outer[j]])
        elif sym_mode == 'xmirror':
            # x-mirror image with independently perturbed y; must satisfy (H5) for index n-j
            Q = [(-x, -y + rng.randint(-1, 1)) for (x, y) in outer[j]]
            lc, lk = longest_cup_cap(Q) if len(Q) else (0, 0)
            from rg import collinear_triples
            if lc <= n - j + 1 and lk <= k - (n - j) - 1 and not collinear_triples(Q):
                outer[n - j] = normalize(Q)
            else:
                outer[n - j] = normalize([(-x, -y) for (x, y) in outer[j]])
        else:
            md2 = rng.choice(['es', 'greedy', 'chain'])
            if n - j == mid + 1:
                md2 = 'chain' if rng.random() < 0.7 else md2
            outer[n - j] = outer_contents(rng, k, n - j, md2)
    mmode = rng.choice(['M0', 'greedy', 'sym', 'pair'])
    midc = middle_contents(rng, m, mmode)
    # flatten the middle cluster horizontally so that its inside slopes are < 1/2
    c_mid = rng.choice([4, 8, 16, 64])
    midc = [(c_mid * x, y) for (x, y) in midc]
    c_out = rng.choice([10 ** e for e in range(4, 9)]) * rng.randint(1, 9)
    off = (0, 0)
    if rng.random() < 0.3:
        off = (rng.randint(-50, 50), rng.randint(-50, 50))
    if tune_h4:
        # largest integer s_mid (by doubling then bisection) such that (H4) holds
        def h4(s):
            cl = assemble(k, base, outer, midc, c_out, s, (off[0] * s, off[1] * s))
            return check(cl, k, xs, gp=False)['H4']
        if not h4(1):
            s_mid = 1
        else:
            lo, hi = 1, 2
            while h4(hi) and hi < 10 ** 12:
                lo, hi = hi, hi * 2
            while hi - lo > 1:
                md_ = (lo + hi) // 2
                if h4(md_):
                    lo = md_
                else:
                    hi = md_
            s_mid = lo
    else:
        s_mid = rng.choice([1, 10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6]) * rng.randint(1, 9)
    cl = assemble(k, base, outer, midc, c_out, s_mid, (off[0] * s_mid, off[1] * s_mid))
    return cl, dict(sym_mode=sym_mode, mmode=mmode, c_out=c_out, s_mid=s_mid, off=off, pert=pert)


def run(k, nsamp, seed, tune_frac):
    rng = random.Random(seed)
    LAM = 10 ** 15
    xs = base_abscissae(k)
    stats = dict(samples=0, degenerate=0, all_hold=0, all_hold_maxk1=0, only_h4_fail=0, only_h4_kgon=0,
                 counterexamples=0, h4_zero_pairs_seen=0)
    t0 = time.time()
    for it in range(nsamp):
        tune = rng.random() < tune_frac
        cl, info = sample(rng, k, LAM, tune_h4=tune)
        pts = [p for B in cl for p in B]
        stats['samples'] += 1
        if len(set(pts)) < len(pts) or len(set(p[0] for p in pts)) < len(pts):
            stats['degenerate'] += 1
            continue
        rep = check(cl, k, xs)
        if not rep['GP']:
            stats['degenerate'] += 1
            continue
        fails = [h for h in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5'] if not rep[h]]
        if not fails:
            stats['all_hold'] += 1
            stats['h4_zero_pairs_seen'] += 1 if rep['H4_zero_sum_skipped'] else 0
            m1, w1 = max_convex_cupcap(pts)
            m2 = max_convex_angular(pts)
            assert m1 == m2 and convex_position_bf(w1)
            if m1 >= k:
                stats['counterexamples'] += 1
                print("COUNTEREXAMPLE", info, cl)
            if m1 == k - 1:
                stats['all_hold_maxk1'] += 1
        elif fails == ['H4']:
            stats['only_h4_fail'] += 1
            m1, w1 = max_convex_cupcap(pts)
            if m1 >= k:
                stats['only_h4_kgon'] += 1
    stats['secs'] = round(time.time() - t0, 1)
    print("k=%d seed=%d tune_frac=%.2f %s" % (k, seed, tune_frac, stats))
    sys.stdout.flush()


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
