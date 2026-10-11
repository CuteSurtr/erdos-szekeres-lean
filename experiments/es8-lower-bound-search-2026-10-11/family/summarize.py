#!/usr/bin/env python3
"""Collect saturation results into out/results.json and print a summary."""
import glob, json, os, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(os.path.join(HERE, 'manifest.json')))
extra = json.load(open(os.path.join(HERE, 'extra_realizations.json')))
meta = {r['id']: r for r in recs if r.get('representative')}
for k, v in extra.items():
    meta[k] = v
walls = {}
for line in open(os.path.join(HERE, 'out', 'queue.log')):
    m = re.match(r'(sat|verify) (\S+) rc=(\S+) wall=(\S+)', line)
    if m:
        walls[(m.group(1), m.group(2))] = m.group(4)
rows = []
for f in sorted(glob.glob(os.path.join(HERE, 'out', '*.sat.json'))):
    oid = os.path.basename(f)[:-len('.sat.json')]
    js = json.load(open(f))
    r = meta[oid]
    base = meta.get(oid.rstrip('mr')) if oid.endswith(('m', 'r')) else r
    row = {
        'id': oid, 'category': r['category'], 'order_type': r['order_type'],
        'hull_size': base.get('hull_size'), 'max_abs_coord': r['max_abs_coord'],
        'largest_convex_subset': r['largest_convex_subset'], 'tree': r['tree'],
        'faces_euler': js['faces_euler'], 'faces_hit': js['faces_hit_by_valid_candidates'],
        'invalid_candidates': js['invalid_candidates'], 'certificates': js['dp_found'],
        'bad_candidates': js['bad_candidates'], 'cpu_seconds': js['cpu_seconds'],
        'wall': walls.get(('sat', oid)),
        'saturated': js['bad_candidates'] == 0 and js['dp_none'] == 0 and
                     js['faces_euler'] == js['faces_hit_by_valid_candidates'],
    }
    vf = os.path.join(HERE, 'out', oid + '.verify.json')
    if os.path.exists(vf):
        v = json.load(open(vf))
        row['verify'] = v
        row['verify_agrees'] = (v['uncovered_distinct_faces'] == 0 and v['uncovered_candidates'] == 0 and
                                v['faces_E_minus_V_plus_1'] == js['faces_euler'] == v['distinct_faces_hit'])
    rows.append(row)
json.dump(rows, open(os.path.join(HERE, 'out', 'results.json'), 'w'), indent=1)
print('tested sets:', len(rows), ' distinct order types:', len({r['order_type'] for r in rows}))
print('saturated:', sum(r['saturated'] for r in rows), ' NOT saturated / incomplete:',
      [r['id'] for r in rows if not r['saturated']])
print('by category:', dict(Counter(r['category'] for r in rows)))
print('hull sizes:', dict(sorted(Counter(r['hull_size'] for r in rows).items())))
print('faces range:', min(r['faces_euler'] for r in rows), max(r['faces_euler'] for r in rows))
print('cpu s range:', min(r['cpu_seconds'] for r in rows), max(r['cpu_seconds'] for r in rows),
      'total cpu', round(sum(r['cpu_seconds'] for r in rows), 1))
print('verify cross-checks:', [(r['id'], r['verify_agrees']) for r in rows if 'verify' in r])
for r in rows:
    print(f"{r['id']:9s} {r['category']:20s} hull={r['hull_size']} maxc={r['max_abs_coord']:>10d} "
          f"F={r['faces_euler']} hit={r['faces_hit']} bad={r['bad_candidates']} cert={r['certificates']} "
          f"cpu={r['cpu_seconds']} wall={r['wall']}")
