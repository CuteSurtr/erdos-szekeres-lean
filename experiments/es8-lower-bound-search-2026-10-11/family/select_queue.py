#!/usr/bin/env python3
"""Pick distinct, verified, in-bound order types and write queue.txt (round-robin by category)."""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from family import parse, bounds, tstr, HERE  # noqa

recs = json.load(open(os.path.join(HERE, 'manifest.json')))
reps = [r for r in recs if r.get('representative')]
ok = [r for r in reps if r['general_position'] and r['distinct_x'] and r['largest_convex_subset'] == 7
      and r['within_2^27']]
print('representatives', len(reps), 'verified & in bound', len(ok))
rng = random.Random(7)


def topsig(r):
    t = parse(r['tree'])
    return (t[0], bounds(t[1]), bounds(t[2]))


cats = {}
for r in ok:
    cats.setdefault(r['category'], []).append(r)
for c in cats:
    rng.shuffle(cats[c])
# right-associated Down chain first among brackets
if 'bracket' in cats:
    def depth_right(r):
        t, d = parse(r['tree']), 0
        while t != 'o' and t[0] == 'D' and bounds(t[1])[0] <= 20 and t[1] in ('o',) or False:
            break
        return 0
    from family import canon_block
    T = [canon_block(7 - j, j + 1) for j in range(7)]
    right = T[6]
    for j in range(5, -1, -1):
        right = f'D({T[j]},{right})'
    cats['bracket'].sort(key=lambda r: r['tree'] != right)
# stratify skeletons by top-level decomposition
for c in ('skeleton', 'skeleton-randblocks', 'random-dec', 'random-tree'):
    if c in cats:
        groups = {}
        for r in cats[c]:
            groups.setdefault(topsig(r), []).append(r)
        keys = list(groups)
        rng.shuffle(keys)
        order = []
        while any(groups.values()):
            for k in keys:
                if groups[k]:
                    order.append(groups[k].pop())
        cats[c] = order
order = ['witness']
cycle = ['bracket', 'skeleton', 'random-dec', 'wblocks-random', 'random-tree', 'skeleton-randblocks']
pos = {c: 0 for c in cycle}
while any(pos[c] < len(cats.get(c, [])) for c in cycle):
    for c in cycle:
        if pos[c] < len(cats.get(c, [])):
            order.append(cats[c][pos[c]]['id'])
            pos[c] += 1
order[0] = cats['witness'][0]['id']
lines = []
for i, oid in enumerate(order):
    lines.append(f'sat {oid}')
    if i in (1, 3):  # independent verify.c cross-check on two variants
        lines.append(f'verify {oid}')
open(os.path.join(HERE, 'queue.txt'), 'w').write('\n'.join(lines) + '\n')
byid = {r['id']: r for r in ok}
print('queue length', len(order), 'first 14:', [(o, byid[o]['category'], byid[o]['max_abs_coord']) for o in order[:14]])
print('per category available:', {c: len(v) for c, v in cats.items()})
