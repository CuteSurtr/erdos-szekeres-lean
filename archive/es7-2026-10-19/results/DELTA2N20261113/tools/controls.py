"""Positive controls on REAL point sets for the encoder of eager_cert.py (Enc).
C1  base clauses:  S(P) satisfies base(a,n,m)  <=>  P has no a-cap and no convex n-gon (independent geometric check).
C2  witnesses/pool: with the intended values of Y, Q4, Z, every witness clause holds, and for random Delta the pool
    clause is true  <=>  Delta fails geometrically (independent check: pyexact chains on the sub-point-sets).
C4  certificate sets of ETVTHY20261113 (real 5-cap-free octagon-/heptagon-free sets with a recorded strong Delta):
    random sub-samples P' of m points; Delta' = Delta & P' must make the pool clause FALSE under S(P').
usage: controls.py seed
"""
import sys, json, random, itertools
import pyexact_etvthy as px
from eager_cert import Enc, exact_sets
comb = itertools.combinations
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
R = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/ETVTHY20261113/data/'

def signs(P):
    P = sorted(P); m = len(P)
    return {t: px.orient(P[t[0]], P[t[1]], P[t[2]]) > 0 for t in comb(range(m), 3)}

def intended(E, o):
    """Full intended assignment var -> bool."""
    val = {v: o[t] for t, v in E.tri.items()}
    for K, lit in E.Y.items():
        iscap = all(not o[K[i], K[i + 1], K[i + 2]] for i in range(E.b - 2))
        if lit > 0: val[lit] = iscap
    c4 = {}
    for Q, v in E.Q4.items():
        x, y, z, w = Q; c4[Q] = (o[x, y, z] == o[x, y, w]) and (o[x, z, w] == o[y, z, w]); val[v] = c4[Q]
    if E.n - 1 != 4:
        for G, v in E.Z.items(): val[v] = all(c4[Q] for Q in comb(G, 4))
    return val

def sat(cl, val): return any(val[abs(l)] == (l > 0) for l in cl)

def geo_fail(P, D, a, n, strong, b):
    """Independent geometric check that Delta (index list into sorted P) fails."""
    P = sorted(P); Ds = set(D)
    PD = [P[i] for i in D]; PC = [P[i] for i in range(len(P)) if i not in Ds]
    def stats(X):
        if len(X) < 3: return (len(X) if len(X) <= 2 else 0, min(len(X), 2), min(len(X), 2))
        return px.summary(X)
    gD, capD, cupD = stats(PD); gC, capC, cupC = stats(PC)
    if capD >= b: return True
    if len(PC) >= n - 1 and gC >= n - 1: return True
    if strong and len(PD) >= n - 1 and gD >= n - 1: return True
    return False

def randset(m, style):
    while True:
        if style == 0: P = [(rnd.randrange(10**6), rnd.randrange(10**6)) for _ in range(m)]
        elif style == 1: P = [(x, x * x + rnd.randrange(-40, 41) * m) for x in rnd.sample(range(-60, 61), m)]      # near a parabola: many cups
        else: P = [(x, -x * x + rnd.randrange(-60, 61) * m) for x in rnd.sample(range(-60, 61), m)]               # near a cap
        P = sorted(set(P))
        if len(P) == m and len({p[0] for p in P}) == m:
            try: px.otable(P); return P
            except ValueError: pass

stats = {'C1_valid': 0, 'C1_invalid': 0, 'C2_delta_fail': 0, 'C2_delta_work': 0, 'C4_sets': 0, 'C4_delta_checked': 0}
# ---- C1 / C2
for (a, n, form) in [(5, 6, 'weak'), (5, 6, 'strong'), (4, 6, 'strong'), (4, 5, 'strong'), (5, 7, 'weak'), (5, 8, 'weak'), (6, 6, 'strong')]:
    for m in range(n - 1, 12):
        E = Enc(a, n, m, form == 'strong')
        for rep in range(40):
            P = randset(m, rep % 3); o = signs(P); val = intended(E, o)
            g, mc, mu = px.summary(P)
            valid_geo = (mc < a) and (g < n)
            valid_cnf = all(sat(c, val) for c in E.base)
            assert valid_geo == valid_cnf, ('C1 mismatch', a, n, m, P)
            stats['C1_valid' if valid_geo else 'C1_invalid'] += 1
            assert all(sat(c, val) for c in E.wit), 'witness clause violated by intended assignment'
            if not valid_geo: continue
            for r2 in range(25):
                D = sorted(rnd.sample(range(m), rnd.randrange(0, m + 1)))
                f_cnf = sat(E.pool_clause(D), val) if E.pool_clause(D) else False
                f_geo = geo_fail(P, D, a, n, form == 'strong', E.b)
                assert f_cnf == f_geo, ('C2 mismatch', a, n, m, P, D)
                stats['C2_delta_fail' if f_geo else 'C2_delta_work'] += 1
print('C1/C2 OK', stats, flush=True)
# ---- C4
W = '/home/jay/research/data/etvthy-20261113/'
_cache = {}
def load(fn, idx):
    if fn not in _cache:
        _cache[fn] = [json.load(open(W + fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(W + fn)]
    return sorted(tuple(p) for p in _cache[fn][idx])
for fn in ['conj8_certs.jsonl', 'conj7_certs.jsonl', 'conj8_sub64_certs.jsonl']:
    recs = [json.loads(l) for l in open(R + fn)]
    rnd.shuffle(recs)
    for rec in recs[:40]:
        P = load(rec['file'], rec['index']); Dfull = set(rec['Delta']); n = rec['k'] + 1
        assert len(P) == rec['n']
        for m in (11, 13):
            if len(P) < m: continue
            idx = sorted(rnd.sample(range(len(P)), m)); P2 = [P[i] for i in idx]
            D2 = [j for j, i in enumerate(idx) if i in Dfull]
            E = Enc(5, n, m, True); o = signs(P2); val = intended(E, o)
            assert all(sat(c, val) for c in E.base), 'C4 base'
            cl = E.pool_clause(D2)
            assert not (cl and sat(cl, val)), ('C4: recorded Delta fails in sub-sample', fn)
            assert not geo_fail(P2, D2, 5, n, True, 4)
            stats['C4_delta_checked'] += 1
        stats['C4_sets'] += 1
print('C4 OK', stats, flush=True)
