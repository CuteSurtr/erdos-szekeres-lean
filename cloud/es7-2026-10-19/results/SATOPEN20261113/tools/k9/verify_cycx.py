#!/usr/bin/env python3
"""For cubes cycx_kK_pP: rebuild the order encoded by the 91 Y units on the 14 layers s = {1..15}-{K} and check that
it is the total order psi_{s_{P+1}} < ... < psi_{s_14} < psi_{s_1} < ... < psi_{s_P}, that no literal mentions layer K,
and (with BASE0) that SHA-256(BASE0 + units) equals the recorded cube hash.  usage: verify_cycx.py [BASE0] NAME..."""
import json, os, re, sys, hashlib
C = '/home/jay/research/data/satopen-20261113/k9/cubes'
args = sys.argv[1:]; base = args.pop(0) if args and args[0].endswith('.cnf') else None
M = json.load(open('/home/jay/research/data/lb-k9oct-20261111/cnf/A_m8K9t16.cnf.json'))
inv = {v: tuple(map(int, k.split(','))) for k, v in M['Y'].items()}
def cnfhash(units):
    h = hashlib.sha256()
    with open(base, 'rb') as f:
        hdr = f.readline().split(); nv, ncl = int(hdr[2]), int(hdr[3])
        h.update(b'p cnf %d %d\n' % (nv, ncl + len(units)))
        for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
    for u in units: h.update(b'%d 0\n' % u)
    return h.hexdigest()
for name in args:
    m = re.match(r'cycx_k(\d+)_p(\d+)$', name); K, P = int(m.group(1)), int(m.group(2))
    d = os.path.join(C, name)
    lits = [int(l.split()[0]) for l in open(os.path.join(d, 'cube.units'))]
    s = [i for i in range(1, 16) if i != K]
    below = {i: set() for i in s}
    ok = len(lits) == 91 and len(set(abs(l) for l in lits)) == 91 and all(abs(l) in inv for l in lits)
    for l in lits:
        a, b = inv[abs(l)]
        if K in (a, b): ok = False; continue
        if l > 0: below[b].add(a)
        else: below[a].add(b)
    order = sorted(s, key=lambda i: len(below[i]))
    ok = ok and sorted(len(below[i]) for i in s) == list(range(14)) and all(below[order[k]] == set(order[:k]) for k in range(14))
    exp = s[P:] + s[:P]
    res = os.path.join(d, 'result.txt'); v = 'no result'; extra = ''
    if os.path.exists(res):
        t = open(res).read(); mm = re.search(r'VERIFIED_LINES (\d+)', t); hs = re.findall(r'^([0-9a-f]{64})\s', t, re.M)
        v = 'VERIFIED_LINES %s cnf %s proof %s' % (mm.group(1) if mm else '?', hs[0][:16] if hs else '?', hs[1][:16] if len(hs) > 1 else '?')
        if base: extra = ' | recomputed cnf hash ' + ('MATCH' if hs and cnfhash(lits) == hs[0] else 'MISMATCH')
    print('%s: order %s; layer %d free; expected cut-%d cyclic spiral: %s; %s%s' % (name, order, K, P, ok and order == exp, v, extra))
