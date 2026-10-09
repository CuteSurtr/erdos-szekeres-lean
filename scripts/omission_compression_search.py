#!/usr/bin/env python3
"""Search residual state subsets admitting a two-level cap-label compression.

The residual catalog comes from Schroeder, DOI 10.5281/zenodo.22842891
(catalog data CC BY 4.0; see docs/THIRD_PARTY.md). This search is independent
new code. It does not assume a rectangular embedding of the 28 ideals.
For every ideal interval [L,U], compatibility cliques collect states whose
required rank-one and rank-two cells are disjoint. Each resulting literal
block still needs a separate Lean geometric check; this program supplies no
formal completeness claim or global Erdős–Szekeres bound.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time


def bit_indices(mask):
    while mask:
        lowest = mask & -mask
        yield lowest.bit_length() - 1
        mask ^= lowest


def search(states, minimum=23):
    cells = [(x, y) for x in range(1, 5) for y in range(1, 7)]
    masks = [sum(1 << i for i, (x, y) in enumerate(cells) if y <= state[x - 1])
             for state in states]
    by_column = [sum(1 << i for i, (x, _) in enumerate(cells) if x == column)
                 for column in range(1, 5)]
    found = {}
    intervals = 0
    calls = 0
    for lower_id, lower in enumerate(masks):
        for upper_id, upper in enumerate(masks):
            if lower & ~upper:
                continue
            inside = [i for i, state in enumerate(masks)
                      if not (lower & ~state or state & ~upper)]
            if len(inside) < minimum:
                continue
            intervals += 1
            active = upper & ~lower
            force_one, force_two = [], []
            for state_id in inside:
                occupied = masks[state_id] & active
                absent = active & ~occupied
                largest_absent = max([0] + [x + 1 for x in range(4) if absent & by_column[x]])
                smallest_present = min([5] + [x + 1 for x in range(4) if occupied & by_column[x]])
                force_one.append(occupied & sum(by_column[:max(0, largest_absent - 1)]))
                force_two.append(absent & sum(by_column[smallest_present:]))
            adjacency = [sum(1 << b for b in range(len(inside)) if a != b and not
                             (force_one[a] & force_two[b] or force_two[a] & force_one[b]))
                         for a in range(len(inside))]

            def visit(selected, possible, excluded):
                nonlocal calls
                calls += 1
                if len(selected) + possible.bit_count() < minimum:
                    return
                if not (possible | excluded):
                    support = tuple(sorted(inside[i] for i in selected))
                    if support in found:
                        return
                    ones = twos = 0
                    for i in selected:
                        ones |= force_one[i]
                        twos |= force_two[i]
                    assert not (ones & twos)
                    thresholds = [max([0] + [x for i, (x, y) in enumerate(cells)
                                                if y == row and ones >> i & 1])
                                  for row in range(1, 7)]
                    active_cells = [cell for i, cell in enumerate(cells) if active >> i & 1]
                    rank = lambda z: 1 if z[0] <= thresholds[z[1] - 1] else 2
                    # Arbitrary compatible binary ranks need not in general be
                    # thresholds. Retain only certificates accepted by the
                    # existing threshold-based BlockCompression interface.
                    threshold_valid = all(rank(z) < rank(w)
                        for s in support for z in active_cells for w in active_cells
                        if z[1] <= states[s][z[0] - 1] and
                        w[1] > states[s][w[0] - 1] and z[0] < w[0])
                    if threshold_valid:
                        found[support] = {'support': list(support), 'lower': lower_id,
                            'upper': upper_id, 'thresholds': thresholds,
                            'active': [list(cell) for cell in active_cells],
                            'demand': len(support) - 22}
                    return
                pivot = max(bit_indices(possible | excluded),
                            key=lambda v: (possible & adjacency[v]).bit_count())
                for vertex in list(bit_indices(possible & ~adjacency[pivot])):
                    visit(selected + [vertex], possible & adjacency[vertex], excluded & adjacency[vertex])
                    possible &= ~(1 << vertex)
                    excluded |= 1 << vertex

            visit([], (1 << len(inside)) - 1, 0)
    supports = list(found)
    sets = list(map(set, supports))
    maximal = [found[support] for i, support in enumerate(supports)
               if not any(sets[i] < other for other in sets)]
    return {'intervals': intervals, 'recursive_calls': calls,
            'interval_maximal_supports': len(found), 'maximal_supports': maximal}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    data = json.loads(args.source.read_text())
    if len(data['states']) != 154 or any(len(state) != 5 or state[-1] != 0 for state in data['states']):
        raise ValueError('Expected the pinned 154-state residual catalog')
    started = time.monotonic()
    result = search(data['states'])
    old = [set(row['support']) for row in data['constraints'] if row['kind'] == 'baek_block']
    result.update({'scope': 'Finite discovery only; validate each row in Lean before use',
        'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'seconds': time.monotonic() - started,
        'catalog_supports_found': sum(any(set(block['support']) == support
            for block in result['maximal_supports']) for support in old),
        'catalog_support_count': len(old)})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'maximal_supports'}))


if __name__ == '__main__':
    main()
