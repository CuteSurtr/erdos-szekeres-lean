"""Threshold rule test (HEURISTIC sampling / exhaustive over an enumeration file).
Levels: M_0 = S, M_{i+1} = M_i minus (Q(M_i) u Q'(M_i)), where inside a set X
   Q(X)  = points of X that start no (a-1)-cap inside X,   Q'(X) = points of X that end no (a-1)-cap inside X.
Rule: Delta(x_0, x_1, ...) = union over levels i of  (Q'(M_i) & [0, x_i))  u  (Q(M_i) & [x_i, m)).
Question: do thresholds exist such that Delta is (a-1)-cap-free and meets every convex (n-1)-gon?"""
import sys, json, itertools, random, collections
from siglib import *
comb = itertools.combinations

def levels(o, m, a, depth):
    X = list(range(m)); out = []
    for i in range(depth):
        if not X: out.append(([], [])); continue
        be, om, cm, cp = ranks(o, m, X)
        Q = [p for p in X if cp[p] <= a - 2]; Qp = [p for p in X if cm[p] <= a - 2]
        out.append((Q, Qp))
        X = [p for p in X if p not in Q and p not in Qp]
    return out, X

def thr_rule(o, m, a, n, depth, need_strong=False):
    """Returns (weak_ok, thresholds) : some threshold vector gives a working weak Delta."""
    lv, rest = levels(o, m, a, depth)
    G = [sum(1 << i for i in g) for g in gons(o, m, n - 1)]
    K = [sum(1 << i for i in c) for c in caps(o, m, a - 1)]
    if not G: return True, None, lv
    for xs in itertools.product(range(m + 1), repeat=depth):
        D = 0
        for (Q, Qp), x in zip(lv, xs):
            for p in Qp:
                if p < x: D |= 1 << p
            for p in Q:
                if p >= x: D |= 1 << p
        if any(D & k == k for k in K): continue
        if all(D & g for g in G): return True, xs, lv
    return False, None, lv

if __name__ == '__main__':
    a, n, m, depth, cnt, seed = [int(x) for x in sys.argv[1:7]]
    from eager_cert import Enc
    from pysat.solvers import Cadical153
    E = Enc(a, n, m, False, base_only=True); rnd = random.Random(seed)
    tris = list(comb(range(m), 3)); st = collections.Counter(); bad = []
    with Cadical153(bootstrap_with=E.base) as s:
        for it in range(cnt):
            vs = list(range(1, E.ntri + 1)); rnd.shuffle(vs)
            ass = [v if rnd.random() < 0.5 else -v for v in vs[:max(1, len(vs) // 10)]]
            if not s.solve(assumptions=ass):
                st['unsat-assump'] += 1; continue
            mod = s.get_model(); o = {t: mod[E.tri[t] - 1] > 0 for t in tris}
            ok, xs, lv = thr_rule(o, m, a, n, depth)
            st['ok' if ok else 'FAIL'] += 1
            if not ok: bad.append(''.join('+' if o[t] else '-' for t in tris))
    print(a, n, m, 'depth', depth, dict(st), flush=True)
    if bad: json.dump(bad, open('thr_fail_a%d_n%d_m%d_d%d.json' % (a, n, m, depth), 'w'))
