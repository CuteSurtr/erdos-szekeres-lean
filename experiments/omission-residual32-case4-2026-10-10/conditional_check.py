#!/usr/bin/env python3
"""Exact conditional replay; adapted from archived resume checker. No Lean claim."""
import argparse,gzip,json,hashlib
from pathlib import Path

def natural(x):
    return type(x) is int and x >= 0


def replay(proof, rows, n, context, allow_pending=False):
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
    pending = 0
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
        elif node['type'] == 'pending' and allow_pending:
            pending += 1
        else:
            raise ValueError('Incomplete or unsupported leaf')
    if len(seen) != len(nodes):
        raise ValueError('Unreachable tree data')
    return {'nodes': len(nodes), 'weighted_leaves': len(margins),
            'over_budget_leaves': over, 'pending': pending, 'complete': pending == 0, 'minimum_margin': min(margins, default=None)}


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('tree',type=Path);p.add_argument('--allow-pending',action='store_true');a=p.parse_args()
    raw=a.source.read_bytes();source=json.loads(raw)
    with (gzip.open(a.tree,'rt') if a.tree.suffix=='.gz' else a.tree.open()) as f:proof=json.load(f)
    assert hashlib.sha256(raw).hexdigest()==proof['source_sha256']=='f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909'
    assert proof['original_node']==4
    print(json.dumps(replay(proof,[(r['support'],r['rhs']) for r in source['constraints']],len(source['states']),{'missing':[54],'occupied':[43,67]},a.allow_pending),indent=2))
