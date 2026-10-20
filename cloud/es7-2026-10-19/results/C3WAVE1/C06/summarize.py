#!/usr/bin/env python3
"""Per-root and per-depth summary of out.jsonl for C06. usage: summarize.py out.jsonl roots.txt"""
import json, sys, collections
sys.path.insert(0, '/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools'); sys.path.insert(0, '/opt/c3s/cloud/es7-2026-10-19/results/C3a')
from hullcase import tree_children, parse_layers, layers_name
recs = [json.loads(l) for l in open(sys.argv[1])]
roots = [l.strip() for l in open(sys.argv[2]) if l.strip()]
cert = {r['node']: r for r in recs if r.get('certified') and r.get('lrat_check') == 'c VERIFIED' and r.get('cake_lpr') == 's VERIFIED UNSAT'}
split = {r['node'] for r in recs if r.get('split')}
tried = {}
for r in recs:
    if 'status' in r: tried.setdefault(r['node'], []).append(r)
def covered(n):
    if n in cert: return True
    if n in split: return all(covered(layers_name(c)) for c in tree_children(11, 7, parse_layers(n)))
    return False
def walk(n, acc):
    d = len(parse_layers(n))
    if n in cert:
        r = cert[n]; acc['cert'][d] += 1; acc['solve'] += r['solve_s']; acc['check'] += r.get('check_s', 0)
    elif n in split:
        acc['split'][d] += 1
        for t in tried.get(n, []): acc['solve'] += t.get('solve_s', 0)
        for c in tree_children(11, 7, parse_layers(n)): walk(layers_name(c), acc)
    else:
        acc['open'][d] += 1
tot = {k: collections.Counter() for k in ('cert', 'split', 'open')}
print('| root | status | certified by depth | splits | open | solve s | check s |')
print('|---|---|---|---|---|---|---|')
nclosed = 0
for rt in roots:
    acc = {'cert': collections.Counter(), 'split': collections.Counter(), 'open': collections.Counter(), 'solve': 0.0, 'check': 0.0}
    walk(rt, acc)
    for k in tot: tot[k].update(acc[k])
    c = covered(rt); nclosed += c
    fmt = lambda C: ', '.join(f'd{d}:{C[d]}' for d in sorted(C)) or '-'
    print(f"| `{rt}` | {'closed' if c else 'open'} | {fmt(acc['cert'])} | {sum(acc['split'].values())} | {sum(acc['open'].values())} | {acc['solve']:.0f} | {acc['check']:.0f} |")
print(f'\nroots closed: {nclosed} / {len(roots)}\n')
print('| depth | certified | split | open (untried or timed out, not split) |')
print('|---|---|---|---|')
for d in sorted(set().union(*[set(c) for c in tot.values()])):
    print(f"| {d} | {tot['cert'][d]} | {tot['split'][d]} | {tot['open'][d]} |")
bad = [r for r in recs if r.get('status') == 'UNSATISFIABLE' and not r.get('certified')]
print('unaccepted UNSAT later certified on re-run:', [r['node'] for r in bad if r['node'] in cert]); bad = [r for r in bad if r['node'] not in cert]
print('\nunaccepted UNSAT records:', [(r['node'], r.get('lrat_check'), r.get('cake_lpr')) for r in bad])
print('SAT records:', [r['node'] for r in recs if r.get('status') == 'SATISFIABLE'])
