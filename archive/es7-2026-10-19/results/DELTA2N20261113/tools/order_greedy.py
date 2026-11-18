"""Greedy 'black iff necessary' in a canonical ORDER pi of the points (HEURISTIC sampling, exact per configuration):
process the points in the order pi; p goes into Delta iff some convex (n-1)-gon through p has all its other vertices
already processed and outside Delta.  Delta then meets every gon; the question is whether it is (a-1)-cap-free.
Orders: sort keys built from ranks (beta, omega, c-, c+), ties by x (both directions)."""
import sys, json, itertools, random, collections
from siglib import *
comb = itertools.combinations
def greedy(m, G, order):
    pos = {p: i for i, p in enumerate(order)}; D = set()
    byp = collections.defaultdict(list)
    for g in G: byp[max(g, key=lambda q: pos[q])].append(g)      # each gon is decided at its last vertex in the order
    for p in order:
        if any(all(q not in D for q in g if q != p) for g in byp[p]): D.add(p)
    return D
def keys(be, om, cm, cp, m):
    K = {}
    stats = {'x': lambda p: 0, 'beta': lambda p: be[p], 'omega': lambda p: om[p], 'cm': lambda p: cm[p], 'cp': lambda p: cp[p],
             'beta-omega': lambda p: be[p] - om[p], 'beta+omega': lambda p: be[p] + om[p], 'cm-cp': lambda p: cm[p] - cp[p], 'cm+cp': lambda p: cm[p] + cp[p],
             'beta+cm': lambda p: be[p] + cm[p], 'omega+cp': lambda p: om[p] + cp[p], 'beta-cp': lambda p: be[p] - cp[p], 'omega-cm': lambda p: om[p] - cm[p],
             'beta+cm-omega-cp': lambda p: be[p] + cm[p] - om[p] - cp[p]}
    for name, f in stats.items():
        for sgn in (1, -1):
            for tie in (1, -1):
                K['%s%s,tie %s' % ('+' if sgn > 0 else '-', name, 'x' if tie > 0 else '-x')] = sorted(range(m), key=lambda p: (sgn * f(p), tie * p))
    return K
if __name__ == '__main__':
    a, n, m, cnt, seed = [int(x) for x in sys.argv[1:6]]
    from eager_cert import Enc
    from pysat.solvers import Cadical153
    E = Enc(a, n, m, False, base_only=True); rnd = random.Random(seed); tris = list(comb(range(m), 3))
    ok = collections.Counter(); tot = 0
    with Cadical153(bootstrap_with=E.base) as s:
        for it in range(cnt):
            vs = list(range(1, E.ntri + 1)); rnd.shuffle(vs)
            if not s.solve(assumptions=[v if rnd.random() < 0.5 else -v for v in vs[:max(1, len(vs) // 10)]]): continue
            mod = s.get_model(); o = {t: mod[E.tri[t] - 1] > 0 for t in tris}
            be, om, cm, cp = ranks(o, m); G = gons(o, m, n - 1); K = [set(c) for c in caps(o, m, a - 1)]
            tot += 1
            for name, order in keys(be, om, cm, cp, m).items():
                D = greedy(m, G, order)
                if not any(k <= D for k in K): ok[name] += 1
    print(a, n, m, 'samples', tot)
    for name, v in ok.most_common(): print('   %-28s %d / %d' % (name, v, tot))
