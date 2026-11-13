#!/usr/bin/env python3
"""For the cubes cycP (P = 4..11): reconstruct the phase order encoded by the 105 Y units (pair (a,b), a < b:
+Y(a,b) means psi_a < psi_b, -Y(a,b) means psi_b < psi_a; JSON variable map) and check that it is the total order
psi_{P+1} < ... < psi_15 < psi_1 < ... < psi_P (cyclic spiral of layers 1..15 cut at layer 0), that the units are
exactly these 105 literals, and print the recorded hashes and cake_lpr verdicts."""
import json, os, re, sys, hashlib
base = sys.argv[1] if len(sys.argv) > 1 else None
def cnfhash(units):
    h = hashlib.sha256()
    with open(base, 'rb') as f:
        hdr = f.readline().split(); nv, ncl = int(hdr[2]), int(hdr[3])
        h.update(b'p cnf %d %d\n' % (nv, ncl + len(units)))
        for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
    for u in units: h.update(b'%d 0\n' % u)
    return h.hexdigest()
C = '/home/jay/research/data/satopen-20261113/k9/cubes'
M = json.load(open('/home/jay/research/data/lb-k9oct-20261111/cnf/A_m8K9t16.cnf.json'))
inv = {v: tuple(map(int, k.split(','))) for k, v in M['Y'].items()}
for P in range(4, 12):
    d = os.path.join(C, 'cyc%d' % P)
    lits = [int(l.split()[0]) for l in open(os.path.join(d, 'cube.units'))]
    below = {i: set() for i in range(1, 16)}
    ok = len(lits) == 105 and len(set(abs(l) for l in lits)) == 105 and all(abs(l) in inv for l in lits)
    for l in lits:
        a, b = inv[abs(l)]
        if l > 0: below[b].add(a)
        else: below[a].add(b)
    order = sorted(range(1, 16), key=lambda i: len(below[i]))
    ok = ok and sorted(len(below[i]) for i in range(1, 16)) == list(range(15))   # a total order
    ok = ok and all(below[order[k]] == set(order[:k]) for k in range(15))      # consistent (transitive)
    exp = list(range(P + 1, 16)) + list(range(1, P + 1))
    res = os.path.join(d, 'result.txt'); v = 'no result'
    if os.path.exists(res):
        t = open(res).read(); m = re.search(r'VERIFIED_LINES (\d+)', t); hs = re.findall(r'^([0-9a-f]{64})\s', t, re.M)
        v = 'VERIFIED_LINES %s cnf %s proof %s' % (m.group(1) if m else '?', hs[0][:16] if hs else '?', hs[1][:16] if len(hs) > 1 else '?')
    extra = ''
    if base and os.path.exists(res):
        rh = re.findall(r'^([0-9a-f]{64})\s', open(res).read(), re.M)
        extra = ' | recomputed cnf hash ' + ('MATCH' if rh and cnfhash(lits) == rh[0] else 'MISMATCH')
    print('cyc%d: order %s; expected cyclic spiral: %s; %s%s' % (P, order, ok and order == exp, v, extra))
