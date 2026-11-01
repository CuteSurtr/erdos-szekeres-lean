#!/usr/bin/env python3
"""Print the k = 7 markdown tables of README.md from summary.json."""
import json
import math
import sys

S = json.load(open(sys.argv[1]))


def fmt_e(x):
    return f'{x:.1e}'


print('### Cube-and-conquer frontier (cnc2, c0 = 20,000 conflicts, every level solved)\n')
print('| run | t (s) | jobs | closed | open | open depth histogram | closed weight | solve CPU (s) | LRAT checked |')
print('|---|---|---|---|---|---|---|---|---|')
for name, r in S['cnc'].items():
    if not name.startswith('cnc_k7'):
        continue
    snaps = r['frontier_snapshots'] or []
    last = r['last']
    rows = list(snaps)
    if last and (not rows or rows[-1]['t'] != last['t']):
        rows.append(last)
    for s in rows:
        hist = ', '.join(f'{k}: {v}' for k, v in s['open_depth_hist'].items())
        print(f"| {name.split('/')[-1]} ({s['kind']}) | {s['t']:.0f} | {s['jobs']} | {s['closed']} | {s['open']} | {hist} | "
              f"{s['closed_weight']} | {s['solve_cpu']:.0f} | {s['checked']} ({s['check_ok']} ok) |")
print()
print('### Random dives (Knuth estimates; one random path per row)\n')
print('| case | dive | solver every | status | leaf depth | leaf conflicts | LRAT | path CPU (s) | est. leaves | est. CPU (s) |')
print('|---|---|---|---|---|---|---|---|---|---|')
rows = []
for name, d in S['dives'].items():
    if not name.startswith('k7'):
        continue
    for x in d['completed_dives']:
        rows.append((name, x))
for name, x in sorted(rows, key=lambda t: (t[0].split('_')[1], t[0], t[1]['dive'])):
    se = x.get('solve_every', 1)
    leaf = x.get('leaf', {})
    print(f"| {name.split('_')[1]} | {name}#{x['dive']} | {se} | {x['status']} | {x['depth']} | {leaf.get('conf', '')} | "
          f"{leaf.get('lrat', '')} | {x['path_cpu']:.0f} | 2^{x['depth']} | {fmt_e(x['cpu_est'])} |")
for name, d in S['dives'].items():
    if name.startswith('k7') and 'censored_dive' in d:
        c = d['censored_dive']
        print(f"| {name.split('_')[1]} | {name}#{c['dive']} (unfinished) | | censored | >= {c['deepest_node']} | | | "
              f"{c['path_cpu']:.0f} | >= 2^{c['log2_leaves_lower_bound']} | >= {fmt_e(c['cpu_lower_bound'])} |")
print()
print('### Per-hull-size estimate summary\n')
print('| h | closed dives | leaf depths | log10 est. CPU-s (min / geometric mean / max) |')
print('|---|---|---|---|')
by_h = {}
for name, x in rows:
    if x['status'] != 'closed':
        continue
    by_h.setdefault(name.split('_')[1], []).append(x)
for h in sorted(by_h, reverse=True):
    xs = by_h[h]
    l = [math.log10(x['cpu_est']) for x in xs]
    print(f"| {h[1:]} | {len(xs)} | {', '.join(str(x['depth']) for x in xs)} | {min(l):.1f} / {sum(l) / len(l):.1f} / {max(l):.1f} |")
