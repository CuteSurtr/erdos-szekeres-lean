#!/usr/bin/env python3
"""Decode clsat2 (m=9, n=29) literals into names. usage: decode.py 'JSON list'"""
import sys, json
from itertools import combinations
m, n = 9, 29; B = m - 2; nv = 0; name = {}
def new(s):
    global nv; nv += 1; name[nv] = s
for i, j in combinations(range(n), 2):
    for v in range(1, B): new('L[%d,%d]<=%d' % (i, j, v))
for t in combinations(range(n), 3): new('T%s' % (t,))
for i, j in combinations(range(n), 2):
    for l in range(3, m + 1): new('CU[%d,%d,%d]' % (i, j, l))
for i, j in combinations(range(n), 2):
    for l in range(3, m + 1): new('CA[%d,%d,%d]' % (i, j, l))
for x in range(1, m):
    for a in range(2, m + 1): new('G[%d,%d]' % (x, a))
for x in range(1, m):
    for a in range(2, m + 1): new('H[%d,%d]' % (x, a))
for l in json.loads(sys.argv[1]): print(('' if l > 0 else '~') + name[abs(l)], end='  ')
print()
