#!/usr/bin/env python3
"""Run the production expansion of the ES(8) <= 311 search on ONE balanced context at a given budget.

The node expansion is pbb_strong.Solver.expand imported unchanged from
  <repo>/experiments/omission-final311-2026-10-14/search/pbb_strong.py
with the production settings (balanced V2 catalog, ROOT_OCC empty, K_TOP=40 below D_TOP=12 fixed
states, K_LOW=12 otherwise, HiGHS with 1 thread and presolve off). The depth-first loop below is
pbb_strong.run_context with the same push/pop order; it adds progress logging, an optional
node/time cap, CPU-time accounting and an exact replay of the subtree with
scripts/omission_tree.check_tree (unbounded integers).

One difference from production is unavoidable: production reused one HiGHS instance per worker
across contexts (warm starts from whatever the worker solved before); here every run starts from a
fresh instance. Degenerate LP optima can then pick other branching vertices, so subtree sizes can
differ from the record even with identical rules.

usage:
  run_context.py --budget 64 --ctx 1022 [--contexts contexts.jsonl] [--out DIR]
                 [--max-nodes N] [--max-seconds S] [--no-replay] [--no-tree]
Writes DIR/ctx-<k>-b<B>.json.gz (pbb_strong subtree format, plus budget/rules) and
DIR/ctx-<k>-b<B>.result.json; prints the result JSON on stdout. Exit code 0 closed, 3 witness,
4 capped, 1 error.
"""
import argparse, gzip, importlib.util, json, os, sys, time, traceback
from pathlib import Path

for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[k] = '1'
HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get('ES_REPO', '<repo>'))
PBB = REPO / 'experiments/omission-final311-2026-10-14/search/pbb_strong.py'
BAL = REPO / 'experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
BAL_SHA = 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72'


