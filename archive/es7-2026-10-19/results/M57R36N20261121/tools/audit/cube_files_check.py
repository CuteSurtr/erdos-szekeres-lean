#!/usr/bin/env python3
"""cube_files_check.py -- read-only: every cube CNF now on disk in r36/cubes equals base + units,
with the units decoded from the file name (o = +occ, h = -occ, occ[s] = 32759 + s)."""
import os, re, hashlib
R = '<scratch>/r36'
BASE = {'A': R + '/run/c36_rle13.cnf', 'B': R + '/run/c36_tle22.cnf'}
body = {}
for c, p in BASE.items():
    with open(p, 'rb') as f:
        hdr = f.readline(); body[c] = (hdr.split(), f.read())
n = ok = 0
for fn in sorted(os.listdir(R + '/cubes')):
    m = re.fullmatch(r'([AB])_((?:[oh]\d+)+)\.cnf', fn)
    if not m:
        continue
    case = m.group(1)
    units = [(32759 + int(s)) * (1 if sg == 'o' else -1) for sg, s in re.findall(r'([oh])(\d+)', m.group(2))]
    (_, _, nv, nc), b = body[case]
    want = hashlib.sha256(b'p cnf %s %d\n' % (nv, int(nc) + len(units)) + b
                          + ''.join('%d 0\n' % u for u in units).encode()).hexdigest()
    try:
        h = hashlib.sha256()
        with open(R + '/cubes/' + fn, 'rb') as f:
            for blk in iter(lambda: f.read(1 << 22), b''):
                h.update(blk)
    except FileNotFoundError:
        print(fn, 'vanished (archived) during the check'); continue
    n += 1; ok += h.hexdigest() == want
    print(fn, 'units', units, 'EQUAL base+units' if h.hexdigest() == want else 'DIFFERS')
print('cube CNFs checked', n, 'equal', ok)
