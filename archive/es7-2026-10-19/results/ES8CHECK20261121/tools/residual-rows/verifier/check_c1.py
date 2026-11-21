"""Exact controls for candidate C1 (first-vertex lemma on A_k = {f4 >= k}).

Usage: check_c1.py real57 <residual57_points.json>
       check_c1.py random <seed> <nsets> <nmin> <nmax> <mode>
       check_c1.py cupline <m>            (control without the no-8-cup hypothesis)
modes: unif (uniform box), para (points near y = x^2, cup-rich), mix (half near y=x^2, half near y=-x^2)
"""
import json, random, sys
from geo import Conf, sub, rat_points_to_int


def catalog_ok(f):
    f1, f2, f3, f4 = f
    return 6 >= f1 >= f2 >= f3 >= f4 >= 0 and (f1 < 6 or f2 == 6)


def check(P, tally, tag=''):
    C = Conf(P)
    n = C.n
    assert C.residual(), 'not residual'
    S = C.states()
    tally['sets'] += 1
    tally['points'] += n
    if len(set(S)) != n:
        tally['injective_fail'] += 1
    if not all(catalog_ok(f) for f in S):
        tally['catalog_fail'] += 1
    # label range
    for v in range(n):
        for u in range(v):
            d1, d2 = C.label(u, v)
            if not (1 <= d1 <= 4 and 1 <= d2 <= 6) or (d1, d2) == (1, 6):
                tally['label_fail'] += 1
    # pointwise (a): for every pair with F-(u,v) = 2: E+(u,v) + cupStart(v) <= 8
    for v in range(n):
        for u in range(v):
            if C.Fm[u][v] == 2:
                s = C.Ep[u][v] + C.cupStart[v]
                tally['pair_max'] = max(tally['pair_max'], s)
                if s > 8:
                    tally['pair_fail'] += 1
    # (a): f4(v) >= k  =>  cupStart(v) <= 7 - k, for k = 1..6
    for v in range(n):
        f4 = S[v][3]
        for k in range(1, 7):
            if f4 >= k and C.cupStart[v] > 7 - k:
                tally['a_fail'] += 1
        if f4 >= 1:
            tally['a_sum_max'] = max(tally['a_sum_max'], f4 + C.cupStart[v])
    # (b): owners of A_k contain no (8-k)-cup; record attained longest cup
    for k in range(1, 7):
        own = [v for v in range(n) if S[v][3] >= k]
        if not own:
            continue
        Ck = Conf(sub(C.P, own))
        tally['b_seen'][k] += 1
        if Ck.longcup > 7 - k:
            tally['b_fail'][k] += 1
        if Ck.longcup == 7 - k:
            tally['b_attained'][k] += 1
        tally['b_maxcup'][k] = max(tally['b_maxcup'][k], Ck.longcup)
        if k == 2:
            # N66 class: no 6-cap, no 6-cup, no octagon; count <= 55
            if not (Ck.longcap <= 5 and Ck.longcup <= 5 and Ck.gon() <= 7 and len(own) <= 55):
                tally['k2_class_fail'] += 1
    # negative control: owners of A_1 with a 6-cup (so k = 2 is needed for "no 6-cup")
    own1 = [v for v in range(n) if S[v][3] >= 1]
    if own1 and Conf(sub(C.P, own1)).longcup >= 6:
        tally['neg_A1_has_6cup'] += 1
    # negative control: the same statement with f3 in place of f4 (should FAIL somewhere)
    for v in range(n):
        f3 = S[v][2]
        if f3 >= 1 and f3 + C.cupStart[v] > 7:
            tally['neg_f3_variant_viol'] += 1
            break
    # negative control: off-by-one sharpening "cupStart(v) <= 6 - k" (should FAIL where attained)
    for v in range(n):
        f4 = S[v][3]
        if f4 >= 1 and f4 + C.cupStart[v] > 6:
            tally['neg_sharpened_viol'] += 1
            break
    # Lemma A(i): owners of F = {f1 >= 5} have no 5-cap; owners of A_2 & F: no 5-cap, no 6-cup, <= 35
    ownF = [v for v in range(n) if S[v][0] >= 5]
    if ownF:
        CF = Conf(sub(C.P, ownF))
        if CF.longcap > 4:
            tally['lemmaAi_fail'] += 1
    own2F = [v for v in range(n) if S[v][0] >= 5 and S[v][3] >= 2]
    if own2F:
        C2F = Conf(sub(C.P, own2F))
        tally['A2F_max'] = max(tally['A2F_max'], len(own2F))
        if C2F.longcap > 4 or C2F.longcup > 5 or len(own2F) > 35:
            tally['A2F_fail'] += 1
    return C, S


