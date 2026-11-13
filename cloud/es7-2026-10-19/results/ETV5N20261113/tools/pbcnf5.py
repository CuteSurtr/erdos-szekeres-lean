"""CNF for: exists h in {0,1}^N with h_i = 0 for the two fixed occupied states, sum h <= BUDGET, and every
row sum_{S} h >= d.  UNSAT with an LRAT proof accepted by cake_lpr certifies "holes >= BUDGET+1" over the
given rows, modulo this encoding (pysat CardEnc; brute-force self-test below).
usage: pbcnf5.py <rows.json: [[support, demand], ...]> <budget> <out.cnf>"""
import json, os, sys, hashlib, itertools, random
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def build(rows, budget, N, fixed):
    pool = IDPool(start_from=N + 1)
    var = lambda i: i + 1
    clauses = [[-var(i)] for i in fixed]
    lits = [var(i) for i in range(N) if i not in fixed]
    enc = CardEnc.atmost(lits=lits, bound=budget, vpool=pool, encoding=EncType.seqcounter)
    clauses += enc.clauses
    for s, d in rows:
        L = [var(i) for i in s if i not in fixed]
        if d <= 0: continue
        if d > len(L): return pool.top, clauses + [[]]
        if d == 1: clauses.append(L)
        else: clauses += CardEnc.atleast(lits=L, bound=d, vpool=pool, encoding=EncType.kmtotalizer).clauses
    return pool.top, clauses

def selftest():
    from pysat.solvers import Cadical153
    rng = random.Random(3)
    for t in range(200):
        n = 10; fixed = sorted(rng.sample(range(n), 2)); budget = rng.randrange(1, 6)
        rows = [(sorted(rng.sample(range(n), rng.randrange(2, 7))), rng.randrange(1, 4)) for _ in range(rng.randrange(1, 7))]
        brute = any(all(sum(h[i] for i in s) >= d for s, d in rows) and sum(h) <= budget and all(h[i] == 0 for i in fixed)
                    for h in itertools.product([0, 1], repeat=n))
        top, cls = build(rows, budget, n, fixed)
        if any(len(c) == 0 for c in cls): sat = False
        else:
            with Cadical153(bootstrap_with=cls) as S: sat = S.solve()
        assert sat == brute, (rows, budget, sat, brute)
    print('encoding selftest ok (200 random instances)')

if __name__ == '__main__':
    import etv_common as ec
    selftest()
    rows = json.load(open(sys.argv[1])); budget = int(sys.argv[2]); out = sys.argv[3]
    top, cls = build(rows, budget, ec.N, ec.FIXED_OCC)
    with open(out, 'w') as f:
        f.write(f'p cnf {top} {len(cls)}\n')
        for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
    print('rows', len(rows), 'vars', top, 'clauses', len(cls), 'sha256', hashlib.sha256(open(out, 'rb').read()).hexdigest())
