#!/usr/bin/env python3
"""rows-search exact control (own code, exact integers) for the per-edge extension lemma behind the chain classes:
 (E)  for every edge (v,w), m = points of the longest cap STARTING with (v,w), 2 <= m <= 6:
        f_v(6-m) <= 4  and  cupLabel(v,w) >= 1 + f_v(6-m)
 (E') mirror: m' = points of the longest cup starting with (v,w):  R_{7-m'}(f_v) <= 4 and capLabel(v,w) >= 1 + R_{7-m'}(f_v)
and the conclusion: the owners of every maximal (6,6)-chain-free class contain no 6-cap and no 6-cup; also the
state map is injective; and every 6-cup / 6-cap of H has a state sequence that no chain-free class contains.
Sets: random subsets of an own cup-cap construction X(7,7) (252 points) and random integer sets with no 7-cap/7-cup.
usage: chain_control.py NSUB NRAND SEED"""
import sys, random
import numpy as np
sys.path.insert(0, '<scratch>/agents/rows-search')
import chainrows as cr

def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def cupcap(k, l):
    """own construction: no k-cup, no l-cap, C(k+l-4, k-2) points (exact ints). cup = orient > 0."""
    if k <= 2 or l <= 2:
        return [(0, 0)]
    A = cupcap(k - 1, l)   # no (k-1)-cup: goes left
    B = cupcap(k, l - 1)   # no (l-1)-cap: goes right and far up
    def squash(P, F):
        return [(x * F, y) for x, y in P]
    span = lambda P: (max(y for _, y in P) - min(y for _, y in P)) + 1
    A = squash(A, 4 * span(A)); B = squash(B, 4 * span(B))
    ax = max(x for x, _ in A) + 1 - min(x for x, _ in B)
    B = [(x + ax, y) for x, y in B]
    W = max(x for x, _ in B) - min(x for x, _ in A) + 1
    H = max(abs(y) for _, y in A + B) + 1
    D = 8 * H * W   # B far above every line through two A points, and A far below lines through two B points
    return A + [(x, y + D) for x, y in B]

