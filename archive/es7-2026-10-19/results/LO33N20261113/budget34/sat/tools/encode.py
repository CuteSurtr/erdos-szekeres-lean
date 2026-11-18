#!/usr/bin/env python3
"""Independent, standard-library-only finite-row threshold CNF emitter."""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path

BASE_SHA = '8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa'
POOL_SHA = '91a4e36f31712231ed1386576d6dcbe846ddf6c1b0d4de41e225bbdb4a18bcf8'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_inputs(base, pool, pool_sha=POOL_SHA, pool_count=812):
    assert sha(base) == BASE_SHA, 'base bytes changed'
    assert sha(pool) == pool_sha, 'frozen pool bytes changed'
    b = json.loads(gzip.decompress(Path(base).read_bytes()))
    p = json.loads(Path(pool).read_text())
    assert len(b['states']) == 154
    states = [tuple(s) for s in b['states']]
    assert len(set(states)) == 154 and states[0] == (0, 0, 0, 0, 0)
    expected = {q + (0,) for q in itertools.product(range(7), repeat=4)
                if all(q[i] >= q[i+1] for i in range(3))
                and (q[0] < 6 or q[1] == 6)}
    assert set(states) == expected
    assert len(b['constraints']) == 2650 and len(p) == pool_count
    rows = []
    for origin, data in [('base', b['constraints']), ('pool', p)]:
        for index, row in enumerate(data):
            support, d = row['support'], row['rhs']
            assert isinstance(support, list) and support
            assert all(type(i) is int and 0 <= i < 154 for i in support)
            assert len(support) == len(set(support)), (origin, index, 'duplicates')
            assert type(d) is int and 1 <= d <= len(support)
            if origin == 'pool':
                assert d == 1
            rows.append({'origin': origin, 'index': index,
                         'support': support, 'rhs': d})
    F = [i for i, s in enumerate(states) if s[0] >= 5]
    Lo = [i for i, s in enumerate(states) if s[0] <= 4]
    assert len(F) == 84 and len(Lo) == 70
    assert not set(F) & set(Lo) and set(F) | set(Lo) == set(range(154))
    return states, rows, F, Lo


def neg(lit):
    return not lit if type(lit) is bool else -lit


class CounterCNF:
    def __init__(self, out=None, n=154, retain=False):
        self.out, self.nv, self.nc, self.nl = out, n, 0, 0
        self.clauses = [] if retain else None
        self.gates = [] if retain else None

    def clause(self, *lits):
        if any(lit is True for lit in lits):
            return
        ls = set(lit for lit in lits if lit is not False)
        if any(-lit in ls for lit in ls):
            return
        ls = sorted(ls, key=lambda v: (abs(v), v))
        self.nc += 1
        self.nl += len(ls)
        if self.out:
            self.out.write(' '.join(map(str, ls)) + ' 0\n')
        if self.clauses is not None:
            self.clauses.append(ls)

    def gate(self, a, x, b):
        self.nv += 1
        y = self.nv
        self.clause(neg(a), y)
        self.clause(neg(x), neg(b), y)
        self.clause(-y, a, x)
        self.clause(-y, a, b)
        if self.gates is not None:
            self.gates.append((y, a, x, b))
        return y

    def threshold(self, xs, k):
        if k <= 0:
            return True
        if k > len(xs):
            return False
        prev = [True] + [False] * k
        for i, x in enumerate(xs, 1):
            curr = [True] + [False] * k
            for j in range(1, min(i, k) + 1):
                curr[j] = self.gate(prev[j], x, prev[j-1])
            prev = curr
        return prev[k]

    def atleast(self, xs, d):
        if d == 1:
            self.clause(*xs)
        else:
            self.clause(self.threshold(xs, d))

    def atmost(self, xs, k):
        self.clause(neg(self.threshold(xs, k+1)))


def controls():
    gate_cases = 0
    for a, x, b, y in itertools.product((False, True), repeat=4):
        clauses = ((not a or y), (not x or not b or y),
                   (not y or a or x), (not y or a or b))
        assert all(clauses) == (y == (a or (x and b)))
        gate_cases += 1
    counter_cases = 0
    def val(lit, assignment):
        if type(lit) is bool:
            return lit
        return assignment[abs(lit)] == (lit > 0)
    for n in range(1, 9):
        for k in range(n+2):
            c = CounterCNF(n=n, retain=True)
            out = c.threshold(list(range(1, n+1)), k)
            for bits in itertools.product((False, True), repeat=n):
                assignment = dict(enumerate(bits, 1))
                for y, a, x, b in c.gates:
                    assignment[y] = val(a, assignment) or (
                        val(x, assignment) and val(b, assignment))
                assert all(any(val(l, assignment) for l in row) for row in c.clauses)
                assert val(out, assignment) == (sum(bits) >= k)
                counter_cases += 1
    return {'gate_truth_cases': gate_cases, 'counter_input_threshold_cases': counter_cases,
            'result': 'PASS', 'arithmetic': 'exact integers and Booleans'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    ap.add_argument('--pool', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--slice', type=int, choices=(19, 20))
    ap.add_argument('--pool-sha', default=POOL_SHA)
    ap.add_argument('--pool-count', type=int, default=812)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    assert not (out/'system.cnf').exists(), 'exclusive output already exists'
    states, rows, F, Lo = read_inputs(a.base, a.pool, a.pool_sha, a.pool_count)
    result = controls()
    extra = [{'origin': 'capacity', 'index': 'F', 'support': F, 'rhs': a.slice or 19},
             {'origin': 'capacity', 'index': 'Lo', 'support': Lo,
              'rhs': 34-a.slice if a.slice else 14}]
    rows += extra
    mapping = []
    body = out/'system.body'
    with body.open('w') as stream:
        c = CounterCNF(stream)
        c.clause(-1)
        for row in rows:
            first = c.nc+1
            c.atleast([i+1 for i in row['support']], row['rhs'])
            mapping.append({'origin': row['origin'], 'index': row['index'],
                            'first_clause': first, 'last_clause': c.nc})
        first = c.nc+1
        c.atmost(list(range(1, 155)), 34)
        mapping.append({'origin': 'budget', 'first_clause': first, 'last_clause': c.nc})
    with (out/'system.cnf').open('w') as f, body.open() as src:
        f.write(f'p cnf {c.nv} {c.nc}\n')
        for line in src:
            f.write(line)
    meta = {'base': str(Path(a.base).resolve()), 'pool': str(Path(a.pool).resolve()),
            'base_sha256': sha(a.base), 'pool_sha256': sha(a.pool),
            'cnf_sha256': sha(out/'system.cnf'), 'variables': c.nv,
            'clauses': c.nc, 'literals': c.nl, 'base_rows': 2650,
            'pool_rows': a.pool_count, 'rows_including_capacities': len(rows),
            'slice': a.slice, 'estimated_initial_cadical_MiB':
            [round(c.nl*150/2**20, 2), round(c.nl*250/2**20, 2)],
            'controls': result, 'variable_1_is_hole_0': True,
            'budget': 34, 'F': F, 'Lo': Lo}
    (out/'encoding.json').write_text(json.dumps(meta, indent=2)+'\n')
    (out/'row-clauses.json').write_text(json.dumps(mapping, indent=2)+'\n')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
