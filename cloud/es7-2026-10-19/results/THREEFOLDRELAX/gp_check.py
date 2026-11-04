#!/usr/bin/env python3
"""gp_check.py m K t MODEL : decode the orientation variables of a SAT model and count violated 3-term
Grassmann-Pluecker relations (sign form: for a,b,c,d,e the three products below must not all have one sign)."""
import sys, itertools, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_relax as G
m, K, t = map(int, sys.argv[1:4])
val = set()
for line in open(sys.argv[4]):
    if line.startswith('v'): val.update(int(x) for x in line.split()[1:] if x != '0')
E = G.Enc(m, K, t)
chi = lambda a, b, c: 1 if E.o(a, b, c) in val else -1
n = m * t; bad = tot = 0
for S in itertools.combinations(range(n), 5):
    for a in S:
        b, c, d, e = [x for x in S if x != a]
        s1 = chi(a, b, c) * chi(a, d, e); s2 = -chi(a, b, d) * chi(a, c, e); s3 = chi(a, b, e) * chi(a, c, d)
        tot += 1
        if s1 == s2 == s3: bad += 1
print({'m': m, 'K': K, 't': t, 'gp_checks': tot, 'gp_violated': bad})
