#!/usr/bin/env python3
"""Probe a stronger auxiliary lemma, not Delta itself.

Compare the minimum cup-side transversal with the minimum such transversal
without a four-cap. Integer geometry and cardinality encoding are implemented
here. SAT is only a COMPUTED verdict until the saved CNF has an LRAT certificate.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

from pysat.solvers import Glucose4


def cross(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


class Geometry:
    def __init__(self, points):
        self.P = sorted(map(tuple, points))
        self.m = len(self.P)
        assert len({p[0] for p in self.P}) == self.m
        self.sign = {}
        for i, j, k in itertools.combinations(range(self.m), 3):
            c = cross(self.P[i], self.P[j], self.P[k])
            assert c != 0
            self.sign[i, j, k] = 1 if c > 0 else -1
        self.cap, self.cup = self.between(-1), self.between(1)
        self.maxcap = max(self.cap.values(), default=min(self.m, 1))
        self.gon = max((self.cap[e]+self.cup[e]-2 for e in self.cap), default=0)

    def between(self, sign):
        out = {}
        for u in range(self.m):
            dp = {}
            for j in range(u+1, self.m):
                dp[u, j] = 2
                for i in range(u+1, j):
                    best = 0
                    for h in range(u, i):
                        if dp[h, i] and self.sign[h, i, j] == sign:
                            best = max(best, dp[h, i]+1)
                    dp[i, j] = best
                out[u, j] = max(dp[i, j] for i in range(u, j))
        return out

    def cup_witnesses(self, red, n):
        rest = [i for i in range(self.m) if i not in red]
        out = []
        for iu, u in enumerate(rest):
            targets = {v for v in rest[iu+1:] if self.cap[u, v]+self.cup[u, v] == n+1}
            if not targets:
                continue
            dp = {}
            tail = rest[iu:]
            for jj, j in enumerate(tail[1:], 1):
                dp[u, j] = (u, j)
                for ii in range(1, jj):
                    i = tail[ii]
                    candidates = [dp[h, i]+(j,) for h in tail[:ii]
                                  if dp[h, i] and self.sign[h, i, j] == 1]
                    dp[i, j] = max(candidates, key=len, default=())
                if j in targets:
                    cup = max((dp[i, j] for i in tail[:jj]), key=len)
                    if len(cup) == self.cup[u, j]:
                        out.append(cup)
        return out

    def four_caps(self):
        return [q for q in itertools.combinations(range(self.m), 4)
                if self.sign[q[:3]] == self.sign[q[1:]] == -1]


def cardinality(m):
    """Forward unary counter: threshold[j-1] follows when at least j x's hold.

    Actual prefix counts give a satisfying extension of these clauses. Thus
    negating threshold[k] expresses at most k selected original variables.
    """
    clauses, previous, variable = [], [], m
    for i in range(1, m+1):
        current = []
        for j in range(1, i+1):
            variable += 1
            current.append(variable)
            if j == 1:
                clauses.append([-i, variable])
            else:
                clauses.append([-i, -previous[j-2], variable])
            if j <= len(previous):
                clauses.append([-previous[j-1], variable])
        previous = current
    return clauses, previous, variable


class Probe:
    def __init__(self, geom, n, forbid_caps):
        self.geom, self.n = geom, n
        self.clauses, self.thresholds, self.nv = cardinality(geom.m)
        if forbid_caps:
            self.clauses += [[-i-1 for i in q] for q in geom.four_caps()]
        self.solver = Glucose4(bootstrap_with=self.clauses)
        self.cups = set()
        self.calls = 0

    def at_most(self, k):
        assumptions = [-self.thresholds[k]] if k < self.geom.m else []
        while True:
            self.calls += 1
            if not self.solver.solve(assumptions=assumptions):
                return None
            model = {v for v in self.solver.get_model() if v > 0}
            red = {i for i in range(self.geom.m) if i+1 in model}
            assert len(red) <= k
            cups = self.geom.cup_witnesses(red, self.n)
            if not cups:
                return sorted(red)
            for cup in cups:
                assert cup not in self.cups
                self.cups.add(cup)
                clause = [i+1 for i in cup]
                self.clauses.append(clause)
                self.solver.add_clause(clause)

    def dimacs(self, path, k):
        extra = [[-self.thresholds[k]]] if k < self.geom.m else []
        with open(path, 'w') as f:
            f.write(f'p cnf {self.nv} {len(self.clauses)+len(extra)}\n')
            for clause in self.clauses+extra:
                f.write(' '.join(map(str, clause))+' 0\n')


def check(points, n, out, tag):
    start = time.monotonic()
    g = Geometry(points)
    if n is None:
        n = g.gon+1
        if g.maxcap > 4 or n not in (6, 7, 8):
            return True
    assert g.maxcap <= 4 and g.gon < n
    bare = Probe(g, n, False)
    constrained = Probe(g, n, True)
    try:
        lo, hi, witness = -1, g.m, list(range(g.m))
        while hi-lo > 1:
            k = (hi+lo)//2
            sol = bare.at_most(k)
            if sol is None:
                lo = k
            else:
                hi, witness = len(sol), sol
        capped = constrained.at_most(hi)
        result = dict(tag=tag, n=n, m=g.m, maxcap=g.maxcap, maxgon=g.gon,
                      minimum=hi, bare=witness, cap_free=capped,
                      auxiliary_lemma_holds=capped is not None,
                      calls=[bare.calls, constrained.calls],
                      seconds=round(time.monotonic()-start, 3))
        if capped is None:
            d = out/'counterexample'
            d.mkdir(exist_ok=True)
            result['P'] = g.P
            assert hi > 0
            bare.dimacs(d/'unconstrained_lower.cnf', hi-1)
            constrained.dimacs(d/'cap_free_same_size.cnf', hi)
            result['cup_constraints'] = sorted(constrained.cups)
            (d/'witness.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k: v for k, v in result.items() if k not in ('P', 'cup_constraints')}), flush=True)
        return capped is not None
    finally:
        bare.solver.delete()
        constrained.solver.delete()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--limit', type=int, default=40)
    ap.add_argument('--all-pools', action='store_true')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    base = Path('/home/jay/research/data/etvthy-20261113')
    cases = []
    for name, n in [('etv858.json', 8), ('etv857.json', 8), ('etv757.json', 7)]:
        cases.append((json.loads((base/name).read_text()), n, name))
    pool_paths = sorted(base.glob('pool*.jsonl')) if args.all_pools else [base/'pool_main.jsonl']
    for path in pool_paths:
        for i, line in enumerate(path.open()):
            o = json.loads(line)
            cases.append((o['P'], None, f'{path.name}:{i}'))
            if not args.all_pools and len(cases) >= args.limit:
                break
    if args.all_pools:
        old = Path(__file__).resolve().parents[2]/'DELTA2N20261113'/'data'/'cex'
        for path in sorted(old.glob('*real.json')):
            o = json.loads(path.read_text())
            if o.get('a') == 5 and o.get('n') in (6, 7, 8):
                cases.append((o['P'], o['n'], path.name))
    for points, n, tag in cases:
        if not check(points, n, args.out, tag):
            return
    print(json.dumps(dict(status='DONE', cases=len(cases))), flush=True)


if __name__ == '__main__':
    main()
