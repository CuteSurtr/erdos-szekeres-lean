#!/usr/bin/env python3
"""EXACT verification of a sixfold point set given by integer oblique seeds (stdlib only):
seed z_i = a_i + b_i w (w = exp(i pi/3)); points (i,k) = R^k z_i, R(a,b) = (-b, a+b).
Checks exactly: 6-fold invariance (by construction), distinct points, general position (no zero orientation among all
triples, orientation = (sqrt3/2) * integer form), then writes the orientation table and runs ES8SYM/tools/cvxcheck.c
(two independent exact methods: DFS count of convex k-subsets and a DP for the largest convex subset).
Usage: verify_set.py SEEDS.json OUTPREFIX   (SEEDS.json: {"seeds": [[a,b], ...]} in layer order)"""
import sys, json, itertools, subprocess, os


def rot(p, k):
    for _ in range(k % 6): p = (-p[1], p[0] + p[1])
    return p


def o2(P, Q, R):
    return sum(pa * qb - pb * qa for (pa, pb), (qa, qb) in ((P, Q), (Q, R), (R, P)))


seeds = [tuple(map(int, s)) for s in json.load(open(sys.argv[1]))['seeds']]
pts = [rot(s, k) for s in seeds for k in range(6)]
n = len(pts); assert len(set(pts)) == n, 'coincident points'
zero = 0
tab = {}
for a, b, c in itertools.combinations(range(n), 3):
    v = o2(pts[a], pts[b], pts[c]); s = (v > 0) - (v < 0)
    if s == 0: zero += 1
    for (x, y, z), sg in (((a, b, c), 1), ((b, c, a), 1), ((c, a, b), 1), ((b, a, c), -1), ((a, c, b), -1), ((c, b, a), -1)):
        tab[(x, y, z)] = s * sg
with open(sys.argv[2] + '.otab.txt', 'w') as f:
    f.write('%d\n' % n)
    for a in range(n):
        f.write(' '.join(str(tab.get((a, b, c), 0)) for b in range(n) for c in range(n)) + '\n')
print(json.dumps({'points': n, 'zero_orientations': zero}))
cc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cvxcheck')
r = subprocess.run([cc, sys.argv[2] + '.otab.txt', '8'], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()); print('cvxcheck exit', r.returncode)
ok8 = ('convex 8-subsets: 0' in r.stdout) and any(l.strip() in ('DP largest convex subset: %d' % k for k in range(3, 8)) for l in r.stdout.splitlines())
print('OCTAGON-FREE' if ok8 else 'HAS CONVEX 8-SUBSETS (or check failed)')
sys.exit(0 if (zero == 0 and r.returncode == 0 and ok8) else 1)
