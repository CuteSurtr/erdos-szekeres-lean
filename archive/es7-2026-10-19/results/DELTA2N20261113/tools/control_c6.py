"""C6: independent enumeration of all (a,n)-valid signotopes by incremental extension (no SAT, no Enc):
chain DP for caps and for convex polygons (cap + cup with common ends).  Outputs the number of valid signotopes
per size (to be compared with the SAT enumeration of Enc.base in online_check.py / enum_all.py) and checks by brute
force (4-subset definition of convex sets, all subsets Delta) that every one of them has a working Delta.
usage: control_c6.py a n maxm weak|strong"""
import sys, itertools, time
comb = itertools.combinations
a, n, maxm, form = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
strong = form == 'strong'
def ti(i, j, k): return k * (k - 1) * (k - 2) // 6 + j * (j - 1) // 2 + i
def extensions(sig, k):
    pairs = sorted([(i, j) for j in range(k) for i in range(j)], key=lambda p: (p[1], p[0]))
    new = {}; out = []
    def ok(y, z):
        for x in range(y):
            s = (sig[ti(x, y, z)], new[x, y], new[x, z], new[y, z])
            if (s[0] != s[1]) + (s[1] != s[2]) + (s[2] != s[3]) > 1: return False
        return True
    def rec(t):
        if t == len(pairs): out.append(tuple(new[p] for p in pairs)); return
        y, z = pairs[t]
        for v in (True, False):
            new[y, z] = v
            if ok(y, z): rec(t + 1)
        del new[y, z]
    rec(0); return out
def valid_new(sig, k):
    """the new point k creates no a-cap and no convex n-gon (chain DP)"""
    E = {}
    for j in range(k + 1):
        for i in range(j):
            best = 2
            for h in range(i):
                if not sig[ti(h, i, j)] and E[h, i] + 1 > best: best = E[h, i] + 1
            E[i, j] = best
    if max([1] + [E[i, k] for i in range(k)]) >= a: return False
    for s in range(k):
        Dc = {}; Du = {}
        for j in range(s + 1, k + 1): Dc[s, j] = 2; Du[s, j] = 2
        for j in range(s + 1, k + 1):
            for i in range(s + 1, j):
                bc = bu = 0
                for h in range(s, i):
                    if not sig[ti(h, i, j)]:
                        if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                    else:
                        if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                Dc[i, j] = bc; Du[i, j] = bu
        cb = max(Dc[i, k] for i in range(s, k)); ub = max(Du[i, k] for i in range(s, k))
        if cb + ub - 2 >= n: return False
    return True
def has_delta(sig, m):
    o = lambda x, y, z: sig[ti(x, y, z)]
    caps = [sum(1 << i for i in K) for K in comb(range(m), a - 1) if all(not o(K[i], K[i + 1], K[i + 2]) for i in range(a - 3))]
    gons = [sum(1 << i for i in G) for G in comb(range(m), n - 1)
            if all(o(x, y, z) == o(x, y, w) and o(x, z, w) == o(y, z, w) for x, y, z, w in comb(G, 4))]
    for D in range(1 << m):
        if any(D & c == c for c in caps): continue
        if any(D & g == 0 for g in gons): continue
        if strong and any(D & g == g for g in gons): continue
        return True
    return False
t0 = time.time(); level = [()]; counts = []
for k in range(0, maxm):
    nxt = []
    for sig in level:
        for e in extensions(sig, k):
            s2 = sig + e
            if valid_new(s2, k): nxt.append(s2)
    level = nxt; counts.append(len(level))
    bad = sum(1 for sig in level if not has_delta(sig, k + 1)) if k + 1 >= n - 1 else 0
    print('a=%d n=%d %s: %d points: %d valid signotopes, without working Delta: %d   (%.0fs)' % (a, n, form, k + 1, len(level), bad, time.time() - t0), flush=True)
print('counts', counts)
