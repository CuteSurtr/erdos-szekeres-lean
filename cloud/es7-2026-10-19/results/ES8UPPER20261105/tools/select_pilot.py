#!/usr/bin/env python3
"""Choose the budget-64 pilot contexts, stratified by budget-63 subtree size (leaves in the 311 record).

Strata: the 4,096 depth-12 contexts sorted by (leaves, ctx) and cut into 10 equal deciles of 409-410.
Deciles 1-9: 2 contexts each, drawn with random.Random(SEED); top decile: 10 contexts, namely the
largest context, the one at the 99th percentile, and 8 drawn at random from the rest of the decile.
Total 28. Eight of them (one from deciles 1, 3, 5, 7, 9 and three from the top decile, including
the largest) are also run at budget 63 to pair the record with this machine and HiGHS version.

usage: select_pilot.py contexts.jsonl pilot_contexts.json [SEED]
"""
import json, random, sys

C = [json.loads(l) for l in open(sys.argv[1])]
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20261105
rng = random.Random(seed)
C.sort(key=lambda c: (c['leaves'], c['ctx']))
n = len(C)
cuts = [round(n * k / 10) for k in range(11)]
dec = [C[cuts[k]:cuts[k + 1]] for k in range(10)]
tot = sum(c['leaves'] for c in C)
chosen = []
for k in range(9):
    for c in rng.sample(dec[k], 2):
        chosen.append((k + 1, c))
top = dec[9]
p99 = C[int(0.99 * n)]
fixed = [top[-1], p99]
rest = [c for c in top if c['ctx'] not in {f['ctx'] for f in fixed}]
for c in fixed + rng.sample(rest, 8):
    chosen.append((10, c))
chosen.sort(key=lambda t: (t[0], t[1]['leaves'], t[1]['ctx']))
pair = []
for k in (1, 3, 5, 7, 9):
    pair.append(next(c['ctx'] for d, c in chosen if d == k))
tops = [c for d, c in chosen if d == 10]
pair += [tops[-1]['ctx'], tops[len(tops) // 2]['ctx'], tops[0]['ctx']]
strata = [{'decile': k + 1, 'contexts': len(dec[k]), 'leaves_min': dec[k][0]['leaves'], 'leaves_max': dec[k][-1]['leaves'],
           'leaves_sum': sum(c['leaves'] for c in dec[k]), 'share': round(sum(c['leaves'] for c in dec[k]) / tot, 4)}
          for k in range(10)]
out = {'method': __doc__.strip().split('\n\n')[1], 'seed': seed, 'contexts_total': n, 'leaves_total': tot,
       'strata': strata,
       'pilot': [{'ctx': c['ctx'], 'decile': d, 'b63_leaves': c['leaves'], 'b63_nodes': c['nodes'],
                  'n_missing': len(c['missing']), 'also_b63': c['ctx'] in pair} for d, c in chosen],
       'b63_pair': pair,
       'pilot_b63_leaves_sum': sum(c['leaves'] for _, c in chosen)}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({'pilot': [(p['ctx'], p['decile'], p['b63_leaves']) for p in out['pilot']], 'pair': pair,
                  'pilot_b63_leaves_sum': out['pilot_b63_leaves_sum'],
                  'top_decile_share': strata[9]['share']}))
