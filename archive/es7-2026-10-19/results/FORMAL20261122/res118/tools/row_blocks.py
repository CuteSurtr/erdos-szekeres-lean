#!/usr/bin/env python3
"""Assert how the unit rows of the six slice files nest (read-only; res118-lean, 22 Nov 2026).

Prints the block structure (rows as ordered lists, file order) used by tools/gen_lean.py:
  P   = s19 rows 2..       (812 pool rows)
  Q   = s18-v13 rows 2.. after P     (expected 208)
  U16 = b35s19-v16 rows after the first 1,020   (expected 35)
  A   = b35s20-v169 rows after the first 1,020  (expected 970)
Any deviation raises.
"""
import json, sys
from pathlib import Path
W = Path('/home/jay/research/data/es308-20261114/inputs')
def unit(p):
    ex = json.loads(Path(p).read_text())
    assert all(r['rhs'] == 1 for r in ex[2:])
    return [r['support'] for r in ex[2:]]
s19 = unit(W / 's19/extra.json')
s18 = unit(W / 's18-v13/extra.json')
b18 = unit(W / 'b35s18-v13/extra.json')
b19 = unit(W / 'b35s19-v16/extra.json')
b20 = unit(W / 'b35s20-v169/extra.json')
res = {}
res['s19_len'] = len(s19); res['s18_len'] = len(s18); res['b18_len'] = len(b18); res['b19_len'] = len(b19); res['b20_len'] = len(b20)
res['s19_is_prefix_of_s18'] = s18[:len(s19)] == s19
res['s18_eq_b18'] = s18 == b18
res['s18_is_prefix_of_b19'] = b19[:len(s18)] == s18
res['s18_is_prefix_of_b20'] = b20[:len(s18)] == s18
print(json.dumps(res, indent=1))
if not res['s19_is_prefix_of_s18']:
    # where do the pool rows sit inside s18?
    pos = {tuple(r): i for i, r in enumerate(s18)}
    idx = [pos.get(tuple(r)) for r in s19]
    print('s19 rows found in s18:', sum(i is not None for i in idx), 'monotone:', all(a < b for a, b in zip(idx, idx[1:]) if a is not None and b is not None))
    print('first positions', idx[:20])
