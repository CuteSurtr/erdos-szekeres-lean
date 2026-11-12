#!/usr/bin/env python3
"""Cover check for the monotone-cube certificate (stdlib only).
1. The 16 cubes c_r on Z_i = variable NV0 + i (i = 1..15): c_r = (Z_1..Z_r true, Z_{r+1} false) for r < 15,
   c_15 = (Z_1..Z_15 true).  Every one of the 2^15 assignments of Z_1..Z_15 satisfies exactly one cube (checked by
   enumeration).
2. Each cube formula is BASE (S8.cnf) with the header's clause count increased by the number of cube literals and the
   cube literals appended as unit clauses: its SHA-256 is recomputed from BASE and compared with the recorded hash.
3. Each cube's result.txt records exactly one line 's VERIFIED UNSAT' from cake_lpr, and its CNF hash line.
usage: verify_cover_mono.py BASE.cnf CUBEDIR [NZ=15 [ZOFF=0]]   (S11 family: NZ=14; S13 family: NZ=13 ZOFF=1)"""
import sys, os, hashlib, itertools
base, cdir = sys.argv[1], sys.argv[2]
NZ = int(sys.argv[3]) if len(sys.argv) > 3 else 15
ZOFF = int(sys.argv[4]) if len(sys.argv) > 4 else 0      # decision list on Z_{ZOFF+1}..Z_{ZOFF+NZ}
NV0 = 497697 + ZOFF
cubes = []
for r in range(NZ + 1):
    lits = [NV0 + i for i in range(1, r + 1)] + ([-(NV0 + r + 1)] if r < NZ else [])
    cubes.append(lits)
# 1. cover by enumeration
for bits in itertools.product([False, True], repeat=NZ):
    val = {NV0 + i + 1: bits[i] for i in range(NZ)}
    n = sum(1 for c in cubes if all(val[abs(l)] == (l > 0) for l in c))
    assert n == 1, (bits, n)
print('cover: every assignment of Z_%d..Z_%d lies in exactly one of the %d cubes' % (ZOFF + 1, ZOFF + NZ, NZ + 1))
# 2. hashes
with open(base, 'rb') as f:
    hdr = f.readline()
    body_hash = None
p, c, nv, ncl = hdr.split()
nv, ncl = int(nv), int(ncl)
ok = True
for r, lits in enumerate(cubes):
    h = hashlib.sha256()
    h.update(b'p cnf %d %d\n' % (nv, ncl + len(lits)))
    with open(base, 'rb') as f:
        f.readline()
        while True:
            b = f.read(1 << 24)
            if not b:
                break
            h.update(b)
    for l in lits:
        h.update(b'%d 0\n' % l)
    d = os.path.join(cdir, 'c_%d' % r)
    rec = open(os.path.join(d, 'cnf.sha256')).read().split()[0]
    units = open(os.path.join(d, 'cube.units')).read().split()
    ul = [int(x) for x in units if x != '0']
    res = open(os.path.join(d, 'result.txt')).read()
    nver = res.count('VERIFIED_LINES 1')
    good = (rec == h.hexdigest() and ul == lits and nver == 1 and rec in res)
    ok &= good
    print('c_%-2d cube %-40s cnf %s %s  cake_lpr %s' % (r, ' '.join(map(str, lits))[:40], rec[:16],
          'hash OK' if rec == h.hexdigest() else 'HASH MISMATCH', 'VERIFIED UNSAT' if nver == 1 else 'NOT VERIFIED'))
print('ALL OK' if ok else 'FAIL')
