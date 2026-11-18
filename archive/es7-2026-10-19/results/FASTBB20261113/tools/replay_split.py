#!/usr/bin/env python3
"""Exact replay of a fastbb / pbb_strong output directory, one context at a time.

Usage (from the repository root):  replay_split.py OUTDIR [--jobs J] [--only-closed]

assemble.py builds one big list of nodes and calls scripts/omission_tree.check_tree once; that needs
all context trees in memory together.  This script performs the same check piecewise, with the same
trusted function (check_tree, unchanged, unbounded Python integers):

 1. master.json is replayed with every 'context' node treated as pending.  The path of each context
    node (its missing / occupied sets) is recomputed from the master tree itself.
 2. Every ctx-N.json.gz is checked to state exactly that path, and its subtree is replayed below a
    chain of branch nodes that recreates the path (the other child of each chain node is pending).

The union of the two steps is the assembled tree of assemble.py: the root branches on state 0
(missing side pending, as in assemble.py), every master leaf and every context leaf is checked with
its true path.  Node and leaf totals are reported so that they can be compared with assemble.py.
"""
import gzip, json, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
from omission_tree import check_tree, contexts
from omission_row_probe import read_rows


def load_rows(master):
    src = json.load(gzip.open(master['source']))
    if master.get('extra'):
        src['constraints'] += json.load(open(master['extra']))
    return read_rows(src)


def check_context(args):
    n, rows, budget, path, missing, occupied = args
    rec = json.load(gzip.open(path))
    if sorted(rec['missing']) != sorted(missing) or sorted(rec['occupied']) != sorted(occupied):
        raise ValueError(f'{path}: context sets differ from the master path')
    if rec['root'] != 0:
        raise ValueError('context root must be node 0')
    sub = rec['nodes']
    chain = [(i, 0) for i in sorted(occupied)] + [(i, 1) for i in sorted(missing)]
    k = len(chain)
    nodes = []
    # chain node t has index 2t, its pending sibling 2t+1; the context subtree starts at 2k
    for t, (i, bit) in enumerate(chain):
        nxt = 2 * (t + 1) if t + 1 < k else 2 * k
        pend = 2 * t + 1
        nodes.append({'type': 'branch', 'vertex': i, 'zero': nxt if bit == 0 else pend, 'one': nxt if bit == 1 else pend})
        nodes.append({'type': 'pending'})
    shift = 2 * k
    for nd in sub:
        if nd['type'] == 'branch':
            nodes.append({'type': 'branch', 'vertex': nd['vertex'], 'zero': nd['zero'] + shift, 'one': nd['one'] + shift})
        else:
            nodes.append(nd)
    res = check_tree(n, rows, budget, nodes, 0, allow_pending=True)
    if res['pending'] != k:
        raise ValueError(f'{path}: pending nodes inside a context tree')
    return {'file': Path(path).name, 'nodes': len(sub), 'leaves': res['leaves'] - k, 'minimum_margin': res['minimum_margin']}


def main():
    outdir = Path(sys.argv[1])
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 1
    only_closed = '--only-closed' in sys.argv
    master = json.loads((outdir / 'master.json').read_text())
    n, rows = load_rows(master)
    budget = master['budget']
    # step 1: the master tree below the root branch on state 0 (as in assemble.py)
    mnodes = [{'type': 'branch', 'vertex': 0, 'zero': 2, 'one': 1}, {'type': 'pending'}]
    ctx_index = {}
    for i, nd in enumerate(master['nodes']):
        if nd['type'] == 'branch':
            mnodes.append({'type': 'branch', 'vertex': nd['vertex'], 'zero': nd['zero'] + 2, 'one': nd['one'] + 2})
        elif nd['type'] == 'context':
            ctx_index[i + 2] = nd['context']
            mnodes.append({'type': 'pending'})
        else:
            mnodes.append(nd)
    mres = check_tree(n, rows, budget, mnodes, 0, allow_pending=True)
    if mres['pending'] != 1 + len(ctx_index):
        raise ValueError('unexpected pending nodes in the master tree')
    paths = {}
    for index, missing, occupied in contexts(n, mnodes, 0):
        if index in ctx_index:
            paths[ctx_index[index]] = (sorted(missing), sorted(occupied))
    if len(paths) != len(ctx_index):
        raise ValueError('context nodes are not all leaves of the master tree')
    # step 2: every context
    todo, missing_files = [], []
    for cid, (miss, occ) in sorted(paths.items()):
        p = outdir / f'ctx-{cid}.json.gz'
        if p.exists():
            todo.append((n, rows, budget, str(p), miss, occ))
        else:
            missing_files.append(cid)
    if missing_files and not only_closed:
        print(json.dumps({'complete': False, 'contexts_total': len(paths), 'contexts_missing': len(missing_files),
                          'first_missing': missing_files[:10]}))
    if jobs > 1:
        import multiprocessing as mp
        with mp.Pool(jobs) as pool:
            results = pool.map(check_context, todo, chunksize=1)
    else:
        results = [check_context(a) for a in todo]
    margins = [r['minimum_margin'] for r in results if r['minimum_margin'] is not None]
    if mres['minimum_margin'] is not None:
        margins.append(mres['minimum_margin'])
    master_leaves = mres['leaves'] - mres['pending']
    total_nodes = len(mnodes) - len(results) + sum(r['nodes'] for r in results)
    out = {'contexts_closed': len(results), 'contexts_total': len(paths),
           'nodes': total_nodes, 'leaves': 1 + master_leaves + sum(r['leaves'] for r in results),
           'pending': 1 + len(missing_files), 'complete_except_state0_branch': not missing_files,
           'minimum_margin': min(margins, default=None), 'master_nodes': len(master['nodes']),
           'largest_context_nodes': max((r['nodes'] for r in results), default=0)}
    print(json.dumps(out))


if __name__ == '__main__':
    main()
