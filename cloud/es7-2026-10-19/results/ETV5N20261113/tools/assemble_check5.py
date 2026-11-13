"""Assemble the pbb5 master tree and context subtrees into one tree and replay it with the repo's
independent exact checker scripts/omission_tree.check_tree (allow_pending: the two fixed-state children).
usage: assemble_check5.py <rows.json> <outdir>"""
import gzip, json, sys, hashlib
from pathlib import Path
sys.path.insert(0, '/home/jay/research/lean/erdos-szekeres-lean/scripts')
from omission_tree import check_tree
import etv_common as ec
rowsfile, outdir = sys.argv[1], Path(sys.argv[2])
rows = [(s, d) for s, d in json.load(open(rowsfile))]
master = json.loads((outdir / 'master.json').read_text())
nodes = list(master['nodes'])
for i, nd in enumerate(list(nodes)):
    if nd.get('type') == 'context':
        sub = json.load(gzip.open(outdir / f"ctx-{nd['context']}.json.gz"))
        off = len(nodes)
        for x in sub['nodes']:
            y = dict(x)
            if y.get('type') == 'branch': y['zero'] += off; y['one'] += off
            nodes.append(y)
        # replace context node by the subtree root: copy root into place i and remap
        root = nodes[off + sub['root']]
        nodes[i] = root; nodes[off + sub['root']] = {'type': 'dead'}
# drop dead nodes by renumbering
alive = [i for i, x in enumerate(nodes) if x.get('type') != 'dead']
ren = {i: k for k, i in enumerate(alive)}
out = []
for i in alive:
    y = dict(nodes[i])
    if y.get('type') == 'branch': y['zero'] = ren[y['zero']]; y['one'] = ren[y['one']]
    out.append(y)
res = check_tree(ec.N, rows, master['budget'], out, ren[master['root']], allow_pending=True)
pend = [x for x in out if x.get('type') == 'pending']
assert len(pend) == 2 and all('fixed state' in x.get('note', '') for x in pend), pend
tree = {'rows_sha256': hashlib.sha256(open(rowsfile, 'rb').read()).hexdigest(), 'hole_budget': master['budget'], 'root': ren[master['root']], 'nodes': out}
data = json.dumps(tree, separators=(',', ':')).encode()
with gzip.open(outdir / 'tree.json.gz', 'wb') as f: f.write(data)
res['tree_sha256'] = hashlib.sha256(data).hexdigest(); res['pending_fixed_state_children'] = len(pend)
print(json.dumps(res))
