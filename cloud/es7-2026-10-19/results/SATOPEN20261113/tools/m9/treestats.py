#!/usr/bin/env python3
"""Summary of an m9cc.py tree: node/leaf counts by status, depth range, solver/proof/cake time from result files.
usage: treestats.py OUTDIR [ROOTLEN]"""
import sys, os, re, json
out = sys.argv[1]; rl = int(sys.argv[2]) if len(sys.argv) > 2 else 1
N = {}
for line in open(os.path.join(out, 'tree.tsv')):
    i, par, cube, st = line.rstrip('\n').split('\t'); N[i] = (json.loads(cube), st)
cnt = {}
for i, (c, st) in N.items():
    k = st.split(':')[0]; cnt[k] = cnt.get(k, 0) + 1
t1 = t2 = t3 = 0.0; pb = 0; nres = 0
for i, (c, st) in N.items():
    r = os.path.join(out, 'nodes', i, 'result.txt')
    if st == 'verified' and os.path.exists(r):
        s = open(r).read(); m = re.search(r'solve_noproof ([\d.]+)s proof_run ([\d.]+)s cake ([\d.]+)s', s)
        if m: t1 += float(m.group(1)); t2 += float(m.group(2)); t3 += float(m.group(3)); nres += 1
        b = re.search(r'proof_bytes (\d+)', s); pb += int(b.group(1)) if b else 0
op = [len(c) - rl for c, st in N.values() if st == 'open']
lv = [len(c) - rl for c, st in N.values() if st == 'verified']
print('%s: nodes %d, by status %s; verified leaves depth %s..%s; open depths %s; '
      'sum solve %.0fs, proof runs %.0fs, cake %.0fs, proof bytes %.1f MB' % (out, len(N), cnt, min(lv) if lv else '-', max(lv) if lv else '-',
      sorted(op), t1, t2, t3, pb / 1e6))
