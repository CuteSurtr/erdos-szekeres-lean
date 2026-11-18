#!/usr/bin/env python3
"""Hand-sized adversarial examples and a smoke test; no solver or generation."""
from itertools import combinations, product
import json
from pathlib import Path
import time

from canonical_eval import Geometry, Layout, evaluate


def geometry(points, n):
    def det(i, j, k):
        a, b, c = points[i], points[j], points[k]
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    determinants = [det(*s) for s in combinations(range(len(points)), 3)]
    assert all(determinants)
    signs = ''.join('+' if d > 0 else '-' for d in determinants)
    return Geometry(points, signs, len(points), n, 'cup')


def main():
    started = time.monotonic()
    cnf = Path('/home/jay/research/data/delta3-codex-20261113/encoder/'
               'semantic-4-5-cup-lattice.cnf')
    g = geometry([[0, 0], [1, 1], [2, 4], [3, 9]], 5)
    smoke = evaluate(cnf, g, Layout(g, 'cup', 'lattice'))
    assert smoke['working_deltas'] == 15

    # These test the exact signotope implications used by the written proof.
    packet = lambda q: sum(a != b for a, b in zip(q, q[1:])) <= 1
    allowed = [q for q in product((False, True), repeat=4) if packet(q)]
    assert len(allowed) == 8
    for a, b, c, d in allowed:
        if a == d:
            assert a == b == c == d
        if b != c:
            assert a == b and c == d
    implications = 0
    for cx, cy, cz, z in product((False, True), repeat=4):
        if cx != cy and packet((cx, cx, cy, z)):
            assert z == cy
            implications += 1
        if cy != cz and packet((z, cy, cz, cz)):
            assert z == cy
            implications += 1

    cap_points = [[0, 0], [1, 3], [2, 4], [3, 3], [4, 100]]
    g = geometry(cap_points, 6)
    assert g.caps == {15}
    first4 = [bool(g.a[31 ^ (1 << i)]) for i in range(4)]
    first5 = [bool(g.a[31 ^ (1 << i)]) for i in range(5)]
    assert g.a[31] and not any(first4) and any(first5)

    endpoint_points = [[0, 0], [1, 3], [2, -2], [3, 3], [4, 0]]
    g = geometry(endpoint_points, 6)
    assert g.targets == {21} and g.caps == {27}
    assert not g.a[2] and g.b[31 ^ 2]

    upper, seed, container = 5, 31, 63
    contains = lambda s: s & seed == seed
    assert not any(contains(container ^ (1 << i)) for i in range(upper))
    assert any(contains(container ^ (1 << i)) for i in range(upper + 1))
    report = dict(
        label='COMPUTED', scope='hand-sized proof-schema checks and evaluator smoke only',
        smoke_actual_cnf=str(cnf), smoke=smoke,
        signotope_proof_schemas=dict(allowed_packets=len(allowed),
                                    internal_middle_sign_implications=implications),
        cap_deletion_sharpness=dict(points=cap_points, sole_fourcap=[0, 1, 2, 3],
                                   first_four_children=first4, first_five_children=first5),
        endpoint_support_may_intersect_delta=dict(points=endpoint_points, n=6,
            cap=[0, 1, 3, 4], cup=[0, 2, 4], delta=[1], delta_fails_cup_requirement=True),
        target_cutoff_sharpness=dict(upper=upper, singleton_seed=[0, 1, 2, 3, 4],
            container=[0, 1, 2, 3, 4, 5], five_deletions_lose_seed=True,
            six_deletions_retain_seed=True,
            scope='set-system sharpness, not a claimed geometric counterexample'),
        wall_seconds=round(time.monotonic() - started, 6))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
