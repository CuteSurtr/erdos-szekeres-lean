"""Small helpers on abstract signotopes given as dict triple -> bool (True = cup)."""
import itertools
comb = itertools.combinations
def from_str(s, m):
    return {t: c == '+' for t, c in zip(comb(range(m), 3), s)}
def ranks(o, m, idx=None):
    """beta (longest cup ending), omega (longest cup starting), cm (longest cap ending), cp (longest cap starting);
    computed inside the index set idx (default all)."""
    idx = list(range(m)) if idx is None else sorted(idx)
    E = {}   # (i,j,sign) -> longest chain ending with edge (i,j)
    for b in range(len(idx)):
        for a_ in range(b):
            i, j = idx[a_], idx[b]
            for sg in (True, False):
                best = 2
                for c in range(a_):
                    h = idx[c]
                    if o[h, i, j] == sg: best = max(best, E[h, i, sg] + 1)
                E[i, j, sg] = best
    St = {}
    for a_ in range(len(idx) - 1, -1, -1):
        for b in range(len(idx) - 1, a_, -1):
            i, j = idx[a_], idx[b]
            for sg in (True, False):
                best = 2
                for c in range(b + 1, len(idx)):
                    k = idx[c]
                    if o[i, j, k] == sg: best = max(best, St[j, k, sg] + 1)
                St[i, j, sg] = best
    beta = {p: max([1] + [E[i, p, True] for i in idx if i < p]) for p in idx}
    cm = {p: max([1] + [E[i, p, False] for i in idx if i < p]) for p in idx}
    omega = {p: max([1] + [St[p, j, True] for j in idx if j > p]) for p in idx}
    cp = {p: max([1] + [St[p, j, False] for j in idx if j > p]) for p in idx}
    return beta, omega, cm, cp
def conv(o, G):
    return all(o[x, y, z] == o[x, y, w] and o[x, z, w] == o[y, z, w] for x, y, z, w in comb(G, 4))
def gons(o, m, k, idx=None):
    idx = range(m) if idx is None else sorted(idx)
    return [G for G in comb(idx, k) if conv(o, G)]
def caps(o, m, k, idx=None):
    idx = range(m) if idx is None else sorted(idx)
    return [K for K in comb(idx, k) if all(not o[K[i], K[i + 1], K[i + 2]] for i in range(k - 2))]
def cups(o, m, k, idx=None):
    idx = range(m) if idx is None else sorted(idx)
    return [K for K in comb(idx, k) if all(o[K[i], K[i + 1], K[i + 2]] for i in range(k - 2))]
def bits(D, m): return [i for i in range(m) if D >> i & 1]
