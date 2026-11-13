#!/usr/bin/env python3
"""Exact finite irredundancy controls for the deduplicated coupled templates.

This is a discovery/data check. Lean proves the implication and independence
statements separately; this script does not certify a population bound.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import json


def run(output):
    repo = Path(__file__).resolve().parents[1]
    relative = [
        'experiments/omission-coupled-core-2026-10-10/template-variants.json',
        'experiments/omission-coupled-next-2026-10-10/template-variants.json',
        'experiments/omission-additional-rows-2026-10-10.json',
        'experiments/omission-general-blocks-2026-10-10.json',
        'experiments/omission-residual-geometry-2026-10-09/row-source.json.gz',
    ]
    paths = [repo / p for p in relative]
    first, second, additional, blocks = [json.loads(p.read_text()) for p in paths[:4]]
    original_bytes = gzip.decompress(paths[4].read_bytes())
    original = json.loads(original_bytes)
    prior = list(original['constraints'])
    prior += [{'support': s, 'rhs': 1} for s in additional['cycles']]
    prior += [{'support': additional['block']['support'], 'rhs': 6}]
    prior += [{'support': b['support'], 'rhs': len(b['support']) - 22} for b in blocks['blocks']]
    if (len(first['supports']), len(second['supports']), len(prior)) != (42, 35, 1232):
        raise ValueError('Unexpected family size')
    for r in prior:
        if len(r['support']) != len(set(r['support'])):
            raise ValueError('Duplicate state within an original/prior support')
    supports, indices, mapping = [], {}, []
    for family, rows in [('first', first['supports']), ('second', second['supports'])]:
        for index, row in enumerate(rows):
            key = tuple(sorted(row))
            if len(key) != len(set(key)) or len(key) != 13 or not all(0 <= i < 154 for i in key):
                raise ValueError('Expected thirteen distinct valid states')
            if key not in indices:
                indices[key] = len(supports)
                supports.append(key)
            mapping.append(dict(family=family, index=index, union_index=indices[key]))
    failed, slack = [], []
    for i, support in enumerate(supports):
        margins = [len(set(r['support']) - set(support)) - r['rhs'] for r in prior]
        slack.append(min(margins))
        failed.extend(dict(row=i, prior_row=j, margin=m) for j, m in enumerate(margins) if m < 0)
    redundant = sorted({f['row'] for f in failed})
    independent = [i for i in range(len(supports)) if i not in redundant]
    if (len(supports), len(independent), len(redundant)) != (57, 9, 48):
        raise ValueError('Unexpected classification')
    certificates = [next(f for f in failed if f['row'] == i) for i in redundant]
    if any(c['prior_row'] >= 1187 for c in certificates):
        raise ValueError('Redundancy did not follow from a single original row')
    other = all(len(set(s) - set(t)) >= 1 for i, s in enumerate(supports)
                for j, t in enumerate(supports) if i != j)
    result = dict(
        scope='Exact finite diagnostic: nine union rows independent over original1187+prior45+other56; '
              'remaining48 implied by an original row. Lean results are checked separately. '
              'No cardinality conclusion or geometric realizability claim.',
        families=[42, 35], unique_rows=len(supports), cross_family_duplicates=20,
        prior_rows=len(prior), prior_row_checks=len(prior) * len(supports),
        all_prior_rows_satisfied=not failed, failed_checks=failed,
        minimum_slack_by_witness=slack,
        all_distinct_rows_allow_other_witnesses=other,
        all_own_rows_fail=all(len(set(s) - set(s)) < 1 for s in supports),
        all_prior_45_rows_satisfied=not any(f['prior_row'] >= 1187 for f in failed),
        independent_union_indices=independent, redundant_union_indices=redundant,
        redundancy_certificates=certificates, witness_holes=141,
        mapping=mapping, supports=[list(s) for s in supports],
        sources={p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in relative},
        expanded_original_source_sha256=hashlib.sha256(original_bytes).hexdigest(),
        checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    )
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({key: result[key] for key in
        ['unique_rows', 'cross_family_duplicates', 'independent_union_indices',
         'prior_row_checks', 'all_prior_45_rows_satisfied']}))
