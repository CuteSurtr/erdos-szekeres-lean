"""Hole patterns of abstract 50-point configurations (samples_50.jsonl) vs the ETV patterns H1, H2, H3."""
import sys, json
import fl
from fl import *
H1 = {i for i, f in enumerate(STATES) if f[0] == 4 and f[3] >= 1}
H2 = {i for i, f in enumerate(STATES) if f[0] == 4 and f[1] <= 3}
H3 = {i for i, f in enumerate(STATES) if f[3] == 1}
cls = lambda f: 'X' if (f[0] == 4 and f[3] >= 1) else ('E' if f[0] == 4 else ('A' if f[3] >= 1 else 'Z'))
nm = lambda i: ''.join(map(str, STATES[i]))
allh = []
for fn in sys.argv[1:]:
    for line in open(fn):
        d = json.loads(line)
        for key in ('in_states', 'out_states'):
            occ = set(d[key]); h = set(range(N)) - occ; allh.append(h)
            cnt = {c: sum(1 for i in h if cls(STATES[i]) == c) for c in 'XEAZ'}
            print(fn, 'seed', d['seed'], key, 'n', d['n'], 'holes', len(h), 'by class (X, E-X, A-X, Z):', [cnt[c] for c in 'XEAZ'],
                  'equals H1/H2/H3:', [h == H for H in (H1, H2, H3)], '|h&H1|,|h&H2|,|h&H3| =', len(h & H1), len(h & H2), len(h & H3))
            print('    holes:', ' '.join(sorted(nm(i) for i in h)))
if allh:
    common = set.intersection(*allh); union = set.union(*allh)
    print('states that are holes in every listed pattern:', sorted(nm(i) for i in common))
    print('states that are holes in some listed pattern:', len(union), 'of 70')
