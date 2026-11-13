#!/usr/bin/env python3
"""Rows for the probe table: name | units | result | CaDiCaL s | conflicts | certificate."""
import sys, os, re
C = '/home/jay/research/data/satopen-20261113/k9/cubes'
print('| probe | cube | units | result | CaDiCaL s | conflicts | certificate |')
print('|---|---|---:|---|---:|---:|---|')
for n in sys.argv[1:]:
    d = os.path.join(C, n)
    if not os.path.exists(os.path.join(d, 'solved')): print('| %s | (not run) |' % n); continue
    desc = open(os.path.join(d, 'cube.desc')).read().strip().replace('|', '/')
    nu = sum(1 for _ in open(os.path.join(d, 'cube.units')))
    so = open(os.path.join(d, 'solved')).read()
    m = re.search(r'exit (\d+) seconds (\d+)', so); ec, sec = m.group(1), m.group(2)
    co = re.search(r'c conflicts:\s+(\d+)', open(os.path.join(d, 'cadical.out')).read())
    res = {'20': 'UNSAT', '10': 'SAT', '0': 'unknown (limit)'}.get(ec, 'exit ' + ec)
    cert = 'noproof' if os.path.exists(os.path.join(d, 'noproof')) else ('cake_lpr verified' if os.path.exists(os.path.join(d, 'result.txt')) and 'VERIFIED_LINES 1' in open(os.path.join(d, 'result.txt')).read() else 'check pending')
    if ec != '20' and not os.path.exists(os.path.join(d, 'noproof')): cert = 'partial LRAT kept'
    print('| %s | %s | %d | %s | %s | %s | %s |' % (n, desc[:90], nu, res, sec, '{:,}'.format(int(co.group(1))) if co else '?', cert))
