#!/usr/bin/env python3
"""leafcover35.py STATE.json [--final] -- check that the leaves of every case in a drive.py state file
form a complete cover of that case.

The driver's cubes for case c are sign assignments to a prefix ORDER[c][:d] of the case's split order
(initial depth TOP[c]; a timed-out cube is replaced by its two children on the next state).  A set of
such prefix cubes covers all assignments iff it is prefix-free and sum 2^-d = 1 (Kraft equality).
Leaves = jobs not in status 'split'.  With --final every leaf must have status 'verified'
(cake_lpr printed the exact line 's VERIFIED UNSAT'); otherwise the frontier is only reported.
ORDER/OCC0 are taken from drive.py next to STATE's cubes/ directory (or --drive PATH).
"""
import sys, os, json, importlib.util
from fractions import Fraction
args = [a for a in sys.argv[1:] if not a.startswith('--')]
final = '--final' in sys.argv
state_path = args[0]
drive = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(state_path))), 'drive.py')
for a in sys.argv[1:]:
    if a.startswith('--drive='):
        drive = a.split('=', 1)[1]
spec = importlib.util.spec_from_file_location('drv', drive)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
st = json.load(open(state_path))
ok = True
for case in sorted(m.BASE):
    jobs = [j for j in st['jobs'] if j['case'] == case]
    leaves = [j for j in jobs if j['status'] != 'split']
    keys = set()
    total = Fraction(0)
    for j in leaves:
        vs = [abs(u) - m.OCC0 for u in j['units']]
        assert vs == m.ORDER[case][:len(vs)], (case, j['id'], 'units are not a prefix of ORDER')
        assert len(vs) >= m.TOP[case]
        keys.add(tuple(u > 0 for u in j['units']))
        total += Fraction(1, 2 ** len(vs))
    assert len(keys) == len(leaves), (case, 'duplicate leaves')
    prefix_free = not any(k[:i] in keys for k in keys for i in range(len(k)))
    complete = prefix_free and total == 1
    by = {}
    for j in leaves:
        by[j['status']] = by.get(j['status'], 0) + 1
    allver = all(j['status'] == 'verified' for j in leaves)
    print(case, 'leaves', len(leaves), 'prefix-free', prefix_free, 'Kraft sum', total, 'complete', complete,
          'statuses', by, 'ALL VERIFIED' if allver else '')
    ok &= complete and (allver or not final)
print('LEAF COVER OK' if ok else 'LEAF COVER NOT ESTABLISHED', '(final)' if final else '(structure only)')
sys.exit(0 if ok else 1)
