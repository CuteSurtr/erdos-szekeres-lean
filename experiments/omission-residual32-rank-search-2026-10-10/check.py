#!/usr/bin/env python3
"""Portable integer replay of strict row additions and saved-component coverage."""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def set_checked(indices, expected_size=None):
    require(isinstance(indices, list) and all(type(i) is int and 0 <= i < 154 for i in indices), 'index range/type')
    require(len(indices) == len(set(indices)), 'duplicate index')
    if expected_size is not None:
        require(len(indices) == expected_size, 'index count')
    return set(indices)


def satisfies(holes, row):
    direct = len(holes.intersection(row['support']))
    bitset = (sum(1 << i for i in holes) & sum(1 << i for i in row['support'])).bit_count()
    require(direct == bitset, 'independent row count')
    return direct >= row['rhs']


def countermodel(record, base, previous):
    support = set_checked(record['support'])
    require(record['rhs'] == 1, 'new demand')
    holes = set_checked(record['strict_countermodel_holes'], 33)
    require(0 not in holes, 'state0 must be occupied')
    require(not holes.intersection(support), 'countermodel fails to violate new row')
    require(all(satisfies(holes, row) for row in base + previous), 'countermodel fails preceding row')
    return holes


def coverage(vertices, rows):
    excluded = []
    for point in vertices:
        holes = set_checked(point, 33)
        excluded.append([i for i, row in enumerate(rows) if not satisfies(holes, row)])
    return excluded


def rejected(action, label):
    try:
        action()
    except (ValueError, KeyError, IndexError):
        return label
    raise ValueError('negative control accepted: ' + label)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in manifest['files_sha256'].items():
        require(sha((HERE / name).read_bytes()) == digest, 'changed local input: ' + name)
    for name, digest in manifest['external_sha256'].items():
        require(sha((ROOT / name).read_bytes()) == digest, 'changed external input: ' + name)
    record = json.loads((HERE / 'rows-and-countermodels.json').read_text())
    raw = gzip.decompress((ROOT / record['source']).read_bytes())
    require(sha(raw) == record['source_sha256'], 'catalog hash')
    base = json.loads(raw)['constraints']
    require(len(base) == 2646, 'catalog row count')
    previous, rank_counts = [], []
    for item in record['rows']:
        metadata_raw = (ROOT / item['certificate_metadata']).read_bytes()
        require(sha(metadata_raw) == item['certificate_metadata_sha256'], 'certificate metadata hash')
        metadata = json.loads(metadata_raw)
        require(metadata['support'] == item['support'], 'certificate support')
        count = sum(c['kind'] == 'source_cup' for c in metadata['clauses'])
        require(count == item['source_cup_clauses'], 'source-cup clause count')
        rank_counts.append(count)
        countermodel(item, base, previous)
        previous.append({'support': item['support'], 'rhs': item['rhs']})
    require(len(previous) == 4 and list(map(lambda r: len(r['support']), previous)) == [13, 13, 13, 12], 'batch shape')
    vertices_path = ROOT / manifest['component_vertices']
    vertices = json.loads(vertices_path.read_text())
    require(len(vertices) == len({tuple(v) for v in vertices}) == 306, 'component vertex identity')
    for point in vertices:
        holes = set_checked(point, 33)
        require(0 not in holes and all(satisfies(holes, row) for row in base), 'old component feasibility')
    excluded = coverage(vertices, previous)
    require(all(excluded), 'saved component survivor after full batch')
    core_one_survivors = [v for v, ex in zip(vertices, excluded) if 0 not in ex]
    saved = json.loads((HERE / 'survivors-input.json').read_text())
    require(core_one_survivors == saved['vertices'] and len(core_one_survivors) == 16, 'first-row survivor identity')
    require(all(3 in ex for ex in excluded if 0 not in ex), 'CoreFour misses prior survivor')
    old_near = json.loads((ROOT / manifest['component_near_models']).read_text())['rows']['205']
    require(len(old_near) == 26 and all(not satisfies(set(v), previous[0]) for v in old_near), 'old near-model elimination')
    fake = copy.deepcopy(record['rows'][0])
    fake['strict_countermodel_holes'][0] = fake['strict_countermodel_holes'][1]
    partial_exclusion = coverage(vertices, previous[:1])
    controls = [
        rejected(lambda: countermodel(fake, base, []), 'duplicate hole in countermodel'),
        rejected(lambda: countermodel(record['rows'][0], base, [previous[0]]), 'circular strictness witness'),
        rejected(lambda: require(all(partial_exclusion), 'CoreOne leaves16 survivors'), 'premature complete-component exclusion'),
        rejected(lambda: require(sha(raw + b' ') == record['source_sha256'], 'modified source'), 'modified source bytes'),
    ]
    report = {'complete': True, 'scope': 'Exact finite Boolean countermodels and saved-component coverage; not a global32-hole exclusion or geometric realization proof.',
              'source_sha256': record['source_sha256'], 'new_rows': 4, 'support_sizes': [len(r['support']) for r in previous],
              'successive_strict_countermodels': 4, 'source_cup_clauses': rank_counts,
              'saved_component_vertices': 306, 'saved_component_vertices_excluded': sum(bool(ex) for ex in excluded),
              'excluded_by_each_row': [sum(i in ex for ex in excluded) for i in range(4)],
              'first_row_survivors': 16, 'fourth_row_excludes_all_first_row_survivors': True,
              'previous_row205_near_models_excluded': 26, 'negative_controls_rejected': controls,
              'checker_sha256': sha(Path(__file__).read_bytes())}
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
