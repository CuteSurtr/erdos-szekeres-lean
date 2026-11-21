#!/usr/bin/env python3
"""audit_static.py -- read-only checks of the rung-36 campaign inputs (r36-audit, 21 Nov 2026).

1. SHA-256 of the two base CNFs against the recorded hashes; last byte is a newline; header.
2. names.pkl: occ[s] == 32759 + s for s = 0..55 (both cases); row specs and families.
3. independent re-derivation of the 56 states, the families S1 = {f1<=4}, B2 = {f1=5}, and the split arithmetic.
4. the split orders of drive.py: which family each ORDER list lies in; no repeats.
Nothing is written outside this script's own directory.
"""
import hashlib, itertools, pickle, sys, os

R = '<scratch>/r36'
REC = {'c36_rle13': 'aba65111d42151131a55e7596043721bd86fe94d05c8fea0b2750212d2808bbe',
       'c36_tle22': '08b8ea9c9c588aa242485163a3d4836a0c79f8bd91c61ac25357010dc2bd9339'}
WANT_ROWS = {'c36_rle13': {'S1': 25, 'S2': 25, 'B1': 16, 'B2': 13, 'ALL': 36},
             'c36_tle22': {'S1': 22, 'S2': 25, 'B1': 16, 'B2': 16, 'ALL': 36}}

# independent state catalog (not imported from cat_common)
CA, CB = 3, 5
states = sorted([f for f in itertools.product(range(CB + 1), repeat=CA) if f[0] >= f[1] >= f[2]],
                key=lambda f: (sum(f), f))
assert len(states) == 56
S1 = [i for i, f in enumerate(states) if f[0] <= CB - 1]
S2 = [i for i, f in enumerate(states) if f[CA - 1] >= 1]
B1 = [i for i, f in enumerate(states) if f[CA - 1] == 0]
B2 = [i for i, f in enumerate(states) if f[0] == CB]
fam = {'S1': S1, 'S2': S2, 'B1': B1, 'B2': B2, 'ALL': list(range(56))}
print('family sizes', {k: len(v) for k, v in fam.items()})
assert set(S1) | set(B2) == set(range(56)) and not set(S1) & set(B2)
bad = [(r, 36 - r) for r in range(0, len(B2) + 1) if 0 <= 36 - r <= len(S1) and not (r <= 13 or 36 - r <= 22)]
print('split arithmetic: (r,t) with r+t=36, r<=21, t<=35, violating r<=13 or t<=22:', bad)
# the split is tight: r=14,t=22 and r=13,t=23 both exist; (14,23) would need 37 points
print('first states', states[:3], 'state 0 =', states[0], 'state 1 =', states[1])

for name, rec in REC.items():
    p = f'{R}/run/{name}.cnf'
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        hdr = f.readline()
        h.update(hdr)
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
            last = b
    print(name, 'header', hdr.decode().strip(), 'sha256 match' if h.hexdigest() == rec else 'SHA MISMATCH ' + h.hexdigest(),
          'ends with newline' if last.endswith(b'\n') else 'NO TRAILING NEWLINE')
    meta = pickle.load(open(p + '.names.pkl', 'rb'))
    names = meta['names']
    occ_ok = all(names[('occ', s)] == 32759 + s for s in range(56))
    print('  N,CA,CB,G =', meta['N'], meta['CA'], meta['CB'], meta['G'], '| occ[s] == 32759+s for all 56:', occ_ok)
    rows = {k: v[1] for k, v in meta['rows'].items()}
    print('  rows', rows, 'as wanted' if rows == WANT_ROWS[name] else 'ROWS DIFFER')
    for k, (F, K) in meta['rows'].items():
        assert F == fam[k], ('family differs', name, k)
    print('  row families equal the independent re-derivation')
    nv = int(hdr.split()[2])
    print('  header nv', nv, '== len(names)', len(names), nv == len(names))

ORDER = {'A': [44, 39, 26, 21, 15, 33, 27, 37, 32, 48, 38, 43, 46, 42, 47, 51, 50, 52, 53, 54, 55],
         'B': [34, 31, 16, 28, 22, 36, 29, 25, 23, 40, 49, 45, 41, 35, 30, 24, 20, 19, 18, 17]}
for c, o in ORDER.items():
    print('ORDER', c, 'len', len(o), 'distinct', len(set(o)) == len(o), 'subset of B2:', set(o) <= set(B2),
          'subset of S1:', set(o) <= set(S1), '| B2 \\ ORDER:', sorted(set(B2) - set(o)) if c == 'A' else '',
          '| top states', [states[s] for s in o[:6 if c == 'A' else 5]])
