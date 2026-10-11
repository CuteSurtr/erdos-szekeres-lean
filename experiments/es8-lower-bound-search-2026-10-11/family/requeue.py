#!/usr/bin/env python3
"""Second queue: for every order type use the smallest-coordinate realization among
all generated trees with that order type, so more order types fit the 2^27 bound."""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from family import parse, bounds, realize, verify_set, order_type_key, canon_block, chain_bracketings, HERE, W  # noqa
recs = json.load(open(os.path.join(HERE, 'manifest.json')))
reps = {r['order_type']: r for r in recs if r.get('representative')}
groups = {}
for r in recs:
    if r.get('certified'):
        groups.setdefault(r['order_type'], []).append(r)
chosen = {}  # id -> (tree, category)
for ot, rep in reps.items():
    best = min(groups[ot], key=lambda r: r['max_abs_coord'])
    if rep['within_2^27']:
        chosen[rep['id']] = (rep['tree'], rep['category'], rep['max_abs_coord'])
    elif best['max_abs_coord'] < 2 ** 27:
        chosen[rep['id'] + 'm'] = (best['tree'], rep['category'], best['max_abs_coord'])
# realization control: right-associated chain = same order type as witness(8), other coordinates
T = [canon_block(7 - j, j + 1) for j in range(7)]
right = T[6]
for j in range(5, -1, -1):
    right = f'D({T[j]},{right})'
extra = {}
for oid, (t, cat, m) in list(chosen.items()):
    if oid.endswith('m'):
        P = realize(t)
        info, O = verify_set(P)
        okey, _ = order_type_key(P, O)
        assert okey == reps[[k for k in reps if reps[k]['id'] == oid[:-1]][0]]['order_type']
        assert info['general_position'] and info['distinct_x'] and info['largest_convex_subset'] == 7 and info['within_2^27']
        open(os.path.join(HERE, 'sets', oid + '.txt'), 'w').write(''.join(f'{x} {y}\n' for x, y in P))
        extra[oid] = {'tree': t, 'category': cat, **info, 'order_type': okey}
P = realize(right)
info, O = verify_set(P)
okey, _ = order_type_key(P, O)
assert okey == reps[[k for k in reps if reps[k]['id'] == 'ot0000'][0]]['order_type']
assert P != W.witness(8) and info['largest_convex_subset'] == 7 and info['within_2^27'] and info['general_position']
open(os.path.join(HERE, 'sets', 'ot0000r.txt'), 'w').write(''.join(f'{x} {y}\n' for x, y in P))
extra['ot0000r'] = {'tree': right, 'category': 'witness-realization', **info, 'order_type': okey}
json.dump(extra, open(os.path.join(HERE, 'extra_realizations.json'), 'w'))
cats = {}
for oid, (t, cat, m) in chosen.items():
    cats.setdefault(cat, []).append(oid)
rng = random.Random(11)
old = [l.split()[1] for l in open(os.path.join(HERE, 'queue.txt')) if l.startswith('sat')]
rank = {o: i for i, o in enumerate(old)}
for c in cats:
    # keep previous relative order for ids already ranked; new 'm' ids shuffled in
    ids = cats[c]
    rng.shuffle(ids)
    ids.sort(key=lambda o: rank.get(o, rank.get(o[:-1], 10**6)) if not o.endswith('m') else 10**6)
    if c == 'bracket':
        # interleave m-ids (out-of-bound representatives re-realized) with the others
        a = [o for o in ids if not o.endswith('m')]; b = [o for o in ids if o.endswith('m')]
        ids = [x for pair in zip(a, b) for x in pair] + a[len(b):] + b[len(a):]
    cats[c] = ids
print({c: len(v) for c, v in cats.items()})
order = ['ot0000', 'ot0016', 'ot0229', 'ot0772', 'ot0000r']
cycle = ['bracket', 'skeleton', 'random-dec', 'wblocks-random', 'random-tree', 'skeleton-randblocks']
pos = {c: 0 for c in cycle}
while any(pos[c] < len(cats.get(c, [])) for c in cycle):
    for c in cycle:
        while pos[c] < len(cats.get(c, [])) and cats[c][pos[c]] in order:
            pos[c] += 1
        if pos[c] < len(cats.get(c, [])):
            order.append(cats[c][pos[c]]); pos[c] += 1
lines = []
for o in order:
    lines.append(f'sat {o}')
    if o in ('ot0016', 'ot0772'):
        lines.append(f'verify {o}')
open(os.path.join(HERE, 'queue2.txt'), 'w').write('\n'.join(lines) + '\n')
print('queue2 length', len(order), order[:20])
