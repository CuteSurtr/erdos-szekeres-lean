"""Row rules for a = 4 (exhaustive over the enumerated (4,5)-valid signotopes): Delta = the leftmost (or rightmost) point
of each level of a rank statistic (beta, omega, beta+omega, beta-omega), levels lo..hi.  Counts how often it is a
working strong Delta (or the configuration has no gon)."""
import json, collections
from siglib import *
a, n = 4, 5
data = []
for m in (5, 6, 7):
    for l in open('enum_a4_n5_m%d_strong.jsonl' % m):
        r = json.loads(l); o = from_str(r['s'], m); be, om, cm, cp = ranks(o, m)
        data.append((m, be, om, set(r['W']), r['ngon']))
res = collections.Counter()
for stat in ('beta', 'omega', 'beta+omega', 'beta-omega'):
    for side in ('left', 'right'):
        for lo in (1, 2):
            for hi in (n - 2, n - 1):
                ok = 0
                for (m, be, om, W, ng) in data:
                    val = {'beta': be, 'omega': om, 'beta+omega': {p: be[p] + om[p] for p in be}, 'beta-omega': {p: be[p] - om[p] for p in be}}[stat]
                    rng = range(lo, hi + 1) if stat in ('beta', 'omega') else sorted(set(val.values()))
                    D = 0
                    for j in rng:
                        pts = [p for p in range(m) if val[p] == j]
                        if pts: D |= 1 << (pts[0] if side == 'left' else pts[-1])
                    ok += (D in W) or ng == 0
                res['%s, %smost point of levels %d..%d' % (stat, side, lo, hi)] = ok
print(len(data), 'signotopes ((4,5)-valid, 5-7 points)')
for k, v in res.most_common(): print('   %-48s %d / %d' % (k, v, len(data)))
