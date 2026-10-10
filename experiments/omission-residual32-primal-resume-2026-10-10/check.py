#!/usr/bin/env python3
"""Replay the complete33-hole component and candidate deficits using integers only."""
import argparse
import collections
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, label):
    if not condition:
        raise ValueError(label)


def holes_checked(value, size):
    require(isinstance(value, list) and all(type(x) is int for x in value), 'hole indices')
    require(len(value) == len(set(value)) == size, 'hole count/duplicates')
    require(all(1 <= x < 154 for x in value), 'occupied state0/range')
    return frozenset(value)


def violations(holes, rows):
    S = set(holes)
    bits = sum(1 << i for i in S)
    out = []
    for j, r in enumerate(rows):
        count = len(S.intersection(r['support']))
        require(count == (bits & sum(1 << i for i in r['support'])).bit_count(), 'independent count')
        if count < r['rhs']:
            out.append({'row': j, 'count': count, 'rhs': r['rhs']})
    return out


def component(vertices, rows, seeds):
    points = set(holes_checked(v, 33) for v in vertices)
    require(len(points) == len(vertices), 'duplicate vertices')
    start = [holes_checked(s, 33) for s in seeds]
    require(bool(start), 'empty seed list')
    require(set(start) <= points, 'missing seed')
    queue, reached = collections.deque([start[0]]), {start[0]}
    members = [set(r['support']) for r in rows]
    universe = set(range(1, 154))
    edges, near = 0, {}
    while queue:
        point = queue.popleft()
        counts = [len(point & support) for support in members]
        require(all(c >= r['rhs'] for c, r in zip(counts, rows)), 'infeasible33 vertex')
        tight = [j for j, (c, r) in enumerate(zip(counts, rows)) if c == r['rhs']]
        for drop in sorted(point):
            blockers = [j for j in tight if drop in members[j]]
            require(bool(blockers), 'removable hole/32 witness')
            if len(blockers) == 1:
                near.setdefault(blockers[0], set()).add(tuple(sorted(point - {drop})))
            # A single swap is feasible exactly when its added hole belongs to
            # every previously tight row containing the removed hole.
            allowed = universe - point
            for j in blockers:
                allowed &= members[j]
            for add in allowed:
                child = frozenset((point - {drop}) | {add})
                require(child in points, 'component has outgoing edge')
                edges += 1
                if child not in reached:
                    reached.add(child)
                    queue.append(child)
    require(reached == points, 'unreachable recorded vertices')
    return {'vertices': len(points), 'directed_edges': edges,
            'near_models': {str(k): sorted(map(list, v)) for k, v in sorted(near.items())}}


def partial_checked(record):
    require(record['seen'] - record['processed'] == record['frontier'], 'partial frontier count')
    require(not record['component_exhausted'] or record['frontier'] == 0, 'false exhaustion')
    require(not record['witness_found'], 'unexpected partial witness')


def rejects(action, label):
    try:
        action()
    except (ValueError, KeyError, IndexError):
        return label
    raise ValueError('negative control accepted: ' + label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in manifest['files_sha256'].items():
        require(sha((HERE / name).read_bytes()) == digest, 'record hash: ' + name)
    raw = gzip.decompress((ROOT / manifest['source2598']).read_bytes())
    require(sha(raw) == manifest['source2598_sha256'], 'source2598 hash')
    base = json.loads(raw)['constraints']
    raw2646 = gzip.decompress((ROOT / manifest['source2646']).read_bytes())
    require(sha(raw2646) == manifest['source2646_sha256'], 'source2646 hash')
    rows = json.loads(raw2646)['constraints']
    require(len(base) == 2598 and len(rows) == 2646 and rows[:2598] == base, 'catalog prefix')
    for r in rows:
        require(type(r['rhs']) is int and 0 <= r['rhs'] <= len(r['support']), 'row demand')
        require(len(set(r['support'])) == len(r['support']), 'support duplicates')
        require(all(type(i) is int and 0 <= i < 154 for i in r['support']), 'support range')
    vertices = json.loads((HERE / 'feasible33-vertices.json').read_text())
    seeds = manifest['feasible33_seeds']
    base_result = component(vertices, base, seeds)
    result = component(vertices, rows, seeds)
    require(result == base_result, 'base/augmented graph mismatch')
    require(result['vertices'] == 306 and result['directed_edges'] == 3650, 'component counts')
    near = json.loads((HERE / 'feasible33-near-models.json').read_text())['rows']
    require(result['near_models'] == near, 'complete deletion near-model list')
    require(list(near) == ['205'] and len(near['205']) == 26, 'near-model counts')
    candidates = json.loads((HERE / 'feasible34-checked-near-models.json').read_text())['candidates']
    for c in candidates:
        point = holes_checked(c['holes'], 32)
        actual = violations(point, rows)
        require(actual == c['violations'] and len(actual) == 1, 'near-model deficit')
        require(actual[0]['rhs'] - actual[0]['count'] == 1, 'near-model deficit amount')
    partial = json.loads((HERE / 'feasible34-partial-result.json').read_text())
    partial_checked(partial)
    nonseed = next(v for v in vertices if v not in seeds)
    wrong_partial = copy.deepcopy(partial)
    wrong_partial['component_exhausted'] = True
    # Two isolated33-hole vertices:31 forced holes plus either side of K2,2.
    # An all-seeds BFS incorrectly accepts their disconnected union.
    toy_common = list(range(1, 32))
    toy_points = [toy_common + [32, 33], toy_common + [34, 35]]
    toy_rows = [{'support': [i], 'rhs': 1} for i in toy_common]
    toy_rows += [{'support': [i, j], 'rhs': 1} for i in [32, 33] for j in [34, 35]]
    for point in toy_points:
        toy_result = component([point], toy_rows, [point])
        require(toy_result['vertices'] == 1 and toy_result['directed_edges'] == 0, 'toy component control')
    controls = [
        rejects(lambda: component(toy_points, toy_rows, toy_points), 'disconnected closed union'),
        rejects(lambda: component([v for v in vertices if v != nonseed], rows, seeds), 'omitted component vertex'),
        rejects(lambda: holes_checked([0] + vertices[0][1:], 33), 'occupied state0 changed'),
        rejects(lambda: require(not violations(candidates[0]['holes'], rows), 'near-model is not witness'), 'false32-hole witness'),
        rejects(lambda: partial_checked(wrong_partial), 'partial34 search called exhaustive'),
        rejects(lambda: require(sha(raw + b' ') == manifest['source2598_sha256'], 'source hash'), 'modified source bytes'),
        rejects(lambda: require(result['directed_edges'] + 1 == 3650, 'edge count'), 'incorrect complete edge count'),
    ]
    report = {'complete': True, 'scope': 'Exact local Boolean component and candidate replay only; no global32 exclusion or geometric realization.',
              'catalog_rows': [2598, 2646], 'component_vertices': 306, 'component_directed_edges': 3650,
              'component_removable_holes': 0, 'component_near_models': 26,
              'new_distinct_row_near_models': len(candidates)-1,
              'near_model_failed_rows': [c['violations'][0]['row'] for c in candidates],
              'partial34_search_exhausted': False, 'negative_controls_rejected': controls,
              'source2598_sha256': manifest['source2598_sha256'], 'source2646_sha256': manifest['source2646_sha256'],
              'checker_sha256': sha(Path(__file__).read_bytes())}
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
