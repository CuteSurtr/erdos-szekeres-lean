#!/usr/bin/env python3
"""Independent exact controls for the rooted geometric lemma; not exhaustion."""
from itertools import combinations
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import resource
import time

resource.setrlimit(resource.RLIMIT_AS, (150 << 20, 150 << 20))
resource.setrlimit(resource.RLIMIT_CPU, (18, 19))
start = time.monotonic()
rng = random.Random(202611140831)
counts = Counter()
representatives = {}


def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def hull(points, subset):
    lower, upper = [], []
    for chain, seq in [(lower, subset), (upper, reversed(subset))]:
        for i in seq:
            while len(chain) >= 2 and orient(points[chain[-2]], points[chain[-1]], points[i]) <= 0:
                chain.pop()
            chain.append(i)
    return len(lower[:-1] + upper[:-1]) == len(subset)


def check(points):
    counts['generated'] += 1
    m = len(points)
    triples = {t: orient(*(points[i] for i in t)) for t in combinations(range(m), 3)}
    if any(v == 0 for v in triples.values()):
        counts['degenerate_rejected'] += 1
        return
    if any(all(triples[t] < 0 for t in combinations(q, 3)) for q in combinations(range(m), 4)):
        counts['four_cap_rejected'] += 1
        return
    counts['no_four_cap'] += 1
    r = m-1
    end3 = {c for (a,b,c), value in triples.items() if value < 0}
    cup = lambda subset: all(triples[t] > 0 for t in combinations(sorted(subset), 3))
    prefix = range(r)
    for n in range(5, min(m+2, 9)):
        k = n-1
        if any(cup(t) for t in combinations(prefix, k)):
            counts['long_prefix_cup_rejected'] += 1
            continue
        targets = [t for t in combinations(range(m), k) if hull(points, t)]
        if r in end3:
            branch = 'root_has_cap'
            selected = {max(t) for t in targets if r not in t} | {r}
        else:
            branch = 'root_has_no_cap'
            # Independently enumerate all prefix cups to calculate ending ranks.
            ranks = [1]*r
            for size in range(2, min(k, r+1)):
                for t in combinations(prefix, size):
                    if cup(t):
                        ranks[t[-1]] = max(ranks[t[-1]], size)
            selected = {i for i in prefix if ranks[i] == k-1}
        assert cup(selected), (points, n, 'not cup', selected)
        assert all(set(t) & selected for t in targets), (points, n, 'missed target', selected)
        ordered = sorted(selected)
        assert all(b in end3 for b in ordered[1:]), (points, n, 'unsupported endpoint', selected)
        if ordered and ordered[0] not in end3:
            counts['first_vertex_without_cap_end'] += 1
        counts['checked'] += 1
        counts[f'n{n}_{branch}'] += 1
        if targets:
            counts['nonvacuous'] += 1
            # Deliberately empty selection must fail the direct coverage test.
            assert not all(set(t) & set() for t in targets)
            counts['empty_mutants_rejected'] += 1
        has_ngon = any(hull(points, t) for t in combinations(range(m), n))
        if has_ngon:
            counts['checked_with_n_gon'] += 1
        key = f'n{n}/{branch}/has_ngon={has_ngon}'
        if key not in representatives:
            representatives[key] = {'points': points, 'n': n, 'selected': ordered,
                                    'targets': [list(t) for t in targets], 'has_n_gon': has_ngon}


check([(0,0),(4,4),(6,15),(8,16),(12,36)])
# Pure cups exercise the unsupported-first-point exception in the no-cap branch.
for m in range(4, 9):
    check([(i, i*i) for i in range(m)])
for m in range(6, 10):
    for _ in range(2500):
        xs = sorted(rng.sample(range(0, 2000), m))
        check([(x, rng.randrange(-10000,10001)) for x in xs])

assert counts['checked_with_n_gon'] > 0
assert counts['empty_mutants_rejected'] > 0
assert counts['first_vertex_without_cap_end'] > 0
result = {'status': 'PASS', 'label': 'COMPUTED exact controls; written proof is separate',
          'seed': 202611140831, 'counts': dict(counts),
          'representatives': representatives,
          'seconds': time.monotonic()-start,
          'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'scope': 'Deterministic sampled integer configurations and named controls; no order-type exhaustion or new universal claim.'}
(Path(__file__).parent/'result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['status','counts','seconds','maximum_rss_kib']}))
