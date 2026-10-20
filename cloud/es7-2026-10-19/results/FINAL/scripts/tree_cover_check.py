#!/usr/bin/env python3
"""Check that each case tree is a combinatorial cover node by node (run in es7wt).
usage: tree_cover_check.py REF
For every non-whole case: coverCheck(root children) and, for every split node, coverCheck(its subs),
with coverCheck = split on the first literal of the first cube (as Mir.coverCheck)."""
import sys, json, subprocess, collections
sys.setrecursionlimit(100000)
REF = sys.argv[1]
exec(open(__file__.replace('tree_cover_check.py', 'tree_lib.py')).read())
def restrict(z, cs):
    return [[l for l in c if l != z] for c in cs if -z not in c]
def cover(cs, depth=0):
    if any(len(c) == 0 for c in cs): return True
    if not cs: return False
    z = cs[0][0]
    return cover(restrict(z, cs), depth + 1) and cover(restrict(-z, cs), depth + 1)
bad = collections.Counter(); n = collections.Counter(); examples = []
for case, P in sorted(per.items()):
    if P['whole']: continue
    children = {c + s for c, subs in P['subs'].items() for s in subs}
    roots = sorted(t for t in P['top'] if t not in children)
    n['roots'] += 1
    if not cover([list(r) for r in roots]):
        bad['roots'] += 1; examples.append((case, 'roots', len(roots)))
    for c, subs in P['subs'].items():
        n['split'] += 1
        if not cover([list(s) for s in subs]):
            bad['split'] += 1; examples.append((case, 'split', len(c), len(subs)))
print('checked', dict(n), 'failures', dict(bad))
print(examples[:20])
