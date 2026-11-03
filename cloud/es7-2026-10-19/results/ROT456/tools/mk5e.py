#!/usr/bin/env python3
"""mk5e.py BASE.cnf META.json OUTDIR PARENT : 5-fold sub-cubes of the parent cube PARENT = d<b12 b13 b14 b23 b24 b34>
(units H(1) and the parent's six Y literals) by all 2^4 sign patterns of Y(1,5),Y(2,5),Y(3,5),Y(4,5).
The 16 sub-cubes cover the parent.  queue.txt lists the transitivity-inconsistent ones first."""
import sys, json, itertools, os
base, meta, out, parent = sys.argv[1:5]
d = json.load(open(meta)); Y = d['Y']; h1 = d['H']['1']
pv = [Y[k] for k in ('1,2', '1,3', '1,4', '2,3', '2,4', '3,4')]; nv5 = [Y[k] for k in ('1,5', '2,5', '3,5', '4,5')]
pb = list(map(int, parent[1:7]))
hdr, rest = open(base).read().split('\n', 1); _, _, nv, nc = hdr.split()
def consistent(b):
    y = dict(zip(('12', '13', '14', '23', '24', '34'), pb)); y.update(zip(('15', '25', '35', '45'), b))
    less = lambda i, j: y['%d%d' % (i, j)] if i < j else 1 - y['%d%d' % (j, i)]
    return any(all(less(p[a], p[c]) for a in range(5) for c in range(a + 1, 5)) for p in itertools.permutations(range(1, 6)))
names = []
for b in itertools.product((1, 0), repeat=4):
    lits = [h1] + [v if x else -v for v, x in zip(pv, pb)] + [v if x else -v for v, x in zip(nv5, b)]
    n = 'e%s_%s' % (parent[1:], ''.join(map(str, b))); names.append((consistent(b), n))
    with open(os.path.join(out, n + '.cnf'), 'w') as g:
        g.write('p cnf %s %d\n' % (nv, int(nc) + len(lits))); g.write(rest)
        if not rest.endswith('\n'): g.write('\n')
        for l in lits: g.write('%d 0\n' % l)
open(os.path.join(out, 'queue.txt'), 'w').write('\n'.join(n for c, n in sorted(names)) + '\n')
print(sum(c for c, _ in names), 'consistent of', len(names))
