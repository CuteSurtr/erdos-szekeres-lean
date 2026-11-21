"""review304-controls: exact controls for the balanced side (own code; no project imports).
usage: python run.py <phase> <seed> <seconds> <outprefix>
phases: random | greedy | structured | selftest
"""
import json, sys, time, random, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from esz import (orient, sort_check, sign_tensor, ranks, ranks_pure, states, longest_chains,
                 max_convex, max_convex_brute)

ESB = '<repo>'
OUT = '<scratch>/agents/review304-controls'
SRC = json.load(open(ESB + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
STATES = [tuple(s) for s in SRC['states']]
SIDX = {s: i for i, s in enumerate(STATES)}
Z = [i for i, f in enumerate(STATES) if f[0] <= 4 and f[4] == 0]
ZS = [i for i, f in enumerate(STATES) if f[0] == 5 and f[4] >= 1]
WIDE = [i for i, f in enumerate(STATES) if f[4] == 0]          # negative control: f(0) <= 5, f(4) = 0
ROWS = [(r['support'], r['rhs']) for r in SRC['constraints']]
ROWS_ALL = ROWS + [(Z, 15), (ZS, 15)]
NAMES = ['row%d' % i for i in range(len(ROWS))] + ['Zrow', 'Zsrow']
SUPP = np.zeros((len(ROWS_ALL), 252), dtype=np.int32)
for r, (sup, _) in enumerate(ROWS_ALL):
    SUPP[r, sup] = 1
RHS = np.array([rhs for _, rhs in ROWS_ALL], dtype=np.int32)


def analyse(pts, tag, stats, save_viol=True, do_rows=True):
    """pts: sorted, distinct x. Returns dict of per-set results (or None if not in general position)."""
    S, ok = sign_tensor(pts)
    if not ok:
        return None
    n = len(pts)
    st, mcap, mcup = states(S)
    res = {'n': n, 'mcap': mcap, 'mcup': mcup}
    if mcap >= 7 or mcup >= 7:
        res['balanced_type'] = False
        return res
    res['balanced_type'] = True
    idx = [SIDX[s] for s in st]                 # every state must be a catalog state
    res['distinct'] = len(set(idx)) == n        # (a)
    zown = [v for v in range(n) if idx[v] in set(Z)]
    zsown = [v for v in range(n) if idx[v] in set(ZS)]
    wown = [v for v in range(n) if idx[v] in set(WIDE)]
    zc = longest_chains(S, zown)
    zsc = longest_chains(S, zsown)
    wc = longest_chains(S, wown)
    res['z_owners'] = len(zown); res['zs_owners'] = len(zsown)
    res['z_ok'] = zc[0] <= 5 and zc[1] <= 5     # (b)
    res['zs_ok'] = zsc[0] <= 5 and zsc[1] <= 5  # (c)
    res['z_maxcap_cup'] = zc; res['zs_maxcap_cup'] = zsc
    res['wide_has6'] = wc[0] >= 6 or wc[1] >= 6  # negative control (b')
    res['first_two_ok'] = (st[0] == (0, 0, 0, 0, 0)) and (n < 2 or st[1] == (1, 0, 0, 0, 0))  # (d)
    mc = max_convex(S)
    res['maxconvex'] = mc
    res['octagon_free'] = mc <= 7
    if res['octagon_free'] and n >= 58:
        res['points'] = [list(p) for p in pts]
    if do_rows:
        h = np.ones(252, dtype=np.int32)
        h[idx] = 0
        slack = SUPP @ h - RHS
        res['min_slack'] = int(slack.min())
        res['n_tight'] = int((slack == 0).sum())
        viol = np.nonzero(slack < 0)[0].tolist()
        res['n_viol'] = len(viol)
        if viol:
            res['viol_rows'] = [NAMES[r] for r in viol[:20]]
            if res['octagon_free'] and save_viol:
                fn = '%s/VIOLATION_%s_%d.json' % (OUT, tag, int(time.time() * 1000) % 10**9)
                json.dump({'points': pts, 'states': st, 'state_idx': idx, 'violated': [
                    {'name': NAMES[r], 'support': list(map(int, ROWS_ALL[r][0])), 'rhs': int(ROWS_ALL[r][1]),
                     'lhs': int((SUPP[r] @ h))} for r in viol]}, open(fn, 'w'))
                res['saved'] = fn
    res['occupied'] = len(set(idx))
    return res


def prune_7(pts, rng, S=None):
    """Remove points until no 7-cap and no 7-cup (greedy on endpoints of rank>=7 edges).
    The sign tensor is computed once (exact) and restricted by index."""
    pts = list(pts)
    if S is None:
        S, ok = sign_tensor(pts)
        assert ok
    keep = list(range(len(pts)))
    while True:
        sub = S[np.ix_(keep, keep, keep)]
        Rc = ranks(sub, -1); Ru = ranks(sub, +1)
        bad = (Rc >= 7) | (Ru >= 7)
        if not bad.any():
            return [pts[i] for i in keep]
        cnt = bad.sum(axis=0) + bad.sum(axis=1)
        m = cnt.max()
        cands = np.nonzero(cnt == m)[0].tolist()
        keep.pop(rng.choice(cands))


def gp_clean(pts, rng):
    """Greedy filter in random order: keep a point iff its x is new and it is collinear with no kept pair (exact)."""
    pts = list(set(pts))
    rng.shuffle(pts)
    kept = []
    xs = set()
    for p in pts:
        if p[0] in xs:
            continue
        good = True
        n = len(kept)
        for i in range(n):
            a = kept[i]
            for j in range(i + 1, n):
                if orient(a, kept[j], p) == 0:
                    good = False
                    break
            if not good:
                break
        if good:
            kept.append(p); xs.add(p[0])
    return sorted(kept)


def agg_init():
    return {'sets': 0, 'balanced_type': 0, 'nonbalanced_type': 0, 'a_fail': 0, 'b_fail': 0, 'c_fail': 0,
            'd_fail': 0, 'octfree': 0, 'with_oct': 0, 'e_viol_octfree': 0, 'viol_with_oct_sets': 0,
            'wide_has6': 0, 'max_n_balanced': 0, 'max_n_octfree_bal': 0, 'max_occupied_octfree': 0,
            'max_occupied': 0, 'min_slack_octfree': None, 'max_tight_octfree': 0, 'max_z_owners': 0,
            'max_zs_owners': 0, 'sizes': {}, 'saved': []}


def agg_add(A, r):
    A['sets'] += 1
    if r is None:
        return
    if not r['balanced_type']:
        A['nonbalanced_type'] += 1
        return
    A['balanced_type'] += 1
    n = r['n']
    A['sizes'][str(n // 10 * 10)] = A['sizes'].get(str(n // 10 * 10), 0) + 1
    A['max_n_balanced'] = max(A['max_n_balanced'], n)
    A['a_fail'] += (not r['distinct']); A['b_fail'] += (not r['z_ok']); A['c_fail'] += (not r['zs_ok'])
    A['d_fail'] += (not r['first_two_ok']); A['wide_has6'] += r['wide_has6']
    A['max_occupied'] = max(A['max_occupied'], r['occupied'])
    A['max_z_owners'] = max(A['max_z_owners'], r['z_owners'])
    A['max_zs_owners'] = max(A['max_zs_owners'], r['zs_owners'])
    if r['octagon_free']:
        A['octfree'] += 1
        A['max_n_octfree_bal'] = max(A['max_n_octfree_bal'], n)
        A['max_occupied_octfree'] = max(A['max_occupied_octfree'], r['occupied'])
        A['e_viol_octfree'] += (r.get('n_viol', 0) > 0)
        ms = r.get('min_slack')
        if ms is not None:
            A['min_slack_octfree'] = ms if A['min_slack_octfree'] is None else min(A['min_slack_octfree'], ms)
        A['max_tight_octfree'] = max(A['max_tight_octfree'], r.get('n_tight', 0))
        if 'saved' in r:
            A['saved'].append(r['saved'])
    else:
        A['with_oct'] += 1
        A['viol_with_oct_sets'] += (r.get('n_viol', 0) > 0)


import bisect


def try_insert(pts, S, p):
    """Exact incremental insertion. Returns (new_pts, new_S) or None if p repeats an x or is collinear
    with two points of pts. Orientation signs of new triples come from Python-int determinants."""
    xs = [q[0] for q in pts]
    pos = bisect.bisect_left(xs, p[0])
    if pos < len(xs) and xs[pos] == p[0]:
        return None
    n = len(pts)
    sg = {}
    for i in range(n):
        a = pts[i]
        for j in range(i + 1, n):
            o = orient(a, pts[j], p)
            if o == 0:
                return None
            sg[(i, j)] = 1 if o > 0 else -1
    S2 = np.zeros((n + 1, n + 1, n + 1), dtype=np.int8)
    idx = [i if i < pos else i + 1 for i in range(n)]
    if n:
        S2[np.ix_(idx, idx, idx)] = S
    for (i, j), s in sg.items():
        if j < pos:
            S2[idx[i], idx[j], pos] = s
        elif i < pos:
            S2[idx[i], pos, idx[j]] = -s
        else:
            S2[pos, idx[i], idx[j]] = s
    return pts[:pos] + [p] + pts[pos:], S2


def sample_point(rng, mode, W, cs):
    if mode == 'square':
        return (rng.randrange(W), rng.randrange(W))
    if mode == 'disk':
        while True:
            p = (rng.randrange(-W, W), rng.randrange(-W, W))
            if p[0] * p[0] + p[1] * p[1] <= W * W:
                return p
    if mode == 'parabola':
        x = rng.randrange(-W, W)
        return (x, (x * x) // max(1, W // 8) + rng.randrange(W))
    if mode == 'perm':
        return (rng.randrange(10 * W), rng.randrange(10 * W))
    c = rng.choice(cs)
    return (c[0] + rng.randrange(W), c[1] + rng.randrange(W))


def phase_random(seed, secs, prefix):
    """Random greedy insertion keeping general position, no 7-cap, no 7-cup (octagons allowed),
    up to a random target size in [10, 60]."""
    rng = random.Random(seed)
    A = agg_init()
    t0 = time.time()
    recs = []
    while time.time() - t0 < secs:
        target = rng.randint(10, 60)
        mode = rng.choice(['square', 'disk', 'parabola', 'perm', 'clusters'])
        W = rng.choice([200, 1000, 5000])
        cs = [(rng.randrange(20 * W), rng.randrange(20 * W)) for _ in range(rng.randint(2, 6))]
        pts, S = [], np.zeros((0, 0, 0), dtype=np.int8)
        fails = 0
        while len(pts) < target and fails < 400:
            r = try_insert(pts, S, sample_point(rng, mode, W, cs))
            if r is None:
                fails += 1; continue
            P2, S2 = r
            if len(P2) >= 7 and (int(ranks(S2, -1).max()) >= 7 or int(ranks(S2, +1).max()) >= 7):
                fails += 1; continue
            pts, S = P2, S2
        r = analyse(pts, 'random', A)
        agg_add(A, r)
        if r is not None:
            r['mode'] = mode; r['target'] = target
            recs.append(r)
    A['elapsed'] = time.time() - t0
    json.dump({'agg': A, 'records': recs}, open(prefix + '.json', 'w'))
    print(json.dumps(A, indent=1))


def phase_greedy(seed, secs, prefix):
    """Random greedy insertion keeping general position, no 7-cap, no 7-cup and no convex octagon."""
    rng = random.Random(seed)
    A = agg_init()
    t0 = time.time()
    recs = []
    while time.time() - t0 < secs:
        W = rng.choice([100, 300, 1000, 3000])
        mode = rng.choice(['square', 'disk', 'clusters', 'parabola'])
        cs = [(rng.randrange(10 * W), rng.randrange(10 * W)) for _ in range(rng.randint(2, 5))]
        pts, S = [], np.zeros((0, 0, 0), dtype=np.int8)
        fails = 0
        maxfails = rng.choice([40, 80, 160])
        while fails < maxfails and time.time() - t0 < secs:
            r = try_insert(pts, S, sample_point(rng, mode, W, cs))
            if r is None:
                fails += 1; continue
            P2, S2 = r
            if len(P2) >= 7 and (int(ranks(S2, -1).max()) >= 7 or int(ranks(S2, +1).max()) >= 7):
                fails += 1; continue
            if len(P2) >= 8 and max_convex(S2) >= 8:
                fails += 1; continue
            pts, S = P2, S2
            fails = 0
        if len(pts) < 10:
            continue
        r = analyse(pts, 'greedy', A)
        agg_add(A, r)
        if r is not None:
            r['mode'] = mode; r['W'] = W
            recs.append(r)
    A['elapsed'] = time.time() - t0
    json.dump({'agg': A, 'records': recs}, open(prefix + '.json', 'w'))
    print(json.dumps(A, indent=1))



def load_sets():
    d = ESB + '/archive/es7-2026-10-19/results/ES8SYM/sets/'
    out = {}
    for f in sorted(os.listdir(d)):
        p = d + f
        rows = []
        try:
            for line in open(p):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                rows.append([int(t) for t in line.split()])
        except ValueError:
            continue
        if not rows:
            continue
        w = len(rows[0])
        if any(len(r) != w for r in rows):
            continue
        if w == 2:
            out[f] = [tuple(r) for r in rows]
        elif w == 4 and 'm=4' in open(p).readline():
            # Gaussian integers: sum_j w_j i^j = (w0 - w2) + i (w1 - w3)
            out[f] = [(r[0] - r[2], r[1] - r[3]) for r in rows]
    return out


def phase_structured(seed, secs, prefix):
    rng = random.Random(seed)
    A = agg_init()
    base = load_sets()
    t0 = time.time()
    recs = []
    info = {}
    # 1) each base set as is (if distinct x), full analysis
    for name, P in base.items():
        Q = sort_check(P)
        if Q is None:
            info[name] = {'n': len(P), 'distinct_x': False}
            continue
        S, ok = sign_tensor(Q)
        st, mcap, mcup = states(S)
        info[name] = {'n': len(Q), 'distinct_x': True, 'gp': ok, 'maxconvex': max_convex(S) if ok else None,
                      'mcap': mcap, 'mcup': mcup}
    print(json.dumps(info, indent=1))
    names = [k for k, v in info.items() if v.get('gp', True) and (v.get('maxconvex') or 0) <= 7]
    names = [k for k in base if k in names or not info[k].get('distinct_x', True)]
    print('base sets used:', names)
    # 2) random linear images (exact integer maps, det != 0), prune 7-caps/7-cups, optional random subset
    while time.time() - t0 < secs:
        name = rng.choice(names)
        P = base[name]
        while True:
            a, b, c, dd = [rng.randint(-7, 7) for _ in range(4)]
            if a * dd - b * c != 0:
                break
        # spread the x-direction a bit more with a large shear factor variant
        if rng.random() < 0.5:
            K = rng.choice([1, 3, 1000, 10**6])
            a, b = a * K + rng.randint(-3, 3), b * K + rng.randint(-3, 3)
            if a * dd - b * c == 0:
                continue
        Q = [(a * x + b * y, c * x + dd * y) for x, y in P]
        Q = sort_check(Q)
        if Q is None:
            continue
        S, ok = sign_tensor(Q)
        if not ok:
            continue
        Q = prune_7(Q, rng)
        if rng.random() < 0.3 and len(Q) > 12:
            m = rng.randint(10, len(Q))
            keep = sorted(rng.sample(range(len(Q)), m))
            Q = [Q[i] for i in keep]
        r = analyse(Q, 'struct', A)
        agg_add(A, r)
        if r is not None:
            r['base'] = name; r['map'] = [a, b, c, dd]
            recs.append(r)
    A['elapsed'] = time.time() - t0
    json.dump({'agg': A, 'records': recs, 'base_info': info}, open(prefix + '.json', 'w'))
    print(json.dumps(A, indent=1))


def phase_selftest(seed, secs, prefix):
    rng = random.Random(seed)
    t0 = time.time()
    nr = 0; nbr = 0; bad = []
    # ranks: vectorised vs loop implementation
    while time.time() - t0 < secs * 0.4:
        n = rng.randint(5, 25)
        pts = gp_clean([(rng.randrange(300), rng.randrange(300)) for _ in range(n)], rng)
        S, ok = sign_tensor(pts)
        for col in (-1, 1):
            R1 = ranks(S, col); R2 = ranks_pure(S, col)
            for u in range(len(pts)):
                for v in range(u + 1, len(pts)):
                    if int(R1[u, v]) != R2[u][v]:
                        bad.append(('rank', pts, col, u, v))
        nr += 1
    # max convex: DP vs brute force over subsets
    cnt = {}
    while time.time() - t0 < secs:
        n = rng.randint(8, 12)
        W = rng.choice([50, 300])
        pts = gp_clean([(rng.randrange(W), rng.randrange(W)) for _ in range(n)], rng)
        if rng.random() < 0.5:   # bias towards convex position: points near a circle
            R = W
            pts = []
            for _ in range(n):
                import math
                t = rng.random() * 2 * math.pi
                pts.append((int(R * math.cos(t)) + rng.randrange(3), int(R * math.sin(t)) + rng.randrange(3)))
            pts = gp_clean(pts, rng)
        S, ok = sign_tensor(pts)
        m1 = max_convex(S); m2 = max_convex_brute(pts)
        cnt[m2] = cnt.get(m2, 0) + 1
        if m1 != m2:
            bad.append(('maxconvex', pts, m1, m2))
        nbr += 1
    out = {'rank_sets': nr, 'maxconvex_sets': nbr, 'brute_value_hist': cnt, 'mismatches': len(bad)}
    json.dump({'summary': out, 'bad': bad[:10]}, open(prefix + '.json', 'w'))
    print(json.dumps(out))


if __name__ == '__main__':
    ph, seed, secs, prefix = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    {'random': phase_random, 'greedy': phase_greedy, 'structured': phase_structured,
     'selftest': phase_selftest}[ph](seed, secs, prefix)
