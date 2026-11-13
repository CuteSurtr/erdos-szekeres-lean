#!/usr/bin/env python3
"""Exactly replay catalog binding and the saved-component elimination.

This does not claim the saved component exhausts all hole assignments.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

from catalog import BASE_SHA, HERE, ROOT, build, encoded, extra_rows

VERTICES = ROOT / 'experiments/omission-residual32-primal-resume-2026-10-10/feasible33-vertices.json'


def check_catalog(path=HERE / 'source-2650.json.gz'):
    raw = gzip.decompress(path.read_bytes())
    if raw != encoded():
        raise ValueError('Catalog differs from proved row inputs')
    if json.loads((HERE / 'extra-rows.json').read_text()) != extra_rows():
        raise ValueError('SAT suffix differs from catalog')
    return hashlib.sha256(raw).hexdigest()


def coverage():
    data = build()
    vertices = json.loads(VERTICES.read_text())
    if len(vertices) != 306 or len({tuple(h) for h in vertices}) != 306:
        raise ValueError('Saved component identity/size changed')
    rows = data['constraints']
    for holes in vertices:
        h = set(holes)
        if (len(h) != len(holes) or len(h) != 33 or 0 in h or
                any(type(i) is not int or not 0 <= i < 154 for i in h)):
            raise ValueError('Invalid saved33-hole assignment')
        if any(len(h.intersection(r['support'])) < r['rhs'] for r in rows[:2646]):
            raise ValueError('Saved vertex is not feasible for the2646-row prefix')
    survivors = vertices
    counts = [len(vertices)]
    individually_excluded = []
    for row in rows[2646:]:
        individually_excluded.append(sum(not set(h).intersection(row['support']) for h in vertices))
        survivors = [h for h in survivors if len(set(h).intersection(row['support'])) >= row['rhs']]
        counts.append(len(survivors))
    return {
        'scope': 'Exclusion of the saved306-vertex single-swap component only; not all33-hole assignments.',
        'vertices': str(VERTICES.relative_to(ROOT)),
        'vertices_sha256': hashlib.sha256(VERTICES.read_bytes()).hexdigest(),
        'base_decompressed_sha256': BASE_SHA,
        'catalog_decompressed_sha256': hashlib.sha256(encoded()).hexdigest(),
        'new_supports': [r['support'] for r in rows[2646:]],
        'saved_vertices': len(vertices),
        'all_saved_vertices_satisfy_2646': True,
        'survivors_after_each_prefix': counts,
        'individually_excluded': individually_excluded,
        'remaining_vertices': survivors,
    }


def check_coverage_report(report):
    if report != coverage():
        raise ValueError('Coverage report differs from exact integer replay')


def check():
    digest = check_catalog()
    report = json.loads((HERE / 'coverage.json').read_text())
    check_coverage_report(report)
    if report['survivors_after_each_prefix'] != [306, 16, 16, 16, 0]:
        raise ValueError('Unexpected component elimination')
    return {'catalog_sha256': digest, 'rows': 2650,
            'component_survivors': report['survivors_after_each_prefix']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-coverage', action='store_true')
    args = parser.parse_args()
    if args.write_coverage:
        (HERE / 'coverage.json').write_text(json.dumps(coverage(), indent=2) + '\n')
    print(json.dumps(check(), indent=2))
