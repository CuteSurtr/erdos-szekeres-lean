"""Independent pure-Python verification of the counterexample point sets in cex/ (coordinates only; no SAT, no siglib).
For each file: (1) the set is in general position with distinct x, has no a-cap and no convex n-gon (brute force,
convex position by the monotone-chain hull); (2) all (a-1)-caps and convex (n-1)-gons are listed by brute force;
(3) all working Deltas are listed by brute force over all subsets; (4) the refuted claim is re-checked."""
import sys, json, itertools, glob, os
comb = itertools.combinations
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def convex_position(pts):
    pts = sorted(pts); lo = []; up = []
    for p in pts:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return len(lo) + len(up) - 2 == len(pts)
def is_cap(P, K): return all(orient(P[K[i]], P[K[i + 1]], P[K[i + 2]]) < 0 for i in range(len(K) - 2))
def analyse(P, a, n, strong):
    m = len(P)
    assert all(P[i][0] < P[i + 1][0] for i in range(m - 1)), 'x not increasing'
    assert all(orient(P[i], P[j], P[k]) != 0 for i, j, k in comb(range(m), 3)), 'collinear triple'
    assert not any(is_cap(P, K) for K in comb(range(m), a)), 'has an a-cap'
    assert not any(convex_position([P[i] for i in G]) for G in comb(range(m), n)), 'has a convex n-gon'
    caps = [K for K in comb(range(m), a - 1) if is_cap(P, K)]
    gons = [G for G in comb(range(m), n - 1) if convex_position([P[i] for i in G])]
    cm = [sum(1 << i for i in K) for K in caps]; gm = [sum(1 << i for i in G) for G in gons]
    W = [D for D in range(1 << m) if not any(D & c == c for c in cm) and all(D & g for g in gm)
         and not (strong and any(D & g == g for g in gm))]
    return caps, gons, W
def check(rec):
    P = [tuple(p) for p in rec['P']]; a, n, m = rec['a'], rec['n'], rec['m']; kind = rec['kind']
    strong = rec.get('form') == 'strong'
    caps, gons, W = analyse(P, a, n, strong)
    L = {K[0] for K in caps}; R = {K[-1] for K in caps}
    msg = '%d caps, %d gons, %d working Deltas (%s)' % (len(caps), len(gons), len(W), 'strong' if strong else 'weak')
    assert W, 'no working Delta at all?!'
    if kind == 'threshold-1':
        for x in range(m + 1):
            D = sum(1 << p for p in range(m) if (p < x and p not in R) or (p >= x and p not in L))
            assert D not in W, 'threshold %d works' % x
        return msg + '; no threshold x gives a working Delta_x: VERIFIED'
    if kind in ('allow=QQ', 'allow=Q'):
        allowed = sum(1 << p for p in range(m) if not (p in L and (p in R or kind == 'allow=Q')))
    elif kind == 'allow=ends':
        allowed = sum(1 << p for p in ({G[0] for G in gons} | {G[-1] for G in gons}))
    elif kind in ('upper-chain', 'lower-chain', 'end-pair'):
        parts = []
        for G in gons:
            u, w = G[0], G[-1]
            up = [u] + [x for x in G[1:-1] if orient(P[u], P[x], P[w]) < 0] + [w]
            lo = [u] + [x for x in G[1:-1] if orient(P[u], P[x], P[w]) > 0] + [w]
            parts.append(sum(1 << p for p in (up if kind == 'upper-chain' else lo if kind == 'lower-chain' else [u, w])))
        good = [D for D in W if all(D & q for q in parts)]
        assert not good, 'a Delta meeting every %s exists' % kind
        return msg + '; none of them meets the %s of every gon: VERIFIED' % {'upper-chain': 'cap part', 'lower-chain': 'cup part', 'end-pair': 'pair of ends'}[kind]
    elif kind.startswith('must='):
        def is_cup(G): return all(orient(P[G[i]], P[G[i + 1]], P[G[i + 2]]) > 0 for i in range(len(G) - 2))
        if kind == 'must=cupR': F = {G[-1] for G in gons if is_cup(G)}
        elif kind == 'must=cupRL': F = {G[-1] for G in gons if is_cup(G)} | {G[0] for G in gons if is_cup(G)}
        elif kind == 'must=gonRQ': F = {G[-1] for G in gons} - L
        elif kind == 'must=Qall': F = set(range(m)) - L
        else: raise ValueError(kind)
        Fm = sum(1 << p for p in F)
        assert not any(D & Fm == Fm for D in W), 'a working Delta containing the must-set exists'
        return msg + '; no working Delta contains the must-set %s: VERIFIED' % sorted(F)
    elif kind == 'nosafe':
        # no safe point: for every p there is a working Delta' of P - p such that neither Delta' nor Delta'+p works
        Wset = set(W)
        for p in range(m):
            idx = [i for i in range(m) if i != p]
            _, _, Wp = analyse([P[i] for i in idx], a, n, strong)
            bad = False
            for D in Wp:
                full = sum(1 << idx[i] for i in range(m - 1) if D >> i & 1)
                if full not in Wset and (full | 1 << p) not in Wset: bad = True; break
            assert bad, 'point %d is safe' % p
        return msg + '; no point is safe: VERIFIED'
    else: raise ValueError(kind)
    assert not any(D & ~allowed == 0 for D in W), 'a working Delta inside the allowed set exists'
    return msg + '; allowed set %s contains no working Delta: VERIFIED' % [p for p in range(m) if allowed >> p & 1]
if __name__ == '__main__':
    for fn in sorted(glob.glob(os.path.join(sys.argv[1] if len(sys.argv) > 1 else 'cex', '*.json'))):
        rec = json.load(open(fn))
        if not rec.get('realized'): print(os.path.basename(fn), 'abstract only (not realized) - skipped'); continue
        print(os.path.basename(fn), '(a=%d, n=%d, %d points, %s):' % (rec['a'], rec['n'], rec['m'], rec['kind']), check(rec), flush=True)
