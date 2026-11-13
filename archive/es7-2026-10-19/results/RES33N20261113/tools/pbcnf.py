"""CNF for: exists h in {0,1}^154 with h0 = 0, sum h <= BUDGET, and every row sum_{S} h >= d.
UNSAT (with an LRAT proof checked by cake_lpr) certifies the exclusion of BUDGET holes over the given rows,
modulo the correctness of this encoding (pysat CardEnc, checked by brute force on small cases below)."""
import json, os, sys, hashlib, itertools, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from hfind import load_rows

def build(rows, budget, N=154):
    pool = IDPool(start_from=N + 1)
    var = lambda i: i + 1          # h_i -> DIMACS i+1
    clauses = [[-var(0)]]          # state 0 occupied
    lits = [var(i) for i in range(1, N)]
    enc = CardEnc.atmost(lits=lits, bound=budget, vpool=pool, encoding=EncType.seqcounter)
    clauses += enc.clauses
    for s, d in rows:
        L = [var(i) for i in s if i != 0]
        if d <= 0: continue
        if d > len(L): return None  # trivially UNSAT
        if d == 1:
            clauses.append(L)
        else:
            e = CardEnc.atleast(lits=L, bound=d, vpool=pool, encoding=EncType.kmtotalizer)
            clauses += e.clauses
    return pool.top, clauses

def selftest():
    # brute-force check of the encoding pattern on small random instances
    rng = random.Random(3)
    for t in range(60):
        n = 9; budget = rng.randrange(1, 5)
        rows = []
        for _ in range(rng.randrange(1, 6)):
            s = sorted(rng.sample(range(1, n), rng.randrange(2, 6))); rows.append((s, rng.randrange(1, 3)))
        brute = any(all(sum(h[i] for i in s) >= d for s, d in rows) and sum(h) <= budget
                    for h in ([0] + list(b) for b in itertools.product([0, 1], repeat=n - 1)))
        top, cls = build(rows, budget, N=n) or (None, None)
        from pysat.solvers import Cadical153
        if cls is None:
            sat = False
        else:
            with Cadical153(bootstrap_with=cls) as S: sat = S.solve()
        assert sat == brute, (rows, budget, sat, brute)
    print('encoding selftest ok (60 random instances)')

if __name__ == '__main__':
    selftest()
    budget = int(sys.argv[1]); out = sys.argv[2]
    rows = load_rows()
    top, cls = build(rows, budget)
    with open(out, 'w') as f:
        f.write(f'p cnf {top} {len(cls)}\n')
        for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
    print('rows', len(rows), 'vars', top, 'clauses', len(cls), 'sha256', hashlib.sha256(open(out, 'rb').read()).hexdigest())
