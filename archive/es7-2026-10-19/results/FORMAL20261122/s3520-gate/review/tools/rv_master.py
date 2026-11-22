# Reviewer's own walker over the s35_20 master tree (bb-s1/master.json); no worker code imported.
# Prints node/context statistics and the Lean mask path of context 4274 (innermost decision first, then (0, 2)).
import json, sys, re, hashlib
S = '/home/jay/research/data/es308-20261114/runs/b35s20/bb-s1'
G = '/home/jay/research/data/formalize-20261122/s3520-gate'
raw = open(S + '/master.json', 'rb').read()
print('master sha256', hashlib.sha256(raw).hexdigest())
m = json.loads(raw)
nodes = m['nodes']
types = {}
for nd in nodes: types[nd['type']] = types.get(nd['type'], 0) + 1
print('budget', m['budget'], 'root', m['root'], 'nodes', len(nodes), types, 'contexts field', m['contexts'], 'master_leaves field', m.get('master_leaves'))
# walk from the root with an explicit stack; path entries (vertex, 2) for the zero child, (vertex, 1) for the one child
parent_seen = [0] * len(nodes)
paths = {}           # context id -> path outermost first
leaves = 0
stack = [(m['root'], [])]
while stack:
    i, p = stack.pop()
    parent_seen[i] += 1
    nd = nodes[i]
    if nd['type'] == 'branch':
        stack.append((nd['zero'], p + [(nd['vertex'], 2)]))
        stack.append((nd['one'], p + [(nd['vertex'], 1)]))
    elif nd['type'] == 'context':
        assert nd['context'] not in paths
        paths[nd['context']] = p
    else:
        leaves += 1
assert all(x == 1 for x in parent_seen), 'not a tree / unreachable nodes'
ids = sorted(paths)
missing_ids = sorted(set(range(ids[-1] + 1)) - set(ids))
print('reached all nodes once: yes; placeholders', len(ids), 'min', ids[0], 'max', ids[-1], 'absent ids', missing_ids, 'master weighted/over leaves', leaves)
# vertices repeated on a path?
rep = [c for c, p in paths.items() if len({v for v, _ in p}) != len(p)]
print('contexts whose master path repeats a vertex:', len(rep))
# headers in contexts.json vs paths (missing = 1s, occupied = 2s plus state 0)
hdr = json.load(open(S + '/contexts.json'))
bad = 0
for h in hdr:
    p = paths[h['context']]
    miss = sorted(v for v, x in p if x == 1); occ = sorted([0] + [v for v, x in p if x == 2])
    if miss != sorted(h['missing']) or occ != sorted(h['occupied']): bad += 1
print('contexts.json headers', len(hdr), 'mismatching their master path:', bad)
p4274 = list(reversed(paths[4274])) + [(0, 2)]
lean = '[' + ', '.join('(%d, %d)' % e for e in p4274) + ']'
print('ctx-4274 Lean path (innermost first):', lean)
open(sys.argv[1], 'w').write(lean)
# compare with the worker's U2080.root statement
u = open(G + '/export/3520/src/RS3520/U2080.lean').read()
mm = re.search(r'theorem root : (.*?) := ex', u)
want = '¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3520 4642 154 35 (pmask (zerosF 154) ' + lean + ') holes'
print('U2080.root statement equals the expected text:', mm.group(1) == want)
