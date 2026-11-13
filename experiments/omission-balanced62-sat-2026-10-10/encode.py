"""Exploratory exact Boolean encoding; not a Lean proof certificate."""
import hashlib
import itertools
import json
from pathlib import Path


class CNF:
    def __init__(self, variables):
        self.variables = variables
        self.clauses = []

    def clause(self, *lits):
        if any(x is True for x in lits):
            return
        items = set(x for x in lits if x is not False)
        if any(-x in items for x in items):
            return
        self.clauses.append(sorted(items, key=lambda x: (abs(x), x)))

    @staticmethod
    def neg(x):
        return not x if isinstance(x, bool) else -x

    def threshold(self, literals, bound):
        """Return a literal equivalent to sum(literals) >= bound.

        Each new variable s is equivalent to a OR (b AND x), where a
        represents at least j earlier inputs and b at least j-1 inputs.
        All four implication clauses are emitted, not just one direction.
        """
        if bound <= 0:
            return True
        if bound > len(literals):
            return False
        prev = [True] + [False] * bound
        for i, x in enumerate(literals, 1):
            nxt = [True] + [False] * bound
            for j in range(1, min(i, bound) + 1):
                a, b = prev[j], prev[j - 1]
                self.variables += 1
                s = self.variables
                self.clause(-s, a, b)
                self.clause(-s, a, x)
                self.clause(self.neg(a), s)
                self.clause(self.neg(b), -x, s)
                nxt[j] = s
            prev = nxt
        return prev[bound]


def verify_small():
    # Exhaustively validate that every primary assignment has exactly the
    # expected satisfiable output polarity. Propagate each full recurrence
    # assignment and also inspect every clause (including simplified ones).
    for n in range(1, 7):
        for bound in range(1, n + 1):
            cnf = CNF(n)
            output = cnf.threshold(list(range(1, n + 1)), bound)
            for bits in itertools.product((False, True), repeat=n):
                values = {i + 1: b for i, b in enumerate(bits)}
                v = n
                for i in range(1, n + 1):
                    for j in range(1, min(i, bound) + 1):
                        v += 1
                        values[v] = sum(bits[:i]) >= j
                assert values[output] == (sum(bits) >= bound)
                assert all(any(values[abs(t)] == (t > 0) for t in c)
                           for c in cnf.clauses)
                # Each gate's full truth table validates uniqueness of its
                # output; exhaustive primary assignments validate indexing.
    for a, b, x, s in itertools.product((False, True), repeat=4):
        clauses = ((not s or a or b), (not s or a or x),
                   (not a or s), (not b or not x or s))
        assert all(clauses) == (s == (a or (b and x)))


def main():
    verify_small()
    source = Path('experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json')
    raw = source.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72'
    model = json.loads(raw)
    n = len(model['states'])
    cnf = CNF(n)
    for row in model['constraints']:
        support = row['support']
        assert len(support) == len(set(support))
        assert all(0 <= s < n for s in support)
        literals = [s + 1 for s in support]
        if row['rhs'] == 1:
            cnf.clause(*literals)
        else:
            cnf.clause(cnf.threshold(literals, row['rhs']))
    cnf.clause(cnf.neg(cnf.threshold(list(range(1, n + 1)), 63)))
    out = Path('.cache/balanced62-sat-2026-10-10')
    path = out / 'balanced62.cnf'
    with path.open('w') as f:
        f.write(f'p cnf {cnf.variables} {len(cnf.clauses)}\n')
        for clause in cnf.clauses:
            f.write(' '.join(map(str, clause)) + ' 0\n')
    record = {'source': str(source), 'source_sha256': sha,
              'source_rows': len(model['constraints']), 'primary_variables': n,
              'variables': cnf.variables, 'clauses': len(cnf.clauses),
              'budget': 62, 'positive_variable_means': 'state is missing',
              'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'small_encoding_checks': 'passed; exhaustive primary assignments n<=6 and gate truth table'}
    (out / 'encoding.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
