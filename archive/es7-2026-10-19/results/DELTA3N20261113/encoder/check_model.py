#!/usr/bin/env python3
"""Independent exact sign/coordinate checker; does not import either encoder.
COMPUTED, not an LRAT certification. All counts use exact integer arithmetic.
"""
import argparse
import itertools as it
import json
from pathlib import Path


def analyze(signs, m, n):
    triples = list(it.combinations(range(m), 3))
    if len(signs) != len(triples) or set(signs) - {'+', '-'}:
        raise ValueError('bad sign string')
    t = dict(zip(triples, (c == '+' for c in signs)))
    for a, b, c, d in it.combinations(range(m), 4):
        q = [t[a,b,c], t[a,b,d], t[a,c,d], t[b,c,d]]
        if sum(x != y for x, y in zip(q, q[1:])) > 1:
            raise ValueError('not a signotope')

    def cap(s):
        return all(not t[q] for q in it.combinations(s, 3))

    def convex(s):
        return all(t[a,b,c] == t[a,b,d] and t[a,c,d] == t[b,c,d]
                   for a, b, c, d in it.combinations(s, 4))

    mask = lambda s: sum(1 << x for x in s)
    caps = [mask(s) for s in it.combinations(range(m), 4) if cap(s)]
    cap5 = sum(cap(s) for s in it.combinations(range(m), 5))
    ngons = sum(convex(s) for s in it.combinations(range(m), n))
    targets = {mode: set() for mode in ('weak', 'cup', 'cap')}
    for g in it.combinations(range(m), n-1):
        if not convex(g):
            continue
        u, v = g[0], g[-1]
        targets['weak'].add(mask(g))
        targets['cup'].add(mask([u, v] + [p for p in g[1:-1] if t[u,p,v]]))
        targets['cap'].add(mask([u, v] + [p for p in g[1:-1] if not t[u,p,v]]))

    def upwards(seeds):
        out = bytearray(1 << m)
        for s in seeds:
            out[s] = 1
        # Full subset zeta transform, independent of the encoder's bounded deletion DAG.
        for p in range(m):
            bit = 1 << p
            for block in range(0, 1 << m, 2*bit):
                for x in range(bit):
                    out[block+bit+x] |= out[block+x]
        return out

    a = upwards(caps)
    answer = dict(label='COMPUTED', m=m, n=n, signs=signs, fourcaps=len(caps),
                  fivecaps=cap5, convex_ngons=ngons, valid=(cap5 == ngons == 0), modes={})
    full = (1 << m)-1
    for mode, seeds in targets.items():
        b = upwards(seeds)
        count, first = 0, None
        for delta in range(1 << m):
            if not a[delta] and not b[full ^ delta]:
                count += 1
                if first is None:
                    first = [p for p in range(m) if delta >> p & 1]
        answer['modes'][mode] = dict(targets=len(seeds), working_deltas=count, first_delta=first)
    return answer


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument('--fixture', type=Path)
    source.add_argument('--model', type=Path)
    ap.add_argument('--m', type=int)
    ap.add_argument('--n', type=int)
    ap.add_argument('--mode', choices=['weak', 'cup', 'cap'])
    args = ap.parse_args()
    if args.fixture:
        f = json.loads(args.fixture.read_text())
        m, n, signs = f['m'], f['n'], f['signs']
        if f.get('P') is not None:
            points = f['P']
            assert all(points[i][0] < points[i+1][0] for i in range(m-1))
            def det(a,b,c):
                return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
            determinants = [det(*p) for p in it.combinations(points,3)]
            assert all(determinants), 'degenerate point set'
            assert signs == ''.join('+' if d > 0 else '-' for d in determinants)
    else:
        m, n = args.m, args.n
        if m is None or n is None or not 4 <= m <= 20:
            raise ValueError('require --m 4..20 and --n')
        count = len(list(it.combinations(range(m), 3)))
        val = {}
        with args.model.open() as file:
            for line in file:
                if line.startswith('v '):
                    for literal in map(int, line.split()[1:]):
                        if 0 < abs(literal) <= count:
                            key = abs(literal)
                            assert key not in val or val[key] == (literal > 0)
                            val[key] = literal > 0
        if len(val) != count:
            raise ValueError('solver model omits orientation variables')
        signs = ''.join('+' if val[i] else '-' for i in range(1, count+1))
    result = analyze(signs, m, n)
    if args.mode:
        result['counterexample_mode'] = args.mode
        result['checked_counterexample'] = result['valid'] and result['modes'][args.mode]['working_deltas'] == 0
    print(json.dumps(result, sort_keys=True))
    if args.mode and not result['checked_counterexample']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
