#!/usr/bin/env python3
"""Summarize lpc8.py logs: one row per phase vector (file, layers, result, iterations, cuts, solve time)."""
import sys, re, glob
rows = []
for fn in sys.argv[1:]:
    cur = None
    for line in open(fn):
        m = re.search(r'phase (\S+): th\(deg\)=\[(.*)\]', line)
        if m:
            cur = {'tag': m.group(1), 'n': len(m.group(2).split(',')), 'time': ''}
        m = re.search(r'(PHASE-UNSAT|UNSAT after|phase-SAT).*? ([0-9.]+) s', line)
        if m and cur is not None and not cur['time']:
            cur['time'] = m.group(2)
        m = re.search(r"RESULT (\S+) \('(\w+)', (\d+), (\d+)\)", line)
        if m and cur is not None:
            rows.append((m.group(1), cur['n'], m.group(2), m.group(3), m.group(4), cur['time'], fn.split('/')[-1]))
            cur = None
print('phase_file\tlayers\tresult\titerations\tcuts\tfirst_solve_s\tlog')
for r in rows:
    print('\t'.join(map(str, r)))