def labels(P):
    n = len(P)
    cap = [[0] * n for _ in range(n)]; cup = [[0] * n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            a = b = 1
            for t in range(u):
                o = orient(P[t], P[u], P[v])
                if o == 0: raise ValueError('collinear')
                if o < 0: a = max(a, cap[t][u] + 1)
                else: b = max(b, cup[t][u] + 1)
            cap[u][v], cup[u][v] = a, b   # labels = points - 1
    fcap = [[0] * n for _ in range(n)]; fcup = [[0] * n for _ in range(n)]   # forward: points of longest chain starting (u,v)
    for u in range(n - 1, -1, -1):
        for v in range(n - 1, u, -1):
            a = b = 2
            for w in range(v + 1, n):
                o = orient(P[u], P[v], P[w])
                if o < 0: a = max(a, fcap[v][w] + 1)
                else: b = max(b, fcup[v][w] + 1)
            fcap[u][v], fcup[u][v] = a, b
    return cap, cup, fcap, fcup

def states(n, cap, cup):
    F = []
    for v in range(n):
        F.append(tuple(max([cup[u][v] for u in range(v) if cap[u][v] >= i + 1] or [0]) for i in range(5)))
    return F

R = lambda f, k: sum(1 for x in f if x >= k)

def chains_of(n, P, kind, length, limit=20000, fwd=None):
    """enumerate chains (kind -1 cap, +1 cup) with exactly `length` points, up to limit."""
    out = []
    def ext(seq):
        if len(out) >= limit: return
        if len(seq) == length:
            out.append(tuple(seq)); return
        last = seq[-1]
        for w in range(last + 1, n):
            if len(seq) >= 2 and orient(P[seq[-2]], P[last], P[w]) * kind <= 0: continue
            if fwd is not None and len(seq) + fwd[last][w] - 1 < length: continue
            seq.append(w); ext(seq); seq.pop()
    for s in range(n):
        ext([s])
    return out

def check(P, classes, st):
    P = sorted(P); n = len(P)
    cap, cup, fcap, fcup = labels(P)
    assert max(max(r) for r in cap) <= 5 and max(max(r) for r in cup) <= 5, 'has a 7-cap or 7-cup'
    F = states(n, cap, cup)
    assert len(set(F)) == n, 'not injective'
    for v in range(n):
        for w in range(v + 1, n):
            m = fcap[v][w]
            if 2 <= m <= 6:
                j = 6 - m
                assert F[v][j] <= 4 and cup[v][w] >= 1 + F[v][j], ('E fails', v, w)
                st['E'] += 1
            m2 = fcup[v][w]
            if 2 <= m2 <= 6:
                k = 7 - m2
                assert R(F[v], k) <= 4 and cap[v][w] >= 1 + R(F[v], k), ("E' fails", v, w)
                st['Ep'] += 1
    idx = [cr.IDX[f] for f in F]
    for kind in (-1, 1):
        for ch in chains_of(n, P, kind, 6, fwd=(fcap if kind < 0 else fcup)):
            acc = CM[idx[ch[0]]].copy()
            for p in ch[1:]: acc &= CM[idx[p]]
            assert not acc.any(), 'a 6-chain inside a chain-free class'
            st['six_chains'] += 1
    occ = np.zeros(cr.N, bool); occ[idx] = True
    assert (CM[occ].sum(axis=0) <= 55).all()
    st['max_occ_in_class'] = max(st.get('max_occ_in_class', 0), int(CM[occ].sum(axis=0).max()))
    st['sets'] += 1; st['maxn'] = max(st['maxn'], n)

if __name__ == '__main__':
    nsub, nrand, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    import numpy as np
    A6 = list(cr.chain_free_classes(6, cr.S)); B6 = list(cr.chain_free_classes(6, cr.ST))
    MA = np.zeros((len(A6), cr.N)); MB = np.zeros((len(B6), cr.N))
    for i, c in enumerate(A6): MA[i, list(c)] = 1
    for i, c in enumerate(B6): MB[i, list(c)] = 1
    SZ = MA @ MB.T
    bitA = [sum(1 << j for j in c) for c in A6]; bitB = [sum(1 << j for j in c) for c in B6]
    inter = set(bitA[i] & bitB[j] for i, j in zip(*np.where(SZ >= 56)))
    inter = sorted(inter, key=lambda m: -bin(m).count('1'))
    classes = []
    for m in inter:
        if not any((m & ~g) == 0 for g in classes): classes.append(m)
    print('(6,6) maximal chain-free intersections with >= 56 states: %d; sizes %s; max over all pairs %d' % (
        len(classes), sorted(set(bin(m).count('1') for m in classes)), int(SZ.max())), flush=True)
    global CM
    CM = np.zeros((cr.N, len(classes)), bool)
    for ci, m in enumerate(classes):
        for j in range(cr.N):
            if m >> j & 1: CM[j, ci] = True
    X = cupcap(7, 7); assert len(X) == 252 and len({x for x, _ in X}) == 252
    st = dict(sets=0, E=0, Ep=0, six_chains=0, maxn=0)
    for t in range(nsub):
        keep = rng.uniform(0.06, 0.22)
        Q = [p for p in X if rng.random() < keep]
        if len(Q) >= 8: check(Q, classes, st)
    print('subsets of X(7,7):', st, flush=True)
    st2 = dict(sets=0, E=0, Ep=0, six_chains=0, maxn=0); tries = 0
    while st2['sets'] < nrand and tries < 50 * nrand:
        tries += 1
        n = rng.randint(14, 34)
        Q = list({(rng.randint(0, 10 ** 6), rng.randint(0, 10 ** 6)) for _ in range(n)})
        if len({x for x, _ in Q}) < len(Q): continue
        try:
            Q.sort(); cap, cup, _, _ = labels(Q)
        except ValueError:
            continue
        if max(max(r) for r in cap) > 5 or max(max(r) for r in cup) > 5: continue
        check(Q, classes, st2)
    print('random sets:', st2, 'tries', tries, flush=True)
    print('DONE', flush=True)
