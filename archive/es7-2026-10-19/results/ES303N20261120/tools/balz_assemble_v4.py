#!/usr/bin/env python3
"""Assemble and replay a balanced budget-B tree on the catalog + Z-row + Z*-row (v4, 20 Nov 2026).

v4 = v3 with a second extra row, the Z*-row: support Z* = states with f(0) = 5 and f(4) >= 1 (70 states), rhs 15
(Lean OmissionZStarRow.zs_row, zrow/leanzs/LemmaZStar.lean; N66 <= 55). Rows: catalog, Z-row, Z*-row (3,133).

Rows: the 3,131 rows of balanced-v2-source.json (Lean catalog) followed by ONE extra row, the Z-row:
  support Z = Ferrers states with f(0) <= 4 and f(4) = 0 (70 states), rhs 15.
  Lemma Z: owners of Z-states end no 6-cup and no 6-cap, so they form a set with no 6-cap, no 6-cup and no convex
  octagon; N66 <= 55 (CERTIFIED, N66N20261113) bounds them by 55, so at least 70 - 55 = 15 Z-states are holes.
State 0 is free: the tree is a branch on state 0 whose zero side is the fastbb256 packet OCC (solved on the full rows,
fastbb fixes 0 occupied itself) and whose one side is the packet MIS (solved on the rows with state 0 removed from
every support and every rhs lowered by one where 0 was in the support, budget B - 1; row indices are unchanged, so a
reduced weighted leaf has the same margin in the original instance with 0 missing).
Output: one file per leaf of either master (a context placeholder or a leaf closed in the master), in the format
read by balcheck.cpp: {context, budget, missing, occupied, path, status, root, nodes}; path starts with (0, side).
Replay (trusted core scripts/omission_tree.check_tree): every file, prefixed by its path as a chain of branches with
pending side children, on the original rows + Z-row at budget B; ok iff pending == path length. Summary to OUT/summary.json.
usage: balz_assemble_v3.py B OCC_DIR MIS_DIR OUT_DIR WORKERS
v3 (19 Nov 19:50): MIS_DIR "-" = zero side only. Every file then has the pending side (0 missing) of its first
branch, discharged in Lean by FixedStatesZ.zero_mem_occupied (ExcludesHoleBudgetZF assumes h_0 = 0); the cover
check (balcheck2) must then be given the lemma path "0:1".
"""
import gzip, hashlib, json, os, sys
from multiprocessing import Pool
sys.path.insert(0, '/home/jay/research/lean/erdos-szekeres-lean/scripts')
from omission_row_probe import read_rows
from omission_tree import check_tree

CAT = '/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
CAT_SHA = 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72'
B, OCC, MIS, OUT, NW = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
raw = open(CAT, 'rb').read(); assert hashlib.sha256(raw).hexdigest() == CAT_SHA
cat = json.loads(raw)
Z = [i for i, f in enumerate(cat['states']) if f[0] <= 4 and f[4] == 0]
assert len(Z) == 70 and 0 in Z
n, rows = read_rows(cat)
Zs = [i for i, f in enumerate(cat['states']) if f[0] == 5 and f[4] >= 1]
assert len(Zs) == 70 and Zs == json.load(open('/home/jay/research/data/bal186-20261119/zrow/zstar.json'))['zstar']
rows = rows + [(Z, 15), (Zs, 15)]
assert n == 252 and len(rows) == 3133


def descriptors(side_dir, b0, expect_budget):
    """walk the master only; return light descriptors (path, side_dir, ctx id or the closed master leaf)"""
    m = json.load(open(os.path.join(side_dir, 'master.json')))
    assert m['budget'] == expect_budget, (side_dir, m['budget'], expect_budget)
    nodes = m['nodes']; out = []
    st = [(m['root'], [(0, b0)])]
    seen = set()
    while st:
        i, path = st.pop(); assert i not in seen; seen.add(i); nd = nodes[i]
        if nd['type'] == 'branch':
            v = nd['vertex']; assert v != 0
            st.append((nd['zero'], path + [(v, 0)])); st.append((nd['one'], path + [(v, 1)]))
        elif nd['type'] == 'context':
            out.append((path, side_dir, nd['context'], None))
        elif nd['type'] in ('weighted', 'over_budget'):
            out.append((path, side_dir, None, nd))
        else:
            raise ValueError('unexpected master node ' + nd['type'])
    assert len(seen) == len(nodes), 'unreachable master nodes'
    return out