def load_pbb():
    os.environ['SRC'] = str(BAL)        # balanced catalog, as in search/pipeline.sh
    os.environ['ROOT_OCC'] = ''         # balanced: no state fixed at the root (assemble.py)
    os.environ['K_TOP'] = '40'; os.environ['K_LOW'] = '12'; os.environ['D_TOP'] = '12'   # production rule, fixed
    spec = importlib.util.spec_from_file_location('pbb_strong', PBB)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--budget', type=int, required=True)
    ap.add_argument('--ctx', type=int, required=True, help='context number in contexts.jsonl')
    ap.add_argument('--contexts', default=str(HERE / 'contexts.jsonl'))
    ap.add_argument('--out', default=str(HERE / 'runs'))
    ap.add_argument('--max-nodes', type=int, default=0, help='stop after this many expansions (0 = no cap)')
    ap.add_argument('--max-seconds', type=float, default=0, help='stop after this wall time (0 = no cap)')
    ap.add_argument('--progress', type=float, default=300, help='seconds between progress lines on stderr')
    ap.add_argument('--no-replay', action='store_true')
    ap.add_argument('--no-tree', action='store_true', help='do not write the subtree')
    a = ap.parse_args()

    ctx = None
    with open(a.contexts) as f:
        for line in f:
            c = json.loads(line)
            if c['ctx'] == a.ctx:
                ctx = c; break
    assert ctx is not None, f'context {a.ctx} not found'
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    stem = out / f'ctx-{a.ctx}-b{a.budget}'

    pbb = load_pbb()
    import hashlib, highspy, importlib.metadata as md
    assert hashlib.sha256(BAL.read_bytes()).hexdigest() == BAL_SHA
    pbb.init(None, a.budget)
    s = pbb.G['s']
    N = pbb.N
    assert N == 252 and len(s.rows) == 3131
    missing = sum(1 << j for j in ctx['missing'])
    occupied = sum(1 << j for j in ctx['occupied'])
    res = {'ctx': a.ctx, 'budget': a.budget, 'missing': ctx['missing'], 'occupied': ctx['occupied'],
           'b63_record_nodes': ctx['nodes'], 'b63_record_leaves': ctx['leaves'],
           'rules': {'K_TOP': pbb.STRONG['k'], 'D_TOP': pbb.STRONG['depth'], 'K_LOW': pbb.STRONG['k_low'],
                     'pbb_strong': str(PBB), 'catalog_sha256': BAL_SHA},
           'highspy': md.version('highspy'), 'python': sys.version.split()[0], 'host': os.uname().nodename,
           'pid': os.getpid(), 'started': time.strftime('%F %T')}

    t0, c0 = time.time(), time.process_time()
    nodes = [{'type': 'pending'}]
    stack = [(0, missing, occupied)]
    count = 0
    status = 'closed'
    last = t0
    try:
        while stack:
            i, m, o = stack.pop()
            kind, val = s.expand(m, o)
            count += 1
            if kind == 'leaf':
                nodes[i] = val
            elif kind == 'witness':
                status = 'witness'
                res['witness_holes'] = val
                break
            else:
                z, one = len(nodes), len(nodes) + 1
                nodes += [{'type': 'pending'}, {'type': 'pending'}]
                nodes[i] = {'type': 'branch', 'vertex': val, 'zero': z, 'one': one}
                stack.append((z, m, o | (1 << val)))
                stack.append((one, m | (1 << val), o))
            now = time.time()
            if now - last >= a.progress:
                last = now
                print(json.dumps({'event': 'progress', 'ctx': a.ctx, 'budget': a.budget, 'expanded': count,
                                  'open': len(stack), 'wall': round(now - t0, 1)}), file=sys.stderr, flush=True)
            if (a.max_nodes and count >= a.max_nodes) or (a.max_seconds and now - t0 >= a.max_seconds):
                if stack:
                    status = 'capped'
                break
    except Exception:
        status = 'error'
        res['error'] = traceback.format_exc()
    wall, cpu = time.time() - t0, time.process_time() - c0
    leaves = sum(1 for nd in nodes if nd['type'] in ('weighted', 'over_budget'))
    res.update({'status': status, 'expanded': count, 'nodes': len(nodes), 'leaves': leaves,
                'weighted': sum(1 for nd in nodes if nd['type'] == 'weighted'),
                'over_budget': sum(1 for nd in nodes if nd['type'] == 'over_budget'),
                'pending': sum(1 for nd in nodes if nd['type'] == 'pending'),
                'wall_s': round(wall, 3), 'cpu_s': round(cpu, 3),
                'wall_s_per_node': round(wall / max(count, 1), 5), 'cpu_s_per_node': round(cpu / max(count, 1), 5),
                'finished': time.strftime('%F %T')})
    if status == 'witness':
        # exact check of the reported vector against the rows as read by the certificate code
        sys.path.insert(0, str(REPO / 'scripts'))
        from omission_row_probe import read_rows, valid_holes
        n, rows = read_rows(json.loads(BAL.read_text()))
        res['witness_exact_valid'] = valid_holes(n, rows, a.budget, sorted(res['witness_holes']))
        Path(str(stem) + '.WITNESS.json').write_text(json.dumps(res))
    if status in ('closed', 'capped') and not a.no_replay:
        # Exact replay: prefix the context literals as a chain of branches with pending side children.
        sys.path.insert(0, str(REPO / 'scripts'))
        from omission_row_probe import read_rows
        from omission_tree import check_tree
        n, rows = read_rows(json.loads(BAL.read_text()))
        path = ctx['path']
        L = len(path)
        full = [None] * (2 * L)
        for j, (v, b) in enumerate(path):
            cont = 2 * (j + 1)                  # index of the next chain node (or of the subtree root at j = L-1)
            side = 2 * j + 1                    # pending sibling
            full[2 * j] = {'type': 'branch', 'vertex': v, 'zero': cont if b == 0 else side, 'one': cont if b == 1 else side}
            full[side] = {'type': 'pending'}
        shift = 2 * L
        for nd in nodes:
            if nd['type'] == 'branch':
                nd2 = dict(nd); nd2['zero'] += shift; nd2['one'] += shift; full.append(nd2)
            else:
                full.append(nd)
        try:
            r = check_tree(n, rows, a.budget, full, 0, allow_pending=True)
            res['replay'] = {'ok': r['pending'] == L + res['pending'], 'leaves_checked': r['leaves'] - r['pending'],
                             'pending': r['pending'], 'minimum_margin': r['minimum_margin']}
        except Exception as e:
            res['replay'] = {'ok': False, 'error': repr(e)}
    if not a.no_tree:
        rec = {'context': a.ctx, 'budget': a.budget, 'missing': ctx['missing'], 'occupied': ctx['occupied'],
               'path': ctx['path'], 'status': status, 'root': 0, 'nodes': nodes}
        with gzip.open(str(stem) + '.json.gz', 'wt', compresslevel=6) as f:
            json.dump(rec, f, separators=(',', ':'))
        res['tree_file'] = str(stem) + '.json.gz'
    Path(str(stem) + '.result.json').write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k not in ('missing', 'occupied', 'error')}), flush=True)
    if status == 'error':
        print(res['error'], file=sys.stderr)
    sys.exit({'closed': 0, 'witness': 3, 'capped': 4}.get(status, 1))


if __name__ == '__main__':
    main()
