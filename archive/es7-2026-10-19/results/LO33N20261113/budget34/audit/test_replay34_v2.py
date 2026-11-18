"""Self-check of replay34_v2.frontier: labels may skip numbers; everything else still fails closed."""
import json
from pathlib import Path
import replay34_v2 as v2
import replay34 as v1

def m(nodes, contexts, leaves): return {'nodes': nodes, 'root': 0, 'contexts': contexts, 'master_leaves': leaves}
br = lambda v, z, o: {'type': 'branch', 'vertex': v, 'zero': z, 'one': o}
ctx = lambda c: {'type': 'context', 'context': c}
ok = m([br(3, 1, 2), ctx(0), ctx(7)], 2, 0)
assert v2.frontier(ok) == {0: ((0, 0), (3, 0)), 7: ((0, 0), (3, 1))}
def fails(master):
    try: v2.frontier(master)
    except AssertionError: return True
    return False
assert fails(m([br(3, 1, 2), ctx(7), ctx(7)], 2, 0))           # duplicate label
assert fails(m([br(3, 1, 2), ctx(0), ctx(7)], 3, 0))           # count mismatch
assert fails(m([br(3, 1, 1), ctx(0), ctx(7)], 1, 0))           # unreachable node
assert fails(m([br(3, 1, 2), ctx(0), {'type': 'pending'}], 1, 0))  # uncertified leaf
assert fails(m([br(3, 1, 2), ctx(0), ctx(-1)], 2, 0))          # non-natural label
try: v1.frontier(ok); raise SystemExit('v1 unexpectedly accepted skipped labels')
except AssertionError: pass
W = Path('/home/jay/research/data/es308-20261114/runs/s20')
old = v1.frontier(json.loads((W / 'bb/master.json').read_text()))
new = v2.frontier(json.loads((W / 'bb-s1/master.json').read_text()))
closed = {int(p.name[4:-8]) for p in (W / 'bb').glob('ctx-*.json.gz')}
assert len(old) == 4064 and len(new) == 4274 and len(closed) == 4034
assert all(new[c] == old[c] for c in closed), 'a closed context changed its path'
split = set(old) - closed
assert all(any(new[d][:len(old[c])] == old[c] for c in split) for d in set(new) - closed), 'new context outside split ones'
assert all(sum(1 for d in set(new) - closed if new[d][:len(old[c])] == old[c]) == 8 for c in split)
print('replay34_v2 self-check PASS: synthetic 6 cases; real: 4034 closed paths identical, 30 x 8 split descendants')