def one(args):
    """v2 (17:45): load, write and check ONE context in the worker (v1 held every context in the parent: 6 GB)"""
    k, path, side_dir, c, leaf = args
    if c is not None:
        sub = json.loads(gzip.decompress(open(os.path.join(side_dir, f'ctx-{c}.json.gz'), 'rb').read()))
        pm = {v for v, b in path if b == 1 and v != 0}; po = {v for v, b in path if b == 0 and v != 0} | {0}
        assert set(sub['missing']) == pm and set(sub['occupied']) == po, ('fastbb context fixings differ from the master path', c)
        root, nodes = sub['root'], sub['nodes']
    else:
        root, nodes = 0, [leaf]
    rec = {'context': k, 'budget': B, 'missing': sorted(v for v, b in path if b == 1),
           'occupied': sorted(v for v, b in path if b == 0), 'path': [list(x) for x in path], 'status': 'closed',
           'root': root, 'nodes': nodes}
    with open(os.path.join(OUT, f'ctx-{k}-zb{B}.json.gz'), 'wb') as raw_f, \
            gzip.GzipFile(fileobj=raw_f, mode='wb', compresslevel=6, mtime=0) as f:
        f.write(json.dumps(rec, separators=(',', ':')).encode())
    L = len(path); full = [None] * (2 * L)
    for j, (v, b) in enumerate(path):
        cont, side = 2 * (j + 1), 2 * j + 1
        full[2 * j] = {'type': 'branch', 'vertex': v, 'zero': cont if b == 0 else side, 'one': cont if b == 1 else side}
        full[side] = {'type': 'pending'}
    order = [root] + [j for j in range(len(nodes)) if j != root]
    pos = {j: 2 * L + t for t, j in enumerate(order)}
    for j in order:
        s = dict(nodes[j])
        if s['type'] == 'branch':
            s['zero'] = pos[s['zero']]; s['one'] = pos[s['one']]
        full.append(s)
    r = check_tree(n, rows, B, full, 0, allow_pending=True)
    return k, r['pending'] == L, r['leaves'] - r['pending'], r['minimum_margin'], len(nodes)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    items = descriptors(OCC, 0, B) + ([] if MIS == '-' else descriptors(MIS, 1, B - 1))
    with Pool(NW, maxtasksperchild=200) as pool:
        res = pool.map(one, [(k,) + it for k, it in enumerate(items)], chunksize=4)
    bad = [k for k, ok, _, _, _ in res if not ok]
    mins = [m for _, ok, _, m, _ in res if m is not None]
    summ = {'label': 'EXACT TREE (check_tree on every assembled file)' if not bad else 'NOT CONFIRMED',
            'budget': B, 'rows': len(rows), 'z_row': {'support_size': 70, 'rhs': 15}, 'zstar_row': {'support_size': 70, 'rhs': 15}, 'files': len(items),
            'bad': bad[:20], 'leaves': sum(x[2] for x in res), 'nodes': sum(x[4] for x in res),
            'minimum_margin': min(mins) if mins else None,
            'occ_master_sha256': hashlib.sha256(open(os.path.join(OCC, 'master.json'), 'rb').read()).hexdigest(),
            'mis_master_sha256': None if MIS == '-' else hashlib.sha256(open(os.path.join(MIS, 'master.json'), 'rb').read()).hexdigest(),
            'zero_side_only': MIS == '-'}
    json.dump(summ, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
    print(json.dumps(summ))
    sys.exit(0 if not bad else 1)
