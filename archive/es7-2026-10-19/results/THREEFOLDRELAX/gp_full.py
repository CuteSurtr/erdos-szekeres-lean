#!/usr/bin/env python3
"""gp_full.py m K t BASE.cnf OUT.cnf : BASE + every 3-term Grassmann-Pluecker sign clause (one rotation
representative per 5-set; sound for every planar configuration)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_relax as G
m, K, t = map(int, sys.argv[1:4]); base, out = sys.argv[4], sys.argv[5]
E = G.Enc(m, K, t); n = m * t
gp = set()
for S in itertools.combinations(range(n), 5):
    if S[0] % m != 0: continue
    for a in S:
        b, c, d, e = [x for x in S if x != a]
        L = [E.o(a, b, c), E.o(a, d, e), E.o(a, b, d), E.o(a, c, e), E.o(a, b, e), E.o(a, c, d)]
        for bits in itertools.product([1, -1], repeat=6):
            if bits[0] * bits[1] == -bits[2] * bits[3] == bits[4] * bits[5]:
                gp.add(tuple(sorted(-(L[i] if bits[i] > 0 else -L[i]) for i in range(6))))
hdr = open(base).readline().split()
with open(out, 'w') as f, open(base) as g:
    f.write('p cnf %s %d\n' % (hdr[2], int(hdr[3]) + len(gp))); g.readline()
    f.write(g.read())
    for cl in gp: f.write(' '.join(map(str, cl)) + ' 0\n')
print({'gp_clauses': len(gp)})
