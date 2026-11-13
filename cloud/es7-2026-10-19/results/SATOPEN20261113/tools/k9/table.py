#!/usr/bin/env python3
"""Markdown table of certified cubes: name | cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 | .zst SHA-256
usage: table.py NAME..."""
import sys, os, re
C = '/home/jay/research/data/satopen-20261113/k9/cubes'
print('| cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 | proof.lrat.zst SHA-256 |')
print('|---|---:|---:|---:|---|---|---|---|')
for n in sys.argv[1:]:
    d = os.path.join(C, n); r = os.path.join(d, 'result.txt')
    if not os.path.exists(r): print('| %s | (no result yet) |' % n); continue
    t = open(r).read()
    hs = re.findall(r'^([0-9a-f]{64})\s', t, re.M)
    sec = re.search(r'cadical exit (\d+) seconds (\d+)', t); conf = re.search(r'c conflicts:\s+(\d+)', t)
    pb = re.search(r'proof bytes (\d+)', t); ck = re.search(r'cake_lpr seconds (\d+) heap (\d+)', t)
    v = re.search(r'VERIFIED_LINES (\d+)', t)
    verdict = ('verified, %s s (heap %s)' % (ck.group(1), ck.group(2))) if v and v.group(1) == '1' else 'NOT verified'
    print('| %s | %s | %s | %.2f | %s | `%s…` | `%s…` | `%s…` |' % (n, sec.group(2) if sec else '?', '{:,}'.format(int(conf.group(1))) if conf else '?',
          int(pb.group(1)) / 1e9 if pb else 0, verdict, hs[0][:12] if hs else '?', hs[1][:12] if len(hs) > 1 else '?', hs[2][:12] if len(hs) > 2 else '?'))
