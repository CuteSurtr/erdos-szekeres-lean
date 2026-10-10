"""Exact threshold circuits with shared prefix gates; experimental CNF only.

Each gate T(xs,k) means at least k literals of xs hold. Its four defining
clauses express T(xs,k) iff T(xs[:-1],k) or (xs[-1] and T(xs[:-1],k-1)).
This Python construction has finite exhaustive controls, not a Lean proof.
"""
from itertools import combinations
from math import comb


class Circuit:
    def __init__(self, originals):
        self.variables = originals
        self.clauses = []
        self.thresholds = {}

    @staticmethod
    def neg(x):
        return not x if type(x) is bool else -x

    def clause(self, *xs):
        if any(x is True for x in xs):
            return
        kept = set(x for x in xs if x is not False)
        if any(-x in kept for x in kept):
            return
        self.clauses.append(tuple(sorted(kept, key=lambda x: (abs(x), x))))

    def threshold(self, xs, k):
        xs = tuple(xs)
        if k <= 0:
            return True
        if k > len(xs):
            return False
        if len(xs) == 1:
            return xs[0]
        key = (xs, k)
        if key in self.thresholds:
            return self.thresholds[key]
        a = self.threshold(xs[:-1], k)
        b = self.threshold(xs[:-1], k - 1)
        x = xs[-1]
        self.variables += 1
        t = self.variables
        self.thresholds[key] = t
        self.clause(self.neg(a), t)
        self.clause(self.neg(b), -x, t)
        self.clause(-t, a, b)
        self.clause(-t, a, x)
        return t

    def at_least(self, xs, k):
        if k <= 0:
            return
        if k > len(xs):
            self.clause(False)
            return
        # All complements of (k-1)-subsets must contain a true literal.
        # This direct form avoids gates for the common rhs=1 and rhs=2 rows.
        if comb(len(xs), k - 1) <= 2 * len(xs):
            for omitted in combinations(xs, k - 1):
                self.clause(*(x for x in xs if x not in omitted))
        else:
            self.clause(self.threshold(xs, k))

    def at_most(self, xs, k):
        self.clause(self.neg(self.threshold(xs, k + 1)))

    def dimacs(self, originals):
        lines = [f"p cnf {self.variables} {len(self.clauses)}"]
        lines += [" ".join(map(str, c)) + " 0" for c in self.clauses]
        lines += [f"c {i+1} h_{i}" for i in range(originals)]
        return "\n".join(lines) + "\n"


def encode(n, rows, budget, occupied=(0,), outside_reference=None, radius=None):
    if type(budget) is not int or not 0 <= budget <= n:
        raise ValueError("Invalid budget")
    circuit = Circuit(n)
    for support, demand in rows:
        if len(set(support)) != len(support) or any(type(i) is not int or not 0 <= i < n for i in support):
            raise ValueError("Invalid support")
        if type(demand) is not int or not 0 <= demand <= len(support):
            raise ValueError("Invalid demand")
        circuit.at_least(tuple(i + 1 for i in sorted(support)), demand)
    circuit.at_most(tuple(range(1, n + 1)), budget)
    if outside_reference is not None:
        if radius is None or type(radius) is not int or radius < 0:
            raise ValueError("Invalid radius")
        if len(set(outside_reference)) != len(outside_reference) or any(
                type(i) is not int or not 0 <= i < n for i in outside_reference):
            raise ValueError("Invalid reference holes")
        circuit.at_most(tuple(i + 1 for i in range(n) if i not in outside_reference), radius)
    for i in occupied:
        if type(i) is not int or not 0 <= i < n:
            raise ValueError("Invalid occupied index")
        circuit.clause(-(i + 1))
    return circuit.dimacs(n)
