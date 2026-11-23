#!/usr/bin/env python3
"""balz_assemble_v5n54.py = balz_assemble_v5.py (sha256 964b00007e5b...f6ad) with both extra rows at rhs 16 (b69-prep,
22 Nov 2026). VALID ONLY WITH N66 <= 54 (level-15 cube campaign N66N20261113/cubes20261120 section 8, CERTIFIED and
independently verified; marker zrow/N66_LE_54_VERIFIED): 70 - 54 = 16 holes in Z and in Z*. Lean:
OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 B (ES303N20261120/BalancedBudgetsZZsN.lean). The same changes that
balz_assemble_n54.py makes to v4, plus the summary field assembler = this file.
(v5 text:) Assemble and replay a balanced budget-B tree on the catalog + Z-row + Z*-row (v4, 20 Nov 2026).

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
from array import array
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
RHS = 16                                                          # n54: 70 - 54
rows = rows + [(Z, RHS), (Zs, RHS)]
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



BIG_BYTES = int(os.environ.get('BIG_BYTES', str(10 * 10**6)))   # contexts whose .json.gz is larger go to one_big
SUB_NODES = int(os.environ.get('SUB_NODES', '30000'))          # max nodes per subtree handed to check_tree


def prefix_nodes(path):
    """the same branch/pending prefix that one() builds (v4): branch on v, continuation at 2(j+1), pending side 2j+1"""
    L = len(path); full = [None] * (2 * L)
    for j, (v, b) in enumerate(path):
        cont, side = 2 * (j + 1), 2 * j + 1
        full[2 * j] = {'type': 'branch', 'vertex': v, 'zero': cont if b == 0 else side, 'one': cont if b == 1 else side}
        full[side] = {'type': 'pending'}
    return full


def one_big(args):
    """v5 (22 Nov): memory-lean replacement of one() for very large contexts.
    (a) Streams the context once: writes the SAME output file as one() (byte-identical: json.dumps of the record with
        separators (',', ':') is the concatenation written here) and records, per node, its text offset and, for
        branches, (vertex, zero, one).
    (b) Validates the context's node graph globally: every index in range, every node reached exactly once from the
        root, no unreachable node (as contexts() does inside check_tree for the whole tree).
    (c) Cuts the context tree into subtrees of at most SUB_NODES nodes (a node is a cut root iff its subtree is small
        enough and its parent's is not); every node above the cut is a branch.
    (d) For each cut root f with in-context branch path P_f, calls the UNCHANGED check_tree on
        prefix(path + P_f) + subtree(f) with allow_pending=True and requires pending == len(path) + len(P_f), i.e. the
        only pending leaves are the prefix side leaves. Each leaf is therefore checked with exactly the fixings it has
        in the full assembled tree, and every leaf lies in exactly one subtree.
    Returns the same tuple as one(): (k, ok, non-pending leaves, minimum margin, number of context nodes)."""
    k, path, side_dir, c, leaf = args
    assert c is not None
    text = gzip.decompress(open(os.path.join(side_dir, f'ctx-{c}.json.gz'), 'rb').read()).decode('ascii')
    pos = text.find('"nodes":[')
    assert pos > 0, ('no nodes key', c)
    head = json.loads(text[:pos] + '"nodes":[]}')
    assert list(head) == ['context', 'missing', 'occupied', 'root', 'nodes'] and head['context'] == c, ('header', c)
    pm = {v for v, b in path if b == 1 and v != 0}; po = {v for v, b in path if b == 0 and v != 0} | {0}
    assert set(head['missing']) == pm and set(head['occupied']) == po, ('fastbb context fixings differ from the master path', c)
    root = head['root']
    rec = {'context': k, 'budget': B, 'missing': sorted(v for v, b in path if b == 1),
           'occupied': sorted(v for v, b in path if b == 0), 'path': [list(x) for x in path], 'status': 'closed',
           'root': root}
    hdr = json.dumps(rec, separators=(',', ':'))
    assert hdr.endswith('}')
    dec = json.JSONDecoder()
    offs = array('q'); isbr = bytearray(); bv = array('q'); bz = array('q'); bo = array('q')
    i = pos + len('"nodes":[')
    with open(os.path.join(OUT, f'ctx-{k}-zb{B}.json.gz'), 'wb') as raw_f, \
            gzip.GzipFile(fileobj=raw_f, mode='wb', compresslevel=6, mtime=0) as f:
        f.write((hdr[:-1] + ',"nodes":[').encode())
        first = True
        while True:
            node, j = dec.raw_decode(text, i)
            assert isinstance(node, dict)
            f.write(((',' if not first else '') + json.dumps(node, separators=(',', ':'))).encode()); first = False
            offs.append(i)
            if node.get('type') == 'branch':
                if not all(type(node.get(key)) is int for key in ('vertex', 'zero', 'one')):
                    raise ValueError('Repeated or invalid branch variable')   # natural() would reject bools/floats too
                isbr.append(1); bv.append(node.get('vertex')); bz.append(node.get('zero')); bo.append(node.get('one'))
            else:
                isbr.append(0); bv.append(-1); bz.append(-1); bo.append(-1)
            if text[j] == ',':
                i = j + 1
            else:
                assert text[j:] == ']}', ('trailing text', c, text[j:j + 20])
                break
        f.write(b']}')
    N = len(offs)
    # (b) global validation: in range, each node reached once, all reached; subtree sizes by post-order
    def kid(x):
        if not (type(x) is int and 0 <= x < N):
            raise ValueError('Repeated or invalid tree node')
        return x
    assert type(root) is int and 0 <= root < N
    seen = bytearray(N); size = array('q', [0]) * N; order = []
    st = [root]
    while st:
        x = st.pop()
        if seen[x]:
            raise ValueError('Repeated or invalid tree node')
        seen[x] = 1; order.append(x)
        if isbr[x]:
            st.append(kid(bz[x])); st.append(kid(bo[x]))
    if len(order) != N:
        raise ValueError('Unreachable tree nodes')
    for x in reversed(order):
        size[x] = 1 + (size[bz[x]] + size[bo[x]] if isbr[x] else 0)
    del order
    # (c) cut roots with their in-context paths
    cuts = []; st = [(root, ())]; upper = 0
    while st:
        x, p = st.pop()
        if size[x] <= SUB_NODES:
            cuts.append((x, p))
        else:
            assert isbr[x]; upper += 1
            st.append((bz[x], p + ((bv[x], 0),))); st.append((bo[x], p + ((bv[x], 1),)))
    # (d) unchanged check_tree on each piece
    ok = True; leaves = 0; mins = []; covered = 0
    for x, p in cuts:
        full = prefix_nodes(list(path) + list(p))
        sub = []; st = [x]
        while st:
            y = st.pop(); sub.append(y)
            if isbr[y]:
                st.append(bz[y]); st.append(bo[y])
        base = len(full); posn = {y: base + t for t, y in enumerate(sub)}
        for y in sub:
            s = dec.raw_decode(text, offs[y])[0]
            if s.get('type') == 'branch':
                s['zero'] = posn[s['zero']]; s['one'] = posn[s['one']]
            full.append(s)
        r = check_tree(n, rows, B, full, 0, allow_pending=True)
        need = len(path) + len(p)
        ok = ok and r['pending'] == need
        leaves += r['leaves'] - r['pending']; covered += len(sub)
        if r['minimum_margin'] is not None:
            mins.append(r['minimum_margin'])
    ok = ok and covered + upper == N
    return k, ok, leaves, (min(mins) if mins else None), N


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    items = descriptors(OCC, 0, B) + ([] if MIS == '-' else descriptors(MIS, 1, B - 1))
    jobs = [(k,) + it for k, it in enumerate(items)]
    def is_big(j):
        return j[3] is not None and os.path.getsize(os.path.join(j[2], f'ctx-{j[3]}.json.gz')) > BIG_BYTES
    small = [j for j in jobs if not is_big(j)]; big = [j for j in jobs if is_big(j)]
    NWB = int(os.environ.get('NW_BIG', str(max(1, NW // 2))))
    print(json.dumps({'small_contexts': len(small), 'big_contexts': len(big), 'BIG_BYTES': BIG_BYTES,
                      'SUB_NODES': SUB_NODES, 'NW': NW, 'NW_BIG': NWB}), flush=True)
    with Pool(NWB, maxtasksperchild=20) as pool:          # big pool first: a failure surfaces early
        res = pool.map(one_big, big, chunksize=1)
    print(json.dumps({'big_done': len(res)}), flush=True)
    with Pool(NW, maxtasksperchild=200) as pool:
        res += pool.map(one, small, chunksize=4)
    res.sort()
    bad = [k for k, ok, _, _, _ in res if not ok]
    mins = [m for _, ok, _, m, _ in res if m is not None]
    summ = {'label': 'EXACT TREE (check_tree on every assembled file; files above BIG_BYTES piecewise by the unchanged check_tree, one_big)' if not bad else 'NOT CONFIRMED',
            'budget': B, 'rows': len(rows), 'z_row': {'support_size': 70, 'rhs': RHS}, 'zstar_row': {'support_size': 70, 'rhs': RHS}, 'requires': 'N66 <= 54', 'files': len(items),
            'bad': bad[:20], 'leaves': sum(x[2] for x in res), 'nodes': sum(x[4] for x in res),
            'minimum_margin': min(mins) if mins else None,
            'occ_master_sha256': hashlib.sha256(open(os.path.join(OCC, 'master.json'), 'rb').read()).hexdigest(),
            'mis_master_sha256': None if MIS == '-' else hashlib.sha256(open(os.path.join(MIS, 'master.json'), 'rb').read()).hexdigest(),
            'zero_side_only': MIS == '-', 'assembler': 'balz_assemble_v5n54.py', 'big_contexts': len(big),
            'BIG_BYTES': BIG_BYTES, 'SUB_NODES': SUB_NODES}
    json.dump(summ, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
    print(json.dumps(summ))
    sys.exit(0 if not bad else 1)
