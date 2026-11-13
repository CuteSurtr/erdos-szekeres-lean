#!/usr/bin/env python3
"""Replay complete conditional Boolean-row trees using unbounded Python integers.

This is not a Lean checker. The input catalog and contexts are fixed by hashes,
and every proof remains conditional on its explicit missing/occupied states.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def natural(x):
    return type(x) is int and x >= 0


def replay(proof, rows, n, context):
    missing, occupied = proof['missing'], proof['occupied']
    for values in (missing, occupied):
        if len(values) != len(set(values)) or not all(natural(i) and i < n for i in values):
            raise ValueError('Malformed fixed context')
    if set(missing) & set(occupied):
        raise ValueError('Conflicting fixed context')
    if missing != context['missing'] or occupied != context['occupied']:
        raise ValueError('Context differs from the frozen checkpoint')
    if proof['hole_budget'] != 32:
        raise ValueError('Unexpected hole budget')
    nodes = proof['nodes']
    stack = [(proof['root'], frozenset(missing), frozenset(occupied))]
    seen = set()
    margins = []
    over = 0
    while stack:
        index, M, O = stack.pop()
        if not natural(index) or index >= len(nodes) or index in seen:
            raise ValueError('Repeated or invalid node')
        seen.add(index)
        node = nodes[index]
        if node['type'] == 'branch':
            i = node['vertex']
            if not natural(i) or i >= n or i in M | O:
                raise ValueError('Repeated or invalid branch variable')
            stack.extend([(node['zero'], M, O | {i}), (node['one'], M | {i}, O)])
        elif node['type'] == 'over_budget':
            if len(M) <= 32:
                raise ValueError('Unjustified budget leaf')
            over += 1
        elif node['type'] == 'weighted':
            cap = node['capacity']
            if not natural(cap):
                raise ValueError('Invalid capacity')
            loads = [0] * n
            demand = 0
            used = set()
            for r, w in node['weights']:
                if not natural(r) or r >= len(rows) or r in used or not natural(w):
                    raise ValueError('Invalid row multiplier')
                used.add(r)
                support, rhs = rows[r]
                demand += w * max(rhs - sum(i in M for i in support), 0)
                for i in support:
                    loads[i] += w
            capacity = cap * (32 - len(M))
            capacity += sum(max(loads[i] - cap, 0) for i in range(n) if i not in M | O)
            if demand <= capacity:
                raise ValueError('Nonpositive exact integer margin')
            margins.append(demand - capacity)
        else:
            raise ValueError('Incomplete or unsupported leaf')
    if len(seen) != len(nodes):
        raise ValueError('Unreachable tree data')
    return {'nodes': len(nodes), 'weighted_leaves': len(margins),
            'over_budget_leaves': over, 'minimum_margin': min(margins, default=None)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    base = args.bundle
    manifest = json.loads((base / 'manifest.json').read_text())
    source_bytes = gzip.decompress((base / manifest['source_reference']).read_bytes())
    if digest(source_bytes) != manifest['source_sha256']:
        raise ValueError('Source hash mismatch')
    data = json.loads(source_bytes)
    rows = [(r['support'], r['rhs']) for r in data['constraints']]
    n = len(data['states'])
    for support, rhs in rows:
        if len(set(support)) != len(support) or not natural(rhs) or rhs > len(support):
            raise ValueError('Malformed row')
        if not all(natural(i) and i < n for i in support):
            raise ValueError('Malformed row support')
    pending_raw = (base / manifest['original_contexts_reference']).read_bytes()
    if digest(pending_raw) != manifest['original_contexts_sha256']:
        raise ValueError('Context hash mismatch')
    contexts = {c['node']: c for c in json.loads(pending_raw)['contexts']}
    checked = []
    for item in manifest['conditional_certificates']:
        raw = (base / item['file']).read_bytes()
        if digest(raw) != item['sha256']:
            raise ValueError('Certificate hash mismatch')
        proof = json.loads(gzip.decompress(raw))
        if proof['source_sha256'] != manifest['source_sha256']:
            raise ValueError('Certificate/source mismatch')
        result = replay(proof, rows, n, contexts[proof['original_node']])
        if result != item['checked']:
            raise ValueError('Recorded result mismatch')
        checked.append({'original_node': proof['original_node'], **result})
    print(json.dumps({'scope': 'Exact integer replay only; conditional trees, not Lean proofs',
                      'source_rows': len(rows), 'certificates': checked}, indent=2))


if __name__ == '__main__':
    main()