def new_tally():
    return dict(sets=0, points=0, injective_fail=0, catalog_fail=0, label_fail=0, pair_fail=0, pair_max=0,
                a_fail=0, a_sum_max=0, b_seen=[0] * 7, b_fail=[0] * 7, b_attained=[0] * 7, b_maxcup=[0] * 7,
                k2_class_fail=0, neg_A1_has_6cup=0, neg_f3_variant_viol=0, neg_sharpened_viol=0,
                lemmaAi_fail=0, A2F_fail=0, A2F_max=0)


def gon_witness(C):
    """Return (i, j) endpoints of a convex 8-gon (cap+cup with common ends), or None. Brute DP."""
    from geo import max_gon
    O, n = C.O, C.n
    NEG = -10 ** 9
    for i in range(n):
        capi = {}
        cupi = {}
        for v in range(i + 1, n):
            mc = mu = 2
            capi[(i, v)] = 2
            cupi[(i, v)] = 2
            for u in range(i + 1, v):
                bc = bu = NEG
                for t in range(i, u):
                    if O[t][u][v] < 0:
                        bc = max(bc, capi.get((t, u), NEG) + 1)
                    else:
                        bu = max(bu, cupi.get((t, u), NEG) + 1)
                if bc > 0:
                    capi[(u, v)] = bc
                    mc = max(mc, bc)
                if bu > 0:
                    cupi[(u, v)] = bu
                    mu = max(mu, bu)
            if mc + mu >= 10:
                return (i, v)
    return None


def prune_to_residual(P, rng):
    P = sorted(P)
    while True:
        C = Conf(P)
        n = C.n
        bad = [v for v in range(n) if C.capEnd[v] >= 6]
        if not bad:
            bad = [v for v in range(n) if C.cupEnd[v] >= 6 and C.capStart[v] >= 5]
        if not bad:
            bad = [v for v in range(n) if C.cupEnd[v] >= 8]
        if not bad:
            w = gon_witness(C)
            if w is not None:
                bad = list(w)
        if not bad:
            return P
        drop = rng.choice(bad)
        P = P[:drop] + P[drop + 1:]


def gen(rng, m, mode):
    while True:
        xs = rng.sample(range(-10 ** 6, 10 ** 6), m)
        pts = []
        for i, x in enumerate(xs):
            if mode == 'unif':
                y = rng.randint(-10 ** 6, 10 ** 6)
            elif mode == 'para':
                y = (x * x) // 10 ** 6 + rng.randint(-60000, 60000)
            else:
                sgn = 1 if i % 2 == 0 else -1
                y = sgn * (x * x) // 10 ** 6 + rng.randint(-60000, 60000)
            pts.append((x, y))
        pts.sort()
        try:
            Conf(pts[:3])  # cheap
            from geo import otable
            otable(pts)
            return pts
        except ValueError:
            continue


def report(t):
    out = dict(t)
    print(json.dumps(out))


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'real57':
        d = json.load(open(sys.argv[2]))
        P = rat_points_to_int(d['R_chart_points'])
        idx = sorted(range(len(P)), key=lambda i: P[i][0])
        P = [P[i] for i in idx]
        C = Conf(P)
        print('n', C.n, 'longcap', C.longcap, 'longcup', C.longcup, 'gon', C.gon(), 'junction', C.junction(),
              'residual', C.residual())
        t = new_tally()
        C, S = check(P, t)
        report(t)
        print('states with f4>=1:', sum(1 for f in S if f[3] >= 1), 'A2 owners:', sum(1 for f in S if f[3] >= 2),
              'F owners:', sum(1 for f in S if f[0] >= 5))
        # random subsets of the real set (subsets of residual sets are residual)
        rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 7)
        t2 = new_tally()
        for rep in range(int(sys.argv[4]) if len(sys.argv) > 4 else 60):
            m = rng.randint(20, 56)
            keep = sorted(rng.sample(range(C.n), m))
            check(sub(P, keep), t2)
        print('subsets of real57:')
        report(t2)
    elif what == 'random':
        seed, nsets, nmin, nmax, mode = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
        rng = random.Random(seed)
        t = new_tally()
        sizes = []
        for rep in range(nsets):
            P = gen(rng, rng.randint(nmin, nmax), mode)
            R = prune_to_residual(P, rng)
            sizes.append(len(R))
            check(R, t)
        t['size_min'] = min(sizes)
        t['size_max'] = max(sizes)
        t['mode'] = mode
        t['seed'] = seed
        report(t)
    elif what == 'cupline':
        # positive control for the checker: m points on y = x^2 (one m-cup, no caps, no junction).
        m = int(sys.argv[2])
        P = [(x, x * x) for x in range(m)]
        C = Conf(P)
        S = C.states()
        worst = max(S[v][3] + C.cupStart[v] for v in range(m) if S[v][3] >= 1)
        print('cupline m', m, 'longcup', C.longcup, 'longcap', C.longcap, 'junction', C.junction(),
              'max f4+cupStart', worst, '(statement (a) needs <= 7)')
