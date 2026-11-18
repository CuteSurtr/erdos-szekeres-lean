"""Pointwise rules in Baek's coordinates for a = 4 (exhaustive data, SAT over the rule space).
Baek: label s(p,q) = 2 if some r > q makes (p,q,r) a cap, else 1; beta(p) = longest cup ending at p;
alpha(p) = longest cup ending at p whose last edge has label 1 (1 if none).  p -> (alpha, beta) is injective into
T = {1 <= alpha <= beta <= n-1}.  Rule: Delta_F = {p : (alpha(p), beta(p)) in F} for a fixed F subset of T.
Question: is there an F such that Delta_F works (strong or weak form) for EVERY (4,n)-valid signotope in the data?
Data: all valid signotopes with up to maxm points (incremental enumeration as in control_c6.py).
usage: baek_rule.py n maxm weak|strong [mirror]"""
import sys, itertools, time
from pysat.solvers import Glucose4
comb = itertools.combinations
a = 4; n, maxm, form = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
strong = form == 'strong'
def ti(i, j, k): return k * (k - 1) * (k - 2) // 6 + j * (j - 1) // 2 + i
exec(open('control_c6.py').read().split("def has_delta")[0].split("strong = form == 'strong'")[1])   # extensions, valid_new
def stats(sig, m):
    o = lambda x, y, z: sig[ti(x, y, z)]
    lab = {(p, q): (2 if any(not o(p, q, r) for r in range(q + 1, m)) else 1) for p, q in comb(range(m), 2)}
    E = {}
    for j in range(m):
        for i in range(j):
            best = 2
            for h in range(i):
                if o(h, i, j) and E[h, i] + 1 > best: best = E[h, i] + 1
            E[i, j] = best
    beta = [max([1] + [E[i, j] for i in range(j)]) for j in range(m)]
    alpha = [max([1] + [E[i, j] for i in range(j) if lab[i, j] == 1]) for j in range(m)]
    return alpha, beta
cells = {(i, j): k + 1 for k, (i, j) in enumerate((i, j) for j in range(1, n) for i in range(1, j + 1))}
sol = Glucose4(bootstrap_with=[[v, -v] for v in cells.values()]); t0 = time.time(); level = [()]; nsig = 0; feasible = True
for k in range(0, maxm):
    nxt = []
    for sig in level:
        for e in extensions(sig, k):
            s2 = sig + e
            if valid_new(s2, k): nxt.append(s2)
    level = nxt; m = k + 1
    if m >= n - 1:
        for sig in level:
            o = lambda x, y, z: sig[ti(x, y, z)]
            al, be = stats(sig, m); c = [cells[al[p], be[p]] for p in range(m)]
            assert len(set(c)) == m, 'statistic not injective'
            for K in comb(range(m), 3):
                if not o(*K): sol.add_clause([-c[p] for p in K])
            for G in comb(range(m), n - 1):
                if all(o(x, y, z) == o(x, y, w) and o(x, z, w) == o(y, z, w) for x, y, z, w in comb(G, 4)):
                    sol.add_clause([c[p] for p in G])
                    if strong: sol.add_clause([-c[p] for p in G])
            nsig += 1
    feasible = sol.solve()
    print('n=%d %s: after all valid signotopes with <= %d points (%d used): rule space %s  (%.0fs)' % (n, form, m, nsig, 'NON-EMPTY, e.g. F = %s' % sorted(k for k, v in cells.items() if sol.get_model()[v - 1] > 0) if feasible else 'EMPTY', time.time() - t0), flush=True)
    if not feasible: break
