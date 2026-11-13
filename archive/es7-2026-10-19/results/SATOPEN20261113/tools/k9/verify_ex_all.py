#!/usr/bin/env python3
"""For the unsplit cubes exJ_all (J = 4..12): check that cube.units is exactly the 91 units Y(a,b), a < b,
a, b in {1..15}\\{J} (recomputed from the JSON variable map), recompute nothing else; print the recorded cube-CNF hash,
proof hash, cake_lpr verdict line count and whether the cube CNF hash equals SHA-256(BASE0 + units) recomputed now
(only if BASE0 is given).  usage: verify_ex_all.py [BASE0.cnf]"""
import json, sys, os, re, hashlib
C = '/home/jay/research/data/satopen-20261113/k9/cubes'
M = json.load(open('/home/jay/research/data/lb-k9oct-20261111/cnf/A_m8K9t16.cnf.json'))
Yv = {tuple(map(int, k.split(','))): v for k, v in M['Y'].items()}
base = sys.argv[1] if len(sys.argv) > 1 else None
def cnfhash(units):
    h = hashlib.sha256()
    with open(base, 'rb') as f:
        hdr = f.readline().split(); nv, ncl = int(hdr[2]), int(hdr[3])
        h.update(b'p cnf %d %d\n' % (nv, ncl + len(units)))
        for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
    for u in units: h.update(b'%d 0\n' % u)
    return h.hexdigest()
for J in range(4, 13):
    d = os.path.join(C, 'ex%d_all' % J)
    s = [i for i in range(1, 16) if i != J]
    U = [Yv[a, b] for a in s for b in s if a < b]
    lits = [int(l.split()[0]) for l in open(os.path.join(d, 'cube.units'))]
    okU = sorted(lits) == sorted(U) and len(lits) == 91
    res = os.path.join(d, 'result.txt'); v = 'no result'; rh = None
    if os.path.exists(res):
        t = open(res).read(); m = re.search(r'VERIFIED_LINES (\d+)', t)
        hs = re.findall(r'^([0-9a-f]{64})\s', t, re.M); rh = hs[0] if hs else None
        v = 'VERIFIED_LINES %s cnf %s proof %s' % (m.group(1) if m else '?', hs[0][:16] if hs else '?', hs[1][:16] if len(hs) > 1 else '?')
    extra = ''
    if base and rh: extra = ' | recomputed cnf hash ' + ('MATCH' if cnfhash(lits) == rh else 'MISMATCH')
    print('ex%d_all: units == 91 expected units: %s; %s%s' % (J, okU, v, extra))
