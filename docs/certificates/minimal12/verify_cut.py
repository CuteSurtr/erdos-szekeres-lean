#!/usr/bin/env python3
"""Replay the 28-sign forbidden C3 pattern without any realization or solver."""
from collections import Counter
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(data):
    entries = data['forbidden_signs']
    pattern = {tuple(row['triple']): row['sign'] for row in entries}
    require(len(pattern) == len(entries) == 28, 'Need 28 distinct sign requirements.')
    for triple, sign in pattern.items():
        require(len(triple) == 3 and len(set(triple)) == 3 and
                all(type(v) is int and 0 <= v < 12 for v in triple), 'Invalid triple.')
        require(tuple(sorted(triple)) == triple and sign in (-1, 1), 'Invalid sign entry.')

    def rotate(t, k):
        return tuple(3 * (v // 3) + (v % 3 + k) % 3 for v in t)

    def parity(t):
        return (-1) ** sum(t[i] > t[j] for i in range(3) for j in range(i + 1, 3))

    def representative(t):
        return min(tuple(sorted(rotate(t, k))) for k in range(3))

    require(all(representative(t) == t for t in pattern), 'Noncanonical C3 sign key.')

    def chi(t):
        images = [(tuple(sorted(rotate(t, k))), parity(rotate(t, k))) for k in range(3)]
        key = min(triple for triple, _ in images)
        require(key in pattern, 'A required bracket sign is missing.')
        values = {sign * pattern[key] for triple, sign in images if triple == key}
        require(len(values) == 1, 'Inconsistent C3 sign reconstruction.')
        return values.pop()

    exponents, used = Counter(), set()
    rows = data['certificate_terms']
    require(len(rows) == 8, 'Need eight C3 seed comparisons.')
    for row in rows:
        labels = (row['anchor'], *row['other'])
        require(len(labels) == 5 and len(set(labels)) == 5 and
                all(type(v) is int and 0 <= v < 12 for v in labels), 'Invalid GP labels.')
        require(row['coefficient'] == 1, 'Expected unit coefficients.')
        a, b, c, d, e = labels
        terms = [((a, b, c), (a, d, e), 1),
                 ((a, b, d), (a, c, e), -1),
                 ((a, b, e), (a, c, d), 1)]
        larger, smaller = row['large'], row['small']
        require(larger in range(3) and smaller in range(3) and larger != smaller,
                'Invalid comparison indices.')
        for k in range(3):
            signs = [sign * chi(rotate(t, k)) * chi(rotate(u, k))
                     for t, u, sign in terms]
            require(len(set(signs)) == 2 and signs.count(signs[larger]) == 1 and
                    signs[smaller] != signs[larger], 'The strict GP inequality fails.')
            for j, coefficient in ((larger, 1), (smaller, -1)):
                for triple in terms[j][:2]:
                    exponents[tuple(sorted(rotate(triple, k)))] += coefficient
            for t, u, _ in terms:
                used.update((representative(t), representative(u)))
    require(not any(exponents.values()) and len(exponents) == 48,
            'Ordinary determinant factors do not cancel.')
    require(used == set(pattern), 'The listed signs differ from the proof inputs.')
    return {'verified': True, 'required_signs': len(pattern), 'C3_seed_rows': len(rows),
            'ordinary_GP_comparisons': 3 * len(rows), 'ordinary_bracket_factors': len(exponents),
            'reflection_required_of_target': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path, nargs='?',
                        default=Path(__file__).with_name('c3-cut.json'))
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text())), indent=2))


if __name__ == '__main__':
    main()
