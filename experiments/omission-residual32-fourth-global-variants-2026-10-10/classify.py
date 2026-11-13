#!/usr/bin/env python3
"""Exact single-old-row implication diagnostic; no solver or Lean compilation."""
import gzip
import hashlib
import json
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parents[1]
SOURCE = ROOT / 'experiments/omission-residual32-research-2026-10-10/source.json.gz'
EXPECTED_SOURCE = 'f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    archive = SOURCE.read_bytes()
    raw = gzip.decompress(archive)
    assert sha(raw) == EXPECTED_SOURCE, 'frozen old source identity changed'
    old = json.loads(raw)['constraints']
    bindings = (BUNDLE / 'row-bindings.json').read_bytes()
    new = json.loads(bindings)['rows']
    assert len(old) == 2469 and len(new) == 128
    results = []
    for row in new:
        assert row['rhs'] == 1
        support = set(row['support'])
        certificates = []
        for i, antecedent in enumerate(old):
            outside = sorted(set(antecedent['support']) - support)
            margin = antecedent['rhs'] - len(outside)
            if margin > 0:
                certificates.append({'old_row': i, 'old_rhs': antecedent['rhs'],
                                     'outside_new_support': outside,
                                     'implied_lower_bound': margin})
        results.append({'row': row['row'], 'support': row['support'],
                        'directly_implied': bool(certificates),
                        'certificates': certificates})
    implied = [r['row'] for r in results if r['directly_implied']]
    report = {
        'scope': 'Exact single-row implication test for 128 demand-one Fourth rows; not a test of full logical independence.',
        'criterion': 'old rhs > cardinality(old support minus new support); Boolean holes on the outside contribute at most that cardinality.',
        'negative_result_meaning': 'No single old row certifies this row by this criterion. Combinations of old rows or other geometric consequences may still imply it.',
        'old_source': str(SOURCE.relative_to(ROOT)),
        'source_archive_sha256': sha(archive),
        'source_uncompressed_sha256': sha(raw),
        'row_bindings_sha256': sha(bindings),
        'classifier_sha256': sha(Path(__file__).read_bytes()),
        'old_rows': len(old), 'new_rows': len(new),
        'directly_implied_count': len(implied),
        'not_certified_by_single_row_count': len(new) - len(implied),
        'directly_implied_rows': implied, 'rows': results,
    }
    (BUNDLE / 'direct-implication.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('directly_implied_count', 'not_certified_by_single_row_count', 'directly_implied_rows')}))


if __name__ == '__main__':
    main()
