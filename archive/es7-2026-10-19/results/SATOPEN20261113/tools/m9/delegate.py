#!/usr/bin/env python3
"""Mark open node NODE of tree OUT/tree.tsv as 'delegated:SUBDIR' and print its cube (JSON) for a separate
m9cc.py run with ROOT=<cube> OUT=SUBDIR.  Run only while no m9cc.py process writes OUT/tree.tsv.
usage: delegate.py OUT NODE SUBDIR"""
import sys, json, os
out, node, sub = sys.argv[1:4]
rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(out, 'tree.tsv'))]
hit = [r for r in rows if r[0] == node]
assert len(hit) == 1 and hit[0][3] == 'open', hit
hit[0][3] = 'delegated:' + os.path.abspath(sub)
with open(os.path.join(out, 'tree.tsv.tmp'), 'w') as f:
    for r in rows: f.write('\t'.join(r) + '\n')
os.replace(os.path.join(out, 'tree.tsv.tmp'), os.path.join(out, 'tree.tsv'))
print(hit[0][2])
