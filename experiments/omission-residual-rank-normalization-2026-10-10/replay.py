#!/usr/bin/env python3
"""Exact, solver-free replay of the archived nontrivial clipping example."""
import copy
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parity(q):
    return sum(q[i] > q[j] for i in range(len(q)) for j in range(i + 1, len(q))) % 2


def replay(report=None):
    if report is None:
        report = json.loads((HERE / 'clipping-example.json').read_text())
    raw = gzip.decompress(SOURCE.read_bytes())
    require(hashlib.sha256(raw).hexdigest() == report['source_sha256'], 'Source mismatch')
    catalog = json.loads(raw)['states']
    states = report['support']
    n = len(states)
    require(len(set(states)) == n and all(0 <= s < 154 for s in states), 'Invalid support')
    cells = [{(a + 1, b) for a, h in enumerate(catalog[s][:4])
              for b in range(1, h + 1)} for s in states]
    rawdiff = {(i, j): cells[j] - cells[i] for i, j in itertools.permutations(range(n), 2)}
    differences = {ij: d - {(1, 6)} for ij, d in rawdiff.items()}

    def forced_positive(t):
        for perm in itertools.permutations(range(3)):
            p, q, r = (t[i] for i in perm)
            coord = 1 if parity(perm) else 0
            if rawdiff[p, q] and rawdiff[q, r] and rawdiff[p, r]:
                if max(z[coord] for z in rawdiff[q, r]) > min(z[coord] for z in rawdiff[p, q]):
                    return False
        return True

    def validate(assignment, bound):
        p = assignment['positions']
        require(sorted(p) == list(range(n)), 'Invalid chronology')
        labels = {(i, j): (a, b) for i, j, a, b in assignment['labels']}
        orientations = {tuple(q[:3]): q[3] for q in assignment['orientations']}
        require(len(labels) == len(assignment['labels']) and
                set(labels) == set(itertools.combinations(range(n), 2)), 'Incomplete labels')
        require(len(orientations) == len(assignment['orientations']) and
                set(orientations) == set(itertools.combinations(range(n), 3)) and
                all(type(v) is bool for v in orientations.values()), 'Incomplete orientations')

        def orient(q):
            return orientations[tuple(sorted(q))] ^ bool(parity(q))

        order = sorted(range(n), key=lambda i: p[i])
        for i, j in itertools.combinations(order, 2):
            a, b = labels[tuple(sorted((i, j)))]
            require(1 <= a <= 4 and 1 <= b <= 6, 'Label bounds')
            require((a, b) in differences[i, j], 'Directed domain')
            if bound:
                require(b <= catalog[states[i]][0] + 1, 'Source-cup bound')
        for i, j, k in itertools.combinations(order, 3):
            coord = 1 if orient((i, j, k)) else 0
            require(labels[tuple(sorted((i, j)))][coord] <
                    labels[tuple(sorted((j, k)))][coord], 'Signed growth')
        for quad in itertools.combinations(order, 4):
            vals = [orient(t) for t in itertools.combinations(quad, 3)]
            require(sum(x != y for x, y in zip(vals, vals[1:])) <= 1, 'Orientation packet')
        for t, v in orientations.items():
            if forced_positive(t):
                require(v, 'Fixed positive sign')
            elif forced_positive((t[0], t[2], t[1])):
                require(not v, 'Fixed negative sign')
        convex = {}
        for a, b, c, d in itertools.combinations(range(n), 4):
            x, y, z, w = [orientations[t] for t in
                          [(a, b, c), (a, b, d), (a, c, d), (b, c, d)]]
            convex[a, b, c, d] = sum([not w, z, not y, x]) == 2
        eights = list(itertools.combinations(range(n), 8))
        require(all(not all(convex[q] for q in itertools.combinations(e, 4)) for e in eights),
                'Abstract convex octagon found')
        return len(eights)

    old = report['old_assignment']
    checked_eights = validate(old, False)
    clipped = copy.deepcopy(old)
    changes = []
    for row in clipped['labels']:
        i, j, a, b = row
        source = i if old['positions'][i] < old['positions'][j] else j
        row[3] = min(b, catalog[states[source]][0] + 1)
        if row[3] != b:
            changes.append({'pair': [i, j], 'chronological_source': source,
                            'source_state': states[source], 'before_cup': b, 'after_cup': row[3]})
    require(changes and changes == report['changes'], 'Clipping change record')
    require(clipped == report['clipped_assignment'], 'Clipped assignment mismatch')
    require(validate(clipped, True) == checked_eights, 'Replay mismatch')
    return {'states': n, 'changed_labels': len(changes), 'eights_checked_per_assignment': checked_eights,
            'domains_growth_packets_fixed_signs_and_no_abstract_octagon': True,
            'clipped_bounds': True, 'positions_caps_orientations_unchanged': True}


if __name__ == '__main__':
    print(json.dumps(replay(), indent=2))
