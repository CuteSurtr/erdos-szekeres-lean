#!/usr/bin/env python3
"""mksub.py PARENT.cnf META.json OUTDIR : sub-cubes of a 6-fold parent cube file (base + Y(1,2) + its 5 pattern units)
by all 2^4 sign patterns of Y(1,5),Y(2,5),Y(3,5),Y(4,5); the 16 sub-cubes cover the parent. queue.txt: inconsistent first.
Only for the parent c11111 (psi_1<psi_2<psi_3<psi_4)."""
import sys, json, itertools, os
parent, meta, out = sys.argv[1:4]
Y = json.load(open(meta))['Y']; v5 = [Y[k] for k in ('1,5', '2,5', '3,5', '4,5')]
hdr, rest = open(parent).read().split('\n', 1); _, _, nv, nc = hdr.split()
names = []
for b in itertools.product((1, 0), repeat=4):
    pos = sum(b)                                   # layer 5 after exactly the layers i with Y(i,5)=1
    cons = list(b) == [1] * pos + [0] * (4 - pos)  # consistent with 1<2<3<4 iff b = 1..10..0
    n = 's11111_' + ''.join(map(str, b)); names.append((cons, n))
    with open(os.path.join(out, n + '.cnf'), 'w') as g:
        g.write('p cnf %s %d\n' % (nv, int(nc) + 4)); g.write(rest)
        if not rest.endswith('\n'): g.write('\n')
        for v, x in zip(v5, b): g.write('%d 0\n' % (v if x else -v))
open(os.path.join(out, 'queue.txt'), 'w').write('\n'.join(n for c, n in sorted(names)) + '\n')
print(sum(c for c, _ in names), 'consistent of 16')
