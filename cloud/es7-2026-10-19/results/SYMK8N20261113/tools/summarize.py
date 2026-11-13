#!/usr/bin/env python3
"""Summaries of the logs for the record (counts of evaluated moves, free moves, best octagon counts)."""
import re, sys, glob, os
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')


def twostep_summary(fn):
    runs = []
    cur = None
    for line in open(fn):
        m = re.match(r'^(\S+)( remove=(\S+))? m=(\d) orbits=(\d+) centre=(\S+) base n8=(\S+)', line)
        if m:
            cur = dict(set=m.group(1), remove=m.group(3), orbits=int(m.group(5)), base=m.group(7))
            runs.append(cur)
            continue
        m = re.search(r'single moves=(\d+) free=(\d+) best=\((\S+?),', line)
        if m and cur is not None:
            cur['singles'] = int(m.group(1)); cur['free'] = int(m.group(2)); cur['best1'] = m.group(3)
        m = re.search(r'pairs=(\d+) found=(\d+) best=\((\S+?)[,)]', line)
        if m and cur is not None:
            cur['pairs'] = int(m.group(1)); cur['found'] = int(m.group(2)); cur['best2'] = m.group(3)
    return runs


for name in sys.argv[1:]:
    runs = twostep_summary(os.path.join(L, name))
    S = sum(r.get('singles', 0) for r in runs)
    F = sum(r.get('free', 0) for r in runs)
    P = sum(r.get('pairs', 0) for r in runs)
    FD = sum(r.get('found', 0) for r in runs)
    b1 = [int(r['best1']) for r in runs if r.get('best1') not in (None, 'None') and r.get('remove') is None]
    b1r = [int(r['best1']) for r in runs if r.get('best1') not in (None, 'None') and r.get('remove') is not None]
    b2 = [int(r['best2']) for r in runs if r.get('best2') not in (None, 'None')]
    print('%s: runs=%d singles evaluated=%d free singles=%d pairs evaluated=%d found=%d' % (name, len(runs), S, F, P, FD))
    if b1:
        print('   full sets: min octagons over single moves = %d (per set: %s)' % (min(b1), b1))
    if b1r:
        print('   after removal: min octagons over single moves = %d' % min(b1r))
    if b2:
        print('   min octagons over pairs = %d' % min(b2))
