#!/usr/bin/env python3
"""Export a polynomial (limit) configuration to an exact integer point set with eps = 2^-s.
Input: JSON {"m": m, "points": [[[e, x, y], ...], ...]} (all points, already including rotations and centre).
Output: m = 4 -> ES8SYM .pts rows 'x y 0 0' (point = w0 + w1 i - w2 - w3 i); m = 3 -> rows 'a b' (a + b omega).
usage: export_cfg.py IN.json S OUT"""
import sys, json
d = json.load(open(sys.argv[1])); s = int(sys.argv[2]); out = sys.argv[3]
m = d['m']; pts = d['points']
kmax = max(e for p in pts for (e, x, y) in p)
rows = []
for p in pts:
    X = sum(x << (s * (kmax - e)) for (e, x, y) in p)
    Y = sum(y << (s * (kmax - e)) for (e, x, y) in p)
    rows.append((X, Y))
assert len(set(rows)) == len(rows)
with open(out, 'w') as f:
    f.write('# m=%d n=%d exported from a limit configuration with eps = 2^-%d\n' % (m, len(rows), s))
    for (X, Y) in rows:
        f.write(('%d %d 0 0\n' % (X, Y)) if m == 4 else ('%d %d\n' % (X, Y)))
print('wrote', out, len(rows), 'points')
