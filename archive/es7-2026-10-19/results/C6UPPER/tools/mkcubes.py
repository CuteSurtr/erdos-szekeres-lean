#!/usr/bin/env python3
"""mkcubes.py BASE.cnf META.json OUTDIR : base + unit Y(1,2) (reflection), then all 2^5 sign patterns of
Y(1,3),Y(1,4),Y(2,3),Y(2,4),Y(3,4). The patterns cover every assignment, so UNSAT of all 32 = UNSAT of base+Y12."""
import sys, json, itertools, os
base, meta, out = sys.argv[1], sys.argv[2], sys.argv[3]
Y = json.load(open(meta))['Y']
y12 = Y['1,2']; cv = [Y[k] for k in ('1,3', '1,4', '2,3', '2,4', '3,4')]
body = open(base).read()
hdr, rest = body.split('\n', 1)
p, c, nv, nc = hdr.split()
def write(fn, units):
    with open(fn, 'w') as g:
        g.write('p cnf %s %d\n' % (nv, int(nc) + len(units))); g.write(rest)
        if not rest.endswith('\n'): g.write('\n')
        for l in units: g.write('%d 0\n' % l)
write(os.path.join(out, 'full_Y12.cnf'), [y12])
for bits in itertools.product((1, 0), repeat=5):
    lits = [v if b else -v for v, b in zip(cv, bits)]
    name = 'c' + ''.join(map(str, bits))
    write(os.path.join(out, name + '.cnf'), [y12] + lits)
print('y12', y12, 'cube vars', cv)
