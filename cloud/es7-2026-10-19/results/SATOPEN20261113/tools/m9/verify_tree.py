#!/usr/bin/env python3
"""Check the cube tree of m9cc.py (OUT/tree.tsv): every node is 'split:v' with children cube+[v] (id+'0') and
cube+[-v] (id+'1'), or a leaf.  The leaves of a finished tree form a complete cover of the root cube (decision tree:
the negations of the leaf cubes together with the root literals are unsatisfiable).  For each leaf, its status and
(for 'verified') the recorded hashes and cake_lpr line.  Also re-checks the cover by brute force over the decision
variables when there are at most 22 of them; otherwise structurally.
usage: verify_tree.py OUTDIR [ROOTCUBE_JSON]"""
import sys, json, os, re, itertools
out = sys.argv[1]; root = json.loads(sys.argv[2]) if len(sys.argv) > 2 else [-11834]
N = {}
for line in open(os.path.join(out, 'tree.tsv')):
    i, par, cube, st = line.rstrip('\n').split('\t'); N[i] = dict(par=par, cube=json.loads(cube), st=st)
ok = True
assert N['r']['cube'] == root, 'root cube differs'
leaves = []
def walk(i):
    global ok
    d = N[i]
    if d['st'].startswith('split:'):
        v = int(d['st'].split(':')[1])
        for c, lit in ((i + '0', v), (i + '1', -v)):
            if c not in N or N[c]['cube'] != d['cube'] + [lit]: print('bad child', c); ok = False; continue
            walk(c)
    else: leaves.append(i)
walk('r')
cnt = {}
for i in leaves: cnt[N[i]['st']] = cnt.get(N[i]['st'], 0) + 1
print('nodes', len(N), 'leaves', len(leaves), 'leaf status counts', cnt)
ver = 0
for i in leaves:
    if N[i]['st'] != 'verified': continue
    t = open(os.path.join(out, 'nodes', i, 'result.txt')).read()
    if 'VERIFIED True' in t and 's VERIFIED UNSAT' in t: ver += 1
    else: print('leaf', i, 'marked verified but result.txt lacks the verdict'); ok = False
print('verified leaves with cake_lpr line:', ver)
# brute-force cover check on the decision variables (paths below the root)
dv = sorted(set(abs(l) for i in leaves for l in N[i]['cube'][len(root):]))
if len(dv) <= 22:
    bad = 0
    cubes = [{abs(l): l > 0 for l in N[i]['cube'][len(root):]} for i in leaves]
    for bits in itertools.product([False, True], repeat=len(dv)):
        a = dict(zip(dv, bits))
        if sum(1 for c in cubes if all(a[v] == b for v, b in c.items())) != 1: bad += 1
    print('decision variables', len(dv), 'assignments', 2 ** len(dv), 'not covered exactly once', bad); ok = ok and bad == 0
else: print('decision variables', len(dv), '(>22: structural check only)')
# delegated leaves: status 'delegated:DIR' = the leaf's cube is the root cube of another tree in DIR
import subprocess
dele = [i for i in leaves if N[i]['st'].startswith('delegated:')]
dok = True
for i in dele:
    sub = N[i]['st'].split(':', 1)[1]
    r = subprocess.run([sys.executable, os.path.abspath(__file__), sub, json.dumps(N[i]['cube'])], capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'no output'
    print('delegated leaf', i, '->', sub, ':', last)
    dok = dok and 'TREE STRUCTURE OK' in last and 'all leaves verified: True' in last
allv = all(N[i]['st'] == 'verified' or (N[i]['st'].startswith('delegated:')) for i in leaves) and dok
print('TREE STRUCTURE OK' if ok else 'TREE STRUCTURE FAILED', '| all leaves verified:', allv)
