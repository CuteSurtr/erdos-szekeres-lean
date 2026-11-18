#!/usr/bin/env python3
"""Exact deletion check; a returned SAT witness is directly checked geometrically."""
import itertools
import json
from pathlib import Path
from pysat.solvers import Glucose4
from audit_cup15 import turn, hull

root = Path('/home/jay/research/data/delta3-codex-20261113/coordinator/cup15')
source = json.loads((root/'realized.json').read_text())
P = source['P']
results = []
for deleted in range(len(P)):
    Q = P[:deleted]+P[deleted+1:]
    m = len(Q)
    caps = [k for k in itertools.combinations(range(m), 4)
            if all(turn(Q[a], Q[b], Q[c]) < 0 for a,b,c in itertools.combinations(k, 3))]
    cups = set()
    for g in itertools.combinations(range(m), 5):
        lo, up = hull(Q, g)
        if len(lo)+len(up)-2 == 5:
            cups.add(tuple(lo))
    clauses = [[-i-1 for i in k] for k in caps]+[[i+1 for i in k] for k in sorted(cups)]
    with Glucose4(bootstrap_with=clauses) as s:
        sat = s.solve()
        D = {x-1 for x in (s.get_model() or []) if 0 < x <= m}
    result = {'deleted_original_index': deleted, 'exists_cup_delta': sat}
    if sat:
        assert not any(set(k) <= D for k in caps)
        assert all(set(c) & D for c in cups)
        result['Delta_in_original_indices'] = [i if i < deleted else i+1 for i in sorted(D)]
    else:
        # Standalone exhaustive check independent of solver outcome.
        cap_masks = [sum(1 << i for i in k) for k in caps]
        cup_masks = [sum(1 << i for i in k) for k in cups]
        count = sum(not any(d & k == k for k in cap_masks) and all(d & c for c in cup_masks)
                    for d in range(1 << m))
        assert count == 0
        result['independent_count'] = count
        (root/f'delete_{deleted}_counterexample.json').write_text(json.dumps({'P':Q,'n':6,'m':m})+'\n')
    results.append(result)
out = {'label':'COMPUTED', 'deletion_minimal':all(r['exists_cup_delta'] for r in results), 'results':results}
(root/'deletions.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
