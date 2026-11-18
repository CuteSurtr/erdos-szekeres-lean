#!/usr/bin/env python3
"""V5 cross-check: does the Python pbb_strong.py close the same contexts that fastbb closed?

Usage (from the repository root):
  K_TOP=16 D_TOP=8 K_LOW=4 crosscheck_py.py OUTDIR EXTRA.json BUDGET COUNT SEED TMPDIR [OUT.json]

Picks COUNT random contexts of fastbb's master (OUTDIR/contexts.json), runs pbb_strong.run_context
(unchanged code, HiGHS) on each (missing, occupied) pair and records whether it closes it and with how
many nodes; fastbb's node counts are read from OUTDIR/fastbb.log.jsonl.  The trees differ; only the
verdict (closed, no witness) is compared.  Each Python tree is also replayed with check_tree.
"""
import gzip, json, os, random, sys, time
from pathlib import Path
sys.path.insert(0, 'experiments/omission-final313-2026-10-11/search')
sys.path.insert(0, 'scripts')
import pbb_strong as P
from omission_tree import check_tree


def replay(n, rows, budget, rec):
    chain = [(i, 0) for i in sorted(rec['occupied'])] + [(i, 1) for i in sorted(rec['missing'])]
    k = len(chain)
    nodes = []
    for t, (i, bit) in enumerate(chain):
        nxt = 2 * (t + 1) if t + 1 < k else 2 * k
        nodes.append({'type': 'branch', 'vertex': i, 'zero': nxt if bit == 0 else 2 * t + 1, 'one': nxt if bit == 1 else 2 * t + 1})
        nodes.append({'type': 'pending'})
    for nd in rec['nodes']:
        nodes.append({'type': 'branch', 'vertex': nd['vertex'], 'zero': nd['zero'] + 2 * k, 'one': nd['one'] + 2 * k}
                     if nd['type'] == 'branch' else nd)
    res = check_tree(n, rows, budget, nodes, 0, allow_pending=True)
    return res['pending'] == k


def main():
    outdir, extra, budget, count, seed, tmpdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    Path(tmpdir).mkdir(parents=True, exist_ok=True)
    ctxs = json.load(open(Path(outdir) / 'contexts.json'))
    mine = {}
    for line in open(Path(outdir) / 'fastbb.log.jsonl'):
        r = json.loads(line)
        if r.get('event') == 'closed':
            mine[r['context']] = r
    closed = [c for c in ctxs if (Path(outdir) / f"ctx-{c['context']}.json.gz").exists()]
    random.Random(seed).shuffle(closed)
    pick = closed[:count]
    P.init(extra, budget)
    rows = P.G['s'].rows
    out = []
    for c in pick:
        cid = c['context']
        m = sum(1 << i for i in c['missing']); o = sum(1 << i for i in c['occupied'])
        t0 = time.time()
        r = P.run_context((cid, m, o, tmpdir))
        rec = {'context': cid, 'python_status': r[1], 'python_nodes': r[3], 'python_seconds': round(time.time() - t0, 2),
               'fastbb_nodes': mine.get(cid, {}).get('nodes'), 'fastbb_seconds': mine.get(cid, {}).get('seconds')}
        if r[1] == 'closed':
            tree = json.load(gzip.open(Path(tmpdir) / f'ctx-{cid}.json.gz'))
            rec['python_tree_replayed'] = replay(P.N, rows, budget, tree)
        out.append(rec)
        print(json.dumps(rec), flush=True)
    summary = {'contexts_checked': len(out), 'python_closed': sum(r['python_status'] == 'closed' for r in out),
               'python_witness': sum(r['python_status'] == 'witness' for r in out),
               'python_nodes': sum(r['python_nodes'] for r in out),
               'fastbb_nodes': sum(r['fastbb_nodes'] or 0 for r in out),
               'python_seconds': round(sum(r['python_seconds'] for r in out), 1),
               'fastbb_seconds': round(sum(r['fastbb_seconds'] or 0 for r in out), 2)}
    print(json.dumps({'summary': summary}))
    if len(sys.argv) > 7:
        json.dump({'summary': summary, 'contexts': out}, open(sys.argv[7], 'w'), indent=1)


if __name__ == '__main__':
    main()
