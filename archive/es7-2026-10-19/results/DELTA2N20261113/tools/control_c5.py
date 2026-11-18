"""C5: on ALL signotopes with m points (no other restriction): a subset is a convex set in the 4-subset sense
<=> it is a weak gon (a cap and a cup with common end points covering the subset).  Exhaustive for m = 5, 6, 7."""
import itertools, sys
from pysat.solvers import Cadical153
comb = itertools.combinations
for m in (5, 6, 7):
    tri = {t: i + 1 for i, t in enumerate(comb(range(m), 3))}
    cl = []
    for i, j, k, l in comb(range(m), 4):
        s = [tri[i, j, k], tri[i, j, l], tri[i, k, l], tri[j, k, l]]
        for p, q, r in comb(range(4), 3): cl.append([-s[p], s[q], -s[r]]); cl.append([s[p], -s[q], s[r]])
    cnt = 0; nsub = 0
    with Cadical153(bootstrap_with=cl) as S:
        while S.solve():
            mod = S.get_model(); o = {t: mod[v - 1] > 0 for t, v in tri.items()}
            S.add_clause([-mod[v - 1] for v in tri.values()]); cnt += 1
            for k in range(4, m + 1):
                for G in comb(range(m), k):
                    conv = all(o[x, y, z] == o[x, y, w] and o[x, z, w] == o[y, z, w] for x, y, z, w in comb(G, 4))
                    u, v = G[0], G[-1]; A = [g for g in G[1:-1] if not o[u, g, v]]; B = [g for g in G[1:-1] if o[u, g, v]]
                    c = [u] + A + [v]; d = [u] + B + [v]
                    weak = all(not o[c[i], c[i + 1], c[i + 2]] for i in range(len(c) - 2)) and all(o[d[i], d[i + 1], d[i + 2]] for i in range(len(d) - 2))
                    assert conv == weak, (m, G); nsub += 1
    print('m =', m, 'signotopes', cnt, 'subsets checked', nsub, 'convex(4-subset test) == weak gon: OK', flush=True)
