#!/usr/bin/env python3
"""Collect Task G results from the work directory into summary.json and trimmed logs.

usage: summarize.py WORKDIR RESULTS_DIR
"""
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path


def read_time(p):
    d = {}
    if not p.exists():
        return d
    for line in p.read_text().split('\n'):
        t = line.split()
        if len(t) >= 2 and t[0] in ('real', 'user', 'sys'):
            d[t[0]] = float(t[1])
        elif line.startswith('res '):
            d['result'] = line.split()[-1]
        elif line.startswith('lrat_bytes'):
            d['lrat_bytes'] = int(t[1])
    return d


def direct_block(dirp, names):
    out = {}
    for n in names:
        d = read_time(dirp / f'{n}.time')
        chk = dirp / f'{n}.check'
        if chk.exists():
            d['lrat_check'] = 'VERIFIED' if 'c VERIFIED' in chk.read_text() and 'NOT VERIFIED' not in chk.read_text() else 'FAILED'
            d['lrat_check_time'] = read_time(dirp / f'{n}.checktime')
        out[n] = d
    return out


def dives_block(dirp):
    nodes = []
    p = dirp / 'nodes.jsonl'
    if p.exists():
        nodes = [json.loads(l) for l in p.read_text().split('\n') if l.strip()]
    dives = []
    p2 = dirp / 'dives.jsonl'
    if p2.exists():
        for l in p2.read_text().split('\n'):
            if l.strip():
                r = json.loads(l)
                path = r.pop('path', [])
                if path:
                    r['leaf'] = path[-1]
                    r['solver_nodes'] = [(n['depth'], n['res'], n['conf'], round(n['cpu'], 2)) for n in path if n['res'] != 'L']
                r.pop('lits', None)
                dives.append(r)
    # reconstruct the in-progress (censored) dive from nodes
    done = {(d['dive']) for d in dives}
    cur = [n for n in nodes if n['dive'] not in done]
    res = {'completed_dives': dives, 'nodes_total': len(nodes)}
    if cur:
        dmax = max(n['depth'] for n in cur)
        res['censored_dive'] = {'dive': cur[0]['dive'], 'deepest_node': dmax, 'last_res': cur[-1]['res'],
                                'path_cpu': round(sum(n['cpu'] for n in cur), 1),
                                'cpu_lower_bound': sum((2 ** n['depth']) * n['cpu'] for n in cur),
                                'log2_leaves_lower_bound': dmax + (1 if cur[-1]['res'] == 'K' else 0)}
    res['node_cpu_by_depth'] = {}
    for n in nodes:
        res['node_cpu_by_depth'].setdefault(str(n['depth']), []).append(round(n['cpu'], 2))
    return res


def main():
    W = Path(sys.argv[1])
    R = Path(sys.argv[2])
    (R / 'logs').mkdir(parents=True, exist_ok=True)
    S = {}
    S['k6_direct'] = direct_block(W / 'k6', ['n17_h3', 'n17_h4', 'n17_h5', 'n17_hge6', 'base17', 'n16_h3', 'n16_h4', 'n16_h5', 'n16_hge6'])
    S['k6_direct_lemma'] = direct_block(W / 'lemma', ['n17_h3', 'n17_h4', 'n17_h5', 'n16_h3', 'n16_h4', 'n16_h5'])
    S['k6_models'] = {}
    for sub in ('k6', 'lemma'):
        p = W / sub / 'models.jsonl'
        if p.exists():
            S['k6_models'][sub] = [json.loads(l) for l in p.read_text().split('\n') if l.strip()]
    S['controls'] = {}
    for name in ('k6_n16', 'k6_n16_lemma', 'k7_n32', 'k7_n33_ae', 'k7_n32_lemma'):
        p = W / 'controls' / f'{name}.jsonl'
        if p.exists():
            lines = p.read_text().split('\n')
            S['controls'][name] = json.loads(lines[0])
            shutil.copy(p, R / 'logs' / f'controls_{name}.jsonl')
    p = W / 'controls' / 'k7_pool_hull_hist.json'
    if p.exists():
        S['k7_pool_hull_hist'] = json.loads(p.read_text())
    S['cnc'] = {}
    for sub in ('cnc_k6', 'cnc_k7'):
        if not (W / sub).exists():
            continue
        for run in sorted((W / sub).iterdir()):
            if not run.is_dir():
                continue
            log = run / 'cnc2.log'
            if not log.exists():
                continue
            lines = [json.loads(l) for l in log.read_text().split('\n') if l.strip()]
            snaps = [l for l in lines if l.get('kind') in ('frontier', 'final')]
            last = [l for l in lines if 'kind' in l][-1] if any('kind' in l for l in lines) else None
            res = [l['result'] for l in lines if 'result' in l]
            S['cnc'][f'{sub}/{run.name}'] = {'start': lines[0], 'last': last, 'frontier_snapshots': snaps,
                                             'result': res[-1] if res else 'RUNNING'}
            # trimmed logs: frontier/final snapshots and every 5th status line
            keep = [lines[0]] + [l for i, l in enumerate(lines[1:]) if l.get('kind') != 'status' or i % 5 == 0]
            with open(R / 'logs' / f'{sub}_{run.name}_cnc2.log', 'w') as f:
                for l in keep:
                    f.write(json.dumps(l) + '\n')
            tree = run / 'tree.jsonl'
            if tree.exists() and tree.stat().st_size < 20_000_000:
                shutil.copy(tree, R / 'logs' / f'{sub}_{run.name}_tree.jsonl')
    S['dives'] = {}
    if (W / 'dives').exists():
        for run in sorted((W / 'dives').iterdir()):
            if run.is_dir():
                S['dives'][run.name] = dives_block(run)
                for fn in ('nodes.jsonl', 'dives.jsonl'):
                    if (run / fn).exists():
                        shutil.copy(run / fn, R / 'logs' / f'dives_{run.name}_{fn}')
    # Knuth estimates from completed dives (unbiased for the tree defined by budget + split rule)
    est = {}
    for name, d in S['dives'].items():
        comp = [x for x in d['completed_dives'] if x['status'] == 'closed']
        e = {'closed_dives': len(comp)}
        if comp:
            leaves = [2 ** x['depth'] for x in comp]
            cpus = [x['cpu_est'] for x in comp]
            e.update({'leaf_depths': [x['depth'] for x in comp],
                      'mean_leaves_est': sum(leaves) / len(leaves),
                      'mean_cpu_est_s': sum(cpus) / len(cpus),
                      'min_cpu_est_s': min(cpus), 'max_cpu_est_s': max(cpus)})
        if 'censored_dive' in d:
            e['censored'] = d['censored_dive']
        est[name] = e
    S['knuth_estimates'] = est
    with open(R / 'summary.json', 'w') as f:
        json.dump(S, f, indent=1)
    print('wrote', R / 'summary.json')


if __name__ == '__main__':
    main()
