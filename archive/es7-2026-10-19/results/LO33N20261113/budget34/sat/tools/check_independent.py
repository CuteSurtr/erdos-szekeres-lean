#!/usr/bin/env python3
"""Exact checks. Deliberately does not import the encoder or any finder."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
import os
import random
import sys
from pathlib import Path


def digest(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while block := f.read(1024*1024):
            h.update(block)
    return h.hexdigest()


def read(base, pool):
    with gzip.open(base, 'rt') as f:
        b = json.load(f)
    with open(pool) as f:
        p = json.load(f)
    assert len(b['states']) == 154 and len(b['constraints']) == 2650 and len(p) >= 812
    for r in b['constraints'] + p:
        assert len(r['support']) == len(set(r['support']))
        assert all(type(i) is int and 0 <= i < 154 for i in r['support'])
        assert type(r['rhs']) is int and 1 <= r['rhs'] <= len(r['support'])
    return b, p


def evaluate(h, b, p, check_budget=True, slice_value=None):
    assert len(h) == 154 and all(type(x) is int and x in (0, 1) for x in h)
    F = [i for i in range(154) if b['states'][i][0] >= 5]
    Lo = [i for i in range(154) if b['states'][i][0] < 5]
    assert len(F) == 84 and len(Lo) == 70
    rows = b['constraints'] + p + [
        {'support': F, 'rhs': slice_value or 19},
        {'support': Lo, 'rhs': 34-slice_value if slice_value else 14}]
    counts = [sum(h[i] for i in r['support']) for r in rows]
    bad = [i for i, (v, r) in enumerate(zip(counts, rows)) if v < r['rhs']]
    valid = not bad and h[0] == 0 and (not check_budget or sum(h) <= 34)
    return {'valid': valid, 'holes': sum(h), 'F_holes': sum(h[i] for i in F),
            'Lo_holes': sum(h[i] for i in Lo), 'h0': h[0], 'violated_rows': bad,
            'row_lhs': counts, 'row_margins': [v-r['rhs'] for v, r in zip(counts, rows)]}


def check_model(a, b, p):
    assignment = {}
    with open(a.solution) as f:
        for line in f:
            if not line.startswith('v '):
                continue
            for token in line.split()[1:]:
                lit = int(token)
                if not lit:
                    continue
                assert abs(lit) not in assignment or assignment[abs(lit)] == (lit > 0)
                assignment[abs(lit)] = lit > 0
    assert all(i in assignment for i in range(1, 155)), 'missing hole assignment'
    h = [int(assignment[i+1]) for i in range(154)]
    r = evaluate(h, b, p, slice_value=a.slice)
    clauses = 0
    with open(a.cnf) as f:
        for line in f:
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                _, _, nv, nc = line.split()
                assert set(range(1, int(nv)+1)) <= set(assignment), 'partial CNF witness'
                continue
            lits = [int(t) for t in line.split()]
            assert lits[-1] == 0 and 0 not in lits[:-1]
            assert any(assignment[abs(l)] == (l > 0) for l in lits[:-1]), clauses+1
            clauses += 1
    assert clauses == int(nc) and r['valid'], r
    r.update({'label': 'COMPUTED; exact integer SAT witness verified',
              'hole_bits_index_0_first': ''.join(map(str, h)),
              'hole_indices': [i for i, v in enumerate(h) if v],
              'cnf_clauses_checked': clauses, 'cnf_sha256': digest(a.cnf),
              'solution_sha256': digest(a.solution), 'base_sha256': digest(a.base),
              'pool_sha256': digest(a.pool), 'scope': 'abstract holes; no realization claimed'})
    Path(a.out).write_text(json.dumps(r, indent=2)+'\n')
    print(json.dumps({k: v for k, v in r.items() if k not in ('row_lhs', 'row_margins')}, indent=2))
    return r


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def hull(points):
    low, high = [], []
    for stack, seq in ((low, points), (high, points[::-1])):
        for p in seq:
            while len(stack) >= 2 and orient(stack[-2], stack[-1], p) <= 0:
                stack.pop()
            stack.append(p)
    return low[:-1]+high[:-1]


def real_controls(a, b, pool):
    rng = random.Random(30820261114)
    accepted, rejected = [], collections.Counter()
    state_index = {tuple(s): i for i, s in enumerate(b['states'])}
    # All coordinates, orientations, ranks and support sums are integers.
    assert 1 <= a.min_points <= a.max_points <= 16
    for attempt in range(a.attempts):
        n = a.min_points + attempt % (a.max_points-a.min_points+1)
        pts = [(i, rng.randrange(-100000, 100001)) for i in range(n)]
        if any(orient(*triple) == 0 for triple in itertools.combinations(pts, 3)):
            rejected['not_general_position'] += 1
            continue
        cup_end = {(u, v): 2 for u in range(n) for v in range(u+1, n)}
        cap_start = dict(cup_end)
        for v in range(n):
            for u in range(v):
                cup_end[u, v] = max([2] + [cup_end[t, u]+1 for t in range(u)
                    if orient(pts[t], pts[u], pts[v]) > 0])
        for u in reversed(range(n)):
            for v in range(u+1, n):
                cap_start[u, v] = max([2] + [cap_start[v, w]+1 for w in range(v+1, n)
                    if orient(pts[u], pts[v], pts[w]) < 0])
        if max(cap_start.values(), default=1) >= 6:
            rejected['six_cap'] += 1
            continue
        if any(len(hull(list(subset))) == 8 for subset in itertools.combinations(pts, 8)):
            rejected['convex_octagon'] += 1
            continue
        if any(max([1]+[cup_end[t, u] for t in range(u)]) >= 6
               and max([1]+[cap_start[u, v] for v in range(u+1, n)]) >= 5
               for u in range(n)):
            rejected['six_cup_five_cap_junction'] += 1
            continue
        # A second, exhaustive subsequence calculation checks both DP ranks.
        ec = {(u, v): 2 for u in range(n) for v in range(u+1, n)}
        sc = dict(ec)
        for length in range(3, n+1):
            for seq in itertools.combinations(range(n), length):
                signs = [orient(pts[seq[i]], pts[seq[i+1]], pts[seq[i+2]])
                         for i in range(length-2)]
                if all(v > 0 for v in signs):
                    ec[seq[-2], seq[-1]] = max(ec[seq[-2], seq[-1]], length)
                if all(v < 0 for v in signs):
                    sc[seq[0], seq[1]] = max(sc[seq[0], seq[1]], length)
        assert ec == cup_end and sc == cap_start
        occupied = []
        for v in range(n):
            shape = tuple(max([0] + [cup_end[u, v]-1 for u in range(v)
                              if i+1 <= 6-cap_start[u, v]]) for i in range(4)) + (0,)
            assert shape in state_index, (pts, shape)
            occupied.append(state_index[shape])
        assert len(set(occupied)) == n and occupied[0] == 0
        h = [int(i not in occupied) for i in range(154)]
        result = evaluate(h, b, pool, check_budget=False, slice_value=a.slice)
        assert result['valid'], (pts, result)
        accepted.append({'points': pts, 'owners': occupied, 'n': n,
                         'F_holes': result['F_holes'], 'Lo_holes': result['Lo_holes'],
                         'min_row_margin': min(result['row_margins']),
                         'all_rows_pass': True})
    assert len(accepted) >= a.minimum_controls
    out = {'label': 'COMPUTED exact integer positive controls', 'attempted': a.attempts,
           'accepted': len(accepted), 'rejected_by_hypothesis': dict(rejected),
           'accepted_size_histogram': dict(collections.Counter(x['n'] for x in accepted)),
           'row_evaluations': (2652+len(pool))*len(accepted), 'rank_crosscheck': 'exhaustive subsequences',
           'base_sha256': digest(a.base), 'pool_sha256': digest(a.pool),
           'budget_note': '34-hole target omitted: small real sets have many more holes',
           'controls': accepted}
    Path(a.out).write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'controls'}, indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=('model', 'real'))
    ap.add_argument('--base', required=True)
    ap.add_argument('--pool', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--solution')
    ap.add_argument('--cnf')
    ap.add_argument('--slice', type=int, choices=(19, 20))
    ap.add_argument('--min-points', type=int, default=1)
    ap.add_argument('--max-points', type=int, default=12)
    ap.add_argument('--attempts', type=int, default=240)
    ap.add_argument('--minimum-controls', type=int, default=100)
    args = ap.parse_args()
    data, pool = read(args.base, args.pool)
    if args.mode == 'model':
        checked = check_model(args, data, pool)
        if Path('/home/jay/research/data/es308-20261114/continuation/events.json').exists():
            vector = Path(args.out).parent/'checked-hole-vector.json'
            vector.write_text(json.dumps([int(v) for v in checked['hole_bits_index_0_first']])+'\n')
            sys.stdout.flush()
            os.execv(sys.executable, [sys.executable, str(Path(__file__).with_name('check_latest.py')),
                     str(vector), str(Path(args.out).parent/'latest-pool-check.json')])
    else:
        real_controls(args, data, pool)
