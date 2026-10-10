#!/usr/bin/env python3
"""Reconstruct the 2,650-row search input from its proved literal families.

This integer binding is not a global hole exclusion or a Lean catalog bridge.
The four new geometric proofs are audited in the adjacent certificate bundle.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = ROOT / 'experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz'
BASE_SHA = '151ea1bfb175f6507d910521eb96961c82b54add2fb7e49e13b864b87241123e'
CORES = ROOT / 'experiments/omission-residual32-rank-certificates-2026-10-10'
NAMES = ('one', 'two', 'three', 'four')


def build():
    raw = gzip.decompress(BASE.read_bytes())
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError('Changed 2,646-row prefix')
    parent = json.loads(raw)
    if len(parent['states']) != 154 or len(parent['constraints']) != 2646:
        raise ValueError('Unexpected parent catalog dimensions')
    rows = list(parent['constraints'])
    bindings = []
    for index, name in enumerate(NAMES):
        core = CORES / ('core-' + name + '.json')
        support = json.loads(core.read_text())['support']
        if (not 8 <= len(support) <= 154 or len(set(support)) != len(support) or
                any(type(i) is not int or not 0 <= i < 154 for i in support)):
            raise ValueError('Invalid core support')
        rows.append({'support': sorted(support), 'rhs': 1})
        bindings.append({
            'row': 2646 + index,
            'core': str(core.relative_to(ROOT)),
            'core_sha256': hashlib.sha256(core.read_bytes()).hexdigest(),
            'theorem': 'ErdosSzekeres.Omission.CoupledCoreRankSearch' + name.title() + '.hole_bound',
        })
    return {
        'schema': 'residual-rank-search-2650-v1',
        'scope': 'Search catalog with individually proved geometric rows; no complete32-hole exclusion.',
        'attribution': 'The inherited catalog includes Schroeder version1 data; see docs/THIRD_PARTY.md.',
        'parent': str(BASE.relative_to(ROOT)),
        'parent_decompressed_sha256': BASE_SHA,
        'states': parent['states'], 'constraints': rows, 'new_row_bindings': bindings,
    }


def encoded():
    return (json.dumps(build(), sort_keys=True, separators=(',', ':')) + '\n').encode()


def extra_rows():
    """Input format for the unchanged 2,598-row SAT runner."""
    rows = build()['constraints'][2598:]
    return {
        'source_sha256': '01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b',
        'scope': '48 proved relaxed Sixth rows followed by the four proved rank-search rows.',
        'rows': rows,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    raw = encoded()
    if args.write:
        (HERE / 'source-2650.json.gz').write_bytes(gzip.compress(raw, mtime=0))
        (HERE / 'extra-rows.json').write_text(json.dumps(extra_rows(), indent=2) + '\n')
    else:
        if gzip.decompress((HERE / 'source-2650.json.gz').read_bytes()) != raw:
            raise ValueError('Archived catalog does not match proved row inputs')
        if json.loads((HERE / 'extra-rows.json').read_text()) != extra_rows():
            raise ValueError('SAT suffix does not match catalog')
    print(json.dumps({'rows': 2650, 'decompressed_sha256': hashlib.sha256(raw).hexdigest()}))
