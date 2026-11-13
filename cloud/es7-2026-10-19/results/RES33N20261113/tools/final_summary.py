"""Final tallies for R/RES33N20261113 (read-only)."""
import json, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import STATES, ROWS, check
F = {i for i in range(154) if STATES[i][0] >= 5}
rows = json.load(open('newrows.json'))
cert = [json.loads(l) for l in open('certified.jsonl')]
cs = [set(c['support']) for c in cert if c['verdict'] == 's VERIFIED UNSAT']
kinds = collections.Counter(r.get('kind') or 'core' for r in rows)
sizes = collections.Counter(len(r['support']) for r in rows)
print('ROWS', len(rows), dict(kinds), dict(sorted(sizes.items())), 'templates', sum(1 for _ in open('newtemplates.jsonl')))
print('CERTIFIED', len(cert), dict(collections.Counter(c['verdict'][:16] for c in cert)))
W = json.load(open('/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/ES8SLACK/witnesses.json'))['residual_2650_33_hole_witnesses_state0_occupied']
V4 = [12, 17, 25, 27, 33, 34, 35, 36, 44, 45, 57, 58, 60, 62, 72, 81, 85, 88, 92, 96, 98, 100, 101, 107, 109, 111, 116, 117, 119, 124, 126, 127, 138]
named = [('W0', W[0]), ('W1', W[1]), ('W2', W[2]), ('V4', V4)]
seen = [v for _, v in named]
for i, v in enumerate(json.load(open('vectors.json'))):
    if v not in seen: seen.append(v); named.append((f'N{len(named) - 3}', v))
cap = [json.loads(l) for l in open('capvec.jsonl')] if os.path.exists('capvec.jsonl') else []
for c in cap:
    if 'holes' in c and c['holes'] not in seen: seen.append(c['holes']); named.append(('C59', c['holes']))
newr = [(tuple(r['support']), 1) for r in rows]
print('| vector | holes | F occupied | violated new rows | violated cake_lpr-certified rows |')
for name, v in named:
    occ = set(range(154)) - set(v)
    print(f'| {name} | {len(v)} | {len(F & occ)} | {len(check(v, newr))} | {sum(1 for s in cs if s <= occ)} |')
fl = [json.loads(l) for l in open('finder.jsonl')]
rounds = [x for x in fl if 'round_status' in x]
print('FINDER rounds', len(rounds), 'capped rounds', sum(1 for x in rounds if x.get('capc')),
      'finds', sum(1 for x in fl if 'holes' in x), 'last find', max((x['t'] for x in fl if 'holes' in x), default=None))
for f in ('knuth32_base.json', 'knuth33_all.json'):
    if os.path.exists(f):
        d = json.load(open(f)); print('KNUTH', f, {k: d[k] for k in ('budget', 'rows', 'dives', 'log10_mean_nodes', 'median_depth', 'witnesses')})
