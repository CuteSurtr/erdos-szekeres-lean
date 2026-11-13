#!/usr/bin/env python3
"""Cover check for the 'monotone except layer J' family: cubes cubes/exJ_r{0..14}.
(1) every cube's units = the 91 units Y(a,b), a<b in {1..15}\\{J} (recomputed from the JSON variable map) + Z literals only;
(2) the Z parts cover every assignment of Z_{s_1..s_14} exactly once (enumeration of all 2^14 assignments);
(3) prints each cube's recorded CNF hash, proof hash and the cake_lpr verdict line count (result.txt).
usage: verify_cover_ex.py J [CUBEDIR]"""
import json, sys, os, itertools, re
J = int(sys.argv[1]); C = sys.argv[2] if len(sys.argv) > 2 else '/home/jay/research/data/satopen-20261113/k9/cubes'
M = json.load(open('/home/jay/research/data/lb-k9oct-20261111/cnf/A_m8K9t16.cnf.json'))
Yv = {tuple(map(int, k.split(','))): v for k, v in M['Y'].items()}
s = [i for i in range(1, 16) if i != J]
U = set(Yv[a, b] for a in s for b in s if a < b); assert len(U) == 91
Zvar = {497697 + i: i for i in range(1, 16)}
parts = []; ok = True
for r in range(15):
    d = os.path.join(C, 'ex%d_r%d' % (J, r))
    lits = [int(l.split()[0]) for l in open(os.path.join(d, 'cube.units'))]
    yl = set(l for l in lits if abs(l) not in Zvar); zl = [l for l in lits if abs(l) in Zvar]
    if yl != U: print('cube', r, 'Y part differs'); ok = False
    if any(Zvar[abs(l)] == J for l in zl): print('cube', r, 'uses Z_J'); ok = False
    parts.append({abs(l): l > 0 for l in zl})
    res = os.path.join(d, 'result.txt')
    v = 'no result'
    if os.path.exists(res):
        t = open(res).read(); m = re.search(r'VERIFIED_LINES (\d+)', t)
        hs = re.findall(r'^([0-9a-f]{64})\s', t, re.M)
        v = 'VERIFIED_LINES %s cnf %s proof %s' % (m.group(1) if m else '?', hs[0][:16] if hs else '?', hs[1][:16] if len(hs) > 1 else '?')
    print('ex%d_r%d: %d units, Z part %s; %s' % (J, r, len(lits), ''.join(('+' if parts[-1][497697 + i] else '-') + str(i) + ' ' for i in s if 497697 + i in parts[-1]), v))
zs = [497697 + i for i in s]; bad = 0
for bits in itertools.product([False, True], repeat=14):
    a = dict(zip(zs, bits))
    n = sum(1 for p in parts if all(a[v] == b for v, b in p.items()))
    if n != 1: bad += 1
print('assignments of Z_s: %d, covered exactly once: %d, bad: %d' % (2 ** 14, 2 ** 14 - bad, bad))
print('COVER OK' if ok and bad == 0 else 'COVER FAILED')
