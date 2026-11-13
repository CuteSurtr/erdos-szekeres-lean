"""Assemble pbb.py context subtrees into one omission tree and replay it exactly.

The root branches on state 0: the 'zero' child (state 0 occupied) is the searched
tree; the 'one' child (state 0 missing) stays pending, to be discharged by the
separately proved occupancy of state 0.
"""
import gzip, json, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
from omission_tree import check_tree
from omission_row_probe import read_rows

outdir = Path(sys.argv[1]); target = sys.argv[2] if len(sys.argv) > 2 else None
master = json.loads((outdir / 'master.json').read_text())
import hashlib
src = json.load(gzip.open(master['source']) if master['source'].endswith('.gz') else open(master['source']))
SRC_SHA = hashlib.sha256(open(sys.argv[3],'rb').read()).hexdigest() if len(sys.argv) > 3 else None
if master.get('extra'):
    src['constraints'] += json.load(open(master['extra']))
n, rows = read_rows(src)
nodes = [{'type': 'branch', 'vertex': 0, 'zero': 1, 'one': 2}, None, {'type': 'pending'}]
offset = len(nodes) - 1  # master node i -> offset + i  (master root 0 -> 1)
mnodes = master['nodes']
nodes[1:2] = []  # placeholder removed; rebuild
if master.get('root_occupied', [0]) == [0]:
    # Residual: the root branches on state 0; only the occupied side is searched.
    nodes = [{'type': 'branch', 'vertex': 0, 'zero': 2, 'one': 1}, {'type': 'pending'}]
else:
    assert master.get('root_occupied') == [], 'unsupported root context'
    nodes = []  # Balanced: the master root is the tree root.
base = len(nodes)
def remap(node, shift):
    if node['type'] == 'branch':
        return {'type': 'branch', 'vertex': node['vertex'], 'zero': node['zero'] + shift, 'one': node['one'] + shift}
    return node
ctx_slots = {}
for i, nd in enumerate(mnodes):
    if nd.get('type') == 'context':
        ctx_slots[nd['context']] = base + i
        nodes.append({'type': 'pending'})
    else:
        nodes.append(remap(nd, base))
closed = 0
for cid, slot in ctx_slots.items():
    p = outdir / f'ctx-{cid}.json.gz'
    if not p.exists():
        continue
    rec = json.load(gzip.open(p))
    shift = len(nodes)
    sub = [remap(x, shift) for x in rec['nodes']]
    # The subtree root replaces the pending slot.
    nodes[slot] = sub[0]
    nodes.extend(sub)  # index shift+0 becomes unreachable duplicate; mark it
    nodes[shift] = {'type': 'pending'}  # orphan; removed below
    closed += 1
# Remove orphans by rebuilding reachable nodes.
order = {}; new = []
stack = [0]
while stack:
    i = stack.pop()
    if i in order: continue
    order[i] = len(new); new.append(i)
    nd = nodes[i]
    if nd['type'] == 'branch': stack += [nd['one'], nd['zero']]
final = []
for i in new:
    nd = dict(nodes[i])
    if nd['type'] == 'branch': nd['zero'] = order[nd['zero']]; nd['one'] = order[nd['one']]
    final.append(nd)
res = check_tree(n, rows, master['budget'], final, 0, allow_pending=True)
print(json.dumps({'contexts_closed': closed, 'contexts_total': len(ctx_slots), 'nodes': len(final), 'replay': res}))
if target:
    with gzip.open(target, 'wt', compresslevel=6) as f:
        json.dump({'hole_budget': master['budget'], 'source_sha256': SRC_SHA, 'root': 0, 'nodes': final}, f, separators=(',', ':'))
